from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Clash Coach AI!</h1><p>Smart Clash Royale tips coming soon.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    from fastapi import Request
from pydantic import BaseModel

class DeckRequest(BaseModel):
    cards: list[str]

@app.post("/analyze-deck")
def analyze_deck(data: DeckRequest):
    cards = [card.lower() for card in data.cards]

    advice = []

    # Example logic (you can expand this later)
    if "golem" in cards:
        advice.append("Golem deck detected — make sure you have a good air defense like Mega Minion or Baby Dragon.")
    if "hog rider" in cards:
        advice.append("Hog Rider deck — Tornado or Cannon are great counters.")
    if "lava hound" in cards:
        advice.append("Lava Hound deck — carry at least one high-damage air troop.")
    if not advice:
        advice.append("Deck looks balanced, test it out and adjust based on your matchups.")

    return {"deck": data.cards, "advice": advice}

