# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import PlannedSet, CompletedSet
from datetime import date
from flask import Flask, render_template
from init_workouts import monday, tuesday
from dotenv import load_dotenv
import os
import json
from database import DatabaseManager

db = DatabaseManager()

load_dotenv()

id_to_name = json.loads(os.environ.get("ID_TO_NAME"))

app = Flask(__name__)
app.secret_key = 'dev'

# Simulated planned sets (normally pulled from a DB)
planned_sets = [w.model_dump() for w in tuesday]
for s in planned_sets:
    s["exercise_name"] = id_to_name[s["exercise_id"]]
    

print("Planned sets:", planned_sets)


@app.route('/')
def index():
    return render_template('planned_sets.html', sets=planned_sets)

@app.route('/log/<exercise_id>', methods=['GET', 'POST'])
def log_set(exercise_id):
    planned = next((s for s in planned_sets if s.exercise_id == exercise_id), None)
    if not planned:
        return "Set not found", 404

    if request.method == 'POST':
        # Capture form input
        completed = CompletedSet(
            workout_name=planned.workout_name,
            actual_weight=float(request.form['actual_weight']),
            actual_reps=int(request.form['actual_reps']),
            exercise_id=exercise_id,
            exercise_notes=request.form.get('notes', ''),
            set_number=planned.set_number,
            date=planned.date
        )
        # Save it (could be to a DB, file, or print to console)
        print("Logged:", completed.model_dump())
        flash('Set logged successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('log_set.html', planned=planned)

@app.route('/log_all', methods=['GET', 'POST'])
def log_all_sets():
    if request.method == 'POST':
        completed_sets = []
        for i in range(len(planned_sets)):
            completed_sets.append({
                "workout_name": request.form.get(f"workout_name_{i}"),
                "exercise_id": request.form.get(f"exercise_id_{i}"),
                "actual_weight": float(request.form.get(f"actual_weight_{i}")),
                "actual_reps": int(request.form.get(f"actual_reps_{i}")),
                "exercise_notes": request.form.get(f"notes_{i}", ""),
                "set_number": int(request.form.get(f"set_number_{i}")),
                "date": date.today().isoformat()
            })
        for s in completed_sets:
            model = CompletedSet(**s)
            print(model)
        print("Completed sets:", completed_sets)
        flash("All sets logged!")
        return redirect(url_for('log_all_sets'))

    return render_template('log_all.html', sets=planned_sets)

