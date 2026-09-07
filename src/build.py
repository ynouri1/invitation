"""Build ../invitation.html from invitation.tpl.html by embedding the photos as data URIs.

Reads the three source photos from ./assets, re-encodes each (max 1600 px wide, JPEG q82)
so the page stays well under the artifact size limit, and measures the door opening on the
closed-door photo to position the two swinging leaves.

Usage:  cd src && python build.py
Requires: opencv-python-headless, numpy   (pip install opencv-python-headless numpy)
"""
import base64
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, os.pardir, "index.html")  # served at the site root by GitHub Pages
MAX_W = 1600

SOURCES = {
    "CLOSED": "01-porte-fermee.jpg",   # closed palace door (intro)
    "SALON":  "02-salon.jpg",          # golden reception hall (cover / closing)
    "OPEN":   "03-porte-ouverte.jpg",  # doorway opening onto the lit hall
}


def encode(path):
    im = cv2.imread(path)
    if im is None:
        sys.exit("cannot read image: " + path)
    h, w = im.shape[:2]
    if w > MAX_W:
        im = cv2.resize(im, (MAX_W, int(h * MAX_W / w)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 82])
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.tobytes()).decode()
    return uri, im.shape[1], im.shape[0]


def door_box(path):
    """Fraction (left, right, bottom) of the green double door, measured on the closed photo."""
    im = cv2.imread(path)
    h, w = im.shape[:2]
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 40, 20), (95, 255, 140))          # dark-green door panels
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((max(9, w // 55),) * 2, np.uint8))
    mask[:, : int(w * 0.28)] = 0
    mask[:, int(w * 0.72):] = 0                                    # ignore the rose leaves at the sides
    ys, xs = np.where(mask > 0)
    left, right = xs.min() / w, (xs.max() + 1) / w
    bottom = min(0.985, (ys.max() + 1) / h + 0.06)
    return left, right, bottom


def main():
    vals = {}
    for key, name in SOURCES.items():
        src = os.path.join(ASSETS, name)
        uri, w, h = encode(src)
        vals["IMG_" + key] = uri
        print(f"{key}: {name} -> {w}x{h}, {len(uri) // 1024} KB")
        if key == "CLOSED":
            vals["AR_CLOSED"] = f"{w / h:.5f}"
            l, r, b = door_box(src)
            vals["DOOR_L"], vals["DOOR_R"], vals["DOOR_B"] = f"{l:.4f}", f"{r:.4f}", f"{b:.4f}"
            print(f"door: left {l:.3f} right {r:.3f} bottom {b:.3f}")

    tpl = open(os.path.join(HERE, "invitation.tpl.html"), encoding="utf-8").read()
    for k, v in vals.items():
        tpl = tpl.replace("%%" + k + "%%", v)
    assert "%%" not in tpl, "unreplaced placeholder remains"
    open(OUT, "w", encoding="utf-8").write(tpl)
    print("wrote", os.path.abspath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
