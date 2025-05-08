from typing import Any, Iterable, Union
import logging
import datetime

from pydantic import ValidationError

from app.models.sets import KeyedModel, CompletedSet, Exercise
from app.core.errors import ModelError, ParsingError

logger = logging.getLogger(__name__)


def parse_data(data: Union[Any, Iterable], model: KeyedModel) -> Union[dict, list[dict]]:
    parser = _get_parser_for_model(model)

    if isinstance(data, dict):
        return parser(data)
    elif isinstance(data, Iterable):
        return [parser(item) for item in data]

    logger.info("No data to parse.")
    return []


def _get_parser_for_model(model: KeyedModel):
    if model == CompletedSet:
        return parse_set_data
    if model == Exercise:
        return parse_exercise_data
    raise ValueError(f"Unsupported model type: {model}")


def parse_set_data(data: dict) -> dict:
    try:
        props = data.get("properties", {})
        set_data = {
            "workout_name": props.get("Workout Title", {}).get("select", {}).get("name"),
            "weight": props.get("Weight", {}).get("number"),
            "reps": props.get("Reps", {}).get("number"),
            "exercise_id": props.get("Exercise Reference", {}).get("relation", [{}])[0].get("id"),
            "set_number": props.get("Set #", {}).get("number"),
            "date": props.get("Date", {}).get("date", {}).get("start"),
            "page_id": data.get("id"),
            "exercise_notes": extract_text(props.get("Notes", {}).get("rich_text", [])),
        }
        return CompletedSet(**set_data).model_dump()
    except ValidationError as e:
        raise ModelError("Parsed set did not match model schema", context=e.errors())
    except Exception as e:
        raise ParsingError("Failed to parse set data", context={"data": data, "error": str(e)}, original_exception=e)


def parse_exercise_data(data: dict) -> dict:
    try:
        props = data.get("properties", {})

        name = extract_title(props.get("Name", {}).get("title", []))
        exercise_data = {
            "id": data.get("id"),
            "name": name,
            "category": extract_select(props.get("Category", {}).get("select")),
            "equipment": extract_select(props.get("Equipment", {}).get("select")),
            "force": extract_select(props.get("Force", {}).get("select")),
            "level": extract_select(props.get("Level", {}).get("select")),
            "mechanic": extract_select(props.get("Mechanic", {}).get("select")),
            "instructions": extract_text(props.get("Instructions", {}).get("rich_text", [])),
            "primary_muscles": [d.get("name") for d in props.get("Primary Muscles", {}).get("multi_select", [])],
            "secondary_muscles": [d.get("name") for d in props.get("Secondary Muscles", {}).get("multi_select", [])],
        }
        return Exercise(**exercise_data).model_dump()
    except ValidationError as e:
        raise ModelError("Parsed exercise did not match model schema", context=e.errors())
    except Exception as e:
        raise ParsingError("Failed to parse exercise data", context={"data": data, "error": str(e)}, original_exception=e)


def extract_text(blocks: list[dict]) -> str:
    if blocks and isinstance(blocks[0], dict):
        return blocks[0].get("text", {}).get("content", "").replace("\n", " ")
    return ""


def extract_select(field: dict) -> str:
    return field.get("name") if field else ""


def extract_title(block: list[dict]) -> str:
    if block and isinstance(block[0], dict):
        return block[0].get("text", {}).get("content", "")
    return "Unnamed Exercise"


def parse_database_info(data: dict) -> dict:
    return {
        "id": data.get("id"),
        "title": data.get("title", [{}])[0].get("text", {}).get("content", ""),
        "created_time": data.get("created_time"),
        "last_edited_time": data.get("last_edited_time"),
        "properties": data.get("properties"),
    }
