from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os, json

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

os.makedirs("uploads", exist_ok=True)

MEMORY_FILE = "memory.json"


# ---------------------------
# 📘 MEMORY SYSTEM
# ---------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_memory(entry):
    memory = load_memory()
    memory.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory[-50:], f, indent=2)  # keep last 50 memories


# ---------------------------
# ⚔️ DECK ANALYZER
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        deck = request.form['deck']
        memory = load_memory()
        recent_context = "\n".join(
            [f"- {m['type']}: {m['summary']}" for m in memory[-5:]]
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Clash Royale deck analyst that remembers past analyses."
                    },
                    {
                        "role": "user",
                        "content": f"""
Here’s some past knowledge:
{recent_context}

Now analyze this new deck: {deck}

Give:
- Strengths
- Weaknesses
- Ideal Playstyle
- Best Counters
- Average Elixir Cost
- Rating /100
"""
                    }
                ]
            )
            result = response.choices[0].message.content

            save_memory({
                "type": "deck_analysis",
                "deck": deck,
                "summary": result[:200] + "...",
            })

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)


# ---------------------------
# 🧠 FRAME ANALYZER
# ---------------------------
@app.route("/analyze_frames", methods=["POST"])
def analyze_frames():
    files = request.files.getlist("frames")
    if not files:
        return jsonify({"error": "No frames uploaded"}), 400

    analyses = []
    memory = load_memory()
    recent_context = "\n".join(
        [f"- {m['type']}: {m['summary']}" for m in memory[-5:]]
    )

    try:
        for i, file in enumerate(files):
            filename = file.filename
            path = os.path.join("uploads", filename)
            file.save(path)

            with open(path, "rb") as img_file:
                image_bytes = img_file.read()

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Clash Royale coach that analyzes gameplay frames. "
                            "You also remember recent matches from memory."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Recent knowledge:\n{recent_context}\n\nNow analyze frame {i+1}:"},
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

            save_memory({
                "type": "frame_analysis",
                "summary": ai_comment[:200] + "...",
            })

        return jsonify({
            "status": "ok",
            "frames_analyzed": len(analyses),
            "analyses": analyses
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# 🚀 RUN
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
import cv2
import tempfile
import os

@app.route('/upload_video', methods=['POST'])
def upload_video():
    video = request.files['video']
    if not video:
        return render_template('index.html', result="No video uploaded!")

    # Save video temporarily
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video.save(temp_video.name)

    cap = cv2.VideoCapture(temp_video.name)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frames = []
    count = 0

    # Extract 1 frame every 10 seconds
    interval = frame_rate * 10

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(1)) % interval == 0:
            frame_path = f"frame_{count}.jpg"
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            count += 1
    cap.release()

    # Delete temp video
    os.remove(temp_video.name)

    # Example placeholder analysis text
    analysis = f"Extracted {len(frames)} frames from the video. Ready for AI analysis!"

    return render_template('index.html', result=analysis)
