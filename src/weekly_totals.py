"""This module is used to get the WTD and MTD totals for all relevent clients to see where issues lay
"""
import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters/src")

from datetime import timedelta
import time
import pandas as pd
from constants import *
import logging
import gspread

logging.basicConfig(
    filename="/Users/louisrae/Documents/dev/dfy_setters/logs/weekly_totals.log",
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s:%(message)s",
)


class SSBTotals:
    def __init__(self, mtd_start, mtd_end, wtd_start, wtd_end) -> None:
        """Main class that houses functions to pull data

        Args:
            mtd_start (datetime.date): The start date used if you want to pull MTD numbers
            mtd_end (datetime.date): The end date used if you want to pull MTD numbers
            wtd_start (datetime.date): The start date used if you want to pull WTD numbers
            wtd_end (datetime.date): The end date used if you want to pull WTD numbers
        """
        self.mtd_start = mtd_start
        self.mtd_end = mtd_end
        self.wtd_start = wtd_start
        self.wtd_end = wtd_end

    def getDayList(self, start_date, end_date):
        """Creates a list of datetime objects to check in further functions

        Args:
            start_date (datetime.date): Start date of desired time frame
            end_date (datetime.date): End date of desired time frame

        Returns:
            list: List of datetime.date objects
        """

        daylist = []
        delta = end_date - start_date
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            daylist.append(day.strftime("%Y-%m-%d"))

        return daylist

    def getMTDDateList(self):
        """Gets the list of dates between MTD Start and MTD End

        Returns:
            list: List of Datetime objects between two dates
        """
        return self.getDayList(self.mtd_start, self.mtd_end)

    def getWTDDateList(self):
        """Gets the list of dates between MTD Start and MTD End

        Returns:
            list: List of Datetime objects between two dates
        """
        return self.getDayList(self.wtd_start, self.wtd_end)

    def changeDateColumnToDatetime(self, sheet):
        """Converts the first column to datetime for future referencing with date lists

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook

        Returns:
            [type]: [description]
        """
        df = pd.DataFrame(sheet.get_all_records())
        df["Date"] = pd.to_datetime(df[df.columns[0]])

        return df

    def getSSForEachDayInDayList(self, sheet, day_list):
        """Gives the amount of SS booked in a given time period

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook
            day_list (list): List of datetime.date objects to check

        Returns:
            int: Returns int of the amount of SS booked in that time period
        """
        df = self.changeDateColumnToDatetime(sheet)
        list_of_values = []
        for day in day_list:
            list_of_values.append(df[df["Date"] == day]["Total SSB"].values[0])

        week_total_ss = sum([i for i in list_of_values if i])
        return week_total_ss

    def getWTDSSTotal(self, sheet):
        """Gives the amount of SS booked WTD

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook

        Returns:
            dict: Returns dict of k:Title of sheet and v: amount of SS booked in WTD period
        """
        week_totals = {}
        week_time_frame = self.getWTDDateList()
        week_ss_total = self.getSSForEachDayInDayList(sheet, week_time_frame)
        week_totals[sheet.title] = week_ss_total

        return week_totals

    def getMTDSSTotal(self, sheet):
        """Gives the amount of SS booked MTD

        Args:
            sheet (gspread.worksheet): Worksheet from a gspread workbook

        Returns:
            dict: Returns dict of k:Title of sheet and v: amount of SS booked in MTD period
        """
        month_totals = {}
        month_time_frame = self.getMTDDateList()
        month_ss_total = self.getSSForEachDayInDayList(sheet, month_time_frame)
        month_totals[sheet.title] = month_ss_total

        return month_totals

    def getWTDandMTDTotalsDataframe(self):
        """Pulls together all the client WTD and MTD SS totals and puts them in dataframe

        Returns:
            tuple: 2 dataframes with WTD and MTD totals of every client
        """
        full_week_totals = {}
        full_month_totals = {}
        gc = gspread.oauth(
            credentials_filename=GSPREAD_CREDENTIALS,
            authorized_user_filename=AUTHORIZED_USER,
        )

        daily_kpis = gc.open_by_url(DAILY_KPIS_URL)

        for sheet in daily_kpis:
            try:
                full_week_totals.update(self.getWTDSSTotal(sheet))
                time.sleep(3)
                full_month_totals.update(self.getMTDSSTotal(sheet))

            except Exception as e:
                logging.info(f"{sheet.title}: {e}")

        week_df = pd.DataFrame(full_week_totals.items()).sort_values(by=1)
        month_df = pd.DataFrame(full_month_totals.items()).sort_values(by=1)

        return week_df, month_df
