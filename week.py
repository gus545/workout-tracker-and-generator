from datetime import datetime, timedelta
from api_manager import API_Manager

class Week:

    def __init__(self, week_number):
        self.week_start = self.get_week_start()
        self.week_number = week_number
        self.week_end = self.week_start + timedelta(days=6)
        self.api_manager = API_Manager()

    def get_week_start(self):
        # Return date of most recent Monday
        today = datetime.now()
        today = today - timedelta(days=today.weekday())
        return today.date()
    
    def fetch_week_sets(self):

        """
        Fetches exercises for the week from the Notion database.
        
        Returns:
            list: A list of exercises for the week.
        """
        try:
            exercises = self.api_manager.query_sets_in_date_range(self.week_start, self.week_end)
            return exercises
        except Exception as e:
            print(f"Error fetching exercises: {e}")
            return []

