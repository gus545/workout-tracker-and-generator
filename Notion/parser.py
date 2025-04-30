from models import WorkoutSet, Exercise

def parse_set_data(data : dict) -> dict:
    """
    Function to parse set data from a dictionary.
    
    Args:
        data (dict): The set data to parse.
    
    Returns:
        dict: Parsed set data.
    """

    set_data = data.get("properties", {})
    set_data = {
        "workout_name": data.get("properties", {}).get("Workout Title", {}).get("select", {}).get("name"),
        "weight": set_data.get("Weight", {}).get("number"),
        "reps": set_data.get("Reps", {}).get("number"),
        "exercise_id": set_data.get("Exercise Reference", {}).get("relation", [{}])[0].get("id", {}),
        "set_number": set_data.get("Set #", {}).get("number"),
        "date": data.get("properties", {}).get("Date", {}).get("date", {}).get("start")
    }

    set = WorkoutSet(**set_data)

    return set.model_dump()

def parse_exercise_data(data : dict) -> dict:
    """
    Function to parse exercise data from a dictionary.
    
    Args:
        data (dict): The exercise data to parse.
    
    Returns:
        dict: Parsed exercise data.
    """
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

    exercise = Exercise(**exercise_data)
    return exercise.model_dump()

def parse_pages(data : dict, parse_function) -> list:
    """
    Function to parse pages from a dictionary using a specified parsing function.
    
    Args:
        data (dict): The data to parse.
        parse_function (function): The function to use for parsing.
    
    Returns:
        list: A list of parsed data.
    """

    parsed_data = []
    for page in data:
        parsed_data.append(parse_function(page))
    
    return parsed_data

    
def extract_text(block: list[dict]) -> str:
        if block and isinstance(block[0], dict):
            return block[0].get("text", {}).get("content", "").replace("\n", " ")
        return "No instructions provided."

def extract_select(field: dict) -> str:
    return field.get("name") if field else "Not provided."
