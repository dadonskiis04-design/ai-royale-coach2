from flask import Flask, request, jsonify
from pydantic import BaseModel
from typing import List

app = Flask(__name__)

# Simple homepage to confirm the app is running
@app.route('/')
def home():
    return "<h1>Welcome to Clash Coach AI!</h1><p>Use POST /analyze-deck with a JSON deck list.</p>"

# Define the data model (manually validated, since we're not using FastAPI here)
@app.route('/analyze-deck', methods=['POST'])
def analyze_deck():
    data = request.get_json()
    cards = [c.lower() for c in data.get("cards", [])]

    advice = []

    if "golem" in cards:
        advice.append("Golem deck detected — make sure you have a good air defense like Mega Minion or Baby Dragon.")
    if "hog rider" in cards:
        advice.append("Hog Rider deck — Tornado or Cannon are great counters.")
    if "lava hound" in cards:
        advice.append("Lava Hound deck — carry at least one high-damage air troop.")
    if not advice:
        advice.append("Deck looks balanced, test it out and adjust based on your matchups.")

    return jsonify({"deck": data.get("cards", []), "advice": advice})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
