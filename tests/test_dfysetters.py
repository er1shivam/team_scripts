import gspread
import pytest
import numpy as np
import pandas as pd
import datetime
from src.facebook_tracking import AveragePerConversation
from src.facebook_tracking import UnansweredMessages
from src.facebook_tracking import ScheduleOnce
from src.facebook_tracking import Leaderboard
from src.constants import *
from src.roles import Roles

Roles().register_all_members()
ls = Roles().listAllTeamMembersInCompany()
role_dict = {
    "Pod Lead": [],
    "Snr Specialist": [],
    "Jnr Specialist": [],
    "Setter": [],
}
for i in ls:
    role_dict[i.role].append(i.name)

ROLE_DICTIONARY = role_dict


gc = gspread.oauth(
    credentials_filename=GSPREAD_CREDENTIALS,
    authorized_user_filename=AUTHORIZED_USER,
)

level_10_sheet = gc.open_by_url(LEVEL_10_SHEET_URL).sheet1
message_data_sheet = gc.open_by_url(MESSAGE_DATA_URL).sheet1


@pytest.fixture()
def tracking():
    tracking = UnansweredMessages(message_data_sheet, SPECIALIST_NAME)
    return tracking


@pytest.fixture()
def average():
    average = AveragePerConversation(message_data_sheet)
    return average


@pytest.fixture()
def leaderboard():
    leaderboard = Leaderboard(level_10_sheet, role_dict)
    return leaderboard


class TestFBTracking:
    def test_specialistIsInDataframe(self, tracking):
        df, gdf = tracking.getSheetValuesToDataframe()
        assert SPECIALIST_NAME in list(df["Sender"].values)

    def test_canPerformMathOnTimestamp(self, tracking):
        df, gdf = tracking.getSheetValuesToDataframe()
        assert sum(gdf.values) == 262789701437672


class TestAveragePerConversation:
    def test_DictionaryHasTimetampValues(self, average):
        d = average.getProspectNamesInDictionary()
        total_timestamps = sum([sum(ls) for ls in list(d.values())])
        assert total_timestamps == 1269609215323793

    def test_DictionaryReturnsCorrectAverage(self, average):
        d = average.getProspectNamesInDictionary()
        avg = average.getAverageMinutesToReplyForAllConversations(d)
        assert avg == 43.65


class TestLeaderboard:
    def test_getWeekTotalromLevel10(self, leaderboard):
        data = leaderboard.getWeekTotalFromLevel10()
        week_data = data["Week Total"].values
        sum_of_week_total = sum([i for i in week_data if isinstance(i, int)])
        assert isinstance(sum_of_week_total, int)

    def test_getDictionaryOfCellsToCheck(self, leaderboard):
        returned_dict = leaderboard.getDictionaryOfCellsToCheck()
        list_of_keys_in_dictionary = list(returned_dict.values())
        list_of_keys_in_data = list(
            leaderboard.getWeekTotalFromLevel10().index.values
        )
        flattened_dictionary = [
            item for sublist in list_of_keys_in_dictionary for item in sublist
        ]
        assert all(
            elem in list_of_keys_in_data for elem in flattened_dictionary
        )

    def test_getValueForEachTeamMemberInTheirRole(self, leaderboard):
        df = leaderboard.getValueForEachTeamMemberInTheirRole()
        frame_columns = list(df.columns)
        role_columns = list(role_dict.keys())
        assert role_columns == frame_columns

    def test_getSortedTCandSSNumbersForTeamMember(self, leaderboard):
        df = leaderboard.getSortedTCandSSNumbersForTeamMember()
        basic_df = leaderboard.getWeekTotalFromLevel10()

        girls_ss_sorted = int(df.loc["Girls SS"]["Pod Lead"])
        isela_ss_sorted = int(df.loc["Isela SS"]["Snr Specialist"])
        amanda_tc_sorted = int(df.loc["Amanda TC"]["Setter"])

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
