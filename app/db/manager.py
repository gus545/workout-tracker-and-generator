import os
import logging
from datetime import datetime
from typing import Optional, List, Union
from tinydb import TinyDB, Query

from app.models.sets import KeyedModel
from app.core.errors import (
    TableNotFoundError,
    MetadataNotFoundError,
    CompositeKeyError,
    DatabaseError
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages TinyDB operations including table creation, insertion, updating,
    and metadata tracking for sync and composite keys.
    """

    def __init__(self, db_path: str = 'data/database/tinydb.json'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db = TinyDB(db_path)

    @property
    def metadata_table(self):
        return self.db.table('metadata')

    def get_table(self, table_name: str):
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name, context={"available_tables": list(self.db.tables())})
        return self.db.table(table_name)

    def get(self, table_name: str, filters: dict) -> List[dict]:
        table = self.get_table(table_name)
        query = self._composite_query(filters)
        return table.search(query)

    def delete(self, table_name: str, key_dict: dict) -> bool:
        table = self.get_table(table_name)
        query = self._composite_query(key_dict)
        return bool(table.remove(query))

    def update(self, table_name: str, entry: dict):
        if not entry:
            raise DatabaseError("Entry cannot be empty.")

        table = self.get_table(table_name)
        key_fields = self.get_composite_key_fields(table_name)
        key_values = {field: entry[field] for field in key_fields}
        query = self._composite_query(key_values)

        if not query:
            raise DatabaseError("Missing composite key fields.")

        updated = table.update(entry, query)
        if updated:
            logger.info(f"Updated entry in '{table_name}'.")
            return entry
        return None

    def create_table(self, table_name: str, model: KeyedModel, remote_id: Optional[str] = None):
        if table_name not in self.db.tables():
            self.db.table(table_name).insert({"_init": True})
            self._init_metadata(table_name, model, remote_id)
            logger.info(f"Table '{table_name}' created.")
        else:
            logger.warning(f"Table '{table_name}' already exists.")

    def _init_metadata(self, table_name: str, model: KeyedModel, remote_id: Optional[str]):
        if not self.metadata_table.contains(Query().table_name == table_name):
            self.metadata_table.insert({
                "table_name": table_name,
                "table_model": model.model_json_schema(),
                "composite_key": model.get_key(),
                "remote_id": remote_id,
                "synced_at": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
        else:
            logger.warning(f"Metadata for '{table_name}' already exists.")

    def get_composite_key_fields(self, table_name: str) -> List[str]:
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name)
        metadata = self.metadata_table.get(Query().table_name == table_name)
        if not metadata:
            raise MetadataNotFoundError(table_name)
        return metadata["composite_key"]

    def build_composite_key(self, keys: List[str], entry: dict) -> str:
        missing = [k for k in keys if k not in entry]
        if missing:
            raise CompositeKeyError(f"Missing keys: {missing}", context={"entry_keys": list(entry.keys())})
        return "_".join(str(entry[k]) for k in keys)

    def _composite_query(self, key_values: dict):
        query = None
        for key, val in key_values.items():
            if val is None:
                raise CompositeKeyError(f"Missing value for key field '{key}'")
            condition = Query()[key] == val
            query = condition if query is None else query & condition
        return query

    def filter_duplicates(self, table_name: str, entries: List[dict]):
        table = self.get_table(table_name)
        existing = table.all()
        keys = self.get_composite_key_fields(table_name)

        existing_keys = {self.build_composite_key(keys, e) for e in existing}

        to_insert, failed, dupes = [], [], []
        for entry in entries:
            try:
                key = self.build_composite_key(keys, entry)
                if key not in existing_keys:
                    to_insert.append(entry)
                    existing_keys.add(key)
                else:
                    dupes.append(entry)
            except CompositeKeyError:
                failed.append(entry)

        return to_insert, failed, dupes

    def add(self, table_name: str, entries: Union[dict, List[dict]]):
        if isinstance(entries, dict):
            entries = [entries]

        if not entries:
            logger.warning(f"No entries provided for '{table_name}'.")
            return

        if not self.metadata_table.get(Query().table_name == table_name):
            raise MetadataNotFoundError(table_name)

        table = self.get_table(table_name)
        table.remove(Query()._init == True)

        to_insert, failed, dupes = self.filter_duplicates(table_name, entries)

        if to_insert:
            table.insert_multiple(to_insert)
            self._update_timestamp(table_name)
            logger.info(f"Inserted {len(to_insert)} entries into '{table_name}'.")

        return {"inserted": to_insert, "duplicates": dupes, "failed": failed}

    def get_new_entries(self, incoming: List[dict], table_name: str):
        table = self.get_table(table_name)
        db_entries = table.all()
        keys = self.get_composite_key_fields(table_name)

        incoming_keys = {self.build_composite_key(keys, e) for e in incoming}
        existing_keys = {self.build_composite_key(keys, e) for e in db_entries}

        new_keys = incoming_keys - existing_keys
        return [e for e in incoming if self.build_composite_key(keys, e) in new_keys]

    def _update_timestamp(self, table_name: str):
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name)
        self.metadata_table.update(
            {"updated_at": datetime.now().isoformat()},
            Query().table_name == table_name
        )

    def update_last_sync_time(self, table_name: str):
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name)

        updated = self.metadata_table.update(
            {"synced_at": datetime.now().isoformat()},
            Query().table_name == table_name
        )

        if not updated:
            logger.warning(f"No metadata entry to update sync time for '{table_name}'.")
        else:
            logger.info(f"Updated sync time for '{table_name}'.")

    def get_last_sync_time(self, table_name: str) -> Optional[datetime]:
        if table_name not in self.db.tables():
            raise TableNotFoundError(table_name)

        record = self.metadata_table.get(Query().table_name == table_name)
        if not record:
            raise MetadataNotFoundError(table_name)

        return record["synced_at"]
