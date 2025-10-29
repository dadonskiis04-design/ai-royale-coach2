from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    deck = request.form['deck']
    cards = [c.strip().lower() for c in deck.split(',') if c.strip()]

    # --- Basic scoring system ---
    score = 50  # baseline

    # Card count bonus/penalty
    if len(cards) == 8:
        score += 10
    elif len(cards) < 6:
        score -= 10
    elif len(cards) > 10:
        score -= 5

    # Keyword bonuses
    air = ["baby dragon", "minions", "minion horde", "archer queen"]
    spell = ["fireball", "log", "zap", "arrows", "rocket"]
    building = ["cannon", "inferno tower", "tesla", "bomb tower"]
    tank = ["giant", "golem", "pekka", "royal giant", "lava hound"]

    if any(c in card for c in cards for card in air):
        score += 5
    if any(c in card for c in cards for card in spell):
        score += 5
    if any(c in card for c in cards for card in building):
        score += 5
    if any(c in card for c in cards for card in tank):
        score += 5

    # Keep within 0-100 range
    score = max(0, min(100, score))

    # Messages
    if score > 85:
        message = "🔥 Excellent deck with strong synergy and coverage!"
    elif score > 70:
        message = "⚔️ Solid and balanced deck overall!"
    elif score > 50:
        message = "⚠️ Decent deck, but could use some tuning."
    else:
        message = "💀 Weak composition — may struggle against meta decks."

    return render_template('result.html', score=score, message=message)
