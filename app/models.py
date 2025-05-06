from pydantic import BaseModel, model_validator
from typing import Optional
from typing import List
from abc import ABC, abstractmethod
import logging
from typing import Union

logger = logging.getLogger(__name__)


class KeyedModel(BaseModel):
    """
    Abstract base class for models with a composite key.
    """
    @abstractmethod
    def get_key():
        """
        Abstract method to get the composite key of the model.
        """
        pass



class Exercise(KeyedModel):
    """
    Class representing an exercise.

    Attributes:
        name (str): The name of the exercise.
        id (str): The ID of the exercise.
        category (str): The category of the exercise.
        equipment (str): The equipment used for the exercise.
        force (str): The type of force applied in the exercise.
        level (str): The level of difficulty of the exercise.
        mechanic (str): The mechanic of the exercise.
        primary_muscles (List[str]): A list of primary muscles targeted by the exercise.
        secondary_muscles (List[str]): A list of secondary muscles targeted by the exercise.
    """
    name: str
    id: str
    category: str
    equipment: str
    force: str
    level: str
    mechanic: str
    primary_muscles: List[str]
    secondary_muscles: List[str]

    def get_key():
        return ['id']
    def to_notion_format(self):
        return{
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": self.name
                        }
                    }
                ]
            },
            "Category": {
                "select": {
                    "name": self.category
                }
            },
            "Equipment": {
                "select": {
                    "name": self.equipment
                }
            },
            "Force": {
                "select": {
                    "name": self.force
                }
            },
            "Level": {
                "select": {
                    "name": self.level
                }
            },
            "Mechanic": {
                "select": {
                    "name": self.mechanic
                }
            },
            "Primary Muscles":{
                "multi_select": [
                    {
                        "name": muscle
                    } for muscle in self.primary_muscles
                ]
            },
            "Secondary Muscles": {
                "multi_select": [
                    {
                        "name": muscle
                    } for muscle in self.secondary_muscles
                ]
            }
        }

class BaseSetModel(BaseModel):
    """
    Abstract base class for sets.
    """
    workout_name: str
    exercise_id: str
    set_number: int

class CompletedSet(BaseSetModel,KeyedModel):
    """
    Class representing a set of an exercise.

    Attributes:
        workout_name (str): The name of the workout.
        weight (Optional[float]): The weight used in the set.
        reps (int): The number of repetitions performed in the set.
        exercise_id (str): The ID of the exercise.
        set_number (int): The number of the set in the workout.
        date (str): The date of the workout.
    """
    weight: Optional[float] = None
    reps: int
    date: str
    page_id: Optional[str] = None
    exercise_notes: str
    def get_key():
        return ['date', 'set_number', 'exercise_id']
    def to_notion_format(self):
        return {
            "Date":{
                "date": {
                    "start": self.date
                }
            },
            "Set #": {
                "number": self.set_number
            },
            "Reps": {
                "number": self.reps
            },
            "Weight": {
                "number": self.weight
            },
            "Exercise Reference": {
                "relation": [
                    {
                        "id": self.exercise_id
                    }
                ]
            },
            "Workout Title": {
                "select": {
                    "name": self.workout_name
                }
            },
            "Notes": {
                "rich_text": [
                    {
                        "text": {
                            "content": self.exercise_notes
                        }
                    }
                ]
            }
        }

class PlannedSet(BaseSetModel):
    """
    Class representing a form for creating a set.
    """
    expected_weight: float
    expected_reps: Union[int,str]
    description: str

