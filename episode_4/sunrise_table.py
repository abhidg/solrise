from sunrise import sunset
import datetime

latitude = 51.75  # Put your own coordinates here!
longitude = -1.25


def sunset_table(latitude, longitude, start_date, duration_days: int = 30):
    "Will show table of sunsets for the given location"
    for i in range(duration_days):
        cur_date = start_date + datetime.timedelta(days=i)
        print(sunset(latitude, longitude, date=cur_date))


if __name__ == "__main__":
    today = datetime.datetime.now().date()
    sunset_table(latitude, longitude, datetime.date(today.year, today.month, 1))
