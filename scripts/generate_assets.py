#!/usr/bin/env python3
"""
Generator aset orisinal untuk aplikasi "Doa Anak - Hafalan Doa Harian".

Semua gambar dibuat dari nol dengan bentuk-bentuk vektor sederhana (Pillow),
tanpa mengambil/menyalin artwork pihak lain, sehingga bebas masalah copyright.

Pemakaian:
    python3 scripts/generate_assets.py

Output:
    assets/doa/<id>.png   -> ilustrasi 1280x720 untuk tiap kartu doa
    assets/header.png     -> banner beranda
    assets/icon.png, assets/android-icon-*.png, assets/favicon.png,
    assets/splash-icon.png
"""

import math
import os
import random

from PIL import Image, ImageChops, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOA_DIR = os.path.join(ROOT, "assets", "doa")
ASSET_DIR = os.path.join(ROOT, "assets")

W, H = 1280, 720

random.seed(42)


# --------------------------------------------------------------------------
# helpers dasar
# --------------------------------------------------------------------------

def hx(s: str):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gradient(size, top, bottom):
    w, h = size
    top, bottom = hx(top) if isinstance(top, str) else top, \
        hx(bottom) if isinstance(bottom, str) else bottom
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def new_scene(top, bottom):
    img = gradient((W, H), top, bottom)
    return img, ImageDraw.Draw(img)


def circle(d, cx, cy, r, fill, outline=None, width=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=outline, width=width)


def star(d, cx, cy, r, fill, points=5, inner=0.45, rot=-90):
    pts = []
    for i in range(points * 2):
        ang = math.radians(rot + i * 180 / points)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def crescent(img, cx, cy, r, color, cut=0.42, cut_r=0.82):
    """Bulan sabit aman dipakai di atas gradien (lewat mask)."""
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    r2 = r * cut_r
    md.ellipse([cx - r2 + cut * r, cy - r2, cx + r2 + cut * r, cy + r2], fill=0)
    img.paste(Image.new("RGB", img.size, hx(color)), (0, 0), mask)


def cloud(d, cx, cy, s, color):
    d.rounded_rectangle([cx - s * 1.25, cy, cx + s * 1.25, cy + s * 0.55],
                        radius=s * 0.3, fill=color)
    circle(d, cx, cy - s * 0.05, s * 0.62, color)
    circle(d, cx - s * 0.75, cy + s * 0.1, s * 0.45, color)
    circle(d, cx + s * 0.75, cy + s * 0.1, s * 0.45, color)


def sun(d, cx, cy, r, core="#FFD54F", ray="#FFE082", rays=12):
    for i in range(rays):
        a = math.radians(i * 360 / rays)
        x1 = cx + math.cos(a) * r * 1.25
        y1 = cy + math.sin(a) * r * 1.25
        x2 = cx + math.cos(a) * r * 1.65
        y2 = cy + math.sin(a) * r * 1.65
        d.line([(x1, y1), (x2, y2)], fill=ray, width=max(3, int(r * 0.18)))
    circle(d, cx, cy, r, core)


def starfield(d, n=26, color="#FFE082", ymax=None, xmin=40, xmax=None):
    xmax = xmax or (W - 40)
    ymax = ymax or int(H * 0.55)
    for _ in range(n):
        x = random.randint(xmin, xmax)
        y = random.randint(30, ymax)
        r = random.choice([4, 5, 6, 8, 10])
        star(d, x, y, r, color)


def hills(d, y, color, bumps=((-150, 620), (520, 760), (1020, 640))):
    for x, r in bumps:
        d.ellipse([x - r, y - r * 0.55, x + r, y + r * 1.4], fill=color)


def ground(img, d, y, color):
    d.rectangle([0, y, W, H], fill=color)


def flowers(d, ys, color="#F48FB1", leaf="#66BB6A"):
    for x, y in ys:
        d.line([(x, y), (x, y + 26)], fill=leaf, width=5)
        for dx, dy in ((-11, -6), (11, -6), (0, -16), (-7, 4), (7, 4)):
            circle(d, x + dx, y + dy, 8, color)
        circle(d, x, y - 4, 6, "#FFD54F")


def arch(d, x1, y1, x2, y2, fill):
    r = (x2 - x1) / 2
    d.pieslice([x1, y1, x2, y1 + 2 * r], 180, 360, fill=fill)
    d.rectangle([x1, y1 + r, x2, y2], fill=fill)


def tiles(d, x1, y1, x2, y2, c1, c2, n=8):
    tw = (x2 - x1) / n
    th = tw * 0.72
    r = 0
    y = y1
    while y < y2:
        c = 0
        x = x1
        while x < x2:
            col = c1 if (r + c) % 2 == 0 else c2
            d.rectangle([x, y, min(x + tw, x2), min(y + th, y2)], fill=col)
            x += tw
            c += 1
        y += th
        r += 1


def drop(d, cx, cy, r, color):
    d.polygon([(cx, cy - r * 1.7), (cx - r * 0.95, cy + r * 0.25),
               (cx + r * 0.95, cy + r * 0.25)], fill=color)
    circle(d, cx, cy, r, color)


def line(d, p1, p2, fill, width):
    d.line([p1, p2], fill=fill, width=width)


# --------------------------------------------------------------------------
# karakter anak (chibi, dr wajah sederhana)
# --------------------------------------------------------------------------

