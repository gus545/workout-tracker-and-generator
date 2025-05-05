from app.models import KeyedModel, CompletedSet, Exercise
from functools import singledispatch
from typing import Any, Iterable, Union
import logging
from errors import ModelError, ParsingError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def get_parsing_function(model: KeyedModel):
    """
    Function to get the parsing function based on the model type.

    Args:
        model (KeyedModel): The model to use for parsing.
    
    Returns:
        function: The parsing function.
    """
    if model == CompletedSet:
        return parse_set_data
    elif model == Exercise:
        return parse_exercise_data
    else:
        raise ValueError("Unsupported model type")


def parse_data(data: Union[Any, Iterable], model: KeyedModel) -> dict:
    """
    Function to parse data from a dictionary or an iterable using a specified model.

    Args:
        data (Union[Any, Iterable]): The data to parse.
        model (KeyedModel): The model to use for parsing.
    Returns:
        dict: Parsed data.
    """

    # Get the parsing function based on the model type
    parse_func = get_parsing_function(model)


    if isinstance(data, dict):
        return parse_func(data)
    elif isinstance(data, Iterable):
        return [parse_func(item) for item in data]
    
    # Nothing to parse
    logger.info("No data to parse.")
    return []



def parse_set_data(data : dict) -> dict:
    """
    Function to parse set data from a dictionary.
    
    Args:
        data (dict): The set data to parse.
    
    Returns:
        dict: Parsed set data.
    """
    try:
        set_data = data.get("properties", {})
        set_data = {
            "workout_name": data.get("properties", {}).get("Workout Title", {}).get("select", {}).get("name"),
            "weight": set_data.get("Weight", {}).get("number"),
            "reps": set_data.get("Reps", {}).get("number"),
            "exercise_id": set_data.get("Exercise Reference", {}).get("relation", [{}])[0].get("id", {}),
            "set_number": set_data.get("Set #", {}).get("number"),
            "date": set_data.get("Date", {}).get("date", {}).get("start"),
            "page_id": data.get("id"),
            "exercise_notes": extract_text(set_data.get("Notes", {}).get("rich_text", [{}]))
        }
    except Exception as e:
        raise ParsingError(f"Failed to parse data.", context={"data": data, "error": str(e)}, original_exception=e)
    
    try:
        set = CompletedSet(**set_data)
    except ValidationError as e:
        raise ModelError(f"Parsed data did not match model schema", context=e.errors())

    return set.model_dump()

def parse_exercise_data(data : dict) -> dict:
    """
    Function to parse exercise data from a dictionary.
    
    Args:
        data (dict): The exercise data to parse.
    
    Returns:
        dict: Parsed exercise data.
    """
    try:
        properties = data.get("properties", {})

        instructions = extract_text(properties.get("Instructions", {}).get("rich_text", []))
        force = extract_select(properties.get("Force", {}).get("select"))
        equipment = extract_select(properties.get("Equipment", {}).get("select"))
        mechanic = extract_select(properties.get("Mechanic", {}).get("select"))
        level = extract_select(properties.get("Level", {}).get("select"))
        category = extract_select(properties.get("Category", {}).get("select"))

        # Handle name with fallback
        title_block = properties.get("Name", {}).get("title", [])
        name = (
            title_block[0].get("text", {}).get("content")
            if title_block and isinstance(title_block[0], dict)
            else "Unnamed Exercise"
        )

        primary_muscles = [d.get("name") for d in properties.get("Primary Muscles", {}).get("multi_select", [])]
        secondary_muscles = [d.get("name") for d in properties.get("Secondary Muscles", {}).get("multi_select", [])]

        exercise_data = {
            "name": name,
            "id": data.get("id"),
            "category": category,
            "equipment": equipment,
            "force": force,
            "level": level,
            "mechanic": mechanic,
            "instructions": instructions,
            "primary_muscles": primary_muscles,
            "secondary_muscles": secondary_muscles,
        }
    except Exception as e:
        raise ParsingError(f"Failed to parse data.", context={"data": data, "error": str(e)}, original_exception=e)
    
    try:
        exercise = Exercise(**exercise_data)
        return exercise.model_dump()
    except ValidationError as e:
        raise ModelError(f"Parsed data did not match model schema", context=e.errors())
        

    
def extract_text(block: list[dict]) -> str:
        if block and isinstance(block[0], dict):
            return block[0].get("text", {}).get("content", "").replace("\n", " ")
        return "No instructions provided."

def extract_select(field: dict) -> str:
    return field.get("name") if field else "Not provided."

def parse_database_info(data: dict) -> dict:
    """
    Function to parse database information from a dictionary.
    
    Args:
        data (dict): The database data to parse.
    
    Returns:
        dict: Parsed database information.
    """
    return {
        "id": data.get("id"),
        "title": data.get("title", [{}])[0].get("text", {}).get("content", ""),
        "created_time": data.get("created_time"),
        "last_edited_time": data.get("last_edited_time"),
        "properties": data.get("properties")
    }