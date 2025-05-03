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
            self.db.table(table_name)
            self.initialize_metadata(table_name, model, remote_id)
        else:
            print(f"Table {table_name} already exists.")

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
            print(f"Metadata for table '{table_name}' created.")
        else:
            print(f"Metadata for table {table_name} already exists.")

    def add(self, table_name: str, entries : Union[List[dict], dict]):
        """
        Adds an entry to the specified table in the database.
        """
        table = self.db.table(table_name)
               
        if isinstance(entries, dict):   
            entries = [entries]

        if not self.metadata_table.get(Query().table_name == table_name):
            raise ValueError(f"Metadata for table '{table_name}' not found.")
        
        existing_entries = table.all()
        existing_keys = set()

        for entry in existing_entries:
            existing_keys.add(self._build_composite_key(table_name, entry))

        to_insert = []

        for entry in entries:
            composite_key = self._build_composite_key(table_name, entry)
            if composite_key not in existing_keys:
                to_insert.append(entry)
                existing_keys.add(composite_key)
            # else:
            #     print(f"Duplicate entry found for {composite_key}. Entry not added.")
        
        if to_insert:
            table.insert_multiple(to_insert)
            self.update_timestamp(table_name)
            print(f"Inserted {len(to_insert)} new entries into '{table_name}' table.")
        else:
            print("No new entries to insert.")     
            
    def _check_duplicates(self, table_name: str, entry: dict) -> bool:
        """
        Checks for duplicate entries in the specified table.
        """
        table = self.db.table(table_name)

        try:
            query = self.get_table_key_query(table_name, entry)
            result = table.search(query)
            return len(result) > 0
        except ValueError as e:
            print(f"Error checking for duplicate: {e}")
            return False    
        
    def get_table_key_query(self, table_name: str, entry: dict) -> Query:
        """
        Retrieves the query for the table key.
        """
        
        # Check if the table exists in the metadata

        # Retrieve the metadata for the specified table
        metadata = self.metadata_table.get(Query().table_name == table_name)


        if metadata:
            composite_key = metadata['composite_key']
            q = Query()
            full_query = None

            for key in composite_key:
                if key in entry:
                    condition = (q[key] == entry[key])
                    if full_query is None:
                        full_query = condition
                    else:
                        full_query &= condition

            if full_query is None:
                raise ValueError("Cannot build a query: No matching composite key fields in entry")

            return full_query
        else:
            raise ValueError(f"Table '{table_name}' not found in metadata")
        
    def _build_composite_key(self, table_name: str, entry: dict) -> str:
        """
        Builds a composite key for the specified table.
        """
        metadata = self.metadata_table.get(Query().table_name == table_name)
        composite_key = metadata['composite_key']

        try:
        
            return "_".join([str(entry[key]) for key in composite_key])
        except KeyError as e:
            raise ValueError(f"Missing key '{e.args[0]}' in entry for composite key generation")
    
    def update_timestamp(self, table_name: str):
        """
        Updates the timestamp of the specified table in the metadata.
        """
        self.metadata_table.update({'updated_at': datetime.now().isoformat()}, Query().table_name == table_name)
        print(f"Updated timestamp for table '{table_name}'.")