def kid(d, cx, base_y, s, shirt="#42A5F5", pants="#37474F", skin="#FFCC80",
        hair="#4E342E", hijab=None, pose="pray", backpack=None,
        eyes="open", face_dir=1):
    """Anak chibi: base_y = garis kaki, s = tinggi total."""
    hr = s * 0.17                      # radius kepala
    hcy = base_y - s + hr              # pusat kepala
    b_top = hcy + hr + s * 0.015
    b_bot = base_y - s * 0.30
    bw = s * 0.30                      # lebar badan
    leg_w = max(6, int(s * 0.085))

    # ransel (di belakang badan)
    if backpack:
        d.rounded_rectangle(
            [cx - bw * 0.62, b_top - s * 0.02, cx + bw * 0.62, b_bot - s * 0.02],
            radius=s * 0.05, fill=backpack)

    # kaki
    if pose == "walk":
        hip_y = b_bot
        foot_y = base_y
        line(d, (cx - bw * 0.2, hip_y), (cx - bw * 0.55, foot_y - s * 0.03),
             pants, leg_w)
        line(d, (cx + bw * 0.2, hip_y), (cx + bw * 0.5, foot_y),
             pants, leg_w)
        circle(d, cx - bw * 0.62, foot_y - s * 0.01, leg_w * 0.75, "#37474F")
        circle(d, cx + bw * 0.55, foot_y - s * 0.01, leg_w * 0.75, "#37474F")
    else:
        for off in (-bw * 0.26, bw * 0.26):
            d.rounded_rectangle(
                [cx + off - leg_w / 2, b_bot - s * 0.02,
                 cx + off + leg_w / 2, base_y - s * 0.03],
                radius=leg_w / 2, fill=pants)
            d.rounded_rectangle(
                [cx + off - leg_w * 0.75, base_y - s * 0.055,
                 cx + off + leg_w * 0.9, base_y],
                radius=leg_w * 0.4, fill="#263238")

    # badan
    d.rounded_rectangle(
        [cx - bw / 2, b_top, cx + bw / 2, b_bot],
        radius=bw * 0.34, fill=shirt)

    # lengan
    arm_w = max(6, int(s * 0.075))
    sh_y = b_top + s * 0.05
    if pose == "pray":
        # lengan dengan siku di luar siluet badan supaya terlihat jelas
        for sgn in (-1, 1):
            sh = (cx + sgn * bw * 0.46, sh_y)
            el = (cx + sgn * bw * 0.9, sh_y + s * 0.17)
            hd = (cx + sgn * bw * 0.2, b_top + s * 0.24)
            line(d, sh, el, shirt, arm_w)
            line(d, el, hd, shirt, arm_w)
        circle(d, cx - bw * 0.15, b_top + s * 0.25, s * 0.04, skin)
        circle(d, cx + bw * 0.15, b_top + s * 0.25, s * 0.04, skin)
    elif pose == "walk":
        line(d, (cx - bw * 0.46, sh_y), (cx - bw * 0.78, b_bot - s * 0.06),
             shirt, arm_w)
        line(d, (cx + bw * 0.46, sh_y), (cx + bw * 0.74, b_top + s * 0.22),
             shirt, arm_w)
        circle(d, cx - bw * 0.8, b_bot - s * 0.04, s * 0.04, skin)
        circle(d, cx + bw * 0.76, b_top + s * 0.24, s * 0.04, skin)
    elif pose == "wave":
        line(d, (cx - bw * 0.44, sh_y), (cx - bw * 0.6, b_bot - s * 0.04),
             shirt, arm_w)
        circle(d, cx - bw * 0.62, b_bot - s * 0.02, s * 0.04, skin)
        line(d, (cx + bw * 0.44, sh_y), (cx + bw * 0.85, sh_y - s * 0.14),
             shirt, arm_w)
        circle(d, cx + bw * 0.9, sh_y - s * 0.16, s * 0.045, skin)
    elif pose == "down":
        line(d, (cx - bw * 0.44, sh_y), (cx - bw * 0.58, b_bot - s * 0.03),
             shirt, arm_w)
        line(d, (cx + bw * 0.44, sh_y), (cx + bw * 0.58, b_bot - s * 0.03),
             shirt, arm_w)
        circle(d, cx - bw * 0.6, b_bot - s * 0.015, s * 0.04, skin)
        circle(d, cx + bw * 0.6, b_bot - s * 0.015, s * 0.04, skin)

    # ransel (di depan badan, tali)
    if backpack:
        d.rounded_rectangle(
            [cx - bw * 0.42, b_top + s * 0.06, cx + bw * 0.42, b_bot - s * 0.06],
            radius=s * 0.045, fill=backpack)
        d.rounded_rectangle(
            [cx - bw * 0.2, b_top + s * 0.16, cx + bw * 0.2, b_top + s * 0.24],
            radius=s * 0.02, fill="#FFFFFF")
        circle(d, cx, b_top + s * 0.2, s * 0.018, "#FFD54F")

    # kepala
    if hijab:
        circle(d, cx, hcy + hr * 0.1, hr * 1.24, hijab)
        d.polygon([(cx - hr * 1.1, hcy + hr * 0.7),
                   (cx + hr * 1.1, hcy + hr * 0.7),
                   (cx + hr * 0.9, b_top + s * 0.02),
                   (cx - hr * 0.9, b_top + s * 0.02)], fill=hijab)
        circle(d, cx + face_dir * hr * 0.06, hcy + hr * 0.3, hr * 0.84, skin)
        fy = hcy + hr * 0.34
        fxc = cx + face_dir * hr * 0.06
    else:
        circle(d, cx, hcy, hr, skin)
        d.pieslice([cx - hr, hcy - hr, cx + hr, hcy + hr], 180, 360, fill=hair)
        d.pieslice([cx - hr * 1.02, hcy - hr * 1.05, cx + hr * 1.02,
                    hcy + hr * 0.45], 200, 340, fill=hair)
        fy = hcy + hr * 0.12
        fxc = cx

    # wajah
    er = max(3, int(hr * 0.12))
    if eyes == "closed":
        d.arc([fxc - hr * 0.42, fy - hr * 0.05, fxc - hr * 0.14, fy + hr * 0.18],
              200, 340, fill="#3E2723", width=er)
        d.arc([fxc + hr * 0.14, fy - hr * 0.05, fxc + hr * 0.42, fy + hr * 0.18],
              200, 340, fill="#3E2723", width=er)
    else:
        circle(d, fxc - hr * 0.3, fy, er, "#263238")
        circle(d, fxc + hr * 0.3, fy, er, "#263238")
        circle(d, fxc - hr * 0.26, fy - er * 0.35, er * 0.35, "#FFFFFF")
        circle(d, fxc + hr * 0.34, fy - er * 0.35, er * 0.35, "#FFFFFF")
    d.arc([fxc - hr * 0.34, fy + hr * 0.12, fxc + hr * 0.34, fy + hr * 0.52],
          15, 165, fill="#5D4037", width=max(2, int(hr * 0.1)))
    # pipi merona
    circle(d, fxc - hr * 0.55, fy + hr * 0.3, hr * 0.14, "#F8BBD0")
    circle(d, fxc + hr * 0.55, fy + hr * 0.3, hr * 0.14, "#F8BBD0")


# --------------------------------------------------------------------------
# objek-objek pemandangan
# --------------------------------------------------------------------------

def bed(d, x, base_y, w, wood="#8D6E63", blanket="#42A5F5", pillow="#FFF9C4",
        mattress="#FFFFFF"):
    h = w * 0.30
    for lx in (x + w * 0.03, x + w * 0.9):
        d.rounded_rectangle([lx, base_y - h * 0.1, lx + w * 0.05, base_y + h * 0.18],
                            radius=w * 0.015, fill="#5D4037")
    d.rounded_rectangle([x, base_y - h * 0.75, x + w, base_y],
                        radius=h * 0.2, fill=wood)
    d.rounded_rectangle([x, base_y - h * 1.9, x + w * 0.07, base_y],
                        radius=w * 0.03, fill=wood)
    d.rounded_rectangle([x + w * 0.05, base_y - h * 1.3, x + w * 0.97,
                         base_y - h * 0.5],
                        radius=h * 0.24, fill=mattress)
    d.rounded_rectangle([x + w * 0.07, base_y - h * 1.5, x + w * 0.34,
                         base_y - h * 1.05],
                        radius=h * 0.3, fill=pillow)
    d.rounded_rectangle([x + w * 0.33, base_y - h * 1.42, x + w * 0.96,
                         base_y - h * 0.45],
                        radius=h * 0.24, fill=blanket)
    return base_y - h * 1.42  # garis atas selimut


def sleeping_kid(d, cx, top_y, s, skin="#FFCC80", hair="#4E342E"):
    """Kepala anak yang tidur, menyembul dari balik selimut."""
    hr = s * 0.16
    circle(d, cx, top_y - hr * 0.15, hr, skin)
    d.pieslice([cx - hr, top_y - hr * 1.15 - hr * 0.15,
                cx + hr, top_y + hr * 0.85 - hr * 0.15], 180, 360, fill=hair)
    d.arc([cx - hr * 0.45, top_y - hr * 0.3, cx - hr * 0.1, top_y + hr * 0.05],
          200, 340, fill="#3E2723", width=max(2, int(hr * 0.11)))
    d.arc([cx + hr * 0.1, top_y - hr * 0.3, cx + hr * 0.45, top_y + hr * 0.05],
          200, 340, fill="#3E2723", width=max(2, int(hr * 0.11)))
    d.arc([cx - hr * 0.28, top_y + hr * 0.1, cx + hr * 0.28, top_y + hr * 0.45],
          15, 165, fill="#5D4037", width=max(2, int(hr * 0.1)))
    circle(d, cx - hr * 0.6, top_y + hr * 0.25, hr * 0.13, "#F8BBD0")
    circle(d, cx + hr * 0.6, top_y + hr * 0.25, hr * 0.13, "#F8BBD0")


