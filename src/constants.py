import os


GSPREAD_CREDENTIALS = f"/Users/{os.environ['USER']}/Documents/d4ysetters/credentials/credentials.json"
AUTHORIZED_USER = f"/Users/{os.environ['USER']}/Documents/d4ysetters/credentials/authorized_user.json"

LEVEL_10_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"

SPECIALIST_NAME = "Tylee Evans Groll"

MESSAGE_DATA_URL = "https://docs.google.com/spreadsheets/d/1IfZlLzzwkC05I6fv-4ZRNFOc7ul7k0qIfeG-bk9j6AA/edit#gid=81738738"

SCHEDULE_ONCE_HEADERS = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}

SCHEDULE_ONCE_URL = (
    "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"
)

DAILY_KPIS_URL = "https://docs.google.com/spreadsheets/d/18AgIMFyPCOxHYQXRYJowihJd_i2kRMB9pzB5jdA3ZVc/edit#gid=1070219116"

PATH_TO_CSV = "/Users/louisrae/Documents/dev/dfy_setters/src/db_people.csv"
