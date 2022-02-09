from src.facebook_tracking import Leaderboard
from src.constants import *
from src.roles import *
from src.weekly_totals import *
import gspread
from datetime import date

gc = gspread.oauth(
    credentials_filename=GSPREAD_CREDENTIALS,
    authorized_user_filename=AUTHORIZED_USER,
)

level_10_sheet = gc.open_by_url(LEVEL_10_SHEET_URL).sheet1

Roles().register_all_members()
role_list = [PodLead(), SnrSpecialist(), JnrSpecialist(), Setter()]
l = Leaderboard(level_10_sheet)
df = l.getWeekTotalFromLevel10()
vc = l.getSortedTCandSSNumbersForTeamMembers(role_list, df)
print(vc)


mtd_start = date(2022, 2, 1)
mtd_end = date.today()
wtd_start = date(2022, 2, 7)
wtd_end = date.today()

df, df1 = SSBTotals(
    mtd_start, mtd_end, wtd_start, wtd_end
).getWTDandMTDTotalsDataframe()

print("This is week")
print(df)

print("This is month")
print(df1)
