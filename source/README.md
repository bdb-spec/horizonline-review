# Horizon Line — review site source

`index.html` (repo root) is the deployed, self-contained page (~2.3 MB, all images base64-inlined). Live at **https://horizonlinefilms.com** — Cloudflare Pages project `horizonline`, deployed with `wrangler` from this repo (since 2026-07-28; the old GitHub Pages URL is a legacy mirror, not the target). This repo is the single durable source of truth for the site; any agent can make changes from a fresh clone with nothing but this README.

## Edit loop
1. Edit `source/hlf-home.tmpl.html` (the ONLY file you hand-edit; it uses image tokens like `__KA_QUEEN__` — full token→file map lives in `source/build.py`).
2. `cd source && python3 build.py` → regenerates `../index.html` with images inlined.
3. Commit `index.html` + `source/hlf-home.tmpl.html` together (`SKIP_SECRET_GATE=1`, see Gotchas) and push, then deploy:
   `D=$(mktemp -d); cp index.html og-card.png favicon.png _redirects $D/ && cp -R fertility $D/; set -a; . ~/.claude/credentials.env; set +a; wrangler pages deploy $D --project-name horizonline --branch main --commit-dirty=true` (token is Pages-scoped; never `rm -rf` in the chain — the destructive-guard hook blocks the whole command).
4. Verify live with a cache-buster (`?v=<anything>`): Pages serves `max-age=600`, so a plain reload can show the stale build for up to 10 min.

### Gotchas (all learned the hard way)
- **Pre-commit secret-gate false-positive:** 16-digit runs inside the base64 image bytes look like card numbers. Before committing, verify zero card-shaped runs in VISIBLE text (`re.sub` the `data:image…base64,` blobs to `[IMG]`, then scan for `\d{13,19}`), then commit with `SKIP_SECRET_GATE=1 git commit …`. Expected on every image-heavy commit.
- **New key art:** put the jpg in `source/web/`, add a `__TOKEN__` entry to the map in `build.py`, reference the token in the template. If a card renders as a broken image, a token is missing from `build.py`'s map (this happened with Model Citizen).
- **Head block is load-bearing:** the doctype / `<html lang>` / charset / viewport / OG / favicon block at the top of the template keeps the page out of quirks mode, makes phones render the responsive layout, and gives link unfurls the brand card. Never strip it. `og:url`/`og:image` hardcode the Pages URL — update both when the site moves to horizonlinefilms.com.

## Hero animation — "sunrise" (architecture as of 2026-07-28, commit 3abc174)
The hero enacts a sunrise; every piece below was a deliberate Bennet decision — do not simplify away.

