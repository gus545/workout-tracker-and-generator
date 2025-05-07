from flask import request, jsonify
from app.db.manager import DatabaseManager
from app.models.sets import CompletedSet

db = DatabaseManager()
db.create_table("completed_sets", CompletedSet)

def register_routes(app):
    @app.route("/sets", methods=["POST"])
    def create_set():
        data = request.get_json()
        result = db.add("completed_sets", data)
        return jsonify(result), 201

    @app.route("/sets", methods=["GET"])
    def get_set():
        key = {
            "date": request.args.get("date"),
            "set_number": int(request.args.get("set_number")),
            "exercise_id": request.args.get("exercise_id")
        }
        results = db.get("completed_sets", key)
        return jsonify(results), 200
    
    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        return jsonify(db.db.all())

    @app.route("/workouts", methods=["POST"])
    def create_workout():
        data = request.get_json()
        data = CompletedSet(**data).model_dump()
        workout = db.add("workout_log",data)
        return jsonify(workout), 201

    @app.route("/workouts/<string:workout_id>", methods=["PUT"])
    def update_workout(workout_id):
        data = request.get_json()
        data = CompletedSet(**data).model_dump()
        updated = db.update(workout_id, data)
        return jsonify(updated)

    @app.route("/workouts/<string:workout_id>", methods=["DELETE"])
    def delete_workout(workout_id):
        data = CompletedSet(**data).model_dump()
        db.db.remove(workout_id)
        return '', 204
