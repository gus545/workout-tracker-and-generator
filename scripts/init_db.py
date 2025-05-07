from app.db.manager import DatabaseManager
from app.services.notion.parser import parse_data
from app.services.notion.fetcher import Fetcher
from app.services.notion.client import initialize_notion_client
from app.services.notion.setter import Setter
import os
from dotenv import load_dotenv
from app.services.sync_service import SyncService
import json
import logging

logger = logging.getLogger(__name__)


def initialize_db():

    load_dotenv()

    client = initialize_notion_client(os.environ["NOTION_API_KEY"])
    fetcher = Fetcher(client)
    db = DatabaseManager()
    setter = Setter(client)

    ss = SyncService(fetcher, db, setter)

    workout_log_info = json.loads(os.environ["WORKOUT_LOG"])
    exercise_info = json.loads(os.environ["EXERCISE"])
    print(exercise_info)


    
    ss.sync_remote_to_local(workout_log_info)
    ss.sync_remote_to_local(exercise_info)
    