from flask import Flask, request, jsonify
from app.db.manager import DatabaseManager  # your custom database wrapper
from .models.sets import CompletedSet

app = Flask(__name__)
db = DatabaseManager()

if __name__ == "__main__":
    app.run(debug=True)
