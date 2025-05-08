import os
import shutil
import traceback
import logging
from datetime import datetime
from typing import Optional, Dict
from json import loads, JSONDecodeError

from dotenv import load_dotenv
from notion_client.errors import APIResponseError

from app.services.notion.fetcher import Fetcher
from app.services.notion.setter import Setter
from app.services.notion.parser import parse_data
from app.db.manager import DatabaseManager
from app.models.sets import KeyedModel, Exercise, CompletedSet
from app.core.errors import (
    TableNotFoundError, CompositeKeyError, DatabaseError,
    SyncError, MetadataNotFoundError, log_error
)

logger = logging.getLogger(__name__)
DEFAULT_SYNC_TIME = datetime.fromisoformat("2000-01-01T00:00:00")


class SyncService:
    def __init__(self, database: DatabaseManager, fetcher: Fetcher = Fetcher(), setter: Setter = Setter()):
        self.database = database
        self.fetcher = fetcher
        self.setter = setter
        self.model_registry = {
            "exercise": Exercise,
            "workout_log": CompletedSet,
        }
        load_dotenv()

    def sync_all(self):
        """
        Syncs all registered databases in both directions.
        """
        try:
            exercise_db = loads(os.environ["EXERCISE"])
            workout_db = loads(os.environ["WORKOUT_LOG"])
        except KeyError as e:
            logger.error(f"Missing environment variable: {e}")
            return
        except JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return

        for db_info in [exercise_db, workout_db]:
            self.sync_remote_to_local(db_info)
            self.sync_local_to_remote(db_info)

    def sync_remote_to_local(self, db_info: Dict[str, str]):
        db_id = db_info["id"]
        db_name = db_info["name"]
        logger.info(f"📥 Syncing from Notion → Local for '{db_name}'")

        model = self.model_registry.get(db_name)
        if not model:
            logger.error(f"No model registered for '{db_name}'")
            return

        if db_name not in self.database.db.tables():
            logger.info(f"Creating local table for '{db_name}'")
            self.database.create_table(db_name, model, remote_id=db_id)

        try:
            last_sync = self.database.get_last_sync_time(db_name) or DEFAULT_SYNC_TIME
            logger.info(f"Last sync: {last_sync}")
        except (DatabaseError, MetadataNotFoundError) as e:
            log_error(logger, e)
            last_sync = DEFAULT_SYNC_TIME

        try:
            new_pages = self.fetcher.query_pages_by_last_edited_time(db_id, last_sync)
            parsed_data = parse_data(new_pages, model)
        except (APIResponseError, SyncError) as e:
            log_error(logger, e)
            return

        if not parsed_data:
            logger.info("No new data to sync from Notion.")
            return

        logger.info(f"Inserting {len(parsed_data)} records into '{db_name}'")
        result = self.database.add(db_name, parsed_data)
        logger.debug(f"Add result: {result}")
        self.database.update_last_sync_time(db_name)
        logger.info(f"✅ Sync complete for '{db_name}'")

    def sync_local_to_remote(self, db_info: Dict[str, str]):
        db_id = db_info["id"]
        db_name = db_info["name"]
        logger.info(f"📤 Syncing from Local → Notion for '{db_name}'")

        model = self.model_registry.get(db_name)
        if not model:
            logger.error(f"No model registered for '{db_name}'")
            return

        try:
            remote_pages = self.fetcher.fetch_all_pages(db_id)
            parsed_remote = parse_data(remote_pages, model)
            new_entries = self.database.get_new_entries(parsed_remote, db_name)
        except (APIResponseError, SyncError) as e:
            log_error(logger, e)
            return
        except Exception as e:
            logger.error(traceback.format_exc())
            return

        if not new_entries:
            logger.info("No new entries to upload.")
            return

        for entry in new_entries:
            try:
                notion_page = model(**entry).to_notion_format()
                new_id = self.setter.add_page(notion_page, db_id)
                entry["page_id"] = new_id
                self.database.update(db_name, entry)
                logger.info(f"✅ Uploaded new page for '{db_name}' with ID {new_id}")
            except Exception as e:
                logger.error(f"Failed to upload entry: {entry}")
                logger.error(traceback.format_exc())

    def get_model(self, db_name: str) -> KeyedModel:
        model = self.model_registry.get(db_name)
        if not model:
            raise ValueError(f"No model found for '{db_name}'")
        return model

    def backup_database(self, backup_folder="backups"):
        """
        Creates a timestamped backup of the local TinyDB file.
        """
        os.makedirs(backup_folder, exist_ok=True)
        db_path = self.database.db.storage._handle.name
        backup_path = os.path.join(
            backup_folder,
            f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        shutil.copy(db_path, backup_path)
        logger.info(f"📦 Database backed up to: {backup_path}")
