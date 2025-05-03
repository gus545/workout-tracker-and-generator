from notion_client import Client
import os
import datetime
from typing import Union
import logging

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, notion_client):
        self.notion_client = notion_client
        

    def query_pages_by_last_edited_time(self, db_id, last_edited_time: Union[str, datetime.date]):
        """
        Query pages in a Notion database by their last edited time.
        """
        logger.info(f"Querying pages edited since {last_edited_time}...")
        try:
            next_cursor = None
            results = []
            while True:
                response = self.notion_client.databases.query(
                    database_id=db_id,
                    start_cursor=next_cursor,
                    filter = {
                        "timestamp": "last_edited_time",
                        "last_edited_time": {
                            "on_or_after": last_edited_time.isoformat() if isinstance(last_edited_time, datetime.date) else last_edited_time
                        }
                    }
                )
                results.extend(response["results"])
                next_cursor = response.get("next_cursor")
                if not next_cursor:
                    break
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query sets: {e}")


    def query_pages_in_date_range(self, db_id, 
                                  start_date: Union[str, datetime.date], 
                                  end_date: Union[str, datetime.date] = datetime.date.today()):
        """
        Query pages in a Notion database within a specified Date property range.     
           
        Args:
            start_date (str): The start date in ISO format (YYYY-MM-DD).
            end_date (str): The end date in ISO format (YYYY-MM-DD).
        
        Returns:
            list: A list of sets within the specified date range.
        """
        try:
            next_cursor = None
            results = []
            while True:
                response = self.notion_client.databases.query(
                    database_id=db_id,
                    start_cursor=next_cursor,
                    filter={
                        "and": [
                            {"property": "Date",
                            "date": {
                                "on_or_after": start_date.isoformat() if isinstance(start_date, datetime.date) else start_date

                            }},
                            {"property": "Date",
                            "date": {
                                "on_or_before": end_date.isoformat() if isinstance(end_date, datetime.date) else end_date
                            }}
                        ]
                    }
                )
                next_cursor = response.get("next_cursor")
                if not next_cursor:
                    break
                results.extend(response["results"])
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query sets: {e}")
    
    def fetch_database_info(self, database_id):
        """
        Fetches information about a Notion database.

        Args:
            database_id (str): The ID of the Notion database.

        Returns:
            dict: A dictionary containing the database information.
        """
        try:
            response = self.notion_client.databases.retrieve(database_id=database_id)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to fetch database info: {e}")
        
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
    def get1RMEntry(self, exercise_id):
            """
            Function to get the 1RM entry for a given exercise from Notion.
            
            Args:
                exercise_name (str): The name of the exercise.
            
            Returns:
                dict: The 1RM entry details.
            """
            try:
                response = self.notion_client.databases.query(
                    database_id=os.environ["DBID_WORKOUTLOG"],
                    filter={
                        "and": [
                            {
                                "property": "Exercise Reference",
                                "relation": {
                                    "contains": exercise_id
                                }
                            },
                            {
                                "property": "End Time",
                                "date": {
                                    "on_or_after": "2025-01-01T00:00:00Z"
                                }
                            }
                        ]
                    },
                    sorts=[
                        {
                            "property": "Estimated 1RM",
                            "direction": "descending"
                        }
                    ],
                    page_size=1
                )
                # Check if the query returned any results
                if not response["results"]:
                    return None  # Or raise an exception, depending on your use case

                # Extract the first result
                entry = response["results"][0]
                return entry
            except Exception as e:
                raise RuntimeError(f"Failed to query 1RM entry: {e}")
            