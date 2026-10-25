"""Generate a niche post with Gemini and publish it to X.

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
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
HISTORY_FILE = ROOT / "history.json"
MAX_LEN = 280
HISTORY_KEEP = 60


def load_dotenv():
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return []


def save_history(history, text, topic, fmt):
    history.append({
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "topic": topic,
        "format": fmt,
        "text": text,
    })
    HISTORY_FILE.write_text(
        json.dumps(history[-HISTORY_KEEP:], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def build_prompt(topic, fmt, recent):
    recent_block = "\n".join(f"- {p}" for p in recent) or "- (none yet)"
    return f"""You write posts for an X (Twitter) account.

Niche: {CONFIG['niche']}
Audience: {CONFIG['audience']}
Voice: {CONFIG['voice']}

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


def generate(topic, fmt, recent):
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = build_prompt(topic, fmt, recent)
    for _ in range(3):
        text = client.models.generate_content(model=model, contents=prompt).text
        text = (text or "").strip().strip('"').strip()
        if 0 < len(text) <= MAX_LEN:
            return text
        prompt += f"\n\nYour last answer was {len(text)} characters. Make it shorter."
    sys.exit(f"Could not get a post under {MAX_LEN} characters.")


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
    history = load_history()
    recent = [h["text"] for h in history[-15:]]
    topic = random.choice(CONFIG["topics"])
    fmt = random.choice(CONFIG["formats"])

    text = generate(topic, fmt, recent)
    print(f"Topic: {topic}\nFormat: {fmt}\n---\n{text}\n--- ({len(text)} chars)")

    if os.environ.get("DRY_RUN") == "1":
        print("DRY_RUN=1, not posting.")
        return

    tweet_id = publish(text)
    print(f"Posted: https://x.com/i/status/{tweet_id}")
    save_history(history, text, topic, fmt)


if __name__ == "__main__":
    main()
