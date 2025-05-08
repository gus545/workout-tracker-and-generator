from abc import ABC, abstractmethod
from typing import List, Optional, Union
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class KeyedModel(BaseModel, ABC):
    @abstractmethod
    def get_key() -> List[str]:
        pass


class Exercise(KeyedModel):
    name: str
    id: str
    category: str
    equipment: str
    force: str
    level: str
    mechanic: str
    primary_muscles: List[str]
    secondary_muscles: List[str]

    def get_key() -> List[str]:
        return ['id']

    def to_notion_format(self) -> dict:
        return {
            "Name": {"title": [{"text": {"content": self.name}}]},
            "Category": {"select": {"name": self.category}},
            "Equipment": {"select": {"name": self.equipment}},
            "Force": {"select": {"name": self.force}},
            "Level": {"select": {"name": self.level}},
            "Mechanic": {"select": {"name": self.mechanic}},
            "Primary Muscles": {"multi_select": [{"name": m} for m in self.primary_muscles]},
            "Secondary Muscles": {"multi_select": [{"name": m} for m in self.secondary_muscles]},
        }


class BaseSetModel(BaseModel):
    workout_name: str
    exercise_id: str
    set_number: int


class CompletedSet(BaseSetModel, KeyedModel):
    weight: Optional[float] = None
    reps: int
    date: str
    page_id: Optional[str] = None
    exercise_notes: str

    def get_key() -> List[str]:
        return ['date', 'set_number', 'exercise_id']

    def to_notion_format(self) -> dict:
        return {
            "Date": {"date": {"start": self.date}},
            "Set #": {"number": self.set_number},
            "Reps": {"number": self.reps},
            "Weight": {"number": self.weight},
            "Exercise Reference": {"relation": [{"id": self.exercise_id}]},
            "Workout Title": {"select": {"name": self.workout_name}},
            "Notes": {"rich_text": [{"text": {"content": self.exercise_notes}}]},
        }


class PlannedSet(BaseSetModel):
    expected_weight: float
    expected_reps: Union[int, str]
    description: str


class PlannedWorkout(KeyedModel):
    name: str
    sets: List[PlannedSet]

    def get_key() -> List[str]:
        return ['name']
