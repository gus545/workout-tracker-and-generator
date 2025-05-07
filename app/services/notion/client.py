from notion_client import Client
import logging
import app.core.log as log

def initialize_notion_client(api_key):
    """
    Initializes and returns a Notion client for interacting with the Notion API.

    Returns:
        Client: An instance of the Notion client.
    """
        
    return Client(auth=api_key, logger=log.initialize_logger(), log_level = logging.DEBUG)


def test_connection(client):
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