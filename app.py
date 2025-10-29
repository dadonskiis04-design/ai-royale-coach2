from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
