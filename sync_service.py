import shutil
import os
from datetime import datetime
from Notion.fetcher import Fetcher
from Notion.parser import parse_database_info, parse_data
from database import DatabaseManager
from models import KeyedModel, Exercise, WorkoutSet
from dotenv import load_dotenv
from Notion.setter import Setter
import logging

logger = logging.getLogger(__name__)

DEFAULT_SYNC_TIME = datetime.fromisoformat("2000-01-01T00:00:00")

class SyncService:
    def __init__(self, fetcher: Fetcher, database: DatabaseManager, setter: Setter):
        self.setter = setter
        self.fetcher = fetcher
        self.database = database
        self.model_registry = {
            "exercise": Exercise,
            "workout_log": WorkoutSet,
        }
        load_dotenv()
        

    def backup_database(self, backup_folder="backups"):
        """
        Backs up the database to a specified path.
        
        Args:
            database (DatabaseManager): The database manager instance.
            backup_path (str): The path where the backup will be stored.
        
        Returns:
            None
        """
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        
        # Create a backup of the database
        backup_path = os.path.join(backup_folder, f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy(self.database.db_path, backup_path)
        print(f"Database backed up to {backup_path}")

    def sync_remote_to_local(self, db_info):
        """
        Syncs data from the remote Notion database to the local database.
        
        Returns:
            None
        """
            
        db_id = db_info["id"]
        db_name = db_info["name"]  

        if db_name not in self.model_registry:
            logger.error(f"No model found for {db_name}.")
            raise ValueError(f"No model found for {db_name}")
        
        model = self.model_registry[db_name]

        if not self.database.table_exists(db_name):
            logger.info(f"Creating local table for {db_name}...")
            self.database.create_table(db_name, model, remote_id=db_id)
        
        

        try:
            # Get the last sync time from the database
            logger.info("Getting last sync time from database...")
            last_sync = self.database.get_last_sync_time(db_name)
            if not last_sync:
                logger.warning(f"No last sync time found for {db_name}. Using default...")
                last_sync = DEFAULT_SYNC_TIME            
            logger.info(f"Last sync time: {last_sync}")
        except ValueError as e:
            logger.error(f"Error getting last sync time: {e}")
            return

        # Fetch all pages from the Notion database
        new_pages = self.fetcher.query_pages_by_last_edited_time(db_id, last_sync)
        
        # Parse the database information
        parsed_data = parse_data(new_pages, model)

        # Process and store the fetched data in the local database
        logger.info(f"Adding {len(parsed_data)} new pages to the local database.")
        self.database.add(db_name, parsed_data)
        
        self.database.update_last_sync_time(db_name)
        self.last_sync_time = datetime.now()
        print(f"Data synced successfully at {self.last_sync_time}.")

    def sync_local_to_remote(self, db_info):
        """
        Syncs data from the local database to the remote Notion database.
        
        Returns:
            None
        """
        try:
            db_id = db_info["id"]
            db_name = db_info["name"]

            # Fetch all pages from the local database
            remote_pages = self.fetcher.fetch_all_pages(db_id)
            
            # Parse remote pages
            parsed_remote_data = parse_data(remote_pages, self.get_model(db_name))

            to_add = self.database.get_new_entries(parsed_remote_data, db_name)
            
            if not to_add:
                print("No new entries to add.")
                return
            for page in to_add:
                model = self.get_model(db_name)
                notion_page = model(**page).to_notion_format()
                logger.info("Adding page to Notion database...")
                new_page_id = self.setter.add_page(notion_page, db_id)
                logger.info(f"New page with id {new_page_id} added to Notion database.")
                page["page_id"] = new_page_id
                self.database.update(db_name, page)
            


        except Exception as e:
            print(f"Error syncing data: {e}")
            raise


    def get_model(self, db_name) -> KeyedModel:
        """
        Returns the model class associated with the given database ID.
        
        Args:
            database_id (str): The ID of the Notion database.
        
        Returns:
            KeyedModel: The model class associated with the database ID.
        """
        try:
            return self.model_registry.get(db_name)
        except KeyError:
            raise ValueError(f"Model for database ID {db_name} not found.")