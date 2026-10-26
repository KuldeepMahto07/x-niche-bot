# 1. Idea — X Studio as a SaaS

> Research date: 2026-10-26. Prices come from third-party roundups; re-check official pages before quoting them publicly.

## Problem Discovery
**The problem:** Growing on X needs consistent posting (2–5 posts/day) in one niche. Most solo creators, indie hackers and small founders can't keep that up: they run out of ideas, post in bursts, then go silent for weeks.

What they do today:
| Workaround | Why it fails |
|---|---|
| Write and post manually | Takes 30–60 min/day; stops when life gets busy |
| Schedulers (Typefully, Buffer) | Still need *you* to write every post |
| ChatGPT + copy/paste | Generic voice, manual, no schedule |
| Ghostwriters | $500–2,000/month |
| Growth tools (Tweet Hunter) | $29–49/month, built for power users, heavy |

**Problem statement:** *"I know I should post every day in my niche, but I don't have the time or ideas to keep it up."*

## Market Research
- **Platform shift (2026):** X moved its API to pay-per-use on 2026-02-06. Posting costs **$0.015/post** ($0.20 if it contains a link). Old Free/Basic tiers are closed to new developers. A post-only product is now cheap to run: 90 posts/month ≈ **$1.35** in API cost.
- **Supply shrinking:** Hypefury dropped X support (Aug 2026), so its X users need a new home. Every API price change has pushed smaller tools off X, so there's less competition at the low end.
- **Demand signals to check during Validation:** search interest in "Hypefury alternative", "Tweet Hunter alternative", "auto post to X with AI"; threads in r/SaaS, r/Twitter, Indie Hackers.

## Niche Selection
Start narrow, expand later.

**Beachhead customer:** solo builders (indie hackers, developers, AI/tech creators) with 100–5,000 followers who want to grow on X but don't post consistently.
- They already believe in "build in public" and know X matters.
- Price sensitive: $29–49 tools feel expensive at this stage.
- Easy to reach: they hang out on X, Indie Hackers, Reddit, Product Hunt.
- We are the user: the founder runs an AI & tech account with this exact tool.

Later niches: coaches/consultants, local agencies managing several client accounts, non-English creators (Hindi/Hinglish).

## Competitor Analysis
| Tool | Price (approx.) | Writes for you? | Posts on autopilot? | Notes |
|---|---|---|---|---|
| Tweet Hunter | $29 / $49 / ~$200 mo | Yes (Grow plan) | Partly (auto-retweet, plugs) | Power-user growth suite; pricey |
| Typefully | Free (10 posts) / ~$99 yr | AI assist | No: you write and schedule | Best-in-class editor, no autopilot |
| Hypefury | — | — | — | **Dropped X in Aug 2026** |
| Postiz (open source) | Free self-host / paid cloud | AI assist | No | Multi-platform scheduler |
| Buffer | Free / paid per channel | Light AI | No | Generic social scheduler |
| ChatGPT/Claude + manual | ~$20 mo | Yes | No | No schedule, no memory of past posts |

**Gap:** nobody owns *"set your niche once, approve or ignore, it posts every day"* at a solo-builder price.

## Opportunity Mapping
**Positioning:** *Autopilot for your X niche. Tell it your niche once, and it writes and posts 3 times a day in your voice. Review the queue whenever you want, or don't.*

| Opportunity | Size of pain | Our edge | Priority |
|---|---|---|---|
| Autopilot posting in a niche | High | Already built (bot + queue + Studio) | **Now** |
| Hypefury refugees | Medium, time-limited | Migration landing page + import | **Now** |
| Voice matching from past posts | High | Feed last 50 posts to the prompt | Next |
| Multi-account for agencies | Medium | Same engine, more seats | Later |
| Hindi/Hinglish creators | Medium, underserved | Gemini handles it well | Later |
| Replies and engagement | High | Costly API reads ($0.005/read) | Later, paid add-on |

**Unit economics (Pro plan, 3 posts/day):** X API ≈ $1.35 + Gemini ≈ $0.10 (free tier at small scale) + hosting ≈ $0.20 → **≈ $1.65/user/month**. At $9/month that's about an 80% gross margin before payment fees.

**Risks**
1. X changes API prices again → keep posting cost per user visible in the admin dashboard; pass link-post costs to users.
2. X policy on automated accounts → posts are original, ≤ 3–5/day, user-approved option; no follows, likes or DMs.
3. AI content quality → approval queue plus a voice-matching feature; weekly "best posts" review.
