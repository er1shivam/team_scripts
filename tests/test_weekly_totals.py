import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")

import pandas
from src.weekly_totals import SSBTotals
from src.constants import *
import pytest


WTD_DATE_LIST = SSBTotals(
    MTD_START_DATE, MTD_END_DATE, WTD_START_DATE, WTD_END_DATE
).getWTDDateList()

MTD_DATE_LIST = SSBTotals(
    date(2022, 1, 1), MTD_END_DATE, WTD_START_DATE, WTD_END_DATE
).getMTDDateList()


@pytest.fixture
def ss_call():
    ss_call = SSBTotals(
        MTD_START_DATE, MTD_END_DATE, WTD_START_DATE, WTD_END_DATE
    )
    return ss_call


def test_canWTDListOfDaysIsListAndContainsDates(ss_call):
    days = ss_call.getWTDDateList()
    first_date = days[0]
    assert isinstance(days, list) and "2022" in first_date


def test_canMTDListOfDaysIsListAndContainsDates(ss_call):
    days = ss_call.getMTDDateList()
    first_date = days[0]
    assert isinstance(days, list) and "2022" in first_date


def test_canConvertColumnToDate(ss_call):
    df = ss_call.changeDateColumnToDatetime(TESTING_SHEET)
    date_column = df["Date"]
    assert isinstance(date_column.iloc[1], pandas.Timestamp)


def test_getMTDSSTotal(ss_call):
    wtd = ss_call.getWTDSSTotal(TESTING_SHEET)
    ss_num = list(wtd.values())[0]
    assert isinstance(ss_num, int) and (150 > ss_num >= 0)


def test_getWTDSSTotal(ss_call):
    mtd = ss_call.getMTDSSTotal(TESTING_SHEET)
    ss_num = list(mtd.values())[0]
    assert isinstance(ss_num, int) and (150 > ss_num >= 0)


def test_allClientsAreInDataframe(ss_call):
    wtd_ss, mtd_ss = ss_call.getWTDandMTDTotalsDataframe()
    assert (len(wtd_ss.index) > 20) and (len(mtd_ss) > 20)
