"""Futura as SVG paths, from scripts/futura_glyphs.json (see make_glyphs.py).

    from futura import text, width
    text("Hello", "heavy", 24, x, y, anchor="middle", fill="#fff")  ->  '<path d="..." fill="#fff"/>'
"""
import json
import os
import re

_G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "futura_glyphs.json"), encoding="utf-8"))
_NUM = re.compile(r"-?\d+(?:\.\d+)?(?:e-?\d+)?")


def width(s, cut="book", size=16, spacing=0.0):
    f = _G[cut]
    k = size / f["upm"]
    w = 0.0
    for i, ch in enumerate(s):
        g = f["glyphs"].get(ch) or f["glyphs"]["?"]
        w += g["w"] * k + spacing
        if i + 1 < len(s):
            w += f["kern"].get(ch + s[i + 1], 0) * k
    return w - (spacing if s else 0)


def _move(d, k, dx, dy):
    """Scale a glyph's path by k and shift it; its commands are absolute (M L H V Q C Z)."""
    out, xy, cmd = [], 0, "M"
    for tok in re.findall(r"[A-Za-z]|-?\d+(?:\.\d+)?(?:e-?\d+)?", d):
        if tok.isalpha():
            out.append(tok); xy = 0; cmd = tok
        else:
            is_x = cmd == "H" or (cmd != "V" and xy % 2 == 0)
            v = float(tok) * k + (dx if is_x else dy)
            out.append(f"{v:.2f}".rstrip("0").rstrip(".")); xy += 1
    return re.sub(r" (?=[A-Za-z])|(?<=[A-Za-z]) ", "", " ".join(out))


def text(s, cut="book", size=16, x=0.0, y=0.0, anchor="start", fill="#ffffff", spacing=0.0, extra=""):
    f = _G[cut]
    k = size / f["upm"]
    w = width(s, cut, size, spacing)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    parts = []
    for i, ch in enumerate(s):
        g = f["glyphs"].get(ch) or f["glyphs"]["?"]
        if g["d"]:
            parts.append(_move(g["d"], k, x, y))
        x += g["w"] * k + spacing
        if i + 1 < len(s):
            x += f["kern"].get(ch + s[i + 1], 0) * k
    return f'<path d="{"".join(parts)}" fill="{fill}"{extra}/>' if parts else ""