def house(d, cx, base_y, s, wall="#FFE0B2", roof="#E53935", door="#6D4C41",
          win="#4FC3F7", open_door=False, garage=False):
    bw, bh = s, s * 0.6
    d.rectangle([cx - bw / 2, base_y - bh, cx + bw / 2, base_y], fill=wall)
    d.polygon([(cx - bw / 2 - s * 0.09, base_y - bh),
               (cx + bw / 2 + s * 0.09, base_y - bh),
               (cx, base_y - bh - s * 0.42)], fill=roof)
    d.rectangle([cx - bw / 2 - s * 0.09, base_y - bh - s * 0.05,
                 cx + bw / 2 + s * 0.09, base_y - bh], fill="#C62828")
    # pintu
    dw = s * 0.16
    if open_door:
        d.polygon([(cx - dw / 2, base_y), (cx - dw / 2, base_y - bh * 0.55),
                   (cx + dw / 2, base_y - bh * 0.42), (cx + dw / 2, base_y)],
                  fill="#3E2723")
        d.polygon([(cx + dw / 2, base_y - bh * 0.42), (cx + dw * 1.5, base_y - bh * 0.5),
                   (cx + dw * 1.5, base_y - s * 0.03), (cx + dw / 2, base_y)],
                  fill=door)
    else:
        arch(d, cx - dw / 2, base_y - bh * 0.55, cx + dw / 2, base_y, door)
        circle(d, cx + dw * 0.28, base_y - bh * 0.26, s * 0.018, "#FFD54280")
    # jendela
    ws = s * 0.13
    for wx in (cx - bw * 0.3, cx + bw * 0.3):
        wy = base_y - bh * 0.62
        d.rounded_rectangle([wx - ws / 2, wy - ws / 2, wx + ws / 2, wy + ws / 2],
                            radius=s * 0.015, fill=win, outline="#FFFFFF",
                            width=max(2, int(s * 0.012)))
        d.line([(wx, wy - ws / 2), (wx, wy + ws / 2)], fill="#FFFFFF",
               width=max(2, int(s * 0.012)))
        d.line([(wx - ws / 2, wy), (wx + ws / 2, wy)], fill="#FFFFFF",
               width=max(2, int(s * 0.012)))
    # loteng
    d.pieslice([cx - s * 0.09, base_y - bh - s * 0.26, cx + s * 0.09,
                base_y - bh - s * 0.08], 180, 360, fill=win)


def mosque(img, d, cx, base_y, s, body="#F5F5F5", gold="#FFC107",
           dark="#1A237E", trim="#FFB300"):
    """Masjid: badan + kubah besar + 2 menara + pintu lengkung."""
    bw, bh = s, s * 0.5
    mw = s * 0.11
    # menara (di belakang badan)
    for mx in (cx - bw * 0.62, cx + bw * 0.62):
        top = base_y - bh * 1.6
        d.rounded_rectangle([mx - mw / 2, top, mx + mw / 2, base_y],
                            radius=mw * 0.3, fill=body)
        d.rectangle([mx - mw * 0.75, top + bh * 0.3, mx + mw * 0.75,
                     top + bh * 0.42], fill=trim)
        d.pieslice([mx - mw * 0.78, top - mw * 0.95, mx + mw * 0.78,
                    top + mw * 0.6], 180, 360, fill=gold)
        d.rectangle([mx - mw * 0.62, top - mw * 0.18, mx + mw * 0.62,
                     top + mw * 0.12], fill=gold)
        d.rectangle([mx - mw * 0.1, top - mw * 1.2, mx + mw * 0.1,
                     top - mw * 0.85], fill=gold)
        crescent(img, mx, top - mw * 1.42, s * 0.032, "#FFD54F",
                 cut=0.5, cut_r=0.75)
        arch(d, mx - mw * 0.3, base_y - bh * 0.9, mx + mw * 0.3,
             base_y - bh * 0.5, dark)
    # badan utama
    d.rounded_rectangle([cx - bw / 2, base_y - bh, cx + bw / 2, base_y],
                        radius=s * 0.03, fill=body)
    d.rectangle([cx - bw / 2 - s * 0.03, base_y - bh * 0.18,
                 cx + bw / 2 + s * 0.03, base_y], fill=trim)
    # kubah besar tanpa celah antar-bagian
    dr = s * 0.30
    top = base_y - bh
    d.pieslice([cx - dr, top - dr * 1.3, cx + dr, top + dr * 0.7],
               180, 360, fill=gold)
    d.ellipse([cx - dr, top - dr * 0.45, cx + dr, top + dr * 0.25], fill=gold)
    d.rectangle([cx - dr * 0.07, top - dr * 1.58, cx + dr * 0.07,
                 top - dr * 1.2], fill=gold)
    crescent(img, cx, top - dr * 1.78, s * 0.05, "#FFD54F",
             cut=0.5, cut_r=0.75)
    # pintu & jendela lengkung
    arch(d, cx - s * 0.11, base_y - bh * 0.78, cx + s * 0.11, base_y, dark)
    arch(d, cx - s * 0.09, base_y - bh * 0.72, cx + s * 0.09,
         base_y - s * 0.02, "#3949AB")
    for wx in (cx - bw * 0.34, cx + bw * 0.34):
        arch(d, wx - s * 0.05, base_y - bh * 0.72, wx + s * 0.05,
             base_y - bh * 0.3, gold)
        d.rectangle([wx - s * 0.05, base_y - bh * 0.52, wx + s * 0.05,
                     base_y - bh * 0.3], fill=dark)


def car(d, cx, base_y, s, body="#EF5350", glass="#B3E5FC"):
    w, h = s, s * 0.34
    # roda dulu
    for wx in (cx - w * 0.3, cx + w * 0.32):
        circle(d, wx, base_y - h * 0.12, h * 0.34, "#212121")
        circle(d, wx, base_y - h * 0.12, h * 0.15, "#BDBDBD")
    d.rounded_rectangle([cx - w / 2, base_y - h * 0.95, cx + w / 2,
                         base_y - h * 0.22], radius=h * 0.3, fill=body)
    d.rounded_rectangle([cx - w * 0.3, base_y - h * 1.65, cx + w * 0.24,
                         base_y - h * 0.75], radius=h * 0.3, fill=body)
    d.rounded_rectangle([cx - w * 0.24, base_y - h * 1.5, cx - w * 0.03,
                         base_y - h * 0.9], radius=h * 0.12, fill=glass)
    d.rounded_rectangle([cx + w * 0.01, base_y - h * 1.5, cx + w * 0.19,
                         base_y - h * 0.9], radius=h * 0.12, fill=glass)
    circle(d, cx + w * 0.44, base_y - h * 0.55, h * 0.14, "#FFF176")
    circle(d, cx - w * 0.46, base_y - h * 0.55, h * 0.1, "#FFEB3B")
    d.rounded_rectangle([cx - w * 0.5, base_y - h * 0.35, cx + w * 0.5,
                         base_y - h * 0.22], radius=h * 0.06, fill="#B71C1C")


