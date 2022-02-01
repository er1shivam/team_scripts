import imp
import pytest
import numpy as np
import pandas as pd
import datetime
from src.facebook_tracking import AveragePerConversation
from src.facebook_tracking import UnansweredMessages
from src.facebook_tracking import ScheduleOnce
from src.facebook_tracking import Leaderboard
from src.constants import *


@pytest.fixture()
def tracking():
    tracking = UnansweredMessages(MESSAGE_DATA_SHEET, SPECIALIST_NAME)
    return tracking


@pytest.fixture()
def averages():
    df = UnansweredMessages(
        MESSAGE_DATA_SHEET, SPECIALIST_NAME
    ).dictionaryToDataframe()
    averages = AveragePerConversation(df)
    return averages


class TestFBTracking:
    def test_canReturnListFromSheet(self, tracking):
        messages = tracking.getSheetValues()
        assert isinstance(messages, list)

    def test_listOfDictionariesHasCorrectKeys(self, tracking):
        messages = tracking.getSheetValues()
        output_keys = messages[0].keys()
        correct_keys = ["Conversation", "Sender", "Timestamp (ms)"]
        assert all(item in output_keys for item in correct_keys)

    def test_canEmptyListOfBadDictionaryEntries(self, tracking):
        all_messages = tracking.emptyDictionary()
        assert 0 not in [len(i["Conversation"]) for i in all_messages]

    def test_canCreateDataframeFromDictionary(self, tracking):
        dataframe = tracking.dictionaryToDataframe()
        assert isinstance(dataframe, pd.DataFrame)

    def test_canGroupBasedOnConversation(self, tracking):
        grouped_data = tracking.groupbyConversation()
        assert 1610000000000 < np.mean(grouped_data)

    def test_returnSenderOfHighestTimestamp(self, tracking):
        last_sender_list = tracking.listLastSenders()
        assert SPECIALIST_NAME in last_sender_list

    def test_countingHowManyUnanswered(self, tracking):
        unanswered = tracking.countUnanswered()
        assert isinstance(unanswered, int)


class TestAveragePerConversation:
    def test_getProspectNamesInDictionary(self, averages, tracking):
        name_list = averages.getProspectNamesInDictionary()
        df = tracking.dictionaryToDataframe()
        first_name = df["Conversation"].iloc[0]
        assert first_name in name_list

    def test_groupDataframeByTimestamp(self, averages):
        timestamp_df = averages.groupDataframeByTimestamp()
        assert isinstance(timestamp_df, pd.Series)

    def test_createDictionaryWithProspectNamesAndListOfReplyTimes(
        self, averages, tracking
    ):
        dictionary_created = (
            averages.createDictionaryWithProspectNamesAndListOfReplyTimes()
        )
        df = tracking.dictionaryToDataframe()
        first_name = df["Conversation"].iloc[0]

        assert first_name in dictionary_created

    def test_getAverageReplyTimePerConversation(self, averages):
        d = averages.createDictionaryWithProspectNamesAndListOfReplyTimes()
        name = list(d)[0]
        reply_time_avg = averages.getAverageReplyTimePerConversation(name)
        assert (86400000 > reply_time_avg > 1) or isinstance(
            reply_time_avg, type(np.nan)
        )

    def test_getAverageReplyTimeOfAllConversations(self, averages):
        total_average = averages.getAverageReplyTimeOfAllConversations()
        assert isinstance(total_average, float) and 86400000 > total_average > 1

    def test_convertMstoMinutes(self, averages):
        total_average = averages.getAverageReplyTimeOfAllConversations()
        ms_response = averages.convertMstoMinutes(total_average)
        assert 1440 > ms_response > 0.009


class TestLeaderboard:
    def test_getWeekTotalromLevel10(self):
        data = Leaderboard(
            LEVEL_10_SHEET, ROLE_DICTIONARY
        ).getWeekTotalFromLevel10()
        week_data = data["Week Total"].values
        sum_of_week_total = sum([i for i in week_data if isinstance(i, int)])
        assert isinstance(sum_of_week_total, int)

    def test_getDictionaryOfCellsToCheck(self):
        returned_dict = Leaderboard(
            LEVEL_10_SHEET, ROLE_DICTIONARY
        ).getDictionaryOfCellsToCheck()
        list_of_keys_in_dictionary = list(returned_dict.values())
        list_of_keys_in_data = list(
            Leaderboard(LEVEL_10_SHEET, ROLE_DICTIONARY)
            .getWeekTotalFromLevel10()
            .index.values
        )
        flattened_dictionary = [
            item for sublist in list_of_keys_in_dictionary for item in sublist
        ]
        assert all(
            elem in list_of_keys_in_data for elem in flattened_dictionary
        )

    def test_getValueForEachTeamMemberInTheirRole(self):
        df = Leaderboard(
            LEVEL_10_SHEET, ROLE_DICTIONARY
        ).getValueForEachTeamMemberInTheirRole()
        frame_columns = list(df.columns)
        role_columns = list(ROLE_DICTIONARY.keys())
        assert role_columns == frame_columns

    def test_getSortedTCandSSNumbersForTeamMember(self):
        df = Leaderboard(
            LEVEL_10_SHEET, ROLE_DICTIONARY
        ).getSortedTCandSSNumbersForTeamMember()
        basic_df = Leaderboard(
            LEVEL_10_SHEET, ROLE_DICTIONARY
        ).getWeekTotalFromLevel10()

        girls_ss_sorted = int(df.loc["Girls SS"]["Pod Leads"])
        isela_ss_sorted = int(df.loc["Isela SS"]["Snr Specialists"])
        amanda_tc_sorted = int(df.loc["Amanda TC"]["Setters"])

        girls_ss_basic = int(basic_df.loc["Girls SS"]["Week Total"])
        isela_ss_basic = int(basic_df.loc["Isela SS"]["Week Total"])
        amanda_tc_basic = int(basic_df.loc["Amanda TC"]["Week Total"])

        girls_result = girls_ss_basic == girls_ss_sorted
        isela_result = isela_ss_basic == isela_ss_sorted
        amanda_result = amanda_tc_basic == amanda_tc_sorted

        assert all([girls_result, isela_result, amanda_result])


class TestScheduleOnce:
    def test_getFullBookingList(self):
        booking_list = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getFullBookingList()
        assert len(booking_list) == 100

    def test_getTCScheduledorTCBookedYesterday(self):
        booking_list = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getTCScheduledorTCBookedYesterday()

        yesterday = str(datetime.date.today() - datetime.timedelta(1))

        starting_times = set()
        for f in booking_list:
            starting_times.add(f["starting_time"][0:10])

        starting = list(starting_times)[0]

        created = set()
        for f in booking_list:
            created.add(f["creation_time"][0:10])

        create = list(created)[0]
        assert create == yesterday or starting == yesterday

    def test_getBookingDataFromListOfBookings(self):
        booking_data = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getBookingDataFromListOfBookings()
        assert not any(
            d["Page Name"] == "Big Rig Freight Services" for d in booking_data
        )

    def test_getValueCountsFromSourceOfPageName(self):
        booking_data = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromSourceOfPageName()
        indexes = list(booking_data.index)
        check = [item for item in indexes if item[0] == "Big Freight Services"]
        check2 = [item for item in indexes if item[1] == "Outbound Dial"]
        assert (len(check) > 0) and (len(check2) > 0)
