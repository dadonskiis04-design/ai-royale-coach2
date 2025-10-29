from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        deck = request.form['deck']
        # 🔹 You can replace this with your actual AI analysis later
        result = f"Your deck: {deck}\n\nAI Analysis coming soon..."
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
