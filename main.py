from Notion.fetcher import Fetcher
from Notion.client import initialize_notion_client, test_connection
from Notion.fetcher import Fetcher
from database import DatabaseManager
from Notion.parser import parse_set_data, parse_exercise_data
from Notion.setter import Setter
import sys
import os
from sync_service import SyncService
from app.models import CompletedSet, Exercise, KeyedModel
from dotenv import load_dotenv
import datetime
import json
from errors import log_error, ModelError, ParsingError
from pydantic import ValidationError
import logging

# Silence notion-client logger entirely
logging.getLogger("notion-client").setLevel(logging.CRITICAL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',stream = sys.stdout)
logger = logging.getLogger(__name__)


def main():
    test = json.loads(open("exercise_ids.json", "r").read())
    reversed = {}
    for key in test.keys():
        reversed[test[key]] = key
    open("exercise_ids_reversed.json", "w").write(json.dumps(reversed))




    
    
        

if __name__ == "__main__":
    main()
