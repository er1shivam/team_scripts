import dfysetters.facebook_tracking as dfy
import gspread
import pandas as pd
import numpy as np

gc = gspread.oauth()

message_data_sheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1IfZlLzzwkC05I6fv-4ZRNFOc7ul7k0qIfeG-bk9j6AA/edit#gid=81738738"
).sheet1

specialist_name = "Tylee Evans Groll"

level_10 = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1Y7cQYW1MJ1HstJVJEADVqKgbI-bOMyv74159jOJQtc4/edit#gid=1480274768"
).sheet1

role_dictionary = {
    "Pod Leads": ["Girls", "No_name"],
    "Snr Specialists": [
        "Morgan",
        "Isela",
        "Caycee",
        "Pat",
        "Sean",
        "Kayla",
        "Molly N",
    ],
    "Jnr Specialists": ["Noela", "Molly C", "Zach"],
    "Setters": [
        "Alex",
        "Amanda",
        "Donnah",
        "Liz",
        "Jelyn",
        "Monica",
        "Rachel",
        "Suleyma",
    ],
}

headers = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}

url = "https://api.oncehub.com/v2/bookings?expand=booking_page&limit=100"


# leader = dfysetters.Leaderboard(
#     level_10, role_dictionary
# ).getSortedTCandSSNumbersForTeamMember()
# print(leader)

# ua = dfy.FBTracking(message_data_sheet, specialist_name).countUnanswered()
# print(ua)

# df = dfy.ScheduleOnce(url, headers).getValueCountsFromSourceOfPageName()
# print(df)

# new_df = pd.DataFrame(message_data_sheet.get_all_records())

# print(dfy.AveragePerConversation(new_df).getProspectNamesInDictionary())

df = pd.DataFrame(message_data_sheet.get_all_records())
avg = dfy.AveragePerConversation(df).getAverageReplyTimeOfAllConversations()
mins = dfy.AveragePerConversation(df).convertMstoMinutes(avg)
print(mins)
