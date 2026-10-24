#!/usr/bin/env python3
"""Fetch a GitHub user's public contribution calendar into data/contributions.json.

Two sources, tried in order:
  1. GraphQL API  — when GITHUB_TOKEN is set (GitHub Actions provides one).
  2. The public calendar page github.com/users/<login>/contributions — no token needed.

Standard library only. On failure nothing is written and the exit code is 1, so the
committed snapshot stays in place and the heatmap is still rendered from it.

    GH_USERNAME=NIKHIL-956653 python scripts/fetch_contributions.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

LOGIN = os.environ.get("GH_USERNAME", "NIKHIL-956653")
OUT = Path(__file__).resolve().parents[1] / "data" / "contributions.json"
UA = "profile-readme-heatmap (+https://github.com/%s)" % LOGIN


def via_graphql(token: str) -> list[dict]:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    body = json.dumps({"query": query, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if data.get("errors"):
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [{"date": d["date"], "count": int(d["contributionCount"])} for w in weeks for d in w["contributionDays"]]


def via_html() -> list[dict]:
    url = f"https://github.com/users/{LOGIN}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 " + UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", "replace")

    # Day cells carry data-date and an id; a <tool-tip for="<id>"> holds the count in words.
    cells: dict[str, str] = {}
    for tag in re.findall(r"<td\b[^>]*\bdata-date=[^>]*>", page):
        date = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
        cid = re.search(r'\bid="([^"]+)"', tag)
        if date and cid:
            cells[cid.group(1)] = date.group(1)
    tips: dict[str, str] = {}
    for m in re.finditer(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>(.*?)</tool-tip>', page, re.S):
        tips[m.group(1)] = re.sub(r"\s+", " ", m.group(2)).strip()
    if not cells or not tips:
        raise RuntimeError("calendar markup not recognised (GitHub may have changed the page)")

    days = []
    for cid, date in cells.items():
        text = tips.get(cid, "")
        if text.lower().startswith("no contribution"):
            count = 0
        else:
            m = re.match(r"(\d[\d,]*)\s+contribution", text)
            if not m:
                raise RuntimeError(f"unexpected tooltip for {date}: {text!r}")
            count = int(m.group(1).replace(",", ""))
        days.append({"date": date, "count": count})
    return sorted(days, key=lambda d: d["date"])


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    errors = []
    days: list[dict] = []
    source = ""
    if token:
        try:
            days, source = via_graphql(token), "api.github.com/graphql"
        except Exception as e:  # noqa: BLE001 — any failure just means "try the page"
            errors.append(f"graphql: {e}")
    if not days:
        try:
            days, source = via_html(), f"github.com/users/{LOGIN}/contributions"
        except Exception as e:  # noqa: BLE001
            errors.append(f"html: {e}")
    if not days:
        print("fetch failed; keeping the committed snapshot\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1

    days.sort(key=lambda d: d["date"])
    payload = {
        "login": LOGIN,
        "fetched_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
        "from": days[0]["date"],
        "to": days[-1]["date"],
        "total": sum(d["count"] for d in days),
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=0) + "\n", encoding="utf-8")
    print(f"{LOGIN}: {payload['total']} contributions over {len(days)} days via {source} -> {OUT.relative_to(OUT.parents[1])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
