import os
import logging
from notion_client import Client
from dotenv import load_dotenv
import app.core.log as log

logger = logging.getLogger(__name__)

load_dotenv()

_notion = None

def initialize_notion_client(api_key: str) -> Client:
    return Client(auth=api_key, logger=log.initialize_logger(), log_level=logging.DEBUG)

def get_notion_client() -> Client:
    global _notion
    if _notion is None:
        try:
            _notion = initialize_notion_client(os.environ["NOTION_API_KEY"])
        except KeyError:
            logger.error("Missing NOTION_API_KEY in environment.")
            raise
    return _notion

def test_connection(client: Client):
    try:
        client.users.list()
        print("✅ Connection to Notion API successful.")
    except Exception as e:
        logger.error(f"Failed to connect to Notion API: {e}")
        raise
