from tinydb import TinyDB, Query
from datetime import datetime
from typing import Optional, List, Union
from app.models.sets import KeyedModel
import logging
from app.core.errors import TableNotFoundError, MetadataNotFoundError, CompositeKeyError, DatabaseError, log_error
import os
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

        os.makedirs("data/database", exist_ok=True)
        
        self.db = TinyDB(db_path)

    @property
    def metadata_table(self):
        """
        Returns the metadata table from the database.
        """
        return self.db.table('metadata')

    def get(self, table_name: str, filters: dict) -> List[dict]:
        table = self.get_table(table_name)
        query = self.get_query_from_composite_key(filters)
        results = table.search(query)
        return results

    def delete(self, table_name: str, key_dict: dict) -> bool:
        table = self.get_table(table_name)
        query = self.get_query_from_composite_key(key_dict)
        removed = table.remove(query)
        return bool(removed)


    def update(self, table_name: str, entry: dict):
        """
        Updates an entry in the specified table in the database.

        args: 
            table_name (str): The name of the table to update.
            entry (dict): The entry to update.

        returns:
            None
        
        raises: 
            ValueError: If the entry is empty, table does not exist, or entry is missing key requirements.
        """
        if not entry:
            raise DatabaseError("Entry cannot be empty.")
        
        table = self.get_table(table_name)

    
        key_fields = self.get_composite_key_values(table_name)
        key_values = {field: entry[field] for field in key_fields}
        query = self.get_query_from_composite_key(key_values)

             
        if not query:
            raise DatabaseError("Query is empty. Possibly missing key fields in entry.")
        

        updated = table.update(entry, query)
        if updated:
            logger.info(f"Updated entry in '{table_name}' table.")
            return entry
        return None

    def get_query_from_composite_key(self, key_values: dict):
        query = None
        for key, value in key_values.items():
            if value is None:
                raise CompositeKeyError(f"Missing value for composite key field: {key}")
            condition = Query()[key] == value
            query = condition if query is None else query & condition
        return query
        
    def get_new_entries(self, entries : List[dict], table_name : str):
        """
        Retrieves new entries from the specified table in the database.
        """
        table = self.get_table(table_name)
        db_pages = table.all()

        composite_key_values = self.get_composite_key_values(table_name)
        
        # Get keys for input entries
        input_keys = set()
        for entry in entries:
            input_keys.add(self.build_composite_key(composite_key_values, entry))

        # Get keys for existing entries
        existing_keys = set()
        for page in db_pages:
            existing_keys.add(self.build_composite_key(composite_key_values, page))


        # Filter out input_keys from existing_keys
        new_keys = existing_keys - input_keys

        # Get new entries
        new_entries = [entry for entry in db_pages if self.build_composite_key(composite_key_values, entry) in new_keys]

        return new_entries
        



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

        if not self.metadata_table.contains(Metadata.table_name == table_name):
            self.metadata_table.insert({
                'table_name' : table_name,
                'table_model': model.model_json_schema(),
                'composite_key': model.get_key(),
                'remote_id': remote_id,
                'synced_at': None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                })
        else:
            logger.warning(f"Metadata for table '{table_name}' already exists.")

    def filter_duplicates(self, table_name: str, entries : List[dict]):
        """
        Filters out duplicate entries from the specified table in the database.
        """

        table = self.get_table(table_name)

        existing_entries = table.all()
        existing_keys = set()
        composite_key_values = self.get_composite_key_values(table_name)

        for entry in existing_entries:
            existing_keys.add(self.build_composite_key(composite_key_values, entry))

        to_insert = []
        failed_entries = []
        dupe_entries = []

        for entry in entries:
            try:
                composite_key = self.build_composite_key(composite_key_values, entry)
            except CompositeKeyError as e:
                failed_entries.append(entry)
                continue
                
            if composite_key not in existing_keys:
                to_insert.append(entry)
                existing_keys.add(composite_key)
            else:
                dupe_entries.append(entry)
                logger.debug(f"Duplicate entry found for {composite_key}. Entry not added.")
        return to_insert, failed_entries, dupe_entries

        

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
            raise MetadataNotFoundError(f"Metadata for table '{table_name}' not found.")
        
        # Exit if no entries to add
        if not entries:
            logger.warning(f"No entries to add to '{table_name}' table.")
            return
        
        # Get table
        table = self.get_table(table_name)
        
        # Remove placeholder if exists
        table.remove(Query()._init == True)

        print(entries)
        to_insert, failed, dupes = self.filter_duplicates(table_name, entries)
        
        if to_insert:
            table.insert_multiple(to_insert)
            self._update_timestamp(table_name)
            logger.info(f"Inserted {len(to_insert)} new entries into '{table_name}' table.")
        else:
            logger.info("No new entries to insert.")     
        if failed:
            logger.error(f"Failed to insert {len(failed)} entries into '{table_name}' table.")
        return {"inserted": to_insert, "duplicates": dupes, "failed": failed}
        
    def get_composite_key_values(self, table_name: str) -> List[str]:
        """
        Retrieves the composite key values for the specified table.
        """
        
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})

        return self.metadata_table.get(Query().table_name == table_name)['composite_key']
        
    def build_composite_key(self, composite_key: List[str], entry: dict) -> str:
        """
        Builds a composite key for the specified table.
        """
        missing_keys = [key for key in composite_key if key not in entry]
        if missing_keys:
            raise CompositeKeyError(f"Missing keys in entry: {missing_keys}", context={"entry_keys": entry.keys()})
        
        return "_".join([str(entry[key]) for key in composite_key])
    
    def _update_timestamp(self, table_name: str):
        """
        Updates the timestamp of the specified table in the metadata.
        """
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})
        
        self.metadata_table.update({'updated_at': datetime.now().isoformat()}, Query().table_name == table_name)
        logger.info(f"Updated timestamp for table '{table_name}'.")

    def get_last_sync_time(self, table_name: str) -> Optional[datetime]:

        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})

        Metadata = Query()
        result = self.metadata_table.get(Metadata.table_name == table_name)
        
        if result:
            return result['synced_at']
        else:
            raise MetadataNotFoundError(table_name, context= {self.metadata_table.all()})

    def update_last_sync_time(self, table_name: str):
        """
        Updates the last sync time for a table by its remote ID.
        """
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})
        
        synced_at = datetime.now().isoformat()
        
        Metadata = Query()
        updated = self.metadata_table.update({'synced_at': synced_at}, Metadata.table_name == table_name)

        if updated == []:
            logger.warning(f"No metadata entry found for table '{table_name}' to update sync time.")
        else:
            logger.info(f"Updated sync time for table '{table_name}' to {synced_at}.")

    def get_table(self, table_name: str):
        """
        Returns the table if it exists, otherwise raises a ValueError.
        """
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})
        return self.db.table(table_name)