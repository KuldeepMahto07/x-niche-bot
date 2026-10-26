# 3. Planning: from personal bot to multi-user SaaS

> Start building only after the Validation go-gate passes ([02-validation.md](02-validation.md)).

## What exists today (personal version)
| Piece | Today | SaaS version needs |
|---|---|---|
| Post writer | `bot.py` + Gemini | Same logic, per-user config |
| Queue + Studio | Local Flask app, JSON files | Hosted web app, database |
| Scheduler | GitHub Actions cron (one account) | One worker posting for all users |
| X auth | Your own API keys | **"Sign in with X" (OAuth 2.0)**: users connect their account; we hold one developer app |
| Billing | — | Subscriptions |

## Feature Prioritization (RICE-lite: impact × confidence ÷ effort)
| Feature | Impact | Effort | Decision |
|---|---|---|---|
| Sign in with X + connect account | Must | M | MVP |
| Niche setup wizard (niche, audience, voice, topics) | Must | S | MVP |
| AI drafts + approval queue | Must | S (port Studio) | MVP |
| Autopilot schedule (3/day, pick times + timezone) | Must | M | MVP |
| Subscription billing (Free / Pro) | Must | M | MVP |
| Post history | High | S | MVP |
| Voice matching from user's last 50 posts | High | M | v1.1 (reads cost $0.005 each, so ~$0.25 one-off per user) |
| Email: "your queue is low" / weekly recap | Medium | S | v1.1 |
| Threads (multi-post) | Medium | M | v1.2 |
| Analytics (impressions per post) | Medium | M | v1.2, Creator plan |
| Multiple X accounts | Medium | M | v1.2, Creator plan |
| Replies / engagement | High | L, costly | Later, paid add-on |
| Image posts | Low | M | Later |

## MVP Scope (ship in 4 weeks, one developer)
**In:** Sign in with X · niche wizard · AI drafts · queue (edit, reorder, delete) · autopilot at 3 time slots · history · Free & Pro plans · basic landing + pricing page.
**Out (say no for now):** analytics, multi-account, threads, images, replies, teams, mobile app, other platforms.
**Definition of done:** 10 beta users posting on autopilot for 7 days with no missed slots, and at least 1 paid.

## Tech Stack (free tiers at the start, ~$0 until ~100 users)
| Layer | Choice | Why |
|---|---|---|
| Frontend + API | **Next.js (App Router) on Vercel** | One codebase, free hosting, huge ecosystem |
| Database + auth storage | **Supabase (Postgres)** | Free tier, row-level security, built-in cron (`pg_cron`) |
| X login + posting | **X OAuth 2.0 with PKCE**, scopes `tweet.read tweet.write users.read offline.access` | Users authorize their own account; refresh tokens let us post while they're away |
| Scheduler / worker | Supabase cron every 5 min → Next.js route `/api/cron/post` (Vercel Cron as backup) | No servers to run |
| AI writer | Gemini API (Flash), with the prompt ported from `bot.py` | Cheap, good quality, same prompt we've tested |
| Payments | **Lemon Squeezy** (handles global tax, works from India) or Razorpay for INR | Merchant of record = no VAT/GST headaches |
| Email | Resend (free 3k/month) | Transactional + weekly recap |
| Monitoring | Sentry (free) + Vercel logs | Catch failed posts fast |
| Analytics | PostHog (free 1M events) | Funnels and retention later |

**Security must-haves:** encrypt X refresh tokens at rest (Supabase Vault or AES with a server key), row-level security on every table, never log tokens, rate-limit draft generation per user.

## Data model (first cut)
```
users          id, email, x_user_id, x_handle, plan, timezone, created_at
x_tokens       user_id, access_token_enc, refresh_token_enc, expires_at
niche_settings user_id, niche, audience, voice, topics[], formats[]
slots          user_id, time_local ("09:00"), enabled
posts          id, user_id, text, topic, format, status (draft|queued|posted|failed),
               position, scheduled_for, posted_at, x_post_id, error
subscriptions  user_id, provider, provider_sub_id, status, current_period_end
```

## Product Roadmap
| When | Milestone |
|---|---|
| Weeks 1–3 | Validation: landing page, 10 interviews, waitlist, pre-sales |
| Weeks 4–7 | MVP build (plan below) |
| Week 8 | Private beta with 10–20 waitlist users (free) |
| Week 10 | Public launch: Product Hunt, Indie Hackers, X build-in-public thread |
| Month 3 | v1.1: voice matching, emails |
| Month 4–5 | v1.2: Creator plan (analytics, threads, multi-account) |
| Month 6 | Decide: agencies, Hindi/Hinglish creators, or more platforms |

## Development Plan (MVP, 4 weeks)
**Week 1: Foundation.** Next.js + Supabase project · Sign in with X (OAuth 2.0 PKCE) · store encrypted tokens · token refresh helper · deploy to Vercel.
**Week 2: Core.** Niche wizard · port `build_prompt`/`generate` to a TypeScript route · drafts + queue UI (port from Studio) · history page.
**Week 3: Autopilot.** Slots + timezone · cron worker: due users → next queued post, else generate → post → mark posted, retry/backoff, mark failed and email · daily cap per plan.
**Week 4: Money + polish.** Lemon Squeezy checkout + webhook → `plan` · plan limits · onboarding checklist · error monitoring · beta invite emails.

**Testing as we go:** unit tests for the prompt/length rules and plan limits; integration test for the cron worker with a mocked X client; one end-to-end test (sign up → wizard → queue → posted) before beta.
