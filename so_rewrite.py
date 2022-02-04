import pandas as pd
import gspread
from src.constants import *
import numpy as np
from statistics import mean
import datetime
import requests

gc = gspread.oauth(
    credentials_filename=GSPREAD_CREDENTIALS,
    authorized_user_filename=AUTHORIZED_USER,
)

level_10_sheet = gc.open_by_url(LEVEL_10_SHEET_URL).sheet1
message_data_sheet = gc.open_by_url(MESSAGE_DATA_URL).sheet1

from_date = str(datetime.date.today() - datetime.timedelta(1))
to_date = str(datetime.date.today())

params = {"creation_time.gt": "", "creation_time.lt": ""}


class ScheduleOnce:
    def __init__(self, url, headers, from_date, to_date):

        self.url = url
        self.headers = headers
        self.from_date = from_date
        self.to_date = to_date

    def getBookingData(self, params):

        url = self.url
        bookings = []

        while True:
            response = requests.request(
                "GET", url=url, headers=self.headers, params=params
            ).json()["data"]

            for i in response:
                bookings.append(i)

            if len(response) >= 100:
                url = (
                    "https://api.oncehub.com/v2/bookings?after="
                    + bookings[-1]["id"]
                    + "&limit=100&expand=booking_page"
                )

            elif len(response) < 100:
                break

        return bookings

    def getTCScheduledData(self):
        params = {
            "starting_time.gt": self.from_date,
            "starting_time.lt": self.to_date,
        }
        bookings = self.getBookingData(params)
        return bookings

    def getTCBookedData(self):
        params = {
            "creation_time.gt": self.from_date,
            "creation_time.lt": self.to_date,
        }
        bookings = self.getBookingData(params)
        return bookings

    def getValueCountsFromDict(self, data):

        booking_data = []
        for booking in data:
            page_source_name = {}
            page_source_name["Name"] = booking["form_submission"]["name"]
            page_source_name["Page Name"] = booking["booking_page"]["label"]
            try:  # If booked on certain link, there is not a custom field,
                # though we know what the source is
                page_source_name["Source"] = booking["form_submission"][
                    "custom_fields"
                ][0]["value"]
            except:
                page_source_name["Source"] = "Inbound Triage"
            booking_data.append(page_source_name)

        vc = (
            pd.DataFrame(booking_data)
            .groupby("Page Name")["Source"]
            .value_counts()
        )

        return vc

    def getTCScheduledValueCounts(self):
        data = self.getTCScheduledData()
        scheduled_counts = self.getValueCountsFromDict(data)
        return scheduled_counts

    def getTCBookedValueCounts(self):
        data = self.getTCBookedData()
        scheduled_counts = self.getValueCountsFromDict(data)
        return scheduled_counts


data1 = ScheduleOnce(
    SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS, from_date, to_date
).getTCScheduledData()
