from gcsa.google_calendar import GoogleCalendar
from datetime import datetime
from datetime import timedelta
from collections import Counter

today = datetime.today()
week_ago = today - timedelta(days=7)


calendar = GoogleCalendar(token_path="/Users/louisrae/.config/token.pickle")

events = list(
    calendar.get_events(week_ago, today, order_by="startTime", single_events=True)
)

booking_pages = []
for e in events:
    try:
        page = e.description.split()
        page_index = page.index("Booking")
        booking_pages.append(" ".join(page[page_index : page_index + 5]))
    except AttributeError:
        pass
    except ValueError:
        pass


print(Counter(booking_pages))