def open_book(d, cx, base_y, s, cover="#7E57C2", page="#FFFFFF", line="#BDBDBD"):
    """Buku terbuka dilihat dari depan-atas (perspektif sederhana)."""
    w, h = s, s * 0.42
    top = base_y - h
    # sampul
    d.polygon([(cx - w * 0.52, top + h * 0.24), (cx, top + h * 0.05),
               (cx, base_y + h * 0.1), (cx - w * 0.52, base_y + h * 0.16)],
              fill=cover)
    d.polygon([(cx + w * 0.52, top + h * 0.24), (cx, top + h * 0.05),
               (cx, base_y + h * 0.1), (cx + w * 0.52, base_y + h * 0.16)],
              fill=cover)
    # halaman
    d.polygon([(cx - w * 0.47, top + h * 0.22), (cx - w * 0.02, top + h * 0.08),
               (cx - w * 0.02, base_y + h * 0.03), (cx - w * 0.47, base_y + h * 0.08)],
              fill=page)
    d.polygon([(cx + w * 0.47, top + h * 0.22), (cx + w * 0.02, top + h * 0.08),
               (cx + w * 0.02, base_y + h * 0.03), (cx + w * 0.47, base_y + h * 0.08)],
              fill=page)
    d.line([(cx, top + h * 0.07), (cx, base_y + h * 0.04)], fill="#E0E0E0",
           width=max(2, int(s * 0.008)))
    # baris teks
    for i in range(3):
        y0 = top + h * 0.35 + i * h * 0.19
        d.polygon([(cx - w * 0.4, y0), (cx - w * 0.08, y0 - h * 0.055),
                   (cx - w * 0.08, y0 - h * 0.005), (cx - w * 0.4, y0 + h * 0.05)],
                  fill=line)
        d.polygon([(cx + w * 0.4, y0), (cx + w * 0.08, y0 - h * 0.055),
                   (cx + w * 0.08, y0 - h * 0.005), (cx + w * 0.4, y0 + h * 0.05)],
                  fill=line)


def pencil(d, cx, cy, length, angle=-32, body="#FFCA28", tip="#D7CCC8"):
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -math.sin(a), math.cos(a)  # tegak lurus
    wdt = length * 0.09
    x1, y1 = cx - ux * length / 2, cy - uy * length / 2
    x2, y2 = cx + ux * length / 2, cy + uy * length / 2
    d.polygon([(x1 + px * wdt, y1 + py * wdt), (x2 + px * wdt, y2 + py * wdt),
               (x2 - px * wdt, y2 - py * wdt), (x1 - px * wdt, y1 - py * wdt)],
              fill=body)
    # ujung rata
    d.polygon([(x1 + px * wdt, y1 + py * wdt), (x1 - px * wdt, y1 - py * wdt),
               (x1 - px * wdt - ux * wdt * 1.4, y1 - py * wdt - uy * wdt * 1.4),
               (x1 + px * wdt - ux * wdt * 1.4, y1 + py * wdt - uy * wdt * 1.4)],
              fill="#F06292")
    # mata pisau
    tx = x2 + ux * length * 0.16
    ty = y2 + uy * length * 0.16
    d.polygon([(x2 + px * wdt, y2 + py * wdt), (x2 - px * wdt, y2 - py * wdt),
               (tx, ty)], fill=tip)
    d.polygon([(tx + (x2 - tx) * 0.45 + px * wdt * 0.45,
                ty + (y2 - ty) * 0.45 + py * wdt * 0.45),
               (tx + (x2 - tx) * 0.45 - px * wdt * 0.45,
                ty + (y2 - ty) * 0.45 - py * wdt * 0.45),
               (tx, ty)], fill="#4E342E")


def clock(d, cx, cy, r, face="#FFF9C4", frame="#EF5350"):
    d.ellipse([cx - r * 1.18, cy - r * 1.35, cx - r * 0.55, cy - r * 0.72],
              fill=frame)
    d.ellipse([cx + r * 0.55, cy - r * 1.35, cx + r * 1.18, cy - r * 0.72],
              fill=frame)
    circle(d, cx, cy, r, frame)
    circle(d, cx, cy, r * 0.78, face)
    d.line([(cx, cy), (cx, cy - r * 0.5)], fill="#37474F",
           width=max(3, int(r * 0.1)))
    d.line([(cx, cy), (cx + r * 0.4, cy + r * 0.15)], fill="#37474F",
           width=max(3, int(r * 0.1)))
    circle(d, cx, cy, r * 0.09, "#37474F")
    for lx in (-r * 0.5, r * 0.5):
        d.ellipse([cx + lx - r * 0.17, cy + r * 0.8, cx + lx + r * 0.17,
                   cy + r * 1.12], fill="#B71C1C")


def glass_of_water(d, cx, base_y, w, water="#4FC3F7"):
    h = w * 1.55
    d.polygon([(cx - w / 2, base_y - h), (cx + w / 2, base_y - h),
               (cx + w * 0.4, base_y), (cx - w * 0.4, base_y)],
              fill="#E3F2FD")
    wy = base_y - h * 0.62
    d.polygon([(cx - w * 0.47, wy), (cx + w * 0.47, wy),
               (cx + w * 0.4, base_y), (cx - w * 0.4, base_y)], fill=water)
    d.ellipse([cx - w * 0.47, wy - h * 0.045, cx + w * 0.47, wy + h * 0.045],
              fill="#81D4FA")
    d.line([(cx - w * 0.46, base_y - h * 0.95), (cx - w * 0.36, base_y - h * 0.25)],
           fill="#FFFFFF", width=max(3, int(w * 0.07)))
    d.line([(cx - w * 0.28, base_y - h * 0.92), (cx - w * 0.22, base_y - h * 0.55)],
           fill="#FFFFFF", width=max(2, int(w * 0.045)))


def plate(d, cx, cy, r, food=None, clean=False):
    circle(d, cx, cy, r, "#ECEFF1")
    circle(d, cx, cy, r * 0.78, "#FFFFFF")
    if food == "rice":
        d.pieslice([cx - r * 0.5, cy - r * 0.6, cx + r * 0.5, cy + r * 0.35],
                   180, 360, fill="#FFF8E1")
        d.rectangle([cx - r * 0.5, cy - r * 0.13, cx + r * 0.5, cy + r * 0.12],
                    fill="#FFF8E1")
        d.pieslice([cx - r * 0.5, cy - r * 0.13, cx + r * 0.5, cy + r * 0.4],
                   0, 180, fill="#FFF8E1")
        circle(d, cx + r * 0.3, cy + r * 0.05, r * 0.22, "#FFB74D")
        circle(d, cx - r * 0.28, cy + r * 0.12, r * 0.16, "#66BB6A")
    elif food == "bowl":
        d.pieslice([cx - r * 0.62, cy - r * 0.45, cx + r * 0.62, cy + r * 0.55],
                   0, 180, fill="#42A5F5")
        d.ellipse([cx - r * 0.62, cy - r * 0.55, cx + r * 0.62, cy - r * 0.15],
                  fill="#90CAF9")
        circle(d, cx - r * 0.1, cy - r * 0.36, r * 0.1, "#FFF176")
    if clean:
        d.line([(cx - r * 0.3, cy + r * 0.05), (cx, cy - r * 0.15)],
               fill="#CFD8DC", width=4)
        d.line([(cx + r * 0.12, cy + r * 0.22), (cx + r * 0.34, cy + r * 0.02)],
               fill="#CFD8DC", width=4)


def tree(d, cx, base_y, s, leaf="#43A047", leaf2="#66BB6A", trunk="#6D4C41"):
    d.rounded_rectangle([cx - s * 0.06, base_y - s * 0.5, cx + s * 0.06,
                         base_y], radius=s * 0.05, fill=trunk)
    circle(d, cx, base_y - s * 0.72, s * 0.34, leaf)
    circle(d, cx - s * 0.26, base_y - s * 0.56, s * 0.26, leaf2)
    circle(d, cx + s * 0.26, base_y - s * 0.56, s * 0.26, leaf2)
    circle(d, cx, base_y - s * 1.0, s * 0.24, leaf2)


# --------------------------------------------------------------------------
# setiap adegan doa
# --------------------------------------------------------------------------

