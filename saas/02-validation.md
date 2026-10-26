# 2. Validation: prove people want it before building the SaaS

**Goal:** within 3 weeks, get evidence that solo builders will **pay** for X autopilot.
**Budget:** $0–20. **Rule:** no SaaS code until the "go" gate below is met.

## Go / no-go gate (end of week 3)
| Signal | Go | Rethink |
|---|---|---|
| Waitlist signups | ≥ 100 | < 30 |
| Landing page → signup rate | ≥ 10% | < 3% |
| Interviews where they describe the pain unprompted | ≥ 6 of 10 | < 3 of 10 |
| Founding-member pre-sales | ≥ 5 paid | 0 |

If you land in between, change the positioning or the niche (e.g. coaches instead of devs) and run 2 more weeks.

## Customer Interviews (week 1–2, aim for 10)
**Who:** people in the beachhead niche who posted ≥ 5 times last month, then went quiet; anyone tweeting "Hypefury alternative".
**Where:** DMs on X, Indie Hackers, r/SaaS, r/indiehackers, your own followers.

**DM opener:**
> Hey! I'm building a tool for builders who want to post daily on X but can't keep it up. Could I ask you 5 quick questions (10 min call or DM)? Not selling anything.

**Script.** Ask about the past, not the future; never pitch until the end.
1. How often did you post on X last month? What got in the way?
2. Tell me about the last time you tried to post consistently. What happened?
3. What have you tried: schedulers, ChatGPT, ghostwriter? What did you like or hate?
4. What do you pay for any of these today?
5. If posting happened without you, what would worry you? (quality? voice? ban?)
6. *(End)* Show the Studio demo. "Would you use this? What would make it a no-brainer?"

Log each interview in a row: name · niche · followers · pain (1–5) · current spend · objection · would pay (Y/N/$).

## Landing Page Test (week 1)
- Page: [`landing/index.html`](landing/index.html). One promise, a demo, pricing, and an email form.
- Host free: Cloudflare Pages or Netlify (drag the `landing` folder in). Waitlist form: free Formspree or Tally endpoint (paste its URL into the form `action`).
- Traffic (free): post the build-in-public story from your own bot account; Indie Hackers post; reply to "Hypefury alternative" threads with a genuine answer plus the link.
- Measure: visits (Cloudflare Web Analytics, free) vs. signups.

## Waitlist (week 1–3)
- Ask one qualifying question on signup: *"What's your niche?"* This becomes your niche-selection data.
- Email the list every week with progress (build in public), which keeps them warm for launch.

## Pre-Sales (week 2–3)
- **Founding member offer:** $5/month locked for life, limited to the first 50, charged at launch. Or $49 for the first year, paid now.
- Take payment with a Razorpay or Lemon Squeezy payment link (no code). Refund anyone who asks.
- A pre-sale is the only strong signal; signups and "I'd use it" are weak.

## Demand Testing (ongoing)
- **Smoke test the price:** show $9 vs $15 on the pricing section for alternate weeks; compare click-through on "Join".
- **Content test:** your own bot account is the case study. Track followers and impressions per week since autopilot started, and post the numbers.
- **Search test:** check monthly search volume for "Hypefury alternative", "auto tweet AI", "twitter autopilot" (free: Google Keyword Planner, Ubersuggest).
