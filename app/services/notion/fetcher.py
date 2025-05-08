import os
import logging
import datetime
from typing import Union
from notion_client import Client
from app.services.notion.client import get_notion_client

logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, notion_client= get_notion_client()):
        self.notion_client = notion_client

    def query_pages_by_last_edited_time(self, db_id, last_edited_time: Union[str, datetime.date]):
        logger.info(f"🔍 Querying pages edited since {last_edited_time}...")
        try:
            results, next_cursor = [], None
            while True:
                response = self.notion_client.databases.query(
                    database_id=db_id,
                    start_cursor=next_cursor,
                    filter={
                        "timestamp": "last_edited_time",
                        "last_edited_time": {
                            "on_or_after": (
                                last_edited_time.isoformat() if isinstance(last_edited_time, datetime.date) else last_edited_time
                            )
                        }
                    }
                )
                results.extend(response["results"])
                next_cursor = response.get("next_cursor")
                if not next_cursor:
                    break
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query pages by last edited time: {e}")

    def query_pages_in_date_range(self, db_id, start_date: Union[str, datetime.date], end_date: Union[str, datetime.date] = datetime.date.today()):
        try:
            results, next_cursor = [], None
            while True:
                response = self.notion_client.databases.query(
                    database_id=db_id,
                    start_cursor=next_cursor,
                    filter={
                        "and": [
                            {
                                "property": "Date",
                                "date": {"on_or_after": start_date.isoformat() if isinstance(start_date, datetime.date) else start_date}
                            },
                            {
                                "property": "Date",
                                "date": {"on_or_before": end_date.isoformat() if isinstance(end_date, datetime.date) else end_date}
                            }
                        ]
                    }
                )
                results.extend(response["results"])
                next_cursor = response.get("next_cursor")
                if not next_cursor:
                    break
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query pages in date range: {e}")

    def fetch_database_info(self, database_id):
        try:
            return self.notion_client.databases.retrieve(database_id=database_id)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch database info: {e}")

    def fetch_all_pages(self, database_id):
        try:
            results, next_cursor = [], None
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
            raise RuntimeError(f"Failed to fetch all pages: {e}")

    def get1RMEntry(self, exercise_id):
        try:
            response = self.notion_client.databases.query(
                database_id=os.environ["DBID_WORKOUTLOG"],
                filter={
                    "and": [
                        {
                            "property": "Exercise Reference",
                            "relation": {"contains": exercise_id}
                        },
                        {
                            "property": "End Time",
                            "date": {"on_or_after": "2025-01-01T00:00:00Z"}
                        }
                    ]
                },
                sorts=[{"property": "Estimated 1RM", "direction": "descending"}],
                page_size=1
            )
            return response["results"][0] if response["results"] else None
        except Exception as e:
            raise RuntimeError(f"Failed to query 1RM entry: {e}")
