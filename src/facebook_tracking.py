"""This module houses all of the functions needed to pull data from a CSV 
(or Google Sheet) with  Facebook message data, and pull the necessary metrics 
from it """

import datetime
import pandas as pd
import numpy as np
import requests
from statistics import mean


class UnansweredMessages:
    def __init__(self, sheet, specialist):
        """This class has fucntions that allow you to pass in a sheet and a
        desired name, and check how many unanswered messages that name has

        Args:
            sheet (gspread.models.Worksheet): This sheet should have a column
            with a list of messages sent, along with who sent them, the time
            it was sent and which overall conversation those messages belong to

            specialist (string): This is the name of the specialist that runs
            that account and is responsible for those messages
        """
        self.sheet = sheet
        self.specialist = specialist

    def getSheetValuesToDataframe(self):
        """Uses the sheet attribute to get the data needed and return a
        dataframe and grouped dataframe of that data

        Returns:
            tuple: Dataframe, Grouped Dataframe with message data from sheet
        """
        message_data = self.sheet.get_all_records()
        cleaned_message_list = [
            i for i in message_data if (len(i["Conversation"]) > 2)
        ]
        message_dataframe = pd.DataFrame(cleaned_message_list)
        message_groups = message_dataframe.groupby(["Conversation"])[
            "Timestamp (ms)"
        ].max()
        return message_dataframe, message_groups

    def countUnanswered(self, regular_dataframe, grouped_dataframe):
        """Gives a number of unanswered messages in a certain sheet based on
        the specialist name

        Args:
            regular_dataframe (dataframe): regular dataframe from the list of
            dictionaries generated from a worksheet object

            grouped_dataframe (groupby.dataframe): above dataframe grouped by
            Conversation and Timestamp

        Returns:
            int: Returns a number that represents how many unanswered
            messages there are
        """

        list_of_last_senders = []
        for row in grouped_dataframe:
            last_message_time = regular_dataframe.loc[
                regular_dataframe["Timestamp (ms)"] == row
            ]["Sender"].values[0]
            list_of_last_senders.append(last_message_time)

        last_sender_count = len(
            list_of_last_senders
        ) - list_of_last_senders.count(self.specialist)

        return last_sender_count


class AveragePerConversation:
    def __init__(self, sheet):
        """This class passes in a sheet and gives the average amount of time
        elapsed between each message

        Args:
            sheet (gspread.models.Worksheet): This sheet should have a column
            with a list of messages sent, along with who sent them, the time
            it was sent and which overall conversation those messages belong to
        """

        self.sheet = sheet

    def getProspectNamesInDictionary(self):
        """This gets a dictionary of all of the conversation labels in the sheet
        with all of the message time stamps for that conversation

        Returns:
            dict: key: Conversation label value: List of timestamps
        """

        df = pd.DataFrame(self.sheet.get_all_records())
        timestamp_df = df.groupby(["Conversation", "Timestamp (ms)"])[
            "Timestamp (ms)"
        ].unique()
        names = [i for i in df["Conversation"].values if i]
        dictionary_of_reply_times = {}
        for name in names:
            dictionary_of_reply_times[name] = (
                timestamp_df[name].astype(int).tolist()
            )

        return dictionary_of_reply_times

    def getAverageReplyTimePerConversation(self, reply_time_dict, name):
        reply_times = []
        for index, time in enumerate(reply_time_dict[name]):
            if index + 1 == len(reply_time_dict[name]):
                pass
            else:
                first_message_time = reply_time_dict[name][index]
                next_message_time = reply_time_dict[name][index + 1]
                reply_times.append(next_message_time - first_message_time)

        if len(reply_times) < 1:
            return np.nan  # Used for calculating averages in later step
        else:
            return mean(reply_times)

    def getAverageMinutesToReplyForAllConversations(self, reply_time_dict):
        list_of_averages = []
        for name in reply_time_dict:
            avg_time = self.getAverageReplyTimePerConversation(
                reply_time_dict, name
            )
            list_of_averages.append(str(avg_time))

        cleaned_averages = [float(i) for i in list_of_averages if i != "nan"]

        return round(mean(cleaned_averages) / 60000, 2)


