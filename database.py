from tinydb import TinyDB, Query
from datetime import datetime
from typing import Optional, List, Union
from models import KeyedModel
import logging

logger = logging.getLogger(__name__)

# Database manager class DatabaseManager:
class DatabaseManager:
    """
    A class to manage the database operations using TinyDB.
    """

    def __init__(self, db_path='data/database/tinydb.json'):
        """
        Initializes the DatabaseManager with the specified database path.
        """
        self.db = TinyDB(db_path)

    @property
    def metadata_table(self):
        """
        Returns the metadata table from the database.
        """
        return self.db.table('metadata')

    def create_table(self, table_name: str, model : KeyedModel, remote_id: Optional[str] = None):
        """
        Creates a new table in the database.
        """
        if table_name not in self.db.tables():
            self.db.table(table_name).insert({"_init": True})
            self.initialize_metadata(table_name, model, remote_id)
            logger.info(f"Table '{table_name}' created.")
        else:
            logger.warning(f"Table '{table_name}' already exists.")

    def initialize_metadata(self, table_name : str, model : KeyedModel, remote_id, sync = False):
        """
        Creates metadata for a table if it doesn't exist.
        """
        Metadata = Query()
        
        # Check if model is valid
        if not issubclass(model, KeyedModel):
            raise ValueError("Model must be an instance of KeyedModel")

        if not self.metadata_table.contains(Metadata.table_name == table_name):
            self.metadata_table.insert({
                'table_name' : table_name,
                'table_model': model.model_json_schema(),
                'composite_key': model.get_composite_key(),
                'remote_id': remote_id,
                'synced_at': None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                })
        else:
            logger.warning(f"Metadata for table '{table_name}' already exists.")

    def add(self, table_name: str, entries : Union[List[dict], dict]):
        """
        Adds an entry to the specified table in the database, according to the composite key.

        Args: 
            table_name (str): The name of the table to add the entry to.
            entry (dict): The entry to add.
        
        Returns:
            None

        Raises: 
            ValueError: If table does not exist, or entry is missing key requirements.
        """
                  
        if isinstance(entries, dict):   
            entries = [entries]

        if not self.metadata_table.get(Query().table_name == table_name):
            raise ValueError(f"Metadata for table '{table_name}' not found.")
        
        # Exit if no entries to add
        if not entries:
            logger.warning(f"No entries to add to '{table_name}' table.")
            return
        
        # Get table
        table = self.get_table(table_name)
        
        # Remove placeholder if exists
        table.remove(Query()._init == True)

        existing_entries = table.all()
        existing_keys = set()
        composite_key_values = self.get_composite_key_values(table_name)

        for entry in existing_entries:
            try:
                existing_keys.add(self.build_composite_key(composite_key_values, entry))
            except ValueError as e:
                logger.error(f"Invalid entry: {entry}")
                raise

        to_insert = []

        for entry in entries:
            composite_key = self.build_composite_key(composite_key_values, entry)
            if composite_key not in existing_keys:
                to_insert.append(entry)
                existing_keys.add(composite_key)
            # else:
            #     print(f"Duplicate entry found for {composite_key}. Entry not added.")
        
        if to_insert:
            table.insert_multiple(to_insert)
            self._update_timestamp(table_name)
            print(f"Inserted {len(to_insert)} new entries into '{table_name}' table.")
        else:
            print("No new entries to insert.")      
        
    def get_composite_key_values(self, table_name: str) -> List[str]:
        """
        Retrieves the composite key values for the specified table.
        """
        return self.metadata_table.get(Query().table_name == table_name)['composite_key']
        
    def build_composite_key(self, composite_key: List[str], entry: dict) -> str:
        """
        Builds a composite key for the specified table.
        """
        missing_keys = [key for key in composite_key if key not in entry]
        if missing_keys:
            raise ValueError(f"Missing keys in entry: {missing_keys}")
        
        return "_".join([str(entry[key]) for key in composite_key])
    
    def _update_timestamp(self, table_name: str):
        """
        Updates the timestamp of the specified table in the metadata.
        """
        self.metadata_table.update({'updated_at': datetime.now().isoformat()}, Query().table_name == table_name)
        print(f"Updated timestamp for table '{table_name}'.")

    def get_last_sync_time(self, table_name: str) -> Optional[datetime]:
        """
        Retrieves the last sync time for a table by its remote ID.

        args: 
            remote_id (str): The remote ID of the table.

        returns:
            datetime: The last sync time.

        raises:
            ValueError: If the table with the given remote ID is not found in the metadata.
        """
        Metadata = Query()
        result = self.metadata_table.get(Metadata.table_name == table_name)
        
        if result:
            return result['synced_at']
        else:
            raise ValueError(f"Table with name '{table_name}' not found in metadata.")

    def update_last_sync_time(self, table_name: str):
        """
        Updates the last sync time for a table by its remote ID.
        """
        Metadata = Query()
        self.metadata_table.update({'synced_at': datetime.now().isoformat()}, Metadata.table_name == table_name)
        print(f"Updated last sync time for table with name '{table_name}'.")

    def get_table(self, table_name: str):
        """
        Returns the table if it exists, otherwise raises a ValueError.
        """
        if table_name not in self.db.tables():
            raise ValueError(f"Table '{table_name}' does not exist.")
        return self.db.table(table_name)