def scene_bangun_tidur():
    img, d = new_scene("#FFF8E1", "#FFCC80")
    sun(d, 1090, 200, 95)
    cloud(d, 300, 130, 60, "#FFFFFF")
    cloud(d, 640, 90, 46, "#FFFFFF")
    hills(d, 560, "#AED581", bumps=((-120, 520), (680, 640), (1320, 560)))
    ground(img, d, 600, "#8BC34A")
    # jendela
    d.rounded_rectangle([80, 90, 330, 330], radius=18, fill="#B3E5FC",
                        outline="#8D6E63", width=14)
    d.line([(205, 90), (205, 330)], fill="#8D6E63", width=12)
    d.line([(80, 210), (330, 210)], fill="#8D6E63", width=12)
    circle(d, 270, 150, 42, "#FFD54F")
    cloud(d, 140, 270, 34, "#FFFFFF")
    # kasur + anak duduk
    blanket_top = bed(d, 430, 620, 560, blanket="#5C6BC0", pillow="#FFF9C4")
    s = 250
    cx = 640
    hr = s * 0.17
    hcy = blanket_top - hr * 0.6
    # badan menyembul dari selimut
    d.rounded_rectangle([cx - s * 0.15, hcy, cx + s * 0.15, blanket_top + 6],
                        radius=s * 0.06, fill="#42A5F5")
    circle(d, cx, hcy - hr * 0.9, hr, "#FFCC80")
    d.pieslice([cx - hr, hcy - hr * 1.9, cx + hr, hcy + hr * 0.1], 180, 360,
               fill="#4E342E")
    circle(d, cx - hr * 0.3, hcy - hr * 0.85, hr * 0.13, "#263238")
    circle(d, cx + hr * 0.3, hcy - hr * 0.85, hr * 0.13, "#263238")
    d.arc([cx - hr * 0.32, hcy - hr * 0.62, cx + hr * 0.32, hcy - hr * 0.2],
          15, 165, fill="#5D4037", width=5)
    circle(d, cx - hr * 0.58, hcy - hr * 0.42, hr * 0.14, "#F8BBD0")
    circle(d, cx + hr * 0.58, hcy - hr * 0.42, hr * 0.14, "#F8BBD0")
    # lengan menggeliat
    line(d, (cx - s * 0.13, hcy + hr * 0.7), (cx - s * 0.3, hcy - hr * 0.5),
         "#42A5F5", 20)
    line(d, (cx + s * 0.13, hcy + hr * 0.7), (cx + s * 0.3, hcy - hr * 0.5),
         "#42A5F5", 20)
    circle(d, cx - s * 0.32, hcy - hr * 0.62, hr * 0.24, "#FFCC80")
    circle(d, cx + s * 0.32, hcy - hr * 0.62, hr * 0.24, "#FFCC80")
    # jam weker di meja nakas
    d.rounded_rectangle([1030, 520, 1240, 620], radius=16, fill="#8D6E63")
    d.rectangle([1050, 620, 1080, 668], fill="#6D4C41")
    d.rectangle([1190, 620, 1220, 668], fill="#6D4C41")
    clock(d, 1135, 470, 58)
    return img


def scene_sebelum_tidur():
    img, d = new_scene("#0F1B4C", "#3F51B5")
    starfield(d, 34)
    crescent(img, 1080, 155, 95, "#FFE082", cut=0.45, cut_r=0.8)
    cloud(d, 330, 120, 54, "#5C6BC0")
    cloud(d, 760, 180, 42, "#5C6BC0")
    ground(img, d, 610, "#283593")
    # karpet
    d.ellipse([330, 600, 1100, 720], fill="#7E57C2")
    # jendela malam
    d.rounded_rectangle([90, 90, 320, 320], radius=18, fill="#1A237E",
                        outline="#5D4037", width=14)
    d.line([(205, 90), (205, 320)], fill="#5D4037", width=12)
    d.line([(90, 205), (320, 205)], fill="#5D4037", width=12)
    star(d, 150, 150, 16, "#FFE082")
    star(d, 265, 250, 12, "#FFE082")
    crescent(img, 255, 145, 30, "#FFF59D", cut=0.5, cut_r=0.75)
    # kasur + anak tidur
    top = bed(d, 420, 640, 580, blanket="#7E57C2", pillow="#FFF9C4")
    # selimut menutup badan
    d.rounded_rectangle([560, top + 40, 980, 640 - 44], radius=26,
                        fill="#7E57C2")
    d.rounded_rectangle([560, top + 40, 980, 640 - 44], radius=26,
                        outline="#9575CD", width=5)
    sleeping_kid(d, 545, top + 52, 300)
    # meja nakas + lampu
    d.rounded_rectangle([1040, 540, 1230, 640], radius=14, fill="#6D4C41")
    d.rectangle([1060, 640, 1086, 676], fill="#4E342E")
    d.rectangle([1186, 640, 1212, 676], fill="#4E342E")
    d.polygon([(1113, 472), (1157, 472), (1197, 540), (1073, 540)],
              fill="#FFCA28")
    d.line([(1135, 472), (1135, 448)], fill="#FFF9C4", width=8)
    circle(d, 1135, 436, 17, "#FFF59D")
    return img


def scene_sebelum_makan():
    img, d = new_scene("#FFF3E0", "#FFCC80")
    cloud(d, 980, 110, 52, "#FFFFFF")
    cloud(d, 250, 90, 44, "#FFFFFF")
    # dinding & lantai
    d.rectangle([0, 470, W, H], fill="#BCAAA4")
    tiles(d, 0, 470, W, H, "#D7CCC8", "#BCAAA4", n=10)
    # meja
    d.rounded_rectangle([260, 430, 1020, 500], radius=24, fill="#A1887F")
    d.rectangle([330, 500, 380, 660], fill="#795548")
    d.rectangle([900, 500, 950, 660], fill="#795548")
    # anak berdoa di kiri
    kid(d, 165, 700, 330, shirt="#66BB6A", pose="pray")
    # piring, mangkuk, gelas
    plate(d, 640, 440, 95, food="rice")
    d.pieslice([780, 340, 940, 480], 0, 180, fill="#42A5F5")
    d.ellipse([780, 392, 940, 428], fill="#90CAF9")
    circle(d, 845, 406, 13, "#FFEB3B")
    d.arc([798, 400, 852, 424], 200, 340, fill="#E3F2FD", width=6)
    # uap berbentuk S (dua busur pada kotak yang sama agar menyambung)
    for i, x in enumerate((822, 860, 898)):
        y0 = 262 + i * 7
        d.arc([x - 20, y0, x + 4, y0 + 44], 90, 270, fill="#FFFFFF", width=7)
        d.arc([x - 20, y0 + 30, x + 4, y0 + 74], 270, 90, fill="#FFFFFF", width=7)
    glass_of_water(d, 480, 470, 90)
    # sendok
    d.line([(700, 470), (790, 445)], fill="#B0BEC5", width=12)
    circle(d, 797, 443, 15, "#CFD8DC")
    # anak kanan
    kid(d, 1135, 700, 320, shirt="#42A5F5", hijab="#EF9A9A", pose="pray")
    return img


def scene_sesudah_makan():
    img, d = new_scene("#FFEBEE", "#FFCCBC")
    cloud(d, 1020, 100, 50, "#FFFFFF")
    cloud(d, 220, 120, 42, "#FFFFFF")
    d.rectangle([0, 470, W, H], fill="#BCAAA4")
    tiles(d, 0, 470, W, H, "#D7CCC8", "#BCAAA4", n=10)
    d.rounded_rectangle([260, 430, 1020, 500], radius=24, fill="#A1887F")
    d.rectangle([330, 500, 380, 660], fill="#795548")
    d.rectangle([900, 500, 950, 660], fill="#795548")
    plate(d, 640, 445, 100, clean=True)
    # sendok & garpu menyilang
    d.line([(560, 470), (700, 425)], fill="#B0BEC5", width=13)
    circle(d, 710, 422, 16, "#CFD8DC")
    d.line([(720, 470), (580, 425)], fill="#B0BEC5", width=10)
    for i in range(3):
        d.line([(575 + i * 12, 430), (565 + i * 12, 405)], fill="#B0BEC5",
               width=7)
    glass_of_water(d, 480, 470, 84)
    # mangkuk kosong (bibir menempel, tanpa celah)
    d.pieslice([800, 355, 940, 480], 0, 180, fill="#EF9A9A")
    d.ellipse([800, 401, 940, 434], fill="#FFCDD2")
    # anak puas
    kid(d, 165, 700, 330, shirt="#FFA726", pose="down", eyes="closed")
    kid(d, 1135, 700, 320, shirt="#AB47BC", hijab="#CE93D8", pose="down",
        eyes="closed")
    # tanda hati/kilau bersih
    star(d, 1035, 330, 26, "#FFE082")
    star(d, 250, 300, 20, "#FFE082")
    return img


