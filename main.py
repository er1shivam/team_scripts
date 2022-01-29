import dfysetters.facebook_tracking as dfy
from dfysetters.constants import *


df = dfy.ScheduleOnce(
    SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
).getValueCountsFromSourceOfPageName()

booking_data = dfy.ScheduleOnce(
    SCHEDULE_ONCE_URL, SCHEDULE_ONCE_HEADERS
).getBookingDataFromListOfBookings()

for i in booking_data:
    if i["Page Name"] == "The Sponsorship Collective":
        print(i)

print(df)