**Markup** (in the template):
`.lockup > h1.wordmark > [ .wm-l "Horiz" | .o-cell | .wm-l "n Line" ]`
`.o-cell > .o-port > .o-sun("o")` — the sun: gold-gradient glyph, permanently clipped by `.o-port` to show ONLY above the horizon (clip edge = 45% from bottom = the line's `top:55%`).
`.o-cell > .o-mirror > .o-flip > .o-refl("o")` — the reflection: absolute overlay, vertically mirrored about the horizon (`scaleY(-.94)`, origin `50% 55%`), dimmed/blurred, faded with depth by a `mask-image` gradient. `aria-hidden` so screen readers read one O.

**Timeline** (delays from load): `.o-sun` + `.o-refl` rise `translateY(.62em)→0` from **.3 s** over 1.7 s while brightening (`brightness .5→1` + growing drop-shadow) — the reflection runs the SAME `osun` keyframes inside the mirrored frame, so it stretches downward in sync with the sun's climb. Line (`.horizon-rule`) ignites at **.75 s** (as the tip crests) and spreads for 1.4 s FROM the sun: its `transform-origin` and gradient bright-peak both use `--sunx`, set at load by the small JS block at the end of the template (measures `.o-sun` center; falls back to `50%`/`50vw` if JS fails). Letters (`.wm-l`) never move — they resolve from dark warm silhouettes to full ivory (`wlit`: opacity + brightness/sepia ramp, .55–2.45 s) so the name reads as *lit into visibility by the rising sun*. Halo (`.o-sun::before`) blooms at 1.75 s; hero copy (`.hc-*`, `.hero-stats`) fades at 2.3 s; line glow settles at the end of its own keyframes. **There is no traveling glint — it was removed deliberately (no referent in the sunrise vocabulary); do not reintroduce it.**

**Reduced motion:** the `prefers-reduced-motion` block pins everything to the static end state. Any new animated element MUST get a line there.

**The mark:** the finished O = crisp gold dome above the line + soft reflection below. `favicon.png` and `og-card.png` (repo root) carry the same dome-and-reflection mark — regenerate both if the mark changes (favicon via PIL; OG card by rendering `source/og-card.html` — a 1200×630 lockup snapshot that mirrors the sun/rule CSS — with a headless browser at viewport 1200×630, DPR 1). Both regenerated warm 2026-09-10 when the sun went yellow-orange (`#ffe27a → #ffb42e → #f5841f`, glow `rgba(255,160,40)`); the brass line/nav did not change.

## Design system (do not drift)
- Palette/type via CSS vars in `:root` — warm near-black ground, ivory ink, brass accents; Iowan/Palatino serif display, system sans body, mono for metadata only. 3 families is the accepted ceiling.
- Slate/streaming art is **tonally leveled at idle** (`filter:saturate/brightness/sepia` on card imgs, full color on hover) — this is the prestige-grid move; don't remove it. The Raptus feature panel is the one full-color focal point per section.
- No-art slate titles live in the two-column `.slate-index` list (chronological), NOT empty tiles.
- Motion grammar: everything performs once and rests; nothing loops.
- `--ink-faint` is AA-tuned (#8a8375 ≈ 5.26:1 on the ground) — don't darken it back.
- Body copy uses typographic quotes/apostrophes (’ “ ”); keep it that way in new copy.

## /fertility — second page (added 2026-09-10)
- **Key art (2026-09-10, Bennet; v7 — APPROVED, git tag `keyart-v7-approved-2026-09-10`):** `web/key-fertility.jpg` = the ultrasound reference (header-cropped) with FERTILITY at 194px, .16em tracking, spanning ~78% of the frame in the dark band between the probe arc and the head (`top:23.5%`), gradient `#ffb43a → #ff7a28 → #e4471c → #c22a18` (orange-gold → deep red; Bennet: "more red is looking better"); plate `contrast(2.1) brightness(.84) saturate(.78)` plus a radial edge vignette (0.0% clipped white); a 62% brass horizon rule and a tracked mono "Coming Soon" line under the title. Source page `source/key-fertility-art.html` (render 1760×990, DPR 1, JPEG q88). Ships as `fertility/img/key-fertility-v7.jpg` — bump the suffix on every change so browser/edge caches (max-age 14400) miss. /design-review on the image: PASS (weakest gradient stop 3.3:1 vs its ground; one focal point).
- **Template:** `source/fertility.tmpl.html` (hand-edit, same tokens/nav/footer as the home template; nav links point back to `/#slate` and `/#work`). `python3 build.py` also emits `../fertility/index.html`.
- **Images are NOT inlined** on this page (mobile weight): they ship as files, `source/fertility-img/` → `fertility/img/`. `source/prep-fertility-img.py` regenerates `fertility-img/` from the deck assets in `~/Documents/FERTILITY/look-design/_deck-assets` (≤1400px, q78; crops the stock-watermark band off `leah-pregnant.jpg`) and copies the four posters + key art from `web/`. Run it only when a source image changes.
- **Deck:** the page text is the Aug-18 "A Bloodline" master's copy (Bennet confirmed 2026-09-10), ported verbatim. **The PDF is no longer shipped** (`build.py` deletes any `fertility/*.pdf`; `_redirects` sends the old PDF URL to `/fertility/`). Source copies stay in `source/fertility-pdf/`: `FERTILITY-DIRECTORS-VISION-redacted.pdf` (ultrasound header band on p.4 redacted — it carried a patient name/ID/timestamp) and Bennet's original `FERTILITY-DIRECTORS-VISION-2a041427-original.pdf`. `prep-fertility-img.py` never touches this folder. The web `ultrasound.jpg` is cropped 9% from the top by `prep-fertility-img.py` for the same reason. Never publish the header.
- **`_redirects`** (repo root, ships in the bundle): `/director /fertility 301` — the pitch package's old director link.
- **Public-page rules (Bennet, 2026-09-10):** public, no money facts — no budget, no "50% financed", no financing package, no acquisition-target list, no corporation numbers (Horizon Line is a banner; the producing entity is MERC_4 and belongs on paper, not the site). **And it is a coming-soon production page, NOT a pitch** (Bennet, same day: "we are in pre production this is not a pitch. Coming soon"): status "Coming Soon · In Pre-Production"; no script-request or meeting CTAs, no deck download, no "Let's talk" / "cast-ready" / "wide audience" language; contact = press@ + status + IMDb + company. The Director's Vision content stays as the film's look.
- **Open HITL (see the 2026-09-10 fertility design review):** the Leah reference is a watermarked stock comp (license or replace); reference photographs by living/estate photographers are now publicly hosted; nudity in the Woodman/Arbus references on the company domain; the slate card chip still says "Apr 2027".

## Review-gate state
**2026-09-10 pm (live re-gate, both pages)** — Stage-0 facts derived from the live DOM (canvas glyph-width measure per wrapping paragraph). Finding: `ch`-sized caps overrun — `ch` is the zero glyph (~0.62em in the system sans) while prose averages ~0.45em, so 58–62ch ≈ 80–84 characters per line. Fixed: home `.sec-head p` 46ch / `.mediakit p` 50ch / `.press-bg p` 50ch (live median 60, max 69); /fertility `--text` 48ch, logline 30em, film/quote/caption widths tied to `--text` (live median 67, max 71). Rule of thumb for this system: **target 66 characters ≈ 46–48ch.** Set-piece thumbnails at ≤600px are image-beside-caption. Both pages PASS.
**2026-09-10 evening** — /fertility reframed as a coming-soon production page (pitch CTAs and deck download removed; see /fertility rules above). RUN/LOCK moved from In Post-Production to Upcoming (slot 3 behind FERTILITY, chip "Coming Soon"); counts 7 / 17; FERTILITY chip "Apr 2027" → "Coming Soon", link line "About the Film →". Both grids now end in a one-card row (7 cards each) — a known orphan; fix if Bennet wants (feature cell, or a title to the index).
**2026-09-10 (/fertility)** `/design-review` Mode B on the new page: **PASS** after a mobile round (nav wrap, orphaned meta dots, ragged CTAs, 28ch film measure, image-before-heading on flipped blocks, watermark band). Stage-0 FLAGS only (3 faces, 6 levels, 41ch at 390). Artifact: `DESIGN-REVIEW-horizonline-fertility-page-2026-09-10.md` in the WEBSITE-REVIEW folder.
**2026-09-10** `/design-review` Mode B on the live public site after the warm-sun change: **REVISE → PASS (re-gated)**. Findings fixed: letterspaced lowercase (`.slate-count` → tracked caps, footer tracking 0), reduced-motion parity for the reflection glow, hero-stats separator hidden when the stats wrap (≤600px), favicon + OG card regenerated warm. Decision: the horizon rule stays brass — the sun's 26px orange glow already ties line and sun at the contact point; warming the rule would add a second focal point. Artifact: `DESIGN-REVIEW-horizonline-warm-sun-2026-09-10.md` in the WEBSITE-REVIEW folder below. Gotcha: headless Chrome enforces a ~500px minimum window, so `--window-size=390,…` lays out at 500 and crops — use Playwright for sub-500px renders.

### 2026-07-28
`/design-review` Mode B verdict: **PASS for internal-review circulation** (full artifact + QC screenshots: `~/Documents/HORIZON LINE FILM COMPANY/WEBSITE-REVIEW/` in the HOME machine filing, not this repo). Standing items before the site goes truly PUBLIC:
1. Strip the two `TK` tags (press contact + draft-headlines note).
2. Confirm rights to the 12 library streaming titles and announceability of slate cast attachments / press headlines (sourced from the Confidential Grosvenor Park slate).
3. Bennet to decide the contact closer: live says "Let's make them all."; the recorded alternative is "Let's make them great."
4. Domain separation not done: this design → horizonlinefilms.com, Warehouse site → whfdistribution.com.

Full session context: `HANDOFF-2026-07-28-horizon-line-website-mini-major-calling-card.md` and `HANDOFF-2026-07-28-horizon-sunrise-hero-review-baked.md` in the HOME repo `archive/handoffs/`.
