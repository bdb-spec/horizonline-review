#!/usr/bin/env python3
"""Emit ../director/index.html: the Director page, assembled from fertility.tmpl.html (same head styles, nav, the
Bennet-edited director section, contact, footer). Images are referenced from /fertility/img/ so nothing is duplicated.
Run from source/: python3 build_director.py  (build.py calls this too). Bennet 2026-10-24: 'create a deploy' for a director page link."""
import re, pathlib
here = pathlib.Path(__file__).resolve().parent
t = (here / "fertility.tmpl.html").read_text()
def between(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b); return s[i:j]
style   = between(t, "<style>", "</style>")
nav     = between(t, "<nav>", "</nav>")
director= between(t, '<section id="director" class="director">', "</section>")
footer  = between(t, "<footer>", "</footer>")
script  = t[t.index("<script>"):]
# nav: on this page "Director" points at the page itself; add the FERTILITY link
nav = nav.replace('<a href="#director">Director</a>', '<a href="/fertility/">Fertility</a>').replace('<a href="#contact">Contact</a>', '<a href="#films" class="here">Director</a>\n      <a href="#contact">Contact</a>')
# director section: images live under /fertility/img/; the section head doubles as the page's own head, so the eyebrow reads as a page
director = director.replace('src="img/', 'src="/fertility/img/')
director = director.replace('<section id="director" class="director">', '<section id="films" class="director">')
director = director.replace('<p class="eyebrow">The Director · Writer / Director</p>\n      <h2>Bennet De Brabandere</h2>\n      <p>Four films. A genre all their own. FERTILITY is the fifth.</p>',
                            '<p class="eyebrow">Writer / Director · Toronto</p>\n      <h2>Bennet De Brabandere</h2>\n      <p>Four films. A genre all their own. <a href="/fertility/" style="color:var(--brass)">FERTILITY</a> is the fifth.</p>')
assert director.count('/fertility/img/') >= 4, "poster paths not rewritten"
head = f'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bennet De Brabandere, Director · Horizon Line Film Company</title>
<meta name="description" content="Bennet De Brabandere, writer and director: Raptus (Apple TV, Amazon Prime), The Christmas Spirit, Cherrypicker, Salvation. FERTILITY is next.">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://horizonlinefilms.com/director/">
<link rel="canonical" href="https://horizonlinefilms.com/director/">
<meta property="og:title" content="Bennet De Brabandere, Director · Horizon Line Film Company">
<meta property="og:description" content="Four films. A genre all their own. Raptus on Apple TV and Amazon Prime, noticed by The New York Times. FERTILITY is next.">
<meta property="og:image" content="https://horizonlinefilms.com/fertility/img/og-fertility-v11.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0a09">
<link rel="icon" type="image/png" href="/favicon.png">
{style}
'''
page = head + "\n" + nav + '''

<div style="height:calc(64px + 3vw)"></div>
''' + director + '''

<!-- CONTACT -->
<section id="contact" class="contact">
  <div class="wrap contact-in">
    <div class="fade">
      <p class="eyebrow">Contact</p>
      <h2 style="margin-top:14px">Bennet De Brabandere</h2>
      <a class="email" href="mailto:press@horizonlinefilms.com?subject=Bennet%20De%20Brabandere">press@horizonlinefilms.com</a>
    </div>
    <div class="contact-cols fade">
      <div class="row"><span class="l">Next</span><span class="v"><a href="/fertility/">FERTILITY</a> · In pre-production</span></div>
      <div class="row"><span class="l">Director</span><span class="v"><a href="https://www.imdb.com/name/nm3185193/" target="_blank" rel="noopener">IMDb</a></span></div>
      <div class="row"><span class="l">Company</span><span class="v"><a href="/">Horizon Line Film Company</a> · Toronto, Canada</span></div>
    </div>
  </div>
</section>

<div class="horizon-echo" aria-hidden="true"></div>
''' + footer + "\n\n" + script
out = here.parent / "director"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(page)
print("wrote", out / "index.html", len(page), "bytes")
