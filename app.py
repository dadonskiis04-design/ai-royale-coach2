from flask import Flask, render_template_string, request
import os
from openai import OpenAI

# Initialize Flask and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Simple HTML form (we'll style it later)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Clash Coach AI</title>
    <style>
        body { background-color: #111; color: white; font-family: Arial; text-align: center; padding-top: 50px; }
        input, button { padding: 10px; border-radius: 8px; margin: 5px; }
        button { background-color: #ffcc00; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Clash Coach AI</h1>
    <form method="POST">
        <input type="text" name="deck" placeholder="e.g. Golem, Baby Dragon, Night Witch" required style="width: 300px;"><br>
        <button type="submit">Analyze Deck</button>
    </form>
    {% if result %}
    <div style="margin-top: 30px;">
        <h3>AI Analysis:</h3>
        <p>{{ result }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        deck = request.form["deck"]

        prompt = f"Analyze this Clash Royale deck: {deck}. Give advice on strengths, weaknesses, and strategies."

        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an expert Clash Royale coach."},
                      {"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
