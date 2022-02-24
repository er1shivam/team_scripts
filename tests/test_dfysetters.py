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
message_data_workbook = gc.open_by_url(MESSAGE_DATA_WORKBOOK)

from_date = str(datetime.date(2022, 2, 21))
to_date = str(datetime.date(2022, 2, 22))


class TestUnansweredMessages:
    @pytest.fixture()
    def tracking(self):
        tracking = UnansweredMessages(message_data_workbook)
        return tracking

    def test_specialistIsInDataframe(self, tracking):
        df = tracking.get_sheet_values_to_dataframe(
            message_data_workbook.sheet1
        )
        assert "Tylee Evans Groll" in list(df["Sender"].values)

    def test_canPerformMathOnTimestamp(self, tracking):
        d = tracking.get_all_unanswered(message_data_workbook)
        assert 50 == sum(d.values())


class TestAveragePerConversation:
    @pytest.fixture()
    def average(self):
        average = AveragePerConversation(message_data_workbook.sheet1)
        return average

    def test_DictionaryHasTimetampValues(self, average):
        d = average.getProspectNamesInDictionary()
        total_timestamps = sum([sum(ls) for ls in list(d.values())])
        assert total_timestamps == 60763938034603

    def test_DictionaryReturnsCorrectAverage(self, average):
        d = average.getProspectNamesInDictionary()
        avg = average.getAverageMinutesToReplyForAllConversations(d)
        assert avg == 6.62


class TestLeaderboard:
    @pytest.fixture()
    def leaderboard(self):
        leaderboard = Leaderboard(level_10_sheet)
        return leaderboard

    def test_getWeekTotalromLevel10(self, leaderboard):
        data = leaderboard.getWeekTotalFromLevel10()
        assert "Tylee Groll SS" in data.index.values

    def test_canGetAllTeamDataIntoDataframe(self, leaderboard):
        data = leaderboard.getWeekTotalFromLevel10()
        todo = leaderboard.getSortedTCandSSNumbersForTeamMembers(
            role_list, data
        )
        assert 144 == todo.sum().sum()


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

        assert tcs.values.sum() == 71

    def test_allTCBookedInValueCounts(self, scheduleonce):
        booked_params = {
            "creation_time.gt": from_date,
            "creation_time.lt": to_date,
        }

        booked = scheduleonce.getBookingData(booked_params)
        tcb = ScheduleOnce(
            SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
        ).getValueCountsFromDict(booked)

        assert tcb.values.sum() == 60
