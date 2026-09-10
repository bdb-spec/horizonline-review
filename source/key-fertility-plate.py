#!/usr/bin/env python3
"""Plate for the FERTILITY key art (Bennet's pick 2026-09-10 = 'Clarity / local contrast' highlight treatment).
Input : fertility-img/ultrasound.jpg (header-cropped ultrasound)   Output: key-plate.jpg (next to this script)
Recipe: large-radius unsharp mask (radius 32, 70%, threshold 2) for local contrast, then a highlight-only lift
(gamma 0.8 under a soft luminance mask 0.35..0.85). The dark band under the title is untouched.
Run from source/: python3 key-fertility-plate.py ; then render key-fertility-art.html (1760x990) -> web/key-fertility.jpg"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter
here = pathlib.Path(__file__).resolve().parent
src = Image.open(here / "fertility-img" / "ultrasound.jpg").convert("RGB")
cl = np.asarray(src.filter(ImageFilter.UnsharpMask(radius=32, percent=70, threshold=2))).astype(np.float32) / 255.0
lum = 0.2126 * cl[..., 0] + 0.7152 * cl[..., 1] + 0.0722 * cl[..., 2]
t = np.clip((lum - 0.35) / (0.85 - 0.35), 0, 1); hmask = (t * t * (3 - 2 * t))[..., None]
out = cl * (1 - hmask) + (cl ** 0.8) * hmask
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(here / "key-plate.jpg", "JPEG", quality=95)
print("wrote", here / "key-plate.jpg")
