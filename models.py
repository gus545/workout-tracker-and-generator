from pydantic import BaseModel, model_validator
from typing import Optional
from typing import List

class WorkoutSet(BaseModel):
    """
    Class representing a set of an exercise.
    
    Attributes:
        weight (float): The weight lifted in the set.
        reps (int): The number of repetitions performed in the set.
    """
    workout_name : str
    weight: Optional[float] = None
    reps: int
    exercise_id: str
    set_number: int
    date: str

class Workout(BaseModel):
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
