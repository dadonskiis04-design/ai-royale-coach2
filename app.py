from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Clash Coach AI!</h1><p>Smart Clash Royale tips coming soon.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
