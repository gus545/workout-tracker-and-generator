from datetime import datetime, timedelta

class Week:

    def __init__(self, week_number):
        self.week_start = get_week_start()
        self.week_number = week_number

    def get_week_start():
        # Return date of most recent Monday
        today = datetime.now()
        today = today - timedelta(days=today.weekday())
        return today.date()