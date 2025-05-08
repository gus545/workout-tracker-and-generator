from app.db.manager import DatabaseManager
from app.models.sets import PlannedSet, PlannedWorkout
from json import loads
import os
from dotenv import load_dotenv

load_dotenv()

id_to_name = loads(os.environ["ID_TO_NAME"])
id_dict = {v: k for k, v in id_to_name.items()}

monday = [
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 0,
        expected_weight = 135,
        expected_reps = 8,
        description= "0.7 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 1,
        expected_weight = 135,
        expected_reps = 8,
        description= "0.7 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 2,
        expected_weight = 135,
        expected_reps = "AMAP",
        description= "0.7 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Assisted Chin-Up"],
        set_number = 0,
        expected_weight = 115,
        expected_reps = 10,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Assisted Chin-Up"],
        set_number = 1,
        expected_weight = 115,
        expected_reps = 10,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Assisted Chin-Up"],
        set_number = 2,
        expected_weight = 115,
        expected_reps = 10,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Standing face pull"],
        set_number = 0,
        expected_weight = 45,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Standing face pull"],
        set_number = 1,
        expected_weight = 45,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Arnold press"],
        set_number = 0,
        expected_weight = 50,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Arnold press"],
        set_number = 1,
        expected_weight = 60,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Incline dumbbell row"],
        set_number = 0,
        expected_weight = 70,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Incline dumbbell row"],
        set_number = 1,
        expected_weight = 70,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Dumbbell lateral raise"],
        set_number = 0,
        expected_weight = 30,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Dumbbell lateral raise"],
        set_number = 1,
        expected_weight = 30,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 0,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 1,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 2,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 3,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 4,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D1",
        exercise_id = id_dict["Concentration curl"],
        set_number = 5,
        expected_weight = 20,
        expected_reps = 15,
        description= ""
    ),   
]

tuesday = [
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 0,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 1,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 2,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 3,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 4,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Barbell Back Squat"],
        set_number = 5,
        expected_weight = 155,
        expected_reps = 6,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Good Morning"],
        set_number = 0,
        expected_weight = 125,
        expected_reps = 12,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Good Morning"],
        set_number = 1,
        expected_weight = 125,
        expected_reps = 12,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Lateral Band Walk"],
        set_number = 0,
        expected_weight = 20,
        expected_reps = 30,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Lateral Band Walk"],
        set_number = 1,
        expected_weight = 20,
        expected_reps = 30,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["Lateral Band Walk"],
        set_number = 2,
        expected_weight = 20,
        expected_reps = 30,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["V-up"],
        set_number = 0,
        expected_weight = 0,
        expected_reps = 15,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["V-up"],
        set_number = 1,
        expected_weight = 0,
        expected_reps = 15,
        description= ""
        ),
    PlannedSet(
        workout_name="Squat 2x Beg W1D1",
        exercise_id= id_dict["V-up"],
        set_number = 2,
        expected_weight = 0,
        expected_reps = 15,
        description= ""
        )
]

wednesday = [
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 0,
        expected_weight = 145,
        expected_reps = 6,
        description= "0.75 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 1,
        expected_weight = 145,
        expected_reps = 6,
        description= "0.75 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Barbell Bench Press"],
        set_number = 2,
        expected_weight = 145,
        expected_reps = "AMAP",
        description= "0.75 of max weight"
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Overhead Press"],
        set_number = 0,
        expected_weight = 80,
        expected_reps = 8,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Overhead Press"],
        set_number = 1,
        expected_weight = 80,
        expected_reps = 8,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Overhead Press"],
        set_number = 2,
        expected_weight = 80,
        expected_reps = 8,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Single-arm kneeling lat pull-down"],
        set_number = 0,
        expected_weight = 70,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Single-arm kneeling lat pull-down"],
        set_number = 1,
        expected_weight = 70,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Single-arm kneeling lat pull-down"],
        set_number = 2,
        expected_weight = 70,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Single-arm kneeling lat pull-down"],
        set_number = 3,
        expected_weight = 70,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Pendlay Row"],
        set_number = 0,
        expected_weight = 135,
        expected_reps = 10,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Pendlay Row"],
        set_number = 1,
        expected_weight = 135,
        expected_reps = 10,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Standing dumbbell upright row"],
        set_number = 0,
        expected_weight = 60,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Standing dumbbell upright row"],
        set_number = 1,
        expected_weight = 60,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Incline Shrug"],
        set_number = 0,
        expected_weight = 70,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["Incline Shrug"],
        set_number = 1,
        expected_weight = 70,
        expected_reps = 20,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["EZ-Bar Skullcrusher"],
        set_number = 0,
        expected_weight = 60,
        expected_reps = 12,
        description= ""
    ),
    PlannedSet(
        workout_name="Bench 3x Beg W1D2",
        exercise_id = id_dict["EZ-Bar Skullcrusher"],
        set_number = 1,
        expected_weight = 60,
        expected_reps = 12,
        description= ""
    ),
]

thursday = [
]

friday = [
]

saturday = [
]

monday = PlannedWorkout(
    name= "monday", 
    sets =monday)
tuesday = PlannedWorkout(
    name= "tuesday", 
    sets =tuesday)
wednesday = PlannedWorkout(
    name= "wednesday", 
    sets =wednesday)


all_days = [monday, tuesday, wednesday]

