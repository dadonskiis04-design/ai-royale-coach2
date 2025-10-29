from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Pull your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        deck = request.form['deck']

        prompt = f"You are a Clash Royale coach. Analyze this deck and give tips and weaknesses:\n\nDeck: {deck}\n\nAI Analysis:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Clash Royale deck coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )

            result = response['choices'][0]['message']['content']

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