def scene_minum():
    img, d = new_scene("#E1F5FE", "#B3E5FC")
    cloud(d, 1010, 110, 54, "#FFFFFF")
    cloud(d, 260, 140, 46, "#FFFFFF")
    # lantai air bergelombang
    d.rectangle([0, 560, W, H], fill="#4FC3F7")
    d.ellipse([-80, 520, 420, 620], fill="#81D4FA")
    d.ellipse([880, 530, 1360, 625], fill="#81D4FA")
    # gelas besar
    glass_of_water(d, 640, 600, 260)
    # tetesan air
    for x, y, r in ((300, 330, 34), (980, 300, 40), (380, 470, 24),
                    (930, 460, 26), (240, 500, 18)):
        drop(d, x, y, r, "#4FC3F7")
        d.arc([x - r * 0.5, y - r * 0.3, x + r * 0.1, y + r * 0.5],
              120, 240, fill="#E1F5FE", width=4)
    # percikan
    star(d, 1075, 190, 30, "#FFFFFF")
    star(d, 205, 220, 24, "#FFFFFF")
    # anak memegang gelas kecil di kanan
    kid(d, 1120, 700, 300, shirt="#26A69A", pose="wave")
    kid(d, 190, 700, 300, shirt="#EC407A", hijab="#F48FB1", pose="down")
    return img


def scene_masuk_kamar_mandi():
    img, d = new_scene("#E0F7FA", "#B2EBF2")
    # dinding keramik
    tiles(d, 0, 0, W, 520, "#E0F7FA", "#CFE8EF", n=12)
    # lantai
    tiles(d, 0, 520, W, H, "#4DD0E1", "#26C6DA", n=10)
    # pintu terbuka (anak masuk dari kiri, pintu di kanan)
    d.rounded_rectangle([820, 90, 1180, 640], radius=18, fill="#8D6E63")
    d.polygon([(860, 640), (860, 130), (1105, 175), (1105, 640)],
              fill="#FFF8E1")  # cahaya dari dalam
    d.polygon([(860, 640), (860, 130), (700, 105), (700, 640)], fill="#6D4C41")
    circle(d, 735, 400, 16, "#FFD54F")
    # handuk
    d.rounded_rectangle([180, 130, 320, 170], radius=14, fill="#90A4AE")
    d.rounded_rectangle([195, 170, 305, 380], radius=18, fill="#EF5350")
    d.rounded_rectangle([195, 330, 305, 380], radius=18, fill="#E53935")
    # pancuran
    d.line([(480, 0), (480, 90)], fill="#90A4AE", width=14)
    d.pieslice([420, 60, 540, 150], 180, 360, fill="#B0BEC5")
    for i, x in enumerate((445, 480, 515)):
        for j in range(3):
            drop(d, x + (j - 1) * 6, 190 + j * 65 + i * 8, 12, "#4FC3F7")
    # sabun
    d.rounded_rectangle([560, 430, 640, 500], radius=18, fill="#66BB6A")
    d.rounded_rectangle([575, 410, 625, 440], radius=10, fill="#A5D6A7")
    # anak masuk (langkah kiri)
    kid(d, 700, 700, 330, shirt="#5C6BC0", pose="walk")
    return img


def scene_keluar_kamar_mandi():
    img, d = new_scene("#E0F7FA", "#B2EBF2")
    tiles(d, 0, 0, W, 520, "#E0F7FA", "#CFE8EF", n=12)
    tiles(d, 0, 520, W, H, "#4DD0E1", "#26C6DA", n=10)
    # pintu tertutup di kiri
    d.rounded_rectangle([100, 90, 460, 640], radius=18, fill="#8D6E63")
    d.rounded_rectangle([140, 130, 420, 600], radius=12, fill="#A1887F")
    circle(d, 405, 380, 16, "#FFD54F")
    # wastafel + cermin
    d.rounded_rectangle([560, 110, 860, 350], radius=16, fill="#B3E5FC",
                        outline="#E0F7FA", width=12)
    d.rounded_rectangle([580, 380, 840, 440], radius=24, fill="#ECEFF1")
    d.pieslice([620, 400, 800, 500], 0, 180, fill="#CFD8DC")
    d.line([(700, 350), (700, 385)], fill="#90A4AE", width=12)
    # gelembung sabun
    for x, y, r in ((980, 180, 46), (1090, 270, 34), (1170, 160, 26),
                    (1030, 380, 24), (1210, 330, 40), (950, 460, 30)):
        circle(d, x, y, r, None, outline="#FFFFFF", width=5)
        d.arc([x - r * 0.6, y - r * 0.6, x + r * 0.1, y + r * 0.1], 150, 250,
              fill="#FFFFFF", width=4)
    # anak keluar (langkah kanan)
    kid(d, 720, 700, 340, shirt="#29B6F6", pose="walk", face_dir=1)
    return img


def scene_keluar_rumah():
    img, d = new_scene("#90CAF9", "#BBDEFB")
    sun(d, 170, 140, 80)
    cloud(d, 560, 120, 52, "#FFFFFF")
    cloud(d, 950, 170, 44, "#FFFFFF")
    hills(d, 520, "#AED581", bumps=((-160, 560), (700, 520), (1350, 640)))
    ground(img, d, 590, "#7CB342")
    # jalan setapak
    d.polygon([(640, 720), (830, 720), (770, 560), (700, 560)], fill="#BDBDBD")
    # rumah
    house(d, 940, 600, 460, wall="#FFE0B2", roof="#E53935", open_door=True)
    tree(d, 300, 600, 190)
    flowers(d, ((450, 640), (520, 668), (1180, 650), (1230, 676)))
    # anak keluar rumah (berjalan ke kiri)
    kid(d, 745, 700, 340, shirt="#FFA726", pose="walk", backpack="#8E24AA",
        face_dir=-1)
    return img


def scene_masuk_rumah():
    img, d = new_scene("#FFE0B2", "#FFCC80")
    sun(d, 1120, 150, 76, core="#FFB74D", ray="#FFE082")
    cloud(d, 380, 110, 50, "#FFFFFF")
    cloud(d, 760, 160, 40, "#FFFFFF")
    hills(d, 530, "#C5E1A5", bumps=((-140, 600), (640, 560), (1360, 600)))
    ground(img, d, 600, "#8BC34A")
    house(d, 330, 610, 470, wall="#FFCC80", roof="#EF5350", open_door=True)
    # pintu masuk + keset
    d.rounded_rectangle([600, 640, 830, 700], radius=14, fill="#8D6E63")
    d.rounded_rectangle([620, 655, 810, 688], radius=10, fill="#A1887F")
    tree(d, 1060, 610, 200)
    flowers(d, ((940, 655), (1000, 680), (150, 665), (210, 690)))
    # anak masuk rumah (berjalan ke kiri menuju pintu)
    kid(d, 700, 710, 340, shirt="#26A69A", pose="walk", backpack="#1E88E5",
        face_dir=-1)
    return img


