import gspread
from gspread.models import Worksheet
import pandas as pd


def gspread_setup():

    gc = gspread.oauth()
    url = input("Provide the google sheet link you want to use: ")
    sh = gc.open_by_url(url)
    worksheet = sh.sheet1

    return worksheet


def df_setup(worksheet):
    df = pd.DataFrame(worksheet.get_all_records())
    df = df[["Conversation", "Date", "Sender"]]
    group = df.groupby(["Conversation"], sort=False)["Date"].max()

    return group, df


def num_of_unanswered_messages():
    worksheet = gspread_setup()
    group, df = df_setup(worksheet)
    unanswered = []
    for g in group:
        try:
            unanswered.append(df.loc[df["Date"] == g]["Sender"].item())
        except ValueError:
            print(
                "There was a Key Error. This is likely because one of the elements in the list is always really long. Not fully sure why"
            )

    name = input(
        "What is the name of the specialist in this account? Please provide the full name exactly: "
    )
    print(
        f"There are {len(unanswered) - unanswered.count(name)} unanswered messages for {name}"
    )
    print(unanswered)


if __name__ == "__main__":
    num_of_unanswered_messages()
