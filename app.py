from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)


# 🧩 Route 1: Deck Analyzer (Text)
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


# 🧠 Route 2: Gameplay Frame Analyzer (Images)
@app.route("/analyze_frames", methods=["POST"])
def analyze_frames():
    files = request.files.getlist("frames")
    if not files:
        return jsonify({"error": "No frames uploaded"}), 400

    analyses = []

    try:
        for i, file in enumerate(files):
            filename = file.filename
            path = os.path.join("uploads", filename)
            file.save(path)

            # Read the image to send to the Vision model
            with open(path, "rb") as img_file:
                image_bytes = img_file.read()

            # Analyze each frame using GPT-4o-mini (Vision)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Clash Royale coach that analyzes real gameplay screenshots frame-by-frame. "
                            "Describe what is happening in the image, mention what the player is doing well or poorly, "
                            "and give one improvement tip per frame."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"This is frame {i+1} of a Clash Royale match. Analyze it:"},
                            {"type": "image", "image_data": image_bytes}
                        ]
                    }
                ]
            )

            ai_comment = response.choices[0].message.content

            analyses.append({
                "frame": i + 1,
                "filename": filename,
                "analysis": ai_comment
            })

        return jsonify({
            "status": "ok",
            "frames_analyzed": len(analyses),
            "analyses": analyses
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
