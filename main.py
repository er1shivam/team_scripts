from src.facebook_tracking import Leaderboard
from src.facebook_tracking import UnansweredMessages
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
role_list = [
    PodLead(),
    SnrSpecialist(),
    JnrSpecialist(),
    Setter(),
    Operations(),
]
l = Leaderboard(level_10_sheet)
df = l.getWeekTotalFromLevel10()
vc = l.getSortedTCandSSNumbersForTeamMembers(role_list, df)
print(vc)
