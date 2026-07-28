# Horizon Line — review site source

`index.html` (repo root) is the deployed, self-contained page (GitHub Pages, branch main).

To edit:
1. Edit `source/hlf-home.tmpl.html` (uses image tokens like `__KA_QUEEN__`).
2. `cd source && python3 build.py`  → regenerates `../index.html` with images inlined as base64.
3. `git add index.html && git commit && git push`  → Pages rebuilds at https://bdb-spec.github.io/horizonline-review/ in ~1 min.

Images live in `source/web/`. See HANDOFF-2026-07-28-horizon-line-website-mini-major-calling-card.md in the HOME repo for full context.
