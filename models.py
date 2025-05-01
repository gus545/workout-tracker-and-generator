from pydantic import BaseModel, model_validator
from typing import Optional
from typing import List
from abc import ABC, abstractmethod

class KeyedModel(BaseModel):
    """
    Abstract base class for models with a composite key.
    """
    @abstractmethod
    def get_composite_key():
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

    def get_composite_key():
        return ['id']

class WorkoutSet(KeyedModel):
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
    workout_name : str
    weight: Optional[float] = None
    reps: int
    exercise_id: str
    set_number: int
    date: str
    page_id: str
    def get_composite_key():
        return ['date', 'set_number', 'exercise_id']

class Workout(KeyedModel):
    """
    Class representing a workout session.
    
    Attributes:
        date (str): The date of the workout.
        sets (List[Set]): A list of sets performed during the workout.
    """
    workout_id: str
    workout_name: str
    date: str
    sets: List[WorkoutSet]

    @model_validator(mode="after")
    def validate_sets(self):
        """
        Validate the sets in the workout.
        
        Args:
            cls: The class itself.
            values: The values of the attributes.
        
        Returns:
            The validated values.
        """
        for s in self.sets:
            if s.date != self.date:
                raise ValueError(f"Set date {s.date} does not match workout date {self.date}")
        return self
