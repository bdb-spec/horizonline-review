#!/usr/bin/env python3
"""Type-texture pass for the FERTILITY key art (Bennet's pick 2026-09-10 = option 07 "More speckle / fuzz / soft edge").
Renders key-fertility-art.html twice (everything-but-title, title-only on transparent), gives the TITLE the plate's
own speckle (high-pass of key-plate.jpg, k=0.9), a 1.3px softening and a 2.0px nibbled alpha edge, composites, and
writes web/key-fertility.jpg. Plate, rule and "Coming Soon" line are untouched.
Run from source/: python3 key-fertility-plate.py && python3 key-fertility-texture.py"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).resolve().parent
SPECKLE_K, FUZZ_PX, EDGE_PX, EDGE_CUT = 0.9, 1.3, 2.0, 40
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={"width": 1760, "height": 990}, device_scale_factor=1).new_page()
    pg.goto(f"file://{here}/key-fertility-art.html"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.querySelector('.title').style.visibility='hidden'"); pg.wait_for_timeout(120); pg.screenshot(path="/tmp/kf-A.png")
    pg.evaluate("()=>{document.querySelector('.title').style.visibility='visible'; for (const s of ['.plate','.vig','.rule','.sub']) document.querySelector(s).style.visibility='hidden'; document.body.style.background='transparent'; document.documentElement.style.background='transparent'}")
    pg.wait_for_timeout(150); pg.screenshot(path="/tmp/kf-B.png", omit_background=True); b.close()
A = Image.open("/tmp/kf-A.png").convert("RGB"); B = Image.open("/tmp/kf-B.png").convert("RGBA")
plate = Image.open(here / "key-plate.jpg").convert("L").resize(A.size, Image.LANCZOS)
hp = np.asarray(plate).astype(np.float32) - np.asarray(plate.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
amp = float(np.std(hp[np.asarray(plate) > 150]))
t = np.asarray(B).astype(np.float32)
m = np.clip(1 + SPECKLE_K * (hp / max(amp, 1e-6)) * 0.5, 0.35, 1.65); t[..., :3] = np.clip(t[..., :3] * m[..., None], 0, 255)
T = Image.fromarray(t.astype(np.uint8), "RGBA").filter(ImageFilter.GaussianBlur(FUZZ_PX))
t = np.asarray(T).astype(np.float32)
al = Image.fromarray(t[..., 3].astype(np.uint8)).filter(ImageFilter.GaussianBlur(EDGE_PX))
t[..., 3] = np.clip((np.asarray(al).astype(np.float32) - EDGE_CUT) * 1.35, 0, 255)
T = Image.fromarray(t.astype(np.uint8), "RGBA")
out = A.copy(); out.paste(T, (0, 0), T)
out.save(here / "web" / "key-fertility.jpg", "JPEG", quality=88, optimize=True, progressive=True)
print("wrote", here / "web" / "key-fertility.jpg", "speckle amp", round(amp, 1))
