import logging
from notion_client.errors import APIResponseError
import logging

logger = logging.getLogger(__name__)

class Setter:
    def __init__(self, notion_client):
        self.notion_client = notion_client

    def add_page(self, page_data, database_id):
        """
        Function to add a page to Notion.

        Args:
            page_data (dict): The data of the page to add.
        """
        try:
            response = self.notion_client.pages.create(parent={"database_id": database_id}, properties=page_data)
            return response['id']

        except APIResponseError as e:
            logger.error(f"Failed to add page: {page_data}.  Error: {e}")
            raise
        except Exception as e:
            raise RuntimeError
    def set_1RM_reference(self, one_rm_entry):
        """
        Function to set the 1RM reference for a given exercise in Notion.
        
        Args:
            exercise_name (str): The name of the exercise.
            one_rm_entry (dict): The 1RM entry details.
        
        Returns:
            None
        """
        try:
            # Set the 1RM reference in the Notion database
            self.notion_client.pages.update(
                page_id=one_rm_entry["properties"]["Exercise Reference"]["relation"][0]["id"],
                properties={
                    "Max 1RM Instance": {
                        "relation": [
                            {
                                "id": one_rm_entry["id"]
                            }
                        ]
                    }
                }
            )
        except KeyError as e:
            raise KeyError(f"Key error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to set 1RM reference: {e}")       
        
    def update_all_1RMs(self, exercise_ids, one_rm_entries: dict):
        """
        Function to update all 1RMs in Notion.
        
        Args:
            exercise_ids (dict): A dictionary containing exercise names and their corresponding IDs.
            one_rm_entries (dict): A dictionary containing 1RM entries for each exercise.
        
        Returns:
            None
        """

        # Iterate through each exercise and update its 1RM
        for exercise_name in exercise_ids.keys():
            one_rm_entry = one_rm_entries.get(exercise_name)
            if one_rm_entry:
                self.set_1RM_reference(one_rm_entry)
                print(f"Updated 1RM for {exercise_name}.")
            else:
                print(f"No 1RM entry found for {exercise_name}.")