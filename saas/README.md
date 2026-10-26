# X Studio → SaaS

Product: **autopilot for your X niche.** Set your niche once; it writes and posts 3 times a day in your voice, with an approval queue.

| Stage | Status | Doc |
|---|---|---|
| 1. Idea: problem, market, niche, competitors, opportunity | ✅ Done | [01-idea.md](01-idea.md) |
| 2. Validation: interviews, landing page, waitlist, pre-sales, demand | 🟡 Plan + landing page ready; **you run it** | [02-validation.md](02-validation.md), [landing/](landing/index.html) |
| 3. Planning: roadmap, prioritization, MVP, stack, dev plan | ✅ Done | [03-planning.md](03-planning.md) |
| 4. Design: wireframes, UI, UX flows, prototype, design system | ⏳ Next; Studio UI is the starting prototype | |
| 5. Development: frontend, backend, APIs, DB, auth, integrations | ⏳ After validation gate passes | |
| 6. Infrastructure: hosting, CI/CD, monitoring, security | ⏳ | |
| 7. Testing: unit, integration, bugs, performance, beta | ⏳ | |
| 8. Launch: landing, Product Hunt, beta users, early adopters | ⏳ | |
| 9–16. Acquisition → Scaling | ⏳ After launch | |

## Key numbers
- X API: **$0.015 per post**, $0.20 with a link (pay-per-use since Feb 2026)
- Cost to serve a Pro user (90 posts/mo): **≈ $1.65/month**
- Price: Free · **Pro $9/mo** · Creator $19/mo → ~80% gross margin
- Validation go-gate: 100 waitlist · ≥10% signup rate · 6/10 interviews feel the pain · 5 pre-sales

## This week (your to-do)
1. ✅ Landing page live: https://kuldeepmahto07.github.io/x-studio-landing/ (GitHub Pages, public repo `x-studio-landing`).
   Edit `landing/index.html` here, commit, then redeploy with: `git subtree push --prefix saas/landing landing main`
2. ✅ Waitlist connected to the Google Form (name, email, how they heard). Responses land in the linked Google Sheet.
   To collect niche too: add a short-answer "Niche" question, put its entry ID in `GOOGLE_FORM.entries.niche`, redeploy.
3. Turn on your own bot so your account becomes the live case study.
4. Send 20 interview DMs using the script in [02-validation.md](02-validation.md).
