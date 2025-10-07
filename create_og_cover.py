#!/usr/bin/env python3
"""
Create Open Graph cover from hero image.
Takes images/original/hero-nose-cleaner.png, center-crops to 1200x630 (16:9),
exports images/original/og-cover.png and images/webp/og-cover.webp.
"""
from PIL import Image
import os

BASE_DIR = os.path.dirname(__file__)
ORIG_DIR = os.path.join(BASE_DIR, 'images', 'original')
WEBP_DIR = os.path.join(BASE_DIR, 'images', 'webp')

def ensure_dirs():
    os.makedirs(ORIG_DIR, exist_ok=True)
    os.makedirs(WEBP_DIR, exist_ok=True)

def make_og_from_hero():
    hero_path = os.path.join(ORIG_DIR, 'hero-nose-cleaner.png')
    og_png = os.path.join(ORIG_DIR, 'og-cover.png')
    og_webp = os.path.join(WEBP_DIR, 'og-cover.webp')

    if not os.path.exists(hero_path):
        print('ERROR: images/original/hero-nose-cleaner.png not found.')
        return 1

    img = Image.open(hero_path).convert('RGB')
    target_w, target_h = 1200, 630  # 16:9
    sw, sh = img.size
    tr = target_w / target_h
    sr = sw / sh
    if sr > tr:
        # wider: crop width
        new_w = int(sh * tr)
        left = (sw - new_w) // 2
        box = (left, 0, left + new_w, sh)
    else:
        # taller: crop height
        new_h = int(sw / tr)
        top = (sh - new_h) // 2
        box = (0, top, sw, top + new_h)
    img = img.crop(box).resize((target_w, target_h), Image.Resampling.LANCZOS)
    img.save(og_png, 'PNG', optimize=True)
    img.save(og_webp, 'WEBP', quality=90, optimize=True)
    print('Created:', og_png)
    print('Created:', og_webp)
    return 0

if __name__ == '__main__':
    ensure_dirs()
    raise SystemExit(make_og_from_hero())


