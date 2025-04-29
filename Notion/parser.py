from models import WorkoutSet

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

    pass
