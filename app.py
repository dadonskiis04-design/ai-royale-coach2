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
                    {"role": "user", "content": f"Analyze this deck: {deck}"}
                ]
            )
            result = response.choices[0].message.content
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