def scene_naik_kendaraan():
    img, d = new_scene("#B3E5FC", "#81D4FA")
    cloud(d, 300, 110, 56, "#FFFFFF")
    cloud(d, 760, 90, 44, "#FFFFFF")
    cloud(d, 1090, 160, 48, "#FFFFFF")
    tree(d, 140, 540, 170)
    tree(d, 1160, 545, 150, leaf="#2E7D32", leaf2="#43A047")
    # jalan
    d.rectangle([0, 545, W, H], fill="#455A64")
    d.rectangle([0, 545, W, 565], fill="#37474F")
    for i in range(7):
        x = 40 + i * 190
        d.rounded_rectangle([x, 630, x + 100, 650], radius=10, fill="#FFF176")
    d.rectangle([0, 700, W, H], fill="#37474F")
    # mobil
    car(d, 620, 640, 560, body="#EF5350")
    # anak melambai dari dalam kaca jendela (di-clip ke area kaca saja)
    pane = (486, 355, 604, 469)
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    kid(ImageDraw.Draw(tmp), 553, 530, 155, shirt="#FFCA28", pose="wave")
    rect = Image.new("L", img.size, 0)
    ImageDraw.Draw(rect).rectangle(pane, fill=255)
    img.paste(tmp.convert("RGB"), (0, 0),
              ImageChops.multiply(tmp.split()[3], rect))
    # garis kecepatan di langit
    for i, y in enumerate((255, 305, 215)):
        x0 = 55 + i * 30
        d.rounded_rectangle([x0, y, x0 + 145, y + 14], radius=7,
                            fill="#FFFFFF")
    return img


def scene_sebelum_belajar():
    img, d = new_scene("#F3E5F5", "#E1BEE7")
    cloud(d, 1050, 110, 46, "#FFFFFF")
    cloud(d, 230, 90, 42, "#FFFFFF")
    d.rectangle([0, 500, W, H], fill="#CE93D8")
    d.rounded_rectangle([120, 545, 1160, 615], radius=26, fill="#8D6E63")
    d.rectangle([190, 615, 240, 700], fill="#6D4C41")
    d.rectangle([1040, 615, 1090, 700], fill="#6D4C41")
    # buku terbuka di atas meja
    open_book(d, 640, 545, 520)
    # pensil
    pencil(d, 1010, 500, 260, angle=-38)
    # tumpukan buku
    d.rounded_rectangle([150, 470, 400, 512], radius=12, fill="#42A5F5")
    d.rounded_rectangle([170, 430, 385, 472], radius=12, fill="#EF5350")
    d.rounded_rectangle([190, 392, 370, 434], radius=12, fill="#FFCA28")
    # topi wisuda
    d.polygon([(1080, 330), (1180, 375), (1080, 420), (980, 375)],
              fill="#263238")
    d.rectangle([1040, 375, 1120, 415], fill="#37474F")
    d.line([(1080, 375), (1080, 430)], fill="#FFD54F", width=6)
    circle(d, 1080, 435, 12, "#FFD54F")
    # anak berdoa sebelum belajar
    kid(d, 785, 700, 330, shirt="#7E57C2", pose="pray")
    star(d, 500, 240, 24, "#FFE082")
    star(d, 880, 190, 20, "#FFE082")
    return img


def scene_masuk_masjid():
    img, d = new_scene("#101A45", "#3949AB")
    starfield(d, 30, ymax=380)
    crescent(img, 175, 128, 58, "#FFE082", cut=0.45, cut_r=0.8)
    cloud(d, 1050, 120, 48, "#3949AB")
    ground(img, d, 615, "#1A237E")
    # karpet masjid
    d.rounded_rectangle([420, 615, 900, 720], radius=20, fill="#C62828")
    d.rounded_rectangle([450, 640, 870, 720], radius=14, fill="#E53935")
    mosque(img, d, 640, 630, 560, body="#ECEFF1", gold="#FFC107",
           dark="#1A237E")
    # anak masuk masjid
    kid(d, 1090, 710, 320, shirt="#26A69A", hijab="#F48FB1", pose="walk",
        face_dir=-1)
    # lampu gantung di sisi kiri-kanan
    for x in (120, 1160):
        d.line([(x, 0), (x, 340)], fill="#FFD54F", width=5)
        d.polygon([(x - 26, 400), (x + 26, 400), (x + 16, 340), (x - 16, 340)],
                  fill="#FFCA28")
        circle(d, x, 398, 14, "#FFF59D")
    return img


def scene_keluar_masjid():
    img, d = new_scene("#FFE0B2", "#FFB74D")
    sun(d, 1105, 160, 82, core="#FFCC80", ray="#FFE082")
    cloud(d, 300, 120, 52, "#FFFFFF")
    cloud(d, 700, 90, 40, "#FFFFFF")
    ground(img, d, 620, "#8D6E64")
    d.rounded_rectangle([0, 620, W, 720], radius=0, fill="#A1887F")
    mosque(img, d, 420, 630, 560, body="#FFF8E1", gold="#FFB300",
           dark="#4E342E")
    tree(d, 1130, 640, 190)
    # anak keluar masjid (berjalan ke kanan)
    kid(d, 880, 715, 330, shirt="#1E88E5", pose="walk")
    star(d, 1010, 300, 22, "#FFF8E1")
    return img


def scene_pulang_sekolah():
    img, d = new_scene("#FFF9C4", "#FFE082")
    sun(d, 165, 145, 78)
    cloud(d, 560, 110, 52, "#FFFFFF")
    cloud(d, 980, 150, 44, "#FFFFFF")
    ground(img, d, 600, "#9CCC65")
    d.polygon([(660, 720), (850, 720), (790, 575), (700, 575)], fill="#BDBDBD")
    # sekolah
    sx, sy, sw = 950, 615, 520
    d.rectangle([sx - sw / 2, sy - sw * 0.45, sx + sw / 2, sy], fill="#FFCC80")
    d.rectangle([sx - sw / 2 - 14, sy - sw * 0.5, sx + sw / 2 + 14,
                 sy - sw * 0.45], fill="#EF5350")
    d.polygon([(sx - sw * 0.55, sy - sw * 0.5), (sx + sw * 0.55, sy - sw * 0.5),
               (sx, sy - sw * 0.78)], fill="#E53935")
    arch(d, sx - sw * 0.09, sy - sw * 0.3, sx + sw * 0.09, sy, "#5D4037")
    for wx in (sx - sw * 0.33, sx + sw * 0.33):
        d.rounded_rectangle([wx - sw * 0.08, sy - sw * 0.34, wx + sw * 0.08,
                             sy - sw * 0.16], radius=8, fill="#4FC3F7",
                            outline="#FFFFFF", width=6)
        d.line([(wx, sy - sw * 0.34), (wx, sy - sw * 0.16)], fill="#FFFFFF",
               width=5)
    # tiang bendera merah putih
    fx = sx - sw * 0.72
    d.line([(fx, sy), (fx, sy - sw * 0.75)], fill="#90A4AE", width=10)
    d.rectangle([fx, sy - sw * 0.72, fx + 110, sy - sw * 0.635], fill="#E53935")
    d.rectangle([fx, sy - sw * 0.635, fx + 110, sy - sw * 0.55], fill="#FAFAFA")
    # pagar
    for i in range(6):
        px = 140 + i * 46
        d.rounded_rectangle([px, 545, px + 22, 625], radius=8, fill="#FFFFFF")
    d.rectangle([120, 570, 380, 586], fill="#FFFFFF")
    tree(d, 480, 620, 170)
    # anak pulang sekolah
    kid(d, 660, 715, 340, shirt="#42A5F5", pose="walk", backpack="#EC407A")
    return img


