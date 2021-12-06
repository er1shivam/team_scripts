import gspread
import dfysetters
import pandas as pd
from datetime import date


gc = gspread.oauth()
url = input("Which Google Sheet Do You Want Data On? ")
sh = gc.open_by_url(url)
worksheet_list = sh.worksheets()


for worksheet in worksheet_list:
    print(f"Now we are on sheet {worksheet.title}")
    specialist = input("What is the Specialist's full name on this sheet: ")

    data = dfysetters.FBTracking(gc, url, sh, worksheet, specialist)

    message_tracking = data.value_counts_df()  # DF
    conversation_averages = data.average_per_conversation()  # DF

    account_data = pd.DataFrame.from_dict(
        {
            "Date": [date.today()],
            "# Unanswered Messages": data.find_unanswered(),
            "Average Reply Time (m)": data.average_of_all_conversations(),
            "Account": specialist,
        }
    )

    message_tracking_csv = "message_tracking.csv"
    conversation_averages_csv = "conversation_averages.csv"
    account_data_csv = "account_data.csv"

    message_tracking.to_csv(message_tracking_csv, mode="a", header=None)
    print(f"Message Tracking has been pushed to CSV for {specialist}")

    account_data.to_csv(account_data_csv, mode="a", header=None)
    print(f"Account Data has been pushed to CSV for {specialist}")
