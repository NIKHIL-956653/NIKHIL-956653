#!/usr/bin/env python3
"""Render data/contributions.json as assets/contribution-heatmap.svg.

A GitHub-style year grid in the profile's navy-and-cyan theme, with the headline numbers
(contributions, active days, longest streak, busiest day) computed from the data.
Standard library only.

    python scripts/build_heatmap.py
"""
from __future__ import annotations

import datetime as dt
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contribution-heatmap.svg"

W, H = 1200, 410
C = dict(bg0="#070B14", bg1="#0C1527", surf2="#122036", line="#1E2E4A", line2="#2B4166",
         txt="#EAF2FF", muted="#93A6C4", dim="#5F7394", cyan="#22D3EE", cyan2="#67E8F9")
LEVELS = ["#121D32", "#155E75", "#0E8BA8", "#22D3EE", "#C6F7FF"]  # none → most
SERIF = 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def nice(d: dt.date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def level(count: int, top: int) -> int:
    if count <= 0:
        return 0
    if top <= 0:
        return 1
    q = count / top
    return 1 if q <= .25 else 2 if q <= .5 else 3 if q <= .75 else 4


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = sorted(data["days"], key=lambda d: d["date"])
    counts = {dt.date.fromisoformat(d["date"]): int(d["count"]) for d in days}
    first, last = min(counts), max(counts)
    login = data.get("login", "")

    # ---- numbers
    total = sum(counts.values())
    active = sum(1 for v in counts.values() if v > 0)
    top_day = max(counts, key=lambda d: (counts[d], d))
    best, run, run_start, best_range = 0, 0, None, (None, None)
    d = first
    while d <= last:
        if counts.get(d, 0) > 0:
            run_start = run_start or d
            run += 1
            if run > best:
                best, best_range = run, (run_start, d)
        else:
            run, run_start = 0, None
        d += dt.timedelta(days=1)

    # ---- grid geometry (columns are weeks starting on Sunday, like GitHub)
    first_sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    cols = (last - first_sunday).days // 7 + 1
    x0, y0 = 128, 184
    pitch = min(19, (1016) // cols)
    cell = pitch - 4
    grid_w = cols * pitch - 4

    cells, month_labels = [], []
    seen_month = None
    for col in range(cols):
        week_start = first_sunday + dt.timedelta(days=7 * col)
        # label the column that contains the first of a month
        for k in range(7):
            day = week_start + dt.timedelta(days=k)
            if first <= day <= last and day.day == 1 or (col == 0 and k == 0 and day >= first):
                key = (day.year, day.month)
                if key != seen_month:
                    month_labels.append((col, MONTHS[day.month - 1]))
                    seen_month = key
                break
        for row in range(7):
            day = week_start + dt.timedelta(days=row)
            if day < first or day > last:
                continue
            n = counts.get(day, 0)
            lv = level(n, counts[top_day])
            x, y = x0 + col * pitch, y0 + row * pitch
            title = f"{n} contribution{'s' if n != 1 else ''} on {nice(day)}"
            extra = f' stroke="{C["cyan2"]}" stroke-width="1.5"' if day == last else (f' stroke="{C["line"]}"' if lv == 0 else "")
            cells.append(f'<rect class="hm-c" style="animation-delay:{col * .018:.3f}s" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" '
                         f'fill="{LEVELS[lv]}"{extra}><title>{esc(title)}</title></rect>')
    # drop a first-column label that sits on top of the next one
    if len(month_labels) > 1 and month_labels[1][0] - month_labels[0][0] < 3:
        month_labels.pop(0)

    label = (f"GitHub contribution calendar for @{login}: {total} contributions between {nice(first)} and {nice(last)}, "
             f"{active} active days, longest streak {best} days ({nice(best_range[0])} to {nice(best_range[1])}), "
             f"busiest day {nice(top_day)} with {counts[top_day]} contributions. Refreshed daily.")

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}">',
           f"""<defs>
<linearGradient id="hm-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>
<radialGradient id="hm-glow" cx=".15" cy=".2" r=".8"><stop offset="0" stop-color="{C['cyan']}" stop-opacity=".16"/><stop offset=".5" stop-color="{C['cyan']}" stop-opacity=".04"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/></radialGradient>
<pattern id="hm-grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{C['line2']}" opacity=".5"/></pattern>
<linearGradient id="hm-sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".22"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<clipPath id="hm-clip"><rect x="{x0 - 2}" y="{y0 - 2}" width="{grid_w + 4}" height="{7 * pitch}"/></clipPath>
</defs>
<style>
.hm-serif{{font-family:{SERIF}}}.hm-sans{{font-family:{SANS}}}.hm-mono{{font-family:{MONO}}}
.hm-in{{animation:hm-in 1s cubic-bezier(.16,1,.3,1) both}}.hm-d1{{animation-delay:.15s}}.hm-d2{{animation-delay:.3s}}
.hm-c{{animation:hm-c .6s ease-out both}}
.hm-sweep{{animation:hm-sweep 9s cubic-bezier(.45,0,.55,1) 2s infinite}}
@keyframes hm-in{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
@keyframes hm-c{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
@keyframes hm-sweep{{0%{{transform:translateX(0)}}60%{{transform:translateX({grid_w + 240}px)}}100%{{transform:translateX({grid_w + 240}px)}}}}
@media (prefers-reduced-motion:reduce){{.hm-in,.hm-c,.hm-sweep{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" rx="24" fill="url(#hm-bg)"/><rect width="{W}" height="{H}" rx="24" fill="url(#hm-grid)"/><rect width="{W}" height="{H}" rx="24" fill="url(#hm-glow)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" stroke="{C['line']}"/>"""]

    # header
    out.append(f'<g class="hm-in"><text class="hm-mono" x="56" y="66" font-size="11" letter-spacing="3" fill="{C["cyan"]}">COMMIT LOG · REAL GITHUB ACTIVITY</text>'
               f'<text class="hm-serif" x="56" y="104" font-size="27" font-weight="300" fill="{C["txt"]}">Twelve months, <tspan font-style="italic" fill="{C["cyan2"]}">one commit</tspan> at a time.</text></g>')
    stats = [("CONTRIBUTIONS", f"{total:,}", f"{MONTHS[first.month - 1]} {first.year} – {MONTHS[last.month - 1]} {last.year}"),
             ("ACTIVE DAYS", f"{active}", f"of {len(counts)} days"),
             ("LONGEST STREAK", f"{best}", "consecutive days"),
             ("BUSIEST DAY", f"{counts[top_day]}", nice(top_day))]
    xs = [640, 782, 924, 1074]
    for (k, v, s), x in zip(stats, xs):
        out.append(f'<g class="hm-in hm-d1"><text class="hm-mono" x="{x}" y="58" font-size="10" letter-spacing="2.1" fill="{C["cyan"]}">{esc(k)}</text>'
                   f'<text class="hm-serif" x="{x}" y="100" font-size="40" font-weight="300" letter-spacing="-1" fill="{C["txt"]}">{esc(v)}</text>'
                   f'<text class="hm-sans" x="{x}" y="121" font-size="11.5" fill="{C["muted"]}">{esc(s)}</text></g>')

    # month + day labels, cells, sweep
    out.append('<g class="hm-in hm-d2">')
    for col, name in month_labels:
        out.append(f'<text class="hm-sans" x="{x0 + col * pitch}" y="{y0 - 14}" font-size="11.5" fill="{C["muted"]}">{name}</text>')
    for row, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        out.append(f'<text class="hm-sans" x="{x0 - 14}" y="{y0 + row * pitch + cell - 3}" text-anchor="end" font-size="11.5" fill="{C["muted"]}">{name}</text>')
    out.append("</g>")
    out.extend(cells)
    out.append(f'<g clip-path="url(#hm-clip)"><rect class="hm-sweep" x="{x0 - 240}" y="{y0 - 2}" width="200" height="{7 * pitch}" fill="url(#hm-sweep)"/></g>')

    # streak bracket
    if best_range[0]:
        sx = x0 + ((best_range[0] - first_sunday).days // 7) * pitch
        ex = x0 + ((best_range[1] - first_sunday).days // 7) * pitch + cell
        gy = y0 + 7 * pitch + 6
        out.append(f'<g class="hm-in hm-d2"><path d="M{sx} {gy} v6 H{ex} v-6" fill="none" stroke="{C["cyan"]}" stroke-opacity=".8"/>'
                   f'<text class="hm-mono" x="{(sx + ex) / 2:.0f}" y="{gy + 26}" text-anchor="middle" font-size="10.5" letter-spacing="2.4" fill="{C["cyan2"]}">'
                   f'LONGEST STREAK · {best} DAYS · {nice(best_range[0]).upper()} – {nice(best_range[1]).upper()}</text></g>')

    # footer: source + legend
    out.append(f'<text class="hm-sans" x="56" y="{H - 28}" font-size="11.5" fill="{C["dim"]}">Source: public GitHub contribution calendar for @{esc(login)} · snapshot {nice(last)} · refreshed daily by GitHub Actions</text>')
    lx = 1144 - 5 * 18 - 40
    out.append(f'<text class="hm-sans" x="{lx - 8}" y="{H - 28}" text-anchor="end" font-size="11.5" fill="{C["dim"]}">Less</text>')
    for i, colr in enumerate(LEVELS):
        stroke = f' stroke="{C["line"]}"' if i == 0 else ""
        out.append(f'<rect x="{lx + i * 18}" y="{H - 39}" width="14" height="14" rx="3.5" fill="{colr}"{stroke}/>')
    out.append(f'<text class="hm-sans" x="{lx + 5 * 18 + 6}" y="{H - 28}" font-size="11.5" fill="{C["dim"]}">More</text>')
    out.append("</svg>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {total} contributions, {active} active days, streak {best}, busiest {nice(top_day)} ({counts[top_day]})")


if __name__ == "__main__":
    main()
