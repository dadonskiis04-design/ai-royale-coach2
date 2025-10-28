Clash Coach AI - Beginner README
-------------------------------

Files included:
- main.py        : FastAPI backend that analyzes match text and returns feedback
- index.html     : Simple web UI where users paste match summaries and choose tone
- requirements.txt: Python dependencies for deployment (fastapi, uvicorn, pydantic)
- Procfile       : Tells hosting service how to start the app
- README.txt     : This file (beginner-friendly instructions)

Quick upload steps (from your phone):
1. Open this GitHub repo page in your phone browser.
2. Tap "Add file" → "Upload files".
3. Select the files from your Downloads (main.py, index.html, requirements.txt, Procfile, README.txt).
4. Tap "Commit changes" (green button). The files are now in your repo.

Deploy to Render (free tier):
1. Go to https://render.com and sign up / log in.
2. Tap "New" → "Web Service".
3. Connect your GitHub account and choose this repo.
4. For Environment choose "Python".
5. Build Command: (leave empty) or `pip install -r requirements.txt`
6. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Deploy — after a minute Render will give you a website link.
8. Open that link, and you should see the Clash Coach AI web UI.

Testing the app locally (optional):
- If you have a Python environment, run:
  pip install -r requirements.txt
  uvicorn main:app --reload
- Open http://127.0.0.1:8000 in your browser and test.

How to use the site (for users):
1. Paste a short match summary (one or two sentences).
2. Choose a tone (Balanced / Coach / Hype Gamer).
3. Tap Analyze — get reports and advice instantly.

Need help? Reply here and I’ll walk you through any upload or deploy steps.
