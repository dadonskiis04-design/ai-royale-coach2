from flask import Flask, render_template, request
from openai import OpenAI
import os
import cv2
import numpy as np

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ---- ROUTE 1: Deck Analyzer ----
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

# ---- ROUTE 2: Video Upload + Frame Extraction ----
@app.route('/analyze-video', methods=['GET', 'POST'])
def analyze_video():
    analysis = None
    if request.method == 'POST':
        video_file = request.files['video']
        if video_file:
            # Save the uploaded file temporarily
            video_path = os.path.join("static", "uploaded_video.mp4")
            video_file.save(video_path)

            # Extract frames every 3 seconds, skip low-motion scenes
            frames = []
            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            interval = int(fps * 3)  # 3 seconds between frames
            success, prev_frame = cap.read()
            count = 0

            while success:
                if count % interval == 0:
                    frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                    # Skip if next frame has little motion
                    ret, frame = cap.read()
                    if not ret:
                        break
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    motion = np.mean(cv2.absdiff(frame_gray, gray))
                    if motion > 10:  # only keep frames with noticeable motion
                        frames.append(frame)
                success, prev_frame = cap.read()
                count += 1
            cap.release()

            # Describe gameplay frames to the AI (simplified for now)
            frame_count = len(frames)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a Clash Royale match analyst. Only analyze gameplay scenes, ignore menus, commentary, and replays."},
                        {"role": "user", "content": f"""
A Clash Royale video was analyzed.
The AI detected around {frame_count} active gameplay frames (after skipping still scenes).

Based on this, describe possible player mistakes, good plays, and give general strategy feedback.
"""}
                    ]
                )
                analysis = response.choices[0].message.content
            except Exception as e:
                analysis = f"Error: {str(e)}"
    return render_template('video.html', analysis=analysis)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
