class Setter:
    def __init__(self, notion_client):
        self.notion_client = notion_client
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

    def update_big_lift_1RMs(self):
        """
        Function to update the 1RMs for big lifts in Notion.
        
        Args:
            None
        
        Returns:
            None
        """
        # Define the list of big lifts
        big_lifts = ["Barbell Back Squat", "Barbell Bench Press", "Barbell Deadlift"]

        # Iterate through each big lift and update its 1RM
        for lift in big_lifts:
            one_rm_entry = self.get1RMEntry(lift)
            if one_rm_entry:
                self.set_1RM_reference(one_rm_entry)
                print(f"Updated 1RM for {lift}.")
            else:
                print(f"No 1RM entry found for {lift}.")
    def update_all_1RMs(self, exercise_ids : dict):
        """
        Function to update all 1RMs in Notion.
        
        Args:
            exercise_ids (dict): A dictionary containing exercise names and their corresponding IDs.
        
        Returns:
            None
        """

        # Iterate through each exercise and update its 1RM
        for exercise_name in exercise_ids.keys():
            one_rm_entry = self.get1RMEntry(exercise_name)
            if one_rm_entry:
                self.set_1RM_reference(one_rm_entry)
                print(f"Updated 1RM for {exercise_name}.")
            else:
                print(f"No 1RM entry found for {exercise_name}.")