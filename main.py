\
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Clash Coach AI - v1 (Text Analyzer)")

class AnalyzeRequest(BaseModel):
    text: str
    tone: str = "balanced"  # options: coach, hype, balanced

def parse_play_lines(text):
    plays = []
    text_l = text.lower()
    play_patterns = re.findall(r"(?:i|you|we) (?:used|played|dropped) ([a-z0-9 \-]+)|(?:opponent|he|they) (?:used|played|dropped) ([a-z0-9 \-]+)", text_l)
    for p in play_patterns:
        card = p[0] or p[1]
        actor = "you" if p[0] else "opponent"
        plays.append({"actor": actor, "card": card.strip()})
    elixir_mentions = re.findall(r"(\d+)\s*elixir", text_l)
    elixir_numbers = [int(x) for x in elixir_mentions]
    return plays, elixir_numbers

def detect_wasted_spell(text):
    text_l = text.lower()
    spells = ["log","fireball","zap","arrows","rocket","snowball","poison","lightning","earthquake","tornado"]
    wasteds = []
    for sp in spells:
        if sp in text_l:
            targets = ["archer","archers","minion","minions","horde","skeleton","skeletons","tower","musketeer","wizard","collector"]
            if not any(t in text_l for t in targets):
                wasteds.append(sp)
    return wasteds

def make_advice(mistakes, tone):
    out = []
    for m in mistakes:
        if tone == "coach":
            if m["type"] == "overcommit":
                out.append(f"You overcommitted: {m['desc']} Try defending cheaper and save elixir for a counterpush.")
            elif m["type"] == "wasted_spell":
                out.append(f"Possible wasted spell: {m['desc']} Consider holding the spell until there's a clear target.")
            elif m["type"] == "missed_punish":
                out.append(f"Missed punish opportunity: {m['desc']} In those moments, apply immediate pressure to the opposite lane.")
            else:
                out.append(m['desc'])
        elif tone == "hype":
            if m["type"] == "overcommit":
                out.append(f"Bruh — overcommit! Save elixir, hit back hard!")
            elif m["type"] == "wasted_spell":
                out.append(f"That's a wasted spell! Don't throw it away!")
            elif m["type"] == "missed_punish":
                out.append(f"Missed the punish! Should've slammed a Hog or Miner!")
            else:
                out.append(m['desc'])
        else: # balanced
            if m["type"] == "overcommit":
                out.append(f"Overcommit detected: {m['desc']}. Recommend cheaper defense and a quick counterpush.")
            elif m["type"] == "wasted_spell":
                out.append(f"Wasted spell suspected: {m['desc']}. Try to use spells when clear targets appear.")
            elif m["type"] == "missed_punish":
                out.append(f"Punish missed: {m['desc']}. Next time, apply 3-4 elixir pressure opposite lane.")
            else:
                out.append(m['desc'])
    return out

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text or ""
    tone = req.tone or "balanced"
    plays, elixirs = parse_play_lines(text)
    reports = []
    if elixirs:
        if len(elixirs) >= 2:
            you_spent = elixirs[0]
            opp_spent = elixirs[1]
            if you_spent - opp_spent >= 4:
                reports.append({"type":"overcommit","desc":f"You spent {you_spent} elixir vs opponent {opp_spent}."})
        elif len(elixirs) == 1:
            if elixirs[0] >= 8:
                reports.append({"type":"overcommit","desc":f"You mentioned spending {elixirs[0]} elixir — that may be an overcommit."})
    wasted = detect_wasted_spell(text)
    for w in wasted:
        reports.append({"type":"wasted_spell","desc":f"You used {w} but no clear target was described."})
    if any(k in text.lower() for k in ["giant","golem","lava","royal giant","electro giant","e-giant","goblin giant"]):
        if not any(k in text.lower() for k in ["hog","miner","graveyard","push","counterpush","attack"]):
            reports.append({"type":"missed_punish","desc":"Opponent played a big tank but you didn't apply immediate opposite-lane pressure per your text."})
    if not reports:
        reports.append({"type":"none","desc":"No obvious issues detected — good job. Consider posting exact plays for deeper analysis."})
    advice = make_advice(reports, tone)
    return {"reports": reports, "advice": advice}

@app.get("/")
def root():
    return {"message":"Clash Coach AI v1 - POST /analyze with {'text':..., 'tone': 'coach'|'hype'|'balanced'}"}
