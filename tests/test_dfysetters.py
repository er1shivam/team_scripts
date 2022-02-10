import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters")
import gspread
import pytest
import datetime
from src.facebook_tracking import *
from src.constants import *
from src.roles import *

Roles().register_all_members()
role_list = [PodLead(), SnrSpecialist(), JnrSpecialist(), Setter()]

gc = gspread.oauth(
    credentials_filename=GSPREAD_CREDENTIALS,
    authorized_user_filename=AUTHORIZED_USER,
)

level_10_sheet = gc.open_by_url(LEVEL_10_SHEET_URL).sheet1
message_data_sheet = gc.open_by_url(MESSAGE_DATA_URL).sheet1

from_date = str(datetime.date.today() - datetime.timedelta(1))
to_date = str(datetime.date.today())


class TestFBTracking:
    @pytest.fixture()
    def tracking(self):
        tracking = UnansweredMessages(message_data_sheet, SPECIALIST_NAME)
        return tracking

    def test_specialistIsInDataframe(self, tracking):
        df, gdf = tracking.getSheetValuesToDataframe()
        assert SPECIALIST_NAME in list(df["Sender"].values)

    def test_canPerformMathOnTimestamp(self, tracking):
        df, gdf = tracking.getSheetValuesToDataframe()
        assert sum(gdf.values) == 262789701437672


class TestAveragePerConversation:
    @pytest.fixture()
    def average(self):
        average = AveragePerConversation(message_data_sheet)
        return average

    def test_DictionaryHasTimetampValues(self, average):
        d = average.getProspectNamesInDictionary()
        total_timestamps = sum([sum(ls) for ls in list(d.values())])
        assert total_timestamps == 1269609215323793

    def test_DictionaryReturnsCorrectAverage(self, average):
        d = average.getProspectNamesInDictionary()
        avg = average.getAverageMinutesToReplyForAllConversations(d)
        assert avg == 43.65


class TestLeaderboard:
    @pytest.fixture()
    def leaderboard(self):
        leaderboard = Leaderboard(level_10_sheet)
        return leaderboard

    def test_getWeekTotalromLevel10(self, leaderboard):
        data = leaderboard.getWeekTotalFromLevel10()
        assert "Girls SS" in data.index.values

    def test_canGetAllTeamDataIntoDataframe(self, leaderboard):
        data = leaderboard.getWeekTotalFromLevel10()
        todo = leaderboard.getSortedTCandSSNumbersForTeamMembers(
            role_list, data
        )
        assert 165 == todo.sum().sum()


class TestScheduleOnce:
    @pytest.fixture()
    def scheduleonce(self):
        scheduleonce = ScheduleOnce(SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS)
        return scheduleonce

    def test_allTCScheduledInValueCounts(self, scheduleonce):
        scheduled_params = {
            "starting_time.gt": from_date,
            "starting_time.lt": to_date,
        }

        scheduled = scheduleonce.getBookingData(scheduled_params)
        tcs = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromDict(scheduled)

        assert tcs.values.sum() == 79

    def test_allTCBookedInValueCounts(self, scheduleonce):
        booked_params = {
            "creation_time.gt": from_date,
            "creation_time.lt": to_date,
        }

        booked = scheduleonce.getBookingData(booked_params)
        tcb = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromDict(booked)

        assert tcb.values.sum() == 68
