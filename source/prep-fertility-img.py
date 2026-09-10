#!/usr/bin/env python3
"""One-off: pull the FERTILITY page images into source/fertility-img/ (resized for web) and the deck PDF into source/fertility-pdf/.
Sources: the Director's Vision deck assets (Documents/FERTILITY/look-design/_deck-assets) + this repo's web/ posters and key art.
Run from source/: python3 prep-fertility-img.py   (only needed when a source image changes; build.py copies from fertility-img/)."""
import pathlib, shutil
from PIL import Image, ImageOps
here = pathlib.Path(__file__).resolve().parent
deck = pathlib.Path.home() / "Documents/FERTILITY/look-design/_deck-assets"
out = here / "fertility-img"; out.mkdir(exist_ok=True)
DECK = ["scan-pregnant-crewdson","caravaggio-judith","dr-red-theatre","ultrasound","crewdson-beneath-roses","crewdson-cathedral-pines-1",
        "polaroid-geno","woodman-roma","scan-roman-stewart","shauna","leah-pregnant","scan-surrogate-henson","scan-chani-showgirl",
        "golden-helmet","madonna-litta","burning-house"]
for n in DECK:
    im = ImageOps.exif_transpose(Image.open(deck / f"{n}.jpg")).convert("RGB")
    if n == "leah-pregnant":  # stock-agency watermark runs down the left edge; crop it out of the web copy
        w, h = im.size; im = im.crop((int(w * 0.14), 0, w, h))
    im.thumbnail((1400, 1400), Image.LANCZOS)
    im.save(out / f"{n}.jpg", "JPEG", quality=78, optimize=True, progressive=True)
for n in ["key-fertility","poster-raptus","poster-tcs","poster-cherrypicker","poster-salvation"]:
    shutil.copy2(here / "web" / f"{n}.jpg", out / f"{n}.jpg")
src_pdf = pathlib.Path.home() / "Documents/FERTILITY/FERTILITY-DIRECTORS-VISION.pdf"
shutil.copy2(src_pdf, here / "fertility-pdf" / "FERTILITY-DIRECTORS-VISION.pdf")
tot = sum(p.stat().st_size for p in out.glob("*.jpg"))
print(f"{len(list(out.glob('*.jpg')))} images, {tot//1024} KB total; deck pdf copied")
