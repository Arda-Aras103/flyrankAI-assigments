# Three Roads: Choose Your Stack

## Constraints I gave (and still hold)

- **Free only.** No paid host, no paid CMS.
- **Skill level.** Comfortable with Git, Markdown, a little Hugo. Learning frontend; not a designer. Stronger in Go/Python than in JS frameworks.
- **What the site must do.** Home claim, three project cases (gitviz, Project Euler, Task API), About, Contact. Each case is short text + real screenshots + repo link. One action: email for the CV.
- **How work must be shown.** Real terminal/Swagger captures, not AI mockups. Code lives on GitHub. No image gallery product, no embedded live demo, no long-form blog as the main proof.
- **Dynamic yet?** No. No auth, no CMS, no server-rendered app. Static is enough.

## Three options (simplest → most powerful)

### 1. Plain HTML + CSS on GitHub Pages

- **Build:** Hand-written pages, one CSS file from the identity kit.
- **Host:** GitHub Pages (user site).
- **Backend:** No.
- **Trade-off:** Fastest to ship and easiest to maintain. No build step. Weakest structure when pages grow; easy to copy-paste drift.

### 2. Astro (static) on GitHub Pages

- **Build:** Components/layouts, Markdown or `.astro` pages, one shared layout for fonts/colors.
- **Host:** GitHub Pages via GitHub Actions (`npm run build` → `dist`).
- **Backend:** No.
- **Trade-off:** Still static and free. Identity kit stays in one layout. Slightly more to learn and a CI build that can fail. Strong fit for text + images + links.

### 3. Next.js on Vercel

- **Build:** React app, routing, optional API routes later.
- **Host:** Vercel free tier.
- **Backend:** Not required for a portfolio, but the stack invites “just add an API.”
- **Trade-off:** Most powerful and most to maintain. Overkill for three case pages. JS surface area is larger than the proof I need to show.

## Pressure-test

- **If I pick the simplest (plain HTML):** I can finish this week. Risk: pages diverge from the identity kit; no shared layout discipline.
- **If I pick the most powerful (Next.js):** I can show the work, but I maintain a React app and a second platform (Vercel) for a site that does not need interactivity. Two-week finish is possible; long-term cost is higher than the benefit.
- **Can I finish in two weeks?** Yes for 1 or 2. 3 is a time tax I do not need.
- **Does it show the work?** All three can. The work is repos + screenshots. None of them need a backend to prove gitviz or the Task API.

## Decision

**Chosen: Astro + GitHub Pages.**

I did not pick plain HTML because I already want one layout and one CSS token set (Plex, cream, one green) on every page without copy-paste. I did not pick Next.js because nothing on the sitemap is dynamic yet, and a React host is more to keep alive than three static cases justify.

**Can I maintain this?** Yes. One repo, free Actions build, no database, no CMS. When a case changes, I edit a page and push.

**Does it show my work well?** Yes. Cases are text + real PNGs + GitHub links. Astro does not upstage that. Backend stays “not yet.”
