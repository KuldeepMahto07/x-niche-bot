# x-niche-bot

Posts AI & tech content to X automatically, 3 times a day (9:00, 15:00, 20:00 IST).
Gemini writes each post from your niche settings in `config.json`; GitHub Actions runs it for free.

## Setup (about 15 minutes)

### 1. Get a free Gemini key
1. Go to https://aistudio.google.com/apikey and sign in.
2. Click **Create API key** and copy it.

### 2. Get X API keys (free tier)
1. Go to https://developer.x.com and sign up for the **Free** tier with the X account that should post.
2. Open your app in the Developer Portal → **User authentication settings** → **Set up**:
   - App permissions: **Read and write**
   - Type of App: **Web App, Automated App or Bot**
   - Callback URL / Website: any URL you own (e.g. `https://example.com`)
3. Go to **Keys and tokens**:
   - **API Key and Secret** → Regenerate → copy both.
   - **Access Token and Secret** → Generate → copy both.
     Do this *after* step 2, otherwise the token is read-only and posting fails with 403.

### 3. Put it on GitHub
1. Create a new **private** repo on github.com (e.g. `x-niche-bot`).
2. Push this folder:
   ```bash
   git init && git add . && git commit -m "x niche bot"
   git branch -M main
   git remote add origin https://github.com/<you>/x-niche-bot.git
   git push -u origin main
   ```
3. In the repo: **Settings → Secrets and variables → Actions → New repository secret**, add:
   `GEMINI_API_KEY`, `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`

### 4. Test it
**Actions → Post to X → Run workflow**. "Generate only" is ticked by default: the log shows the post without publishing.
Untick it and run again to publish one real post. After that it runs on the schedule by itself.

## X Studio (dashboard)
A local control panel for the bot. Double-click `start-studio.bat` (or run `python studio.py`), then open http://127.0.0.1:5050.

- **Drafts:** Gemini writes posts in your niche; edit them and add the good ones to the queue. Needs `GEMINI_API_KEY` in a local `.env`.
- **Queue:** the bot posts these in order before writing its own. Reorder, edit, or remove.
- **History:** what the bot has posted ("Refresh from GitHub" pulls the latest).
- **Settings:** niche, audience, voice, topics, formats.
- **Publish to bot:** commits and pushes your queue and settings so the next scheduled run uses them.

## Customize
- **Niche, voice, topics, formats:** edit `config.json`.
- **Times:** edit the `cron` lines in `.github/workflows/post.yml` (UTC).
- **Model:** add a secret/variable `GEMINI_MODEL` if `gemini-2.5-flash` is retired.

## Test locally (optional)
```bash
pip install -r requirements.txt
cp .env.example .env   # fill in keys
DRY_RUN=1 python bot.py
```

## Notes
- `history.json` stores the last 60 posts so Gemini avoids repeating itself; the workflow commits it back.
- GitHub pauses scheduled workflows after 60 days with no repo activity; the history commits keep it active.
- 3 posts/day ≈ 90/month, within X's free-tier posting limit (check current limits at developer.x.com).
