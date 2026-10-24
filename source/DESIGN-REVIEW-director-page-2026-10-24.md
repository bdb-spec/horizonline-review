# Design Review — /director/ page, horizonlinefilms.com (2026-10-24)
**Destination:** public web page linked from the Telefilm meeting request and future outreach. **Mode B (layout).** **Verdict: PASS.**

Artifact: `director/index.html` assembled by `source/build_director.py` from `fertility.tmpl.html` (same head, styles, nav and footer; the Bennet-edited director section of the FERTILITY page, posters served from `/fertility/img/`). Rendered at 1280 and 390 wide (`~/.playwright-mcp/director-desktop.png`, `director-mobile.png`) with every fade block revealed.

## Stage 0 — design-verify.py (kind:layout)
Facts measured in the DOM: film-body paragraph 484 px at 16 px system sans on desktop (about 65 characters), 347 px at 390 wide (about 46); three type families by design (Iowan serif for display and quotes, system sans for body, mono for eyebrows), four hierarchy levels, leading 1.6, no element off the two-column grid, no horizontal overflow at either width, one focal point (the name). Verdict PASS, no findings.

## Stage 1 — Composition
- [OK] Gestalt: poster + text pair per film by proximity; the eyebrow/name/line header is the single figure at the top; quotes are set apart by indent and italic, not boxes.
- [OK] Grid: the site's two-column film grid collapses to one column on the phone; the contact block keeps its two columns at desktop and stacks at 390.
- [OK] Typography: measure inside 45-75 on desktop; the mono eyebrows are tracked caps, not letterspaced lowercase; hierarchy unchanged from the live FERTILITY page that already passed this gate on 2026-09-10.

## Stage 2 — Tufte, general
- [OK] Layering and separation by weight and colour (brass eyebrows, ink body, faint cites); no chartjunk; the page carries only what the Telefilm track-record criterion asks for: titles, years, credits, platforms, quotes with sources.

## Content
- Copy is the Bennet-edited director section as live on /fertility/ since 2026-09-10; nothing new was written. Bio names no company other than Horizon Line; no Noble House.
- `_redirects` no longer sends `/director` to `/fertility`; Cloudflare's trailing-slash redirect serves `/director/`.
