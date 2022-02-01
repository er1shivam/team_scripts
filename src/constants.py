import gspread
from src.roles import Roles
from datetime import date

gc = gspread.oauth(
    credentials_filename="/Users/louisrae/Documents/dev/dfy_setters/credentials/credentials.json",
    authorized_user_filename="/Users/louisrae/Documents/dev/dfy_setters/credentials/authorized_user.json",
)

LEVEL_10_SHEET = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
).sheet1

SPECIALIST_NAME = "Tylee Evans Groll"

MESSAGE_DATA_SHEET = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1IfZlLzzwkC05I6fv-4ZRNFOc7ul7k0qIfeG-bk9j6AA/edit#gid=81738738"
).sheet1

SCHEDULE_ONCE_HEADERS = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}

SCHEDULE_ONCE_URL = (
    "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"
)

Roles().register_all_members()
ROLE_DICTIONARY = Roles().all_roles


# Start of constants for wtd and mtd

MTD_START_DATE = date(2022, 2, 1)
MTD_END_DATE = date.today()
WTD_START_DATE = date(2022, 1, 31)
WTD_END_DATE = date.today()

DAILY_KPIS_WORKBOOK = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/18AgIMFyPCOxHYQXRYJowihJd_i2kRMB9pzB5jdA3ZVc/edit#gid=1070219116"
)

TESTING_SHEET = DAILY_KPIS_WORKBOOK.sheet1
