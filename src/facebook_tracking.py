"""This module houses all of the functions needed to pull data from a CSV 
(or Google Sheet) with  Facebook message data, and pull the necessary metrics 
from it """

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
            ]
            last_message_time = last_message_time["Sender"].values[0]
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
        """Gives the average time between timestamps in a dictionary of lists,
        keyed by the conversation name

        Args:
            reply_time_dict (dict): Key: Conversation, Value: List of timestamps
             for each message in that conversation
            name (str): Which key to check the average for, usually used in a
            for loop in other function

        Returns:
            np.nan / float: Returns float of average ms between reply times. If
            certain key does not have average, returns nan to use in future math
        """
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
        """Gets the overall average reply time in a dictionary of lists

        Args:
            reply_time_dict (dict): [Key: Conversation, Value: List of
            timestamps for each message in that conversation

        Returns:
            float: Minutes on average that it took us to reply
        """
        list_of_averages = []
        for name in reply_time_dict:
            avg_time = self.getAverageReplyTimePerConversation(
                reply_time_dict, name
            )
            list_of_averages.append(str(avg_time))

        cleaned_averages = [float(i) for i in list_of_averages if i != "nan"]

        return round(mean(cleaned_averages) / 60000, 2)


class Leaderboard:
    def __init__(self, sheet):
        """This class generates a leaderboard based on our team's metrics in
        any given week

        Args:
            sheet (gspread.models.Worksheet): This sheet should have a week
            total column to pull the relevant metrics from
        """

        self.sheet = sheet

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

    def getValueForEachMemberInRole(self, role, level_10_df):

        values_per_department = {}
        for person in role:
            for metric in list(level_10_df.index.values):
                if person.name in metric:
                    values_per_department[person.name] = int(
                        level_10_df.loc[metric].values[0]
                    )

        return values_per_department

    def getSortedTCandSSNumbersForTeamMembers(self, role_list, level_10_df):
        """Creates a dataframe with all team members and all metrics that
        are relevant to their role

        Returns:
            dataframe: dataframe with columns based on role and index on each
            individual metric. There are a lot of NaN values
        """
        lofd = {}
        for role in role_list:
            ls = role.get_all_members()
            d = self.getValueForEachMemberInRole(ls, level_10_df)
            lofd[role.title] = dict(
                sorted(d.items(), key=lambda item: item[1], reverse=True)
            )

        return pd.DataFrame(lofd)


class ScheduleOnce:
    def __init__(self, url, headers):

        self.url = url
        self.headers = headers

    def getBookingData(self, params):

        url = self.url
        bookings = []

        while True:
            response = requests.request(
                "GET", url=url, headers=self.headers, params=params
            ).json()["data"]

            for i in response:
                bookings.append(i)

            if len(response) >= 100:
                url = (
                    "https://api.oncehub.com/v2/bookings?after="
                    + bookings[-1]["id"]
                    + "&limit=100&expand=booking_page"
                )

            elif len(response) < 100:
                break

        return bookings

    def getValueCountsFromDict(self, data):

        booking_data = []
        for booking in data:
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

        vc = (
            pd.DataFrame(booking_data)
            .groupby("Page Name")["Source"]
            .value_counts()
        )

        return vc
