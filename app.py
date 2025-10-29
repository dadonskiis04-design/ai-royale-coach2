from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        deck = request.form['deck']
        prompt = f"Analyze this Clash Royale deck and format the output with markdown headers and bullet points: {deck}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
