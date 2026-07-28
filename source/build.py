#!/usr/bin/env python3
"""Regenerate ../index.html from hlf-home.tmpl.html, inlining web/*.jpg as base64 data URIs.
Usage: python3 build.py   (run from the source/ dir). Then commit index.html and push -> GitHub Pages."""
import base64, pathlib
here = pathlib.Path(__file__).resolve().parent
web = here / "web"
t = (here / "hlf-home.tmpl.html").read_text()
M = {
 "__P_RAPTUS__":"poster-raptus.jpg","__P_TCS__":"poster-tcs.jpg","__P_CHERRY__":"poster-cherrypicker.jpg","__P_SALV__":"poster-salvation.jpg",
 "__KA_JOURNEY__":"key-journey.jpg","__KA_RUNLOCK__":"key-runlock.jpg","__KA_PRAY__":"key-pray.jpg","__KA_ACTRESS__":"key-actress.jpg",
 "__KA_NFL__":"key-nfl.jpg","__KA_TOFREEDOM__":"key-tofreedom.jpg","__KA_CHANG__":"key-chang.jpg","__KA_KINGSORROW__":"key-kingsorrow.jpg",
 "__KA_QUEEN__":"key-queen.jpg","__KA_FERTILITY__":"key-fertility.jpg","__KA_MODELCITIZEN__":"key-modelcitizen.jpg",
 "__LIB_DEATHWISH__":"lib-deathwish.jpg","__LIB_SKISCHOOL__":"lib-skischool.jpg","__LIB_LASTRESORT__":"lib-lastresort.jpg",
 "__LIB_BREAKOUT__":"lib-breakout.jpg","__LIB_DARKTRUTH__":"lib-darktruth.jpg","__LIB_FIGHTINGMAN__":"lib-fightingman.jpg",
 "__LIB_COMEBACK__":"lib-comeback.jpg","__LIB_BIGWEDDING__":"lib-bigwedding.jpg","__LIB_MYMOM__":"lib-mymom.jpg",
 "__LIB_CLEANER__":"lib-cleaner.jpg","__LIB_BLONDE__":"lib-blonde.jpg","__LIB_POISONROSE__":"lib-poisonrose.jpg","__LIB_HEARTSOFWAR__":"lib-heartsofwar.jpg",
}
for k, f in M.items():
    t = t.replace(k, "data:image/jpeg;base64," + base64.b64encode((web / f).read_bytes()).decode())
out = here.parent / "index.html"
out.write_text(t)
print("wrote", out, out.stat().st_size // 1024, "KB")
