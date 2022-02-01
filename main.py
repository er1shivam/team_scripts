import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")

from src.weekly_totals import SSBTotals
from src.constants import *

func = SSBTotals(MTD_START_DATE, MTD_END_DATE, WTD_START_DATE, WTD_END_DATE)
week, month = func.getWTDandMTDTotalsDataframe()
print(week)
print(month)
