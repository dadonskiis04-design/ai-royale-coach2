from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    deck = request.form['deck']

    # Simple "AI" scoring system (you can tweak this later)
    score = 0
    keywords = {
        'hog': 15, 'giant': 10, 'archer': 10, 'musketeer': 10,
        'cannon': 8, 'log': 8, 'fireball': 10, 'skeletons': 6,
        'ice': 6, 'miner': 12, 'balloon': 14, 'goblin': 9,
        'valkyrie': 11, 'wizard': 10, 'pekka': 13
    }

    # Check for matching keywords to calculate score
    for word, value in keywords.items():
        if word.lower() in deck.lower():
            score += value

    # Cap the score at 100
    if score > 100:
        score = 100

    # Generate a short message
    if score >= 80:
        message = "🔥 Excellent deck — well-balanced and powerful!"
    elif score >= 60:
        message = "💪 Strong deck with solid synergy."
    elif score >= 40:
        message = "⚔️ Decent deck, but could use better synergy."
    else:
        message = "😅 Weak composition — might need stronger cards."

    return render_template('result.html', score=score, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
