"""X Studio: a local dashboard for the bot.

Run:  python studio.py   then open http://127.0.0.1:5050
Edits config.json and queue.json in this folder; "Publish" commits and pushes
them so the GitHub Actions bot picks them up.
"""

import os
import random
import subprocess

from flask import Flask, jsonify, request, send_from_directory

import bot

app = Flask(__name__, static_folder=None)
PORT = int(os.environ.get("STUDIO_PORT", "5050"))
TRACKED = ["config.json", "queue.json"]


def git(*args):
    proc = subprocess.run(
        ["git", *args], cwd=bot.ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def unpublished_changes():
    code, out = git("status", "--porcelain", *TRACKED)
    return code == 0 and bool(out)


def error(message, status=400):
    return jsonify({"error": message}), status


@app.get("/")
def index():
    return send_from_directory(bot.ROOT / "studio", "index.html")


@app.get("/api/state")
def state():
    return jsonify({
        "config": bot.load_config(),
        "queue": bot.load_queue(),
        "history": list(reversed(bot.load_history())),
        "unpublished": unpublished_changes(),
        "has_gemini_key": bool(os.environ.get("GEMINI_API_KEY")),
        "max_len": bot.MAX_LEN,
    })


@app.post("/api/config")
def save_config():
    data = request.get_json(force=True)
    for key in ("niche", "audience", "voice"):
        if not str(data.get(key, "")).strip():
            return error(f"'{key}' can't be empty.")
    for key in ("topics", "formats"):
        items = [s.strip() for s in data.get(key, []) if str(s).strip()]
        if not items:
            return error(f"Add at least one item to '{key}'.")
        data[key] = items
    bot.write_json(bot.CONFIG_FILE, {k: data[k] for k in ("niche", "audience", "voice", "topics", "formats")})
    return jsonify({"ok": True, "unpublished": unpublished_changes()})


@app.post("/api/drafts")
def drafts():
    if not os.environ.get("GEMINI_API_KEY"):
        return error("No GEMINI_API_KEY found. Add it to the .env file in this folder and restart the Studio.")
    count = max(1, min(int(request.get_json(force=True).get("count", 3)), 6))
    config = bot.load_config()
    recent = [h["text"] for h in bot.load_history()[-15:]] + [q["text"] for q in bot.load_queue()]
    results = []
    for _ in range(count):
        topic = random.choice(config["topics"])
        fmt = random.choice(config["formats"])
        try:
            text = bot.generate(config, topic, fmt, recent)
        except Exception as e:  # surface Gemini errors (bad key, quota) to the UI
            return error(f"Gemini error: {e}", 502)
        recent.append(text)
        results.append({"text": text, "topic": topic, "format": fmt})
    return jsonify({"drafts": results})


@app.post("/api/queue")
def save_queue():
    items = request.get_json(force=True).get("queue", [])
    queue = []
    for item in items:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        if len(text) > bot.MAX_LEN:
            return error(f"A queued post is {len(text)} characters; the limit is {bot.MAX_LEN}.")
        queue.append({
            "text": text,
            "topic": item.get("topic", "manual"),
            "format": item.get("format", "manual"),
            "added": item.get("added") or bot.now_iso(),
        })
    bot.save_queue(queue)
    return jsonify({"ok": True, "queue": queue, "unpublished": unpublished_changes()})


@app.post("/api/publish")
def publish():
    if unpublished_changes():
        git("add", *TRACKED)
        code, out = git("commit", "-m", "Update bot settings and queue from X Studio")
        if code != 0:
            return error(f"git commit failed:\n{out}", 500)
    code, out = git("pull", "--rebase", "--autostash")
    if code != 0:
        return error(f"git pull failed:\n{out}", 500)
    code, out = git("push")
    if code != 0:
        return error(f"git push failed:\n{out}", 500)
    return jsonify({"ok": True, "unpublished": False})


@app.post("/api/refresh")
def refresh():
    code, out = git("pull", "--rebase", "--autostash")
    if code != 0:
        return error(f"git pull failed:\n{out}", 500)
    return state()


if __name__ == "__main__":
    bot.load_dotenv()
    print(f"X Studio running at http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, debug=False)
