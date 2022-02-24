import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters")

from src.constants import *
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta


def parse_csv_of_roles():
    """Uses postgres to pull through all members

    Returns:
        dataframe: Returns two columns, name and role
    """
    engine = create_engine(DATABASE_URI)

    myQuery = "SELECT full_name,company_role FROM team"
    df = pd.read_sql_query(myQuery, engine)
    return df


def change_date_to_datetime(sheet):
    df = pd.DataFrame(sheet.get_all_records())
    df["Date"] = pd.to_datetime(df[df.columns[0]])

    return df


def get_day_list(start_date, end_date):

    daylist = []
    delta = end_date - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        daylist.append(day.strftime("%Y-%m-%d"))

    return daylist
