from dfysetters import ScheduleOnce

url = "https://api.oncehub.com/v2/bookings?"
headers = {
    "Accept": "application/json",
    "API-Key": "d7459f78d474f09276b4d708d2f2a161",
}
booking = ScheduleOnce(url, headers)
df = booking.create_value_counts_dataframe()
print(df)
