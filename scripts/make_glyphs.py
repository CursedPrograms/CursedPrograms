#!/usr/bin/env python3
"""Builds scripts/futura_glyphs.json: the outlines of the characters the profile cards use, in four
Futura cuts. GitHub shows README pictures without their fonts, so the cards draw Futura as paths
(like the images/brand headers do); this keeps the font files themselves off GitHub.

Run on a PC with Futura installed (only needed again for new characters):

    python scripts/make_glyphs.py
"""
import json
import os
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
CUTS = {"light": "futura light bt.ttf", "book": "Futura Book font.ttf",
        "heavy": "Futura Heavy font.ttf", "black": "Futura Extra Black font.ttf"}
CHARS = "".join(chr(c) for c in range(32, 127)) + "©·–—’“”…"


def cut(path):
    f = TTFont(path)
    upm = f["head"].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    kern = {}
    if "kern" in f:
        for t in f["kern"].kernTables:
            kern.update({f"{a} {b}": v for (a, b), v in t.kernTable.items()})
    glyphs = {}
    for ch in CHARS:
        name = cmap.get(ord(ch))
        if not name:
            continue
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))  # y down, baseline at 0
        glyphs[ch] = {"d": pen.getCommands(), "w": hmtx[name][0], "n": name}
    names = {g["n"]: ch for ch, g in glyphs.items()}
    pairs = {}
    for k, v in kern.items():
        a, b = k.split(" ")
        if a in names and b in names:
            pairs[names[a] + names[b]] = v
    for g in glyphs.values():
        del g["n"]
    return {"upm": upm, "glyphs": glyphs, "kern": pairs}


if __name__ == "__main__":
    out = {k: cut(os.path.join(FONTS, v)) for k, v in CUTS.items()}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "futura_glyphs.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, separators=(",", ":"), ensure_ascii=False)
    print("wrote", p, os.path.getsize(p), "bytes")