class Leaderboard:
    def __init__(self, sheet, role_dictionary):
        """This class generates a leaderboard based on our team's metrics in
        any given week

        Args:
            sheet (gspread.models.Worksheet): This sheet should have a week
            total column to pull the relevant metrics from

            role_dictionary (dict): key: Each Role (e.g Setter),
            value: List of team members in that role (e.g Amanda)
        """
        self.sheet = sheet
        self.role_dictionary = role_dictionary

    def getWeekTotalFromLevel10(self):
        """Pulls the data needed for analysis from the whole sheet. This the
        total for the week along with the name of the person who achieved
        that total

        Returns:
            dataframe: 1 column dataframe with the index being the person who
            achieved the week total
        """
        level_10_data = self.sheet.get_all_records()
        level_10_df = (
            pd.DataFrame(level_10_data)[["Metric Type", "Week Total"]]
            .dropna()
            .set_index("Metric Type")
        )
        return level_10_df

    def getDictionaryOfCellsToCheck(self):
        """Checks all of the names in role dictionary and gives every metric
        that has their name in the given sheet

        Returns:
            dict: key: Role of person, value: List of metrics in that role
        """
        cells_to_check = {}
        full_list = list(self.getWeekTotalFromLevel10().index.values)

        for role, person_list in self.role_dictionary.items():
            metrics = []
            for person in person_list:
                for metric in full_list:
                    if person in metric:
                        metrics.append(metric)
                        cells_to_check[role] = metrics
        return cells_to_check

    def getValueForEachTeamMemberInTheirRole(self):
        """Creates a dataframe with all team members and all metrics that
        are relevant to their role

        Returns:
            dataframe: dataframe with columns based on role and index on each
            individual metric. There are a lot of NaN values
        """
        df = self.getWeekTotalFromLevel10()
        cells = self.getDictionaryOfCellsToCheck()

        dep_pep = {}  # Department_Person, which are the Key, Value
        for role, person_list in cells.items():
            values_per_department = {}
            for person in person_list:
                values_per_department[person] = int(df.loc[person].values[0])
            dep_pep[role] = values_per_department

        dataframe_with_score_and_role = pd.DataFrame(dep_pep)

        return dataframe_with_score_and_role

    def getSortedTCandSSNumbersForTeamMember(self):
        """Sorts the dataframe generated in
        getValueForEachTeamMemberInTheirRole to only return the TC and SS
        numbers in descending order

        Returns:
            dataframe: dataframe with columns based on role and index on each
            individual metric. Each column is sorted. There are a lot of NaN
        """

        df = self.getValueForEachTeamMemberInTheirRole()
        columns_for_frame = list(self.role_dictionary.keys())

        list_of_df = []
        for col in columns_for_frame:
            if col == "Jnr Specialist" or col == "Setter":
                frame = df[df[col].index.str.contains("TC")]
            elif col == "Snr Specialist" or col == "Pod Lead":
                frame = df[df[col].index.str.contains("SS")]

            res = frame[col].dropna().sort_values(ascending=False)
            list_of_df.append(res)

        sorted_dataframe_of_TC_and_SS = pd.concat(list_of_df, axis=1)

        return sorted_dataframe_of_TC_and_SS


class ScheduleOnce:
    def __init__(self, url, headers):
        """This class calls the Schedule Once API to track TC Scheduled and
        TC Booked

        Args:
            url (string): API url for Schedule Once, ideally with expand
            booking pages and limits included headers (dict): dictionary
            with at least Accept and API Key
        """
        self.url = url
        self.headers = headers

    def getFullBookingList(self):
        """Creates a long list of the data pushed when the class is called
        from the given url

        Returns:
            list: list of dictionaries where each dictionary has the data
            from an individual booking
        """
        response = requests.request("GET", url=self.url, headers=self.headers)
        booking_list = response.json()["data"]

        return booking_list

    def getTCScheduledorTCBookedYesterday(self):
        """Calls the API to get bookings from the previous day, which allows
        us to track TC Booked and Scheduled

        Returns:
            list: Gives list of bookings that are either created or started
            the previous day
        """
        from_date = str(
            datetime.date.today() - datetime.timedelta(1)
        )  # Gives yesterday's date
        to_date = str(datetime.date.today())
        which_params = input(
            "Do you want TC Scheduled (s) or TC Booked (b). Enter s or b: "
        ).lower()
        if which_params == "s":
            params = {
                "starting_time.gt": from_date,
                "starting_time.lt": to_date,
            }
        elif which_params == "b":
            params = {
                "creation_time.gt": from_date,
                "creation_time.lt": to_date,
            }

        response = requests.request(
            "GET", url=self.url, headers=self.headers, params=params
        )
        booking_list = response.json()["data"]

        return booking_list

    def appendMultipleAPIPagesOfTCScheduledorBooked(self):
        """Paginates through all of the bookings from the previous day that
        were either Scheduled or Booked in order to get all of the data

        Returns:
            list: Long list of bookings from the previous day that were either
            created or started, depending on the given input
        """
        bookings = []

        while True:
            all_bookings = self.getTCScheduledorTCBookedYesterday()
            if len(all_bookings) == 100:
                after_id = all_bookings[-1]["id"]
                url = (
                    "https://api.oncehub.com/v2/bookings?after="
                    + after_id
                    + "&limit=100&expand=booking_page"
                )
                new_bookings = ScheduleOnce(
                    url, self.headers
                ).getTCScheduledorTCBookedYesterday()
                bookings.append(new_bookings)
            elif len(all_bookings) < 100:
                bookings.append(all_bookings)
                break

        new_bookings = [
            item for sublist in bookings for item in sublist
        ]  # Flattens list of lists

        return new_bookings

    def getBookingDataFromListOfBookings(self):
        """Takes the booking data in it's normal form and extracts the data
        needed for a value counts dataframe

        Returns:
            list: List of dictionaries that house the Name, Booking Page and
            Source of every booking
        """
        bookings = self.appendMultipleAPIPagesOfTCScheduledorBooked()
        booking_data = []

        for booking in bookings:
            page_source_name = {}
            page_source_name["Name"] = booking["form_submission"]["name"]
            page_source_name["Page Name"] = booking["booking_page"]["label"]
            try:  # If booked on certain link, there is not a custom field,
                # though we know what the source is
                page_source_name["Source"] = booking["form_submission"][
                    "custom_fields"
                ][0]["value"]
            except:
                page_source_name["Source"] = "Inbound Triage"
            booking_data.append(page_source_name)

        return booking_data

    def getValueCountsFromSourceOfPageName(self):
        """Creates the value counts based on the source of each booking for
        each client (page name)

        Returns:
            groupby.dataframe: MultIndex groupby frame with Booking Page and
            Source as the two index's and value counts as the data
        """
        booking_data = self.getBookingDataFromListOfBookings()
        df = pd.DataFrame(booking_data)
        grouped_by_source = df.groupby("Page Name")["Source"].value_counts()

        return grouped_by_source
