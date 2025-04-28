from notion_client import Client
import os

class Fetcher:
    def __init__(self, notion_client):
        self.notion_client = notion_client
        

    def query_pages_in_date_range(self, database_id, start_date, end_date):
        """
        Query pages in a Notion database within a specified Date property range.     
           
        Args:
            start_date (str): The start date in ISO format (YYYY-MM-DD).
            end_date (str): The end date in ISO format (YYYY-MM-DD).
        
        Returns:
            list: A list of sets within the specified date range.
        """
        try:
            response = self.notion_client.databases.query(
                database_id=os.environ["DBID_WORKOUTLOG"],
                filter={
                    "and": [
                        {"property": "Date",
                        "date": {
                            "on_or_after": start_date.isoformat(),

                        }},
                        {"property": "Date",
                        "date": {
                            "on_or_before": end_date.isoformat()
                        }}
                    ]
                }
            )
            return response["results"]
        except Exception as e:
            raise RuntimeError(f"Failed to query sets: {e}")
        
    def fetch_all_pages(self, database_id):
        """
        Fetch all pages from a Notion database.

        Args:
            database_id (str): The ID of the Notion database.

        Returns:
            list: A list of all pages in the database.
        """
        try:
            results = []
            next_cursor = None
            while True:
                response = self.notion_client.databases.query(
                    database_id=database_id,
                    start_cursor=next_cursor
                )
                results.extend(response["results"])
                next_cursor = response.get("next_cursor")
                if not next_cursor:
                    break
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to fetch pages: {e}")