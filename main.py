import sys
from datetime import date

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")

from src.weekly_totals import SSBTotals
from src.constants import *


mtd_start = date(2022, 2, 1)
mtd_end = date.today()
wtd_start = date(2022, 1, 31)
wtd_end = date.today()

func = SSBTotals(mtd_start, mtd_end, wtd_start, wtd_end)
week, month = func.getWTDandMTDTotalsDataframe()
print(week)
print(month)
