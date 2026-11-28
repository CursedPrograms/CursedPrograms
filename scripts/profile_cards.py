#!/usr/bin/env python3
"""The profile README's cards, made here instead of by github-readme-stats / streak-stats on Vercel
(their public instances are paused or rate-limited, and they can't do Futura).

    GITHUB_TOKEN=... python scripts/profile_cards.py [user]        images/stats.svg, streak.svg, top-langs.svg
    python scripts/profile_cards.py --headers                       images/brand/h-*.svg (section headers)

Corporate look: primary blue #005184 panels, white Futura, pink #f088e9 lines; solid colours,
no gradients, no shadows. Futura is drawn as paths (scripts/futura.py), so it shows on GitHub.
The GitHub Action in .github/workflows/top-langs.yml runs it every day and commits the SVGs.
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from futura import text, width  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL, DARK, LINE, PINK, WHITE, MUTED = "#005184", "#004067", "#34A9E3", "#f088e9", "#ffffff", "#c2c2c2"
SKIP = {"Batchfile", "PowerShell", "Shell", "Makefile", "CMake", "Dockerfile"}  # glue, not "languages"
LANG_COLOURS = {
    "Python": "#3572A5", "C#": "#178600", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#663399",
    "C++": "#f34b7d", "C": "#555555", "ShaderLab": "#222c37", "HLSL": "#aace60", "TypeScript": "#3178c6",
    "Java": "#b07219", "Julia": "#a270ba", "Rust": "#dea584", "Go": "#00ADD8", "Kotlin": "#A97BFF",
    "Jupyter Notebook": "#DA5B0B", "GLSL": "#5686a5", "Lua": "#000080", "PHP": "#4F5D95",
}
FALLBACK = [PINK, "#34A9E3", "#168FCC", "#c2c2c2", "#f82098", "#ffffff"]
FADE = ("<style>@keyframes in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }"
        ".a { animation: in .6s ease both; } .b { animation-delay: .15s; } .c { animation-delay: .3s; }"
        ".d { animation-delay: .45s; } .e { animation-delay: .6s; } .f { animation-delay: .75s; }</style>")


# ---------- GitHub ----------

def _req(url, body=None):
    req = urllib.request.Request(url, data=body, headers={"Accept": "application/vnd.github+json",
                                                          "User-Agent": "cursed-profile-cards"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    for attempt in range(4):  # the API sometimes drops a connection; try again
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def gql(query, **v):
    d = _req("https://api.github.com/graphql", json.dumps({"query": query, "variables": v}).encode())
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


def repos(user):
    out, cur = [], None
    while True:
        d = gql("""query($u:String!,$c:String){ user(login:$u){ repositories(first:100, after:$c,
                   ownerAffiliations:OWNER, privacy:PUBLIC){ pageInfo{hasNextPage endCursor}
                   nodes{ name isFork isArchived stargazerCount forkCount } } } }""", u=user, c=cur)
        r = d["user"]["repositories"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]:
            return out
        cur = r["pageInfo"]["endCursor"]


def stats(user, rs):
    year = dt.date.today().year
    d = gql("""query($u:String!,$from:DateTime!){ user(login:$u){ followers{totalCount}
               pullRequests{totalCount}
               contributionsCollection(from:$from){ totalCommitContributions restrictedContributionsCount } } }""",
            u=user, **{"from": f"{year}-01-01T00:00:00Z"})["user"]
    own = [r for r in rs if not r["isFork"]]
    return {
        "Stars earned": sum(r["stargazerCount"] for r in own),
        f"Commits in {year}": d["contributionsCollection"]["totalCommitContributions"]
                               + d["contributionsCollection"]["restrictedContributionsCount"],
        "Public repos": len(own),
        "Pull requests": d["pullRequests"]["totalCount"],
        "Forks": sum(r["forkCount"] for r in own),
        "Followers": d["followers"]["totalCount"],
    }


def days(user):
    years = gql("query($u:String!){ user(login:$u){ contributionsCollection{ contributionYears } } }",
                u=user)["user"]["contributionsCollection"]["contributionYears"]
    out = {}
    for y in sorted(years):
        cal = gql("""query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){ contributionsCollection(from:$f,to:$t){
                     contributionCalendar{ weeks{ contributionDays{ date contributionCount } } } } } }""",
                  u=user, f=f"{y}-01-01T00:00:00Z", t=f"{y}-12-31T23:59:59Z")
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for day in w["contributionDays"]:
                out[day["date"]] = day["contributionCount"]
    return dict(sorted(out.items()))


def streaks(cal):
    today = dt.date.today().isoformat()
    ds = [d for d in cal if d <= today]
    total = sum(cal[d] for d in ds)
    first = next((d for d in ds if cal[d]), ds[0] if ds else today)
    best, run, start, best_range = 0, 0, None, (today, today)
    for d in ds:
        if cal[d]:
            run, start = run + 1, start or d
            if run > best:
                best, best_range = run, (start, d)
        else:
            run, start = 0, None
    cur, i = 0, len(ds) - 1
    if i >= 0 and not cal[ds[i]]:
        i -= 1  # today doesn't break the streak until it's over
    end = ds[i] if i >= 0 else today
    while i >= 0 and cal[ds[i]]:
        cur, i = cur + 1, i - 1
    cur_range = (ds[i + 1] if cur else end, end)
    return total, first, cur, cur_range, best, best_range


def language_totals(user, rs):
    names = [r["name"] for r in rs if not (r["isFork"] or r["isArchived"])]
    totals = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for langs in pool.map(lambda n: _req(f"https://api.github.com/repos/{user}/{n}/languages"), names):
            for lang, size in langs.items():
                if lang not in SKIP:
                    totals[lang] = totals.get(lang, 0) + size
    return totals


# ---------- drawing ----------

def fmt(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 10000 else f"{n:,}"


def day(d):
    return dt.date.fromisoformat(d).strftime("%d %b %Y").lstrip("0")


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{label}">\n<title>{label}</title>\n{FADE}\n'
            f'<rect width="{w}" height="{h}" rx="10" fill="{PANEL}"/>\n' + "\n".join(body) + "\n</svg>\n")


def title(s, w):
    tw = width(s, "heavy", 20, 1.5)
    return [text(s, "heavy", 20, 30, 42, fill=WHITE, spacing=1.5),
            f'<rect x="30" y="52" width="{tw:.1f}" height="3" fill="{PINK}"/>']


def stats_card(st):
    w, h = 590, 220
    body = title("GITHUB STATS", w)
    cls = "abcdef"
    for i, (label, n) in enumerate(st.items()):
        col, row = i % 3, i // 3
        cx, y = 30 + col * 185, 112 + row * 76
        body.append(f'<g class="a {cls[i]}">' + text(fmt(n), "black", 34, cx, y, fill=PINK if i == 0 else WHITE)
                    + text(label.upper(), "light", 11, cx, y + 20, fill=MUTED, spacing=2) + "</g>")
    return svg(w, h, "GitHub stats", body)


def langs_card(totals, count=6):
    w, h = 590, 220
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:count]
    total = sum(v for _, v in top) or 1
    body = title("MOST USED LANGUAGES", w)
    bx, by, bw, bh = 30, 78, w - 60, 10
    body += [f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5"/></clipPath>',
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" fill="{DARK}"/>', '<g clip-path="url(#bar)">']
    x = float(bx)
    colour = {lang: LANG_COLOURS.get(lang, FALLBACK[i % len(FALLBACK)]) for i, (lang, _) in enumerate(top)}
    for lang, size in top:
        sw = bw * size / total
        body.append(f'<rect x="{x:.2f}" y="{by}" width="{sw + 0.5:.2f}" height="{bh}" fill="{colour[lang]}"/>')
        x += sw
    body.append("</g>")
    cls = "abcdef"
    for i, (lang, size) in enumerate(top):
        col, row = i % 2, i // 2
        lx, ly = 30 + col * 270, 130 + row * 32
        pct = f"{100 * size / total:.1f}%"
        body.append(f'<g class="a {cls[i]}"><rect x="{lx}" y="{ly - 11}" width="12" height="12" rx="3" fill="{colour[lang]}"/>'
                    + text(lang, "book", 16, lx + 22, ly, fill=WHITE)
                    + text(pct, "light", 14, lx + 22 + width(lang, "book", 16) + 10, ly, fill=MUTED) + "</g>")
    return svg(w, h, "Most used languages", body)


def streak_card(total, first, cur, cur_range, best, best_range):
    w, h = 1200, 190
    cols = [(fmt(total), "TOTAL CONTRIBUTIONS", f"{day(first)} – present", WHITE),
            (fmt(cur), "CURRENT STREAK", f"{day(cur_range[0])} – {day(cur_range[1])}" if cur else "Back tomorrow", PINK),
            (fmt(best), "LONGEST STREAK", f"{day(best_range[0])} – {day(best_range[1])}", WHITE)]
    body = []
    for i, (big, label, sub, colr) in enumerate(cols):
        cx = 200 + i * 400
        if i:
            body.append(f'<rect x="{cx - 200}" y="40" width="1" height="110" fill="{LINE}"/>')
        if i == 1:
            body.append(f'<circle cx="{cx}" cy="70" r="40" fill="none" stroke="{PINK}" stroke-width="4"/>')
            body.append(f'<g class="a b">' + text(big, "black", 34, cx, 82, "middle", colr) + "</g>")
            body.append(text(label, "heavy", 14, cx, 140, "middle", WHITE, 2.5))
            body.append(text(sub, "light", 13, cx, 162, "middle", MUTED, 1))
        else:
            body.append(f'<g class="a {"ac"[i // 2]}">' + text(big, "black", 46, cx, 92, "middle", colr) + "</g>")
            body.append(text(label, "heavy", 14, cx, 130, "middle", WHITE, 2.5))
            body.append(text(sub, "light", 13, cx, 152, "middle", MUTED, 1))
    return svg(w, h, "Contribution streak", body)


def journey_card(cal, st, joined):
    """Contributions month by month since joining: an area chart with the totals beside it."""
    w, h = 1200, 300
    months = {}
    for d, n in cal.items():
        if d >= joined[:10]:
            months[d[:7]] = months.get(d[:7], 0) + n
    keys = sorted(months)
    body = title("GITHUB JOURNEY", w)
    if not keys:
        return svg(w, h, "GitHub journey", body)
    vals = [months[k] for k in keys]
    top = max(vals) or 1
    # the facts, down the left
    j = dt.date.fromisoformat(joined[:10])
    facts = [(j.strftime("%b %Y").upper(), "JOINED"), (fmt(sum(vals)), "CONTRIBUTIONS"),
             (fmt(st.get("Public repos", 0)), "PUBLIC REPOS"), (fmt(max(vals)), "BEST MONTH")]
    for i, (big, label) in enumerate(facts):
        y = 100 + i * 50
        body.append(f'<g class="a {"abcd"[i]}">' + text(big, "heavy", 22, 30, y, fill=PINK if i == 1 else WHITE)
                    + text(label, "light", 10, 30, y + 16, fill=MUTED, spacing=2) + "</g>")
    # the chart, on the right
    x0, x1, y0, y1 = 250, w - 30, 250, 75
    step = (x1 - x0) / max(1, len(vals) - 1)
    pts = [(x0 + i * step, y0 - (y0 - y1) * v / top) for i, v in enumerate(vals)]
    for frac in (0.25, 0.5, 0.75, 1.0):
        gy = y0 - (y0 - y1) * frac
        body.append(f'<rect x="{x0}" y="{gy:.1f}" width="{x1 - x0}" height="1" fill="{DARK}"/>')
    area = f"M{x0},{y0} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f" L{x1},{y0} Z"
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    body.append(f'<path d="{area}" fill="{PINK}" fill-opacity="0.22"/>')
    body.append(f'<path class="draw" d="{line}" fill="none" stroke="{PINK}" stroke-width="2.5" stroke-linejoin="round"/>')
    body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="1.5" fill="{LINE}"/>')
    for i, k in enumerate(keys):                       # the year under each January (and the first month)
        if i == 0 or k.endswith("-01"):
            x = x0 + i * step
            body.append(f'<rect x="{x:.1f}" y="{y0}" width="1" height="6" fill="{LINE}"/>')
            body.append(text(k[:4], "light", 11, x, y0 + 22, "middle", MUTED, 1.5))
    peak = max(range(len(vals)), key=lambda i: vals[i])
    px, py = pts[peak]
    body.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{WHITE}"/>')
    body.append(text(dt.date.fromisoformat(keys[peak] + "-01").strftime("%b %Y").upper(), "light", 10,
                     min(max(px, x0 + 40), x1 - 40), py - 10, "middle", WHITE, 1.5))
    out = svg(w, h, "GitHub journey: contributions per month", body)
    # the line draws itself in, left to right
    return out.replace("</style>", " .draw { stroke-dasharray: 4000; stroke-dashoffset: 4000; animation: draw 2.2s ease .2s forwards; }"
                       " @keyframes draw { to { stroke-dashoffset: 0; } }</style>", 1)


def header(label):
    """A section header like images/brand/h-games.svg: white Futura Heavy on primary blue, pink line sweeping in."""
    tw = width(label, "heavy", 24, 6)
    x0 = 600 - tw / 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="64" viewBox="0 0 1200 64">\n'
            '<style>@keyframes sweep { from { transform: scaleX(0); } to { transform: scaleX(1); } }\n'
            '.line { transform-origin: 600.0px 0; animation: sweep .9s ease .2s both; }</style>\n'
            f'<rect width="1200" height="64" rx="10" fill="{PANEL}"/>\n'
            + text(label, "heavy", 24, 600, 42, "middle", WHITE, 6) + "\n"
            f'<rect class="line" x="{x0:.3f}" y="52" width="{tw:.3f}" height="3" fill="{PINK}"/>\n</svg>\n')


def button(label, fill, stroke, text_col, w=300):
    """A link button like images/brand/b-*.svg: rounded tab, thin border, Futura Heavy label drawn as paths."""
    h = 52
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label.title()}">\n'
            f'<title>{label.title()}</title>\n'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" ry="5" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n'
            + text(label, "light", 15, w / 2, 32, "middle", text_col, 3.0) + "\n</svg>\n")


def write(path, s):
    path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("wrote", path)


if __name__ == "__main__":
    if "--headers" in sys.argv:
        for name, label in {"h-stats": "STATS", "h-robots": "ROBOTICS", "h-atelier": "CREATIVE TOOLS",
                            "h-ai": "AI", "h-games": "GAMES", "h-made": "MADE WITH", "h-find": "FIND CURSED"}.items():
            write(f"images/brand/{name}.svg", header(label))
        sys.exit()
    if "--buttons" in sys.argv:
        write("images/brand/b-repos.svg", button("EXPLORE REPOSITORIES", PINK, WHITE, "#14141c", 320))
        write("images/brand/b-follow.svg", button("FOLLOW CURSEDPROGRAMS", "#007ab7", WHITE, WHITE, 340))
        sys.exit()
    user = sys.argv[1] if len(sys.argv) > 1 else "CursedPrograms"
    rs = repos(user)
    st = stats(user, rs)
    cal = days(user)
    joined = gql("query($u:String!){ user(login:$u){ createdAt } }", u=user)["user"]["createdAt"]
    write("images/stats.svg", stats_card(st))
    write("images/streak.svg", streak_card(*streaks(cal)))
    write("images/journey.svg", journey_card(cal, st, joined))
    write("images/top-langs.svg", langs_card(language_totals(user, rs)))
