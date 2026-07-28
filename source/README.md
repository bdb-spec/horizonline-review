# Horizon Line — review site source

`index.html` (repo root) is the deployed, self-contained page (GitHub Pages, branch main, ~1.8 MB, all images base64-inlined). Live at **https://bdb-spec.github.io/horizonline-review/** — the internal review link circulated to Bennet's team. This repo is the single durable source of truth for the site; any agent can make changes from a fresh clone with nothing but this README.

## Edit loop
1. Edit `source/hlf-home.tmpl.html` (the ONLY file you hand-edit; it uses image tokens like `__KA_QUEEN__` — full token→file map lives in `source/build.py`).
2. `cd source && python3 build.py` → regenerates `../index.html` with images inlined.
3. Commit `index.html` + `source/hlf-home.tmpl.html` together and push → Pages redeploys the same URL in ~45–75 s.
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

**The mark:** the finished O = crisp gold dome above the line + soft reflection below. `favicon.png` and `og-card.png` (repo root) carry the same dome-and-reflection mark — regenerate both if the mark changes (favicon via PIL; OG card by rendering a 1200×630 lockup snapshot).

## Design system (do not drift)
- Palette/type via CSS vars in `:root` — warm near-black ground, ivory ink, brass accents; Iowan/Palatino serif display, system sans body, mono for metadata only. 3 families is the accepted ceiling.
- Slate/streaming art is **tonally leveled at idle** (`filter:saturate/brightness/sepia` on card imgs, full color on hover) — this is the prestige-grid move; don't remove it. The Raptus feature panel is the one full-color focal point per section.
- No-art slate titles live in the two-column `.slate-index` list (chronological), NOT empty tiles.
- Motion grammar: everything performs once and rests; nothing loops.
- `--ink-faint` is AA-tuned (#8a8375 ≈ 5.26:1 on the ground) — don't darken it back.
- Body copy uses typographic quotes/apostrophes (’ “ ”); keep it that way in new copy.

## Review-gate state (2026-07-28)
`/design-review` Mode B verdict: **PASS for internal-review circulation** (full artifact + QC screenshots: `~/Documents/HORIZON LINE FILM COMPANY/WEBSITE-REVIEW/` in the HOME machine filing, not this repo). Standing items before the site goes truly PUBLIC:
1. Strip the two `TK` tags (press contact + draft-headlines note).
2. Confirm rights to the 12 library streaming titles and announceability of slate cast attachments / press headlines (sourced from the Confidential Grosvenor Park slate).
3. Bennet to decide the contact closer: live says "Let's make them all."; the recorded alternative is "Let's make them great."
4. Domain separation not done: this design → horizonlinefilms.com, Warehouse site → whfdistribution.com.

Full session context: `HANDOFF-2026-07-28-horizon-line-website-mini-major-calling-card.md` and `HANDOFF-2026-07-28-horizon-sunrise-hero-review-baked.md` in the HOME repo `archive/handoffs/`.
