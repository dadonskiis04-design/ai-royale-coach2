from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        deck = request.json['deck']

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Clash Royale coach."},
                {"role": "user", "content": f"Analyze this Clash Royale deck: {deck}. Suggest strengths, weaknesses, and possible improvements."}
            ]
        )

        analysis = response.choices[0].message.content
        return jsonify({'result': analysis})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