SCENES = {
    "bangun-tidur": scene_bangun_tidur,
    "sebelum-tidur": scene_sebelum_tidur,
    "sebelum-makan": scene_sebelum_makan,
    "sesudah-makan": scene_sesudah_makan,
    "minum": scene_minum,
    "masuk-kamar-mandi": scene_masuk_kamar_mandi,
    "keluar-kamar-mandi": scene_keluar_kamar_mandi,
    "keluar-rumah": scene_keluar_rumah,
    "masuk-rumah": scene_masuk_rumah,
    "naik-kendaraan": scene_naik_kendaraan,
    "sebelum-belajar": scene_sebelum_belajar,
    "masuk-masjid": scene_masuk_masjid,
    "keluar-masjid": scene_keluar_masjid,
    "pulang-sekolah": scene_pulang_sekolah,
}


# --------------------------------------------------------------------------
# banner beranda & ikon aplikasi
# --------------------------------------------------------------------------

def header_image():
    img = gradient((1600, 700), "#4FC3F7", "#81C784")
    d = ImageDraw.Draw(img)
    starfield(d, 14, color="#FFF59D", ymax=200, xmax=1560)
    sun(d, 1430, 130, 70)
    cloud(d, 300, 120, 58, "#FFFFFF")
    cloud(d, 760, 90, 44, "#FFFFFF")
    hills(d, 520, "#66BB6A", bumps=((-200, 700), (800, 640), (1750, 700)))
    # masjid kecil di kejauhan
    mosque(img, d, 1250, 560, 380, body="#ECEFF1", gold="#FFC107",
           dark="#1A237E")
    ground(img, d, 560, "#43A047")
    # dua anak berdoa
    kid(d, 430, 680, 400, shirt="#5C6BC0", pose="pray")
    kid(d, 760, 680, 390, shirt="#EC407A", hijab="#F8BBD0", pose="pray")
    # bintang & bulan
    crescent(img, 180, 140, 56, "#FFE082", cut=0.45, cut_r=0.8)
    star(d, 620, 170, 26, "#FFF59D")
    star(d, 980, 220, 20, "#FFF59D")
    return img


def _icon_logo(d, cx, cy, s, mosque_body="#FFFFFF", gold="#FFD54F",
               star_c="#FFFFFF"):
    """Logo masjid + bulan sabit untuk ikon (s = lebar masjid)."""
    # siluet masjid sederhana
    bh = s * 0.42
    base = cy + s * 0.42
    for mx in (cx - s * 0.56, cx + s * 0.56):
        mw = s * 0.14
        d.rounded_rectangle([mx - mw / 2, base - s * 0.72, mx + mw / 2, base],
                            radius=mw * 0.3, fill=mosque_body)
        d.pieslice([mx - mw * 0.75, base - s * 0.86, mx + mw * 0.75,
                    base - s * 0.62], 180, 360, fill=gold)
    d.rounded_rectangle([cx - s * 0.42, base - bh, cx + s * 0.42, base],
                        radius=s * 0.04, fill=mosque_body)
    dr = s * 0.3
    d.pieslice([cx - dr, base - bh - dr * 1.15, cx + dr, base - bh + dr * 0.6],
               180, 360, fill=gold)
    d.ellipse([cx - dr, base - bh - dr * 0.16, cx + dr, base - bh + dr * 0.16],
              fill=gold)
    # pintu lengkung
    d.pieslice([cx - s * 0.1, base - s * 0.4, cx + s * 0.1, base - s * 0.2],
               180, 360, fill=mosque_body)
    d.rectangle([cx - s * 0.1, base - s * 0.3, cx + s * 0.1, base],
                fill=mosque_body)
    # celah pintu
    d.pieslice([cx - s * 0.06, base - s * 0.36, cx + s * 0.06, base - s * 0.24],
               180, 360, fill="#1565C0")
    d.rectangle([cx - s * 0.06, base - s * 0.3, cx + s * 0.06, base],
                fill="#1565C0")
    # jendela
    for wx in (cx - s * 0.28, cx + s * 0.28):
        d.pieslice([wx - s * 0.05, base - s * 0.32, wx + s * 0.05,
                    base - s * 0.22], 180, 360, fill="#1565C0")
        d.rectangle([wx - s * 0.05, base - s * 0.27, wx + s * 0.05,
                     base - bh * 0.35], fill="#1565C0")


def make_icons():
    # ikon utama
    img = gradient((1024, 1024), "#26C6DA", "#1565C0")
    d = ImageDraw.Draw(img)
    star(d, 200, 200, 40, "#FFF59D")
    star(d, 830, 260, 30, "#FFF59D")
    star(d, 300, 820, 26, "#FFF59D")
    crescent(img, 810, 170, 70, "#FFE082", cut=0.45, cut_r=0.8)
    _icon_logo(d, 512, 560, 620)
    img.save(os.path.join(ASSET_DIR, "icon.png"))

    # foreground adaptif android (transparan, area aman 66%)
    fg = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fg)
    _icon_logo(fd, 512, 570, 560)
    crescent(fg, 760, 260, 64, "#FFE082", cut=0.45, cut_r=0.8)
    starfd = ImageDraw.Draw(fg)
    star(starfd, 300, 260, 40, "#FFE082")
    fg.save(os.path.join(ASSET_DIR, "android-icon-foreground.png"))

    # background adaptif
    gradient((1024, 1024), "#E1F5FE", "#B3E5FC").save(
        os.path.join(ASSET_DIR, "android-icon-background.png"))

    # monokrom (putih, untuk theming ikon)
    mono = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    md = ImageDraw.Draw(mono)
    _icon_logo(md, 512, 570, 560, mosque_body="#FFFFFF", gold="#FFFFFF",
               star_c="#FFFFFF")
    mcres = Image.new("L", (1024, 1024), 0)
    mcd = ImageDraw.Draw(mcres)
    mcd.ellipse([660, 170, 900, 410], fill=255)
    mcd.ellipse([720, 150, 930, 360], fill=0)
    mono.paste((255, 255, 255, 255), (0, 0), mcres)
    mono.save(os.path.join(ASSET_DIR, "android-icon-monochrome.png"))

    # favicon kecil
    fav = gradient((96, 96), "#26C6DA", "#1565C0")
    fvd = ImageDraw.Draw(fav)
    _icon_logo(fvd, 48, 54, 58)
    fav.save(os.path.join(ASSET_DIR, "favicon.png"))

    # splash icon (logo transparan)
    sp = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    spd = ImageDraw.Draw(sp)
    _icon_logo(spd, 500, 560, 600, mosque_body="#FFFFFF", gold="#FFD54F")
    scres = Image.new("L", (1000, 1000), 0)
    scd = ImageDraw.Draw(scres)
    scd.ellipse([640, 150, 880, 390], fill=255)
    scd.ellipse([700, 130, 910, 340], fill=0)
    sp.paste((255, 213, 79, 255), (0, 0), scres)
    sp.save(os.path.join(ASSET_DIR, "splash-icon.png"))


# --------------------------------------------------------------------------

def main():
    os.makedirs(DOA_DIR, exist_ok=True)
    for name, fn in SCENES.items():
        out = os.path.join(DOA_DIR, f"{name}.png")
        fn().save(out, optimize=True)
        print("ok", os.path.relpath(out, ROOT))
    header_image().save(os.path.join(ASSET_DIR, "header.png"), optimize=True)
    print("ok assets/header.png")
    make_icons()
    for f in ("icon.png", "android-icon-foreground.png",
              "android-icon-background.png", "android-icon-monochrome.png",
              "favicon.png", "splash-icon.png"):
        print("ok assets/" + f)


if __name__ == "__main__":
    main()
