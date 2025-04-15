import os
from dotenv import load_dotenv
from notion_client import Client
import logging
import log
import structlog



# Load environment variables from the .env file
load_dotenv()

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

