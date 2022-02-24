import os

DATABASE_URI = "postgresql://postgres:qweasdzxcQ101@localhost:5432/general"


GSPREAD_CREDENTIALS = f"/Users/{os.environ['USER']}/Documents/d4ysetters/credentials/credentials.json"
AUTHORIZED_USER = f"/Users/{os.environ['USER']}/Documents/d4ysetters/credentials/authorized_user.json"

LEVEL_10_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"

SPECIALIST_NAME = "Tylee Evans Groll"

SCHEDULE_ONCE_HEADERS = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}

SCHEDULE_ONCE_URL = (
    "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"
)

DAILY_KPIS_URL = "https://docs.google.com/spreadsheets/d/18AgIMFyPCOxHYQXRYJowihJd_i2kRMB9pzB5jdA3ZVc/edit#gid=1070219116"

PATH_TO_CSV = "/Users/louisrae/Documents/dev/dfy_setters/src/db_people.csv"

MESSAGE_DATA_WORKBOOK = "https://docs.google.com/spreadsheets/d/1ilUCdcEP-TDUMrC8Alwp2x3Jq2LYfOzINFfF2MTY91k/edit#gid=1232583697"
