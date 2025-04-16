from datetime import date, timedelta

def get_today():
    return date.today()

def get_tomorrow():
    return date.today() + timedelta(days=1)

# def get_yesterday():
#     return date.today() - timedelta(days=1)

def get_dates_of_week(next=False):
    now = date.today()
    monday = now - timedelta(days=now.weekday())
    if next:
        monday += timedelta(days=7)
    return [monday + timedelta(days=day) for day in range(6)]

