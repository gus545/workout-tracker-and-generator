import logging
from app.services.notion.client import get_notion_client
from notion_client.errors import APIResponseError

logger = logging.getLogger(__name__)


class Setter:
    def __init__(self, notion_client=get_notion_client()):
        self.notion_client = notion_client

    def add_page(self, page_data: dict, database_id: str) -> str:
        try:
            response = self.notion_client.pages.create(
                parent={"database_id": database_id},
                properties=page_data
            )
            return response["id"]
        except APIResponseError as e:
            logger.error(f"Failed to add page: {page_data}. Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while adding page: {e}")
            raise RuntimeError("Unexpected error while adding page.")

    def set_1RM_reference(self, one_rm_entry: dict):
        try:
            page_id = one_rm_entry["properties"]["Exercise Reference"]["relation"][0]["id"]
            self.notion_client.pages.update(
                page_id=page_id,
                properties={
                    "Max 1RM Instance": {
                        "relation": [{"id": one_rm_entry["id"]}]
                    }
                }
            )
        except KeyError as e:
            logger.error(f"Missing expected key when setting 1RM: {e}")
            raise KeyError(f"Key error: {e}")
        except Exception as e:
            logger.error(f"Failed to set 1RM reference: {e}")
            raise RuntimeError(f"Failed to set 1RM reference: {e}")

    def update_all_1RMs(self, exercise_ids: dict, one_rm_entries: dict):
        for exercise_name in exercise_ids:
            one_rm_entry = one_rm_entries.get(exercise_name)
            if one_rm_entry:
                self.set_1RM_reference(one_rm_entry)
                logger.info(f"✅ Updated 1RM for {exercise_name}")
            else:
                logger.info(f"⚠️ No 1RM entry found for {exercise_name}")
