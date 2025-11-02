from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Make sure upload folder exists
os.makedirs("uploads", exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        deck = request.form['deck']
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Clash Royale deck analyst."},
                    {"role": "user", "content": f"""
Analyze this Clash Royale deck: {deck}

Give a structured analysis including:
- Deck Strengths
- Deck Weaknesses
- Ideal Playstyle
- Best Counters
- Average Elixir Cost
- And finally, rate this deck out of 100 points based on balance, synergy, and meta strength.

Format the output neatly with clear sections.
"""}
                ]
            )
            result = response.choices[0].message.content
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('index.html', result=result)

# 🆕 New route: analyze multiple gameplay frames
@app.route("/analyze_frames", methods=["POST"])
def analyze_frames():
    files = request.files.getlist("frames")
    if not files:
        return jsonify({"error": "No frames uploaded"}), 400

    results = []
    for i, file in enumerate(files):
        filename = file.filename
        path = os.path.join("uploads", filename)
        file.save(path)

        # For now, just store confirmation (we’ll add AI vision next)
        results.append({
            "frame": i + 1,
            "filename": filename,
            "status": "saved"
        })

    return jsonify({
        "status": "ok",
        "frames_received": len(results),
        "results": results
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
