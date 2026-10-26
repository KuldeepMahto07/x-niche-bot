"""Publish the next post to X: the first approved post in queue.json,
or, if the queue is empty, a fresh post written by Gemini.

Env vars (set as GitHub Actions secrets, or in a local .env):
  GEMINI_API_KEY, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
Optional:
  GEMINI_MODEL (default gemini-2.5-flash), DRY_RUN=1 (print instead of posting)
"""

import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG_FILE = ROOT / "config.json"
HISTORY_FILE = ROOT / "history.json"
QUEUE_FILE = ROOT / "queue.json"
MAX_LEN = 280
HISTORY_KEEP = 60


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_dotenv():
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


def read_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_config():
    return read_json(CONFIG_FILE, {})


def load_history():
    return read_json(HISTORY_FILE, [])


def load_queue():
    return read_json(QUEUE_FILE, [])


def save_queue(queue):
    write_json(QUEUE_FILE, queue)


def save_history(history, text, topic, fmt):
    history.append({"time": now_iso(), "topic": topic, "format": fmt, "text": text})
    write_json(HISTORY_FILE, history[-HISTORY_KEEP:])


def build_prompt(config, topic, fmt, recent):
    recent_block = "\n".join(f"- {p}" for p in recent) or "- (none yet)"
    return f"""You write posts for an X (Twitter) account.

Niche: {config['niche']}
Audience: {config['audience']}
Voice: {config['voice']}

Write ONE post.
Topic: {topic}
Format: {fmt}

Rules:
- Max {MAX_LEN - 20} characters total, including spaces and line breaks.
- Concrete and specific: name real tools, numbers, or steps. No vague hype.
- No hashtags unless truly natural (at most 1). At most 1 emoji.
- Don't invent news, release dates, or statistics you are not sure of.
- Don't repeat ideas from these recent posts:
{recent_block}

Reply with the post text only, no quotes, no preamble."""


def generate(config, topic, fmt, recent):
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = build_prompt(config, topic, fmt, recent)
    for _ in range(3):
        text = client.models.generate_content(model=model, contents=prompt).text
        text = (text or "").strip().strip('"').strip()
        if 0 < len(text) <= MAX_LEN:
            return text
        prompt += f"\n\nYour last answer was {len(text)} characters. Make it shorter."
    raise RuntimeError(f"Could not get a post under {MAX_LEN} characters.")


def publish(text):
    import tweepy

    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    resp = client.create_tweet(text=text)
    return resp.data["id"]


def main():
    load_dotenv()
    config = load_config()
    history = load_history()
    queue = load_queue()

    if queue:
        item = queue[0]
        text, topic, fmt = item["text"], item.get("topic", "queued"), item.get("format", "queued")
        print(f"From queue ({len(queue)} waiting)")
    else:
        recent = [h["text"] for h in history[-15:]]
        topic = random.choice(config["topics"])
        fmt = random.choice(config["formats"])
        try:
            text = generate(config, topic, fmt, recent)
        except RuntimeError as e:
            sys.exit(str(e))
    print(f"Topic: {topic}\nFormat: {fmt}\n---\n{text}\n--- ({len(text)} chars)")

    if os.environ.get("DRY_RUN") == "1":
        print("DRY_RUN=1, not posting.")
        return

    tweet_id = publish(text)
    print(f"Posted: https://x.com/i/status/{tweet_id}")
    save_history(history, text, topic, fmt)
    if queue:
        save_queue(queue[1:])


if __name__ == "__main__":
    main()
