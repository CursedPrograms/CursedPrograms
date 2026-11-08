#!/usr/bin/env python3
"""Top Languages card for the profile README, without github-readme-stats / Vercel.

Adds up the language bytes of every public, non-fork repo the user owns (GitHub API) and
writes a small SVG card: solid colours, no gradients, no shadows.

    GITHUB_TOKEN=... python scripts/top_langs.py [user] [out.svg] [count]

The GitHub Action in .github/workflows/top-langs.yml runs it every day and commits the SVG.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html import escape

USER = sys.argv[1] if len(sys.argv) > 1 else "CursedPrograms"
OUT = sys.argv[2] if len(sys.argv) > 2 else "images/top-langs.svg"
COUNT = int(sys.argv[3]) if len(sys.argv) > 3 else 6
SKIP = {"Batchfile", "PowerShell", "Shell", "Makefile", "CMake", "Dockerfile"}  # glue, not "languages"

# Cursed colours
BG, BORDER, TITLE, TEXT, DIM = "#14141c", "#e0408a", "#e0408a", "#e6e6ee", "#9a9aae"
# GitHub's own language colours for the usual suspects, so the card reads like GitHub's
LANG_COLOURS = {
    "Python": "#3572A5", "C#": "#178600", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#663399",
    "C++": "#f34b7d", "C": "#555555", "ShaderLab": "#222c37", "HLSL": "#aace60", "TypeScript": "#3178c6",
    "Java": "#b07219", "Julia": "#a270ba", "Rust": "#dea584", "Go": "#00ADD8", "Kotlin": "#A97BFF",
    "Jupyter Notebook": "#DA5B0B", "GLSL": "#5686a5", "Lua": "#000080", "PHP": "#4F5D95", "Red": "#f50000",
    "F#": "#b845fc", "Ballerina": "#FF5000", "Objective-C": "#438eff", "Swift": "#F05138", "Dart": "#00B4AB",
}
FALLBACK = ["#e0408a", "#007ab7", "#34A9E3", "#f088e9", "#c2c2c2", "#5eead4"]


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    for attempt in range(4):  # the API sometimes drops a connection; try again
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def language_totals(user):
    names, page = [], 1
    while True:
        repos = api(f"/users/{user}/repos?type=owner&per_page=100&page={page}")
        if not repos:
            break
        names += [r["name"] for r in repos if not (r["fork"] or r.get("archived") or r.get("private"))]
        page += 1
    totals = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for langs in pool.map(lambda n: api(f"/repos/{user}/{n}/languages"), names):
            for lang, size in langs.items():
                if lang not in SKIP:
                    totals[lang] = totals.get(lang, 0) + size
    return totals


def card(totals, count):
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:count]
    total = sum(v for _, v in top) or 1
    width, pad, bar_y, bar_h = 350, 25, 55, 8
    rows = (len(top) + 1) // 2
    height = bar_y + bar_h + 22 + rows * 25 + 10
    colour = {}
    for i, (lang, _) in enumerate(top):
        colour[lang] = LANG_COLOURS.get(lang, FALLBACK[i % len(FALLBACK)])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Most used languages">',
        "<title>Most used languages</title>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6" fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="{pad}" y="35" fill="{TITLE}" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif" font-size="18" font-weight="600">Most Used Languages</text>',
        f'<clipPath id="bar"><rect x="{pad}" y="{bar_y}" width="{width - 2 * pad}" height="{bar_h}" rx="4"/></clipPath>',
        '<g clip-path="url(#bar)">',
    ]
    x, bar_w = float(pad), width - 2 * pad
    for lang, size in top:
        w = bar_w * size / total
        parts.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{w + 0.5:.2f}" height="{bar_h}" fill="{colour[lang]}"/>')
        x += w
    parts.append("</g>")
    for i, (lang, size) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = pad + col * 155, bar_y + bar_h + 28 + row * 25
        parts.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{colour[lang]}"/>')
        parts.append(
            f'<text x="{lx + 16}" y="{ly}" fill="{TEXT}" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif" font-size="11">'
            f'{escape(lang)} <tspan fill="{DIM}">{100 * size / total:.1f}%</tspan></text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    svg = card(language_totals(USER), COUNT)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("wrote", OUT)
