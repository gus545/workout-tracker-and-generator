from helpers import initialize_notion_client
from dotenv import load_dotenv
import os
import json

class API_Manager:
    def __init__(self):
        self.notion_client = initialize_notion_client()
        self.exercise_ids = {}
        self._load_exercise_ids()
        

    def establish_connection(client):
        """
        Establishes a connection to the Notion API and validates the API key.

        Raises:
            ValueError: If the connection fails or the API key is invalid.
        """
        try:
            client.users.list()
            print("Connection to Notion API established successfully.")
        except ValueError as e:
            print(f"Error establishing connection: {e}")
            raise

    def initialize_notion_client():
        """
        Initializes and returns a Notion client for interacting with the Notion API.

        Returns:
            Client: An instance of the Notion client.
        """
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            raise ValueError("API key is required to initialize the Notion client. Ensure NOTION_API_KEY is set in the .env file.")


        client = Client(auth=api_key, logger=log.initialize_logger(), log_level = logging.DEBUG)

        establish_connection(client)

        return client


    def query_sets_in_date_range(self, start_date, end_date):
        """
        Function to get all sets in a given date range from Notion.
        
        Args:
            start_date (str): The start date in ISO format (YYYY-MM-DD).
            end_date (str): The end date in ISO format (YYYY-MM-DD).
        
        Returns:
            list: A list of sets within the specified date range.
        """
        try:
            response = self.notion_client.databases.query(
                database_id=os.environ["DBID_WORKOUTLOG"],
                filter={
                    "property": "End Time",
                    "date": {
                        "on_or_after": start_date,
                        "on_or_before": end_date
                    }
                }
            )
            return response["results"]
        except Exception as e:
            raise RuntimeError(f"Failed to query sets: {e}")

    def _load_exercise_ids(self):
        exercise_ids_file = os.path.join(os.path.dirname(__file__), "exercise_ids.json")
        if os.path.exists(exercise_ids_file):
            with open(exercise_ids_file, "r") as file:
                self.exercise_ids = json.load(file)
        else:
            raise FileNotFoundError(f"Exercise IDs file not found: {exercise_ids_file}")
        # Load exercise IDs from the JSON file

    def get_exercise_id(self, exercise_name):
        """
        Function to get the exercise ID for a given exercise name.
        
        Args:
            exercise_name (str): The name of the exercise.
        
        Returns:
            str: The ID of the exercise.
        """
        if exercise_name in self.exercise_ids:
            return self.exercise_ids[exercise_name]
        else:
            raise ValueError(f"Exercise name '{exercise_name}' not found in the database.")

    def get_exercise_name(self, exercise_id):
        """
        Function to get the exercise name for a given exercise ID.
        
        Args:
            exercise_id (str): The ID of the exercise.
        
        Returns:
            str: The name of the exercise.
        """

        for name, id in self.exercise_ids.items():
            if id == exercise_id:
                return name
        raise ValueError(f"Exercise ID '{exercise_id}' not found in the database.")

    def get1RMEntry(self, exercise_name):
        """
        Function to get the 1RM entry for a given exercise from Notion.
        
        Args:
            exercise_name (str): The name of the exercise.
        
        Returns:
            dict: The 1RM entry details.
        """
        try:
            response = self.notion_client.databases.query(
                database_id=os.environ["DBID_WORKOUTLOG"],
                filter={
                    "and": [
                        {
                            "property": "Exercise Reference",
                            "relation": {
                                "contains": self.get_exercise_id(exercise_name)
                            }
                        },
                        {
                            "property": "End Time",
                            "date": {
                                "on_or_after": "2025-01-01T00:00:00Z"
                            }
                        }
                    ]
                },
                sorts=[
                    {
                        "property": "Estimated 1RM",
                        "direction": "descending"
                    }
                ],
                page_size=1
            )
            # Check if the query returned any results
            if not response["results"]:
                return None  # Or raise an exception, depending on your use case

            # Extract the first result
            entry = response["results"][0]
            return entry
        except Exception as e:
            raise RuntimeError(f"Failed to query 1RM entry: {e}")

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
    def update_all_1RMs(self):
        """
        Function to update all 1RMs in Notion.
        
        Args:
            None
        
        Returns:
            None
        """
        # Load the list of exercises from the JSON file
        with open(os.path.join(os.path.dirname(__file__), "exercise_ids.json"), "r") as file:
            exercise_ids = json.load(file)

        # Iterate through each exercise and update its 1RM
        for exercise_name, exercise_id in exercise_ids.items():
            one_rm_entry = self.get1RMEntry(exercise_name)
            if one_rm_entry:
                self.set_1RM_reference(one_rm_entry)
                print(f"Updated 1RM for {exercise_name}.")
            else:
                print(f"No 1RM entry found for {exercise_name}.")