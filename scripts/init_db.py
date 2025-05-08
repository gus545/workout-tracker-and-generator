import os
import json
import logging
from dotenv import load_dotenv
from tinydb import Query

from app.db.manager import DatabaseManager
from app.services.sync_service import SyncService
from app.models.sets import PlannedWorkout
from scripts.init_workouts import all_days
from app.core.errors import MetadataNotFoundError

logger = logging.getLogger(__name__)


def initialize_db():
    load_dotenv()

    db = DatabaseManager()
    sync = SyncService(db)

    workout_log_info = json.loads(os.environ["WORKOUT_LOG"])
    exercise_info = json.loads(os.environ["EXERCISE"])
    
    if not db.metadata_table.get(Query().table_name == "premade_workout"):
        logger.info("📋 Creating 'premade_workout' table and metadata...")
        db.create_table("premade_workout", PlannedWorkout, remote_id=None)
        data = [day.model_dump() for day in all_days]
        db.add("premade_workout", data)
    else:
        logger.info("✅ 'premade_workout' already exists with metadata — skipping init.")

    try:
        sync.sync_remote_to_local(workout_log_info)
    except MetadataNotFoundError as e:
        logger.warning(f"⚠️ Metadata missing for workout_log: {e}")

    try:
        sync.sync_remote_to_local(exercise_info)
    except MetadataNotFoundError as e:
        logger.warning(f"⚠️ Metadata missing for exercise: {e}")
