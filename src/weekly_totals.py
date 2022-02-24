"""This module is used to get the WTD and MTD totals for all relevent clients to see where issues lay
"""
import sys


sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")

from datetime import timedelta
import pandas as pd
from constants import *
import logging
from src.common import *


logging.basicConfig(
    filename="/Users/louisrae/Documents/dev/dfy_setters/logs/weekly_totals.log",
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s:%(message)s",
)


class SSBTotals:
    def __init__(self, start_date, end_date) -> None:
        """Main class that houses functions to pull data

        Args:
            start_date (datetime.date): The start date used to pull SS Total
            end_date (datetime.date): The end date used to pull SS Total
        """
        self.start_date = start_date
        self.end_date = end_date

    def getSSForEachDayInDayList(self, sheet, day_list):
        """Gives the amount of SS booked in a given time period

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook
            day_list (list): List of datetime.date objects to check

        Returns:
            int: Returns int of the amount of SS booked in that time period
        """
        df = change_date_to_datetime(sheet)
        totals = {}
        list_of_values = []
        for day in day_list:
            list_of_values.append(df[df["Date"] == day]["Total SSB"].values[0])

        total = sum([i for i in list_of_values if i])
        totals[sheet.title] = total

        return totals

    def getTotalsDataframe(self, gc, day_list):
        """Pulls together all the client SS totals and puts them in dataframe

        Returns:
            df: Dataframe with total SSB based on Timeframe
        """
        totals = {}

        daily_kpis = gc.open_by_url(DAILY_KPIS_URL)

        for sheet in daily_kpis:
            try:
                totals.update(self.getSSForEachDayInDayList(sheet, day_list))

            except Exception as e:
                logging.info(f"{sheet.title}: {e}")

        totals_df = pd.DataFrame(totals.items()).sort_values(by=1)

        return totals_df
