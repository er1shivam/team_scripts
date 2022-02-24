import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")
from src.weekly_totals import SSBTotals
from src.constants import *
from src.common import *
import gspread
from datetime import date


gc = gspread.oauth(
    credentials_filename=GSPREAD_CREDENTIALS,
    authorized_user_filename=AUTHORIZED_USER,
)

start = date(2022, 1, 1)
end = date(2022, 1, 15)


def test_canWTDListOfDaysIsListAndContainsDates():
    days = get_day_list(start, end)
    first_date = days[0]
    assert isinstance(days, list) and "2022" in first_date


def test_canMTDListOfDaysIsListAndContainsDates():
    days = get_day_list(start, end)
    first_date = days[0]
    assert isinstance(days, list) and "2022" in first_date


def test_allClientsAreInDataframe():
    days = get_day_list(start, end)
    ss = SSBTotals(start, end).getTotalsDataframe(gc, days)
    assert sum(ss.index) == 406
