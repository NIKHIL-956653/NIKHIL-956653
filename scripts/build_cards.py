#!/usr/bin/env python3
"""Build the profile README cards (assets/*.svg).

Everything the cards say lives in CONTENT below. Edit it, run

    python scripts/build_cards.py

and commit the regenerated SVGs. No dependencies beyond the standard library.
The contribution heatmap is built separately by scripts/build_heatmap.py.
"""
from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
W = 1200

# --------------------------------------------------------------------------- content

CONTENT = {
    "name_line1": "Nikhil Chandra",
    "name_line2": "Sairam Tokala",
    "handle": "NIKHIL-956653",
    "eyebrow": "AI · ENGINEERING · DEVOPS",
    "role": "AI/ML ENGINEER · GENAI ENGINEER · DEVOPS",
    "tagline": "Agents, retrieval and the plumbing that makes them a product.",
    "strip_left": "DUBAI, UAE · AWS CERTIFIED ×2 · PG DEVOPS · PURDUE × EDUREKA",
    "strip_right": "AGENT PLATFORMS · ENTERPRISE RAG · DOCUMENT AI",
    "terminal_cmd": "~/nikhil $ build --agents",
    "orbit_nodes": ["AGENTS", "RAG", "OCR", "CI / CD", "AWS"],
    "monogram": "NT",
    # 01 about — terminal lines: (command, output)
    "about_lines": [
        ("whoami", "Nikhil Chandra Sairam Tokala · AI/ML Engineer · GenAI Engineer · DevOps"),
        ("cat focus.txt", "agent platforms · enterprise RAG · document AI · CI/CD on AWS"),
        ("ls ./shipped", "enterprise-agent-platform  docgen  medical-bill-ocr  rag-curriculum"),
        ("cat certifications.txt", "AWS Data Analytics – Specialty · AWS Developer – Associate · PG DevOps (Purdue)"),
        ("echo $PRINCIPLE", "treat the model as untrusted · verify locally · ship with tests"),
    ],
    "about_cards": [
        ("PRIMARY LANGUAGE", "Python", "FastAPI · typed · pytest-first"),
        ("WHERE THE AI LIVES", "Agents · RAG", "LangGraph · pgvector · Qdrant"),
        ("DRAWN TO", "DevOps", "Docker · GitHub Actions · AWS"),
    ],
    # 02 credentials
    "credentials": [
        ("CREDENTIAL 01 · AWS", "Data Analytics", "Specialty", "AWS Certified · Amazon Web Services"),
        ("CREDENTIAL 02 · AWS", "Developer", "Associate", "AWS Certified · Amazon Web Services"),
        ("CREDENTIAL 03 · PURDUE", "DevOps", "Post Graduate Program", "Purdue University · delivered by Edureka"),
    ],
    # 03 projects
    "projects": [
        {
            "file": "project-eap",
            "eyebrow": "01 · AI PLATFORM · MULTI-TENANT · 2026",
            "title": "Enterprise Agent Platform",
            "subtitle": ["Multi-tenant AI agents as a service — isolation, audit and", "durable runs, not just prompts."],
            "built": ["Postgres RLS tenant isolation · ABAC clearance inside the RLS predicate",
                      "hash-chained append-only audit log · Temporal workflows · Gemini + Anthropic providers"],
            "stats": [("10", "Alembic migrations"), ("4", "architecture ADRs"), ("160+", "tests, green in CI")],
            "chips": ["FastAPI", "SQLAlchemy 2.0", "pgvector", "Redis", "Temporal", "React"],
            "motif": "tenants",
            "alt": "Enterprise Agent Platform: multi-tenant AI agents as a service with Postgres RLS tenant isolation, ABAC clearance in the RLS predicate, hash-chained audit log, Temporal durable execution and Gemini plus Anthropic providers. 10 migrations, 4 ADRs, 160+ tests green in CI. FastAPI, SQLAlchemy 2.0, pgvector, Redis, Temporal, React.",
        },
        {
            "file": "project-docgen",
            "eyebrow": "02 · GENAI · DOCUMENT AUTOMATION · 2026",
            "title": "Document Writing Assistant",
            "subtitle": ["Jira ticket → LLM → a published Google Doc or Confluence page,", "with an evaluation gate in CI."],
            "built": ["6 YAML document templates · faithfulness / completeness / structure scoring with an LLM judge",
                      "HMAC-verified Jira webhook · in-place document updates with diffs · cloud or fully local LLM"],
            "stats": [("368", "offline tests"), ("95%", "coverage gate in CI"), ("6", "document types")],
            "chips": ["Python", "FastAPI", "Jira REST", "Google Docs API", "Ollama", "Docker"],
            "motif": "pipeline",
            "alt": "GenAI Document Writing Assistant: turns a Jira ticket into a published Google Doc or Confluence page using Gemini via OpenRouter or a local Ollama model. 6 YAML document templates, faithfulness and completeness evaluation with an LLM judge, HMAC-verified Jira webhook, in-place updates. 368 offline tests, 95% coverage gate, 6 document types. Python, FastAPI, Jira REST, Google Docs API, Ollama, Docker.",
        },
        {
            "file": "project-bill-ocr",
            "eyebrow": "03 · DOCUMENT AI · OCR · 2026",
            "title": "Medical Bill OCR",
            "subtitle": ["Scanned bills → validated, review-ready Excel.", "The LLM is treated as an untrusted component."],
            "built": ["OpenCV preprocess → Tesseract 5 → Gemini extraction → local arithmetic validation",
                      "review UI that highlights each value on the page · accuracy tracked by model and by week"],
            "stats": [("45", "offline tests"), ("±$0.05", "reconciliation tolerance"), ("300 DPI", "scan rasterization")],
            "chips": ["OpenCV", "Tesseract 5", "Gemini 2.5 Flash", "FastAPI", "pandas", "pytest"],
            "motif": "checks",
            "alt": "Medical Bill OCR: scanned photos and PDFs become validated Excel and CSV. OpenCV preprocessing, Tesseract 5 OCR, Gemini extraction, then local arithmetic validation; uncertain rows are flagged NEEDS_REVIEW. Review web UI highlights each value on the page. 45 offline tests, ±$0.05 reconciliation tolerance, 300 DPI rasterization. OpenCV, Tesseract 5, Gemini 2.5 Flash, FastAPI, pandas, pytest.",
        },
        {
            "file": "project-rag",
            "eyebrow": "04 · ENTERPRISE RAG · FULLY LOCAL · 2026",
            "title": "Enterprise RAG Pipeline",
            "subtitle": ["Hybrid retrieval over an 18-subject curriculum —", "the patterns that matter at scale, with no external APIs."],
            "built": ["BM25 + dense merged by RRF · parent-child chunking · contextual retrieval",
                      "cross-encoder rerank top-50 → top-5 · per-chunk ACL metadata · RAGAS evaluation"],
            "stats": [("~6,800", "pages ingested"), ("~20K", "chunks indexed"), ("50 → 5", "rerank funnel")],
            "chips": ["Qdrant", "Ollama", "nomic-embed", "BGE reranker", "RAGAS", "Streamlit"],
            "motif": "funnel",
            "alt": "Enterprise RAG Pipeline: a fully local hybrid retrieval system over an 18-subject curriculum of about 6,800 pages and 20K chunks. BM25 plus dense retrieval merged by RRF, parent-child chunking, contextual retrieval, cross-encoder reranking from top-50 to top-5, per-chunk ACL metadata and RAGAS evaluation. Qdrant, Ollama, nomic-embed, BGE reranker, RAGAS, Streamlit.",
        },
    ],
    # 04 toolkit — (label, line1 (primary), line2, line3)
    "toolkit": [
        ("01 LANGUAGES", "Python", "TypeScript · SQL", "Bash · PowerShell"),
        ("02 AI · LLM · AGENTS", "LangGraph · agents", "RAG · rerank · eval", "Gemini · Claude · Ollama"),
        ("03 BACKEND & APIS", "FastAPI · Pydantic", "SQLAlchemy · Alembic", "JWT · RLS · ABAC"),
        ("04 DATA & VECTORS", "Postgres · pgvector", "Qdrant · FAISS", "Redis · SQLite"),
        ("05 DEVOPS & CLOUD", "Docker · Compose", "GitHub Actions CI", "AWS · Temporal"),
        ("06 FRONTEND & QUALITY", "React · Vite · TS", "Streamlit", "pytest · ruff · mypy"),
    ],
    # section titles: (number, kicker, headline, italic part, right label)
    "titles": [
        ("01", "ABOUT", "Hello, I'm ", "Nikhil.", "WHO I AM"),
        ("02", "CREDENTIALS", "Certified, ", "on the record.", "VERIFIABLE"),
        ("03", "SELECTED WORK", "Systems, ", "not scripts.", "SHIPPED · PUBLIC REPOS"),
        ("04", "TOOLKIT", "What I ", "reach for.", "STACK"),
        ("05", "COMMIT LOG", "A year of ", "shipping.", "REFRESHED DAILY"),
        ("06", "CONNECT", "Let's build ", "something real.", "SAY HELLO"),
    ],
    "footer_name": "Nikhil",
    "footer_tagline": "Building AI that holds up in production.",
    "footer_meta": "GITHUB.COM/NIKHIL-956653 · DUBAI, UAE",
}

# --------------------------------------------------------------------------- theme

C = dict(
    bg0="#070B14", bg1="#0C1527", surf="#0E1A2E", surf2="#122036",
    line="#1E2E4A", line2="#2B4166",
    txt="#EAF2FF", muted="#93A6C4", dim="#5F7394",
    cyan="#22D3EE", cyan2="#67E8F9", cyan3="#C6F7FF", teal="#2DD4BF", amber="#F4B860",
)
SERIF = 'Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif'
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text_w(s: str, size: float, kind: str = "sans") -> float:
    """Rough width estimate (the viewer's fonts decide the real width)."""
    k = {"sans": 0.56, "serif": 0.54, "mono": 0.62}[kind]
    return len(s) * size * k


def head(w: int, h: int, label: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">')


def style(p: str, extra: str = "") -> str:
    return f"""<style>
.{p}-serif{{font-family:{SERIF}}}.{p}-sans{{font-family:{SANS}}}.{p}-mono{{font-family:{MONO}}}
.{p}-in{{animation:{p}-in 1s cubic-bezier(.16,1,.3,1) both}}
.{p}-d1{{animation-delay:.12s}}.{p}-d2{{animation-delay:.24s}}.{p}-d3{{animation-delay:.36s}}.{p}-d4{{animation-delay:.48s}}.{p}-d5{{animation-delay:.6s}}.{p}-d6{{animation-delay:.72s}}.{p}-d7{{animation-delay:.84s}}.{p}-d8{{animation-delay:.96s}}
.{p}-draw{{stroke-dasharray:1400;animation:{p}-draw 1.6s cubic-bezier(.65,0,.35,1) .4s both}}
@keyframes {p}-in{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
@keyframes {p}-draw{{from{{stroke-dashoffset:1400}}to{{stroke-dashoffset:0}}}}
.{p}-band{{animation:{p}-band 7s cubic-bezier(.4,0,.6,1) 1.4s infinite}}
@keyframes {p}-band{{0%{{transform:translateX(0)}}40%{{transform:translateX(1600px)}}100%{{transform:translateX(1600px)}}}}
@media (prefers-reduced-motion:reduce){{.{p}-in,.{p}-draw,.{p}-band{{animation:none}}}}
{extra}</style>"""


def panel(p: str, w: int, h: int, glow_cx: float = 0.85, glow_cy: float = 0.1) -> str:
    return f"""<defs>
<linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>
<radialGradient id="{p}-glow" cx="{glow_cx}" cy="{glow_cy}" r="0.75"><stop offset="0" stop-color="{C['cyan']}" stop-opacity=".17"/><stop offset=".45" stop-color="{C['cyan']}" stop-opacity=".04"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/></radialGradient>
<pattern id="{p}-grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{C['line2']}" opacity=".5"/></pattern>
<linearGradient id="{p}-rule" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="1160" y2="0"><stop offset="0" stop-color="{C['cyan']}"/><stop offset=".55" stop-color="{C['line2']}"/><stop offset="1" stop-color="{C['line2']}" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}-sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<radialGradient id="{p}-dot"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="{C['cyan2']}" stop-opacity=".7"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{w}" height="{h}" rx="24" fill="url(#{p}-bg)"/>
<rect width="{w}" height="{h}" rx="24" fill="url(#{p}-grid)"/>
<rect width="{w}" height="{h}" rx="24" fill="url(#{p}-glow)"/>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="23.5" fill="none" stroke="{C['line']}"/>"""


def card(x: float, y: float, w: float, h: float, p: str, accent: bool = True, rx: int = 18) -> str:
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{C["surf"]}" stroke="{C["line"]}"/>'
    if accent:
        s += f'<path d="M{x + 26} {y + .5} H{x + w - 26}" stroke="{C["cyan"]}" stroke-opacity=".55" stroke-width="1.5"/>'
    return s


def chip(x: float, y: float, label: str, p: str, size: float = 12.5) -> tuple[float, str]:
    w = round(text_w(label, size) + 26)
    s = (f'<g><rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{C["surf2"]}" stroke="{C["line2"]}"/>'
         f'<text class="{p}-sans" x="{x + w / 2:.1f}" y="{y + 18.5}" text-anchor="middle" font-size="{size}" '
         f'fill="{C["cyan3"]}">{esc(label)}</text></g>')
    return w, s


def pulse_dot(x1: float, x2: float, y: float, p: str, dur: float = 6, begin: float = 2.2) -> str:
    return (f'<circle cx="{x1}" cy="{y}" r="7" fill="url(#{p}-dot)" opacity="0">'
            f'<animate attributeName="cx" values="{x1};{x2}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1"/>'
            f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;.15;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')


_SHEEN_N = [0]


def sheen(p: str, attrs: str, plain: str, italic: str, base: str, plain_fill: str) -> str:
    """`plain` followed by an italic span in `base`, with a white band sweeping across the text.

    The band is a gradient rect clipped by the text itself and moved with a CSS animation,
    so renderers without animation support simply show the text in its base colours.
    """
    _SHEEN_N[0] += 1
    cid = f"{p}-sc{_SHEEN_N[0]}"
    return (f'<text {attrs} fill="{plain_fill}">{plain}<tspan font-style="italic" fill="{base}">{italic}</tspan></text>'
            f'<clipPath id="{cid}"><text {attrs}>{plain}<tspan font-style="italic">{italic}</tspan></text></clipPath>'
            f'<g clip-path="url(#{cid})"><rect class="{p}-band" x="-360" y="0" width="360" height="100%" fill="url(#{p}-sheen)"/></g>')


def rule(x1: float, x2: float, y: float, p: str) -> str:
    return f'<path class="{p}-draw" d="M{x1} {y} H{x2}" stroke="url(#{p}-rule)" stroke-width="1"/>' + pulse_dot(x1, x2, y, p)


def mono(p: str, x: float, y: float, s: str, size: float = 11.5, fill: str | None = None, ls: float = 2.6,
         anchor: str = "start", cls: str = "") -> str:
    fill = fill or C["cyan"]
    return (f'<text class="{p}-mono {cls}" x="{x}" y="{y}" font-size="{size}" letter-spacing="{ls}" '
            f'fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


# --------------------------------------------------------------------------- cards


def build_title(num: str, kicker: str, plain: str, italic: str, right: str) -> str:
    p = f"t{num}"
    h = 120
    out = [head(W, h, f"{num} {kicker}: {plain}{italic}"), panel(p, W, h, 0.9, 0.5), style(p)]
    out.append(f'<g class="{p}-in"><rect x="40" y="18" width="46" height="30" rx="8" fill="{C["surf2"]}" stroke="{C["line2"]}"/>'
               f'<text class="{p}-mono" x="63" y="38.5" text-anchor="middle" font-size="12" letter-spacing="1" fill="{C["cyan2"]}">{esc(num)}</text>'
               + mono(p, 100, 38, kicker, 12, C["cyan"], 3.4) + "</g>")
    out.append(f'<g class="{p}-in {p}-d2">'
               + sheen(p, f'class="{p}-serif" x="40" y="88" font-size="42" font-weight="300" letter-spacing="-.5"',
                       esc(plain), esc(italic), C["cyan2"], C["txt"]) + "</g>")
    out.append(f'<g class="{p}-in {p}-d3">' + mono(p, 1160, 38, right, 10.5, C["dim"], 2.4, "end") + "</g>")
    out.append(rule(40, 1160, 108, p))
    out.append("</svg>")
    return "\n".join(out)


def build_hero() -> str:
    p = "hero"
    h = 480
    c = CONTENT
    label = (f"{c['name_line1']} {c['name_line2']} — {c['role'].title()}. {c['tagline']} "
             f"{c['strip_left'].title()}.")
    extra = f""".{p}-blink{{animation:{p}-blink 1.1s steps(2,start) infinite}}@keyframes {p}-blink{{to{{visibility:hidden}}}}
.{p}-spin{{transform-origin:955px 232px;animation:{p}-spin 60s linear infinite}}@keyframes {p}-spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.{p}-spin,.{p}-blink{{animation:none}}}}"""
    out = [head(W, h, label), panel(p, W, h, 0.8, 0.5), style(p, extra)]
    # terminal pill
    tw = round(text_w(c["terminal_cmd"], 13.5, "mono") + 56)
    out.append(f'<g class="{p}-in"><rect x="72" y="58" width="{tw}" height="38" rx="19" fill="{C["surf2"]}" stroke="{C["line2"]}"/>'
               f'<circle cx="96" cy="77" r="4" fill="{C["cyan"]}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
               f'<text class="{p}-mono" x="112" y="82" font-size="13.5" fill="{C["muted"]}">{esc(c["terminal_cmd"].split("$")[0])}'
               f'<tspan fill="{C["cyan2"]}">$</tspan><tspan fill="{C["txt"]}">{esc(c["terminal_cmd"].split("$", 1)[1])}</tspan></text>'
               f'<rect class="{p}-blink" x="{72 + tw - 24}" y="67" width="7" height="18" rx="1.5" fill="{C["cyan2"]}"/></g>')
    # eyebrow
    out.append(f'<g class="{p}-in {p}-d1"><path d="M72 134 H104" stroke="{C["cyan"]}" stroke-width="1.5"/>'
               + mono(p, 116, 138, c["eyebrow"], 12, C["cyan"], 4.2) + "</g>")
    # name
    out.append(f'<g class="{p}-in {p}-d2"><text class="{p}-serif" x="68" y="222" font-size="86" font-weight="300" letter-spacing="-2" fill="{C["txt"]}">{esc(c["name_line1"])}</text></g>')
    out.append(f'<g class="{p}-in {p}-d3">'
               + sheen(p, f'class="{p}-serif" x="68" y="310" font-size="86" font-weight="300" letter-spacing="-2"',
                       "", esc(c["name_line2"]), C["cyan3"], C["txt"])
               + f'<text class="{p}-serif" x="68" y="310" font-size="86" font-weight="300" letter-spacing="-2" fill="none">'
                 f'<tspan font-style="italic">{esc(c["name_line2"])}</tspan><tspan fill="{C["cyan"]}">.</tspan></text></g>')
    # role + tagline
    out.append(f'<g class="{p}-in {p}-d4"><text class="{p}-sans" x="72" y="372" font-size="15" font-weight="600" letter-spacing="3.2" fill="{C["txt"]}">{esc(c["role"])}</text></g>')
    out.append(f'<g class="{p}-in {p}-d5"><text class="{p}-serif" x="72" y="410" font-size="22" font-style="italic" fill="{C["muted"]}">{esc(c["tagline"])}</text></g>')
    # bottom strip
    out.append(rule(72, 1128, 436, p))
    out.append(f'<g class="{p}-in {p}-d6">' + mono(p, 72, 460, c["strip_left"], 10.5, C["dim"], 2.4)
               + mono(p, 1128, 460, c["strip_right"], 10.5, C["dim"], 2.4, "end") + "</g>")
    # orbit motif
    cx, cy = 955, 232
    m = [f'<g class="{p}-in {p}-d3">']
    for i, (x, y) in enumerate([(770, 58), (1140, 58), (770, 406), (1140, 406)]):
        dx = 18 if i % 2 == 0 else -18
        dy = 18 if i < 2 else -18
        m.append(f'<path d="M{x} {y + dy} V{y} H{x + dx}" fill="none" stroke="{C["line2"]}" stroke-width="1.5"/>')
    m.append(f'<circle cx="{cx}" cy="{cy}" r="162" fill="none" stroke="{C["line2"]}" stroke-dasharray="3 7" opacity=".9"/>')
    m.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="{C["line2"]}"/>')
    m.append(f'<circle cx="{cx}" cy="{cy}" r="66" fill="none" stroke="{C["line"]}"/>')
    # orbiting dot on the outer ring
    m.append(f'<g class="{p}-spin"><circle cx="{cx + 162}" cy="{cy}" r="3.5" fill="{C["cyan2"]}"/>'
             f'<circle cx="{cx + 162}" cy="{cy}" r="9" fill="url(#{p}-dot)" opacity=".8"/></g>')
    nodes = c["orbit_nodes"]
    for i, name in enumerate(nodes):
        a = math.radians(-90 + i * (360 / len(nodes)))
        nx, ny = cx + 112 * math.cos(a), cy + 112 * math.sin(a)
        m.append(f'<path d="M{cx} {cy} L{nx:.1f} {ny:.1f}" stroke="{C["line2"]}" stroke-width="1" opacity=".8"/>')
        m.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11" fill="{C["cyan"]}" opacity=".16">'
                 f'<animate attributeName="r" values="9;15;9" dur="3.2s" begin="{i * .5}s" repeatCount="indefinite"/></circle>')
        m.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="{C["cyan2"]}" stroke="{C["bg0"]}" stroke-width="2"/>')
        lx = nx + 20 * math.cos(a)
        ly = ny + 20 * math.sin(a) + 4
        anchor = "middle" if abs(math.cos(a)) < .25 else ("start" if math.cos(a) > 0 else "end")
        if abs(math.cos(a)) < .25:
            ly += -10 if math.sin(a) < 0 else 10
        m.append(mono(p, round(lx, 1), round(ly, 1), name, 11, C["muted"], 2.6, anchor))
    m.append(f'<rect x="{cx - 46}" y="{cy - 46}" width="92" height="92" rx="24" fill="{C["surf2"]}" stroke="{C["cyan"]}" stroke-opacity=".6"/>')
    m.append(f'<text class="{p}-serif" x="{cx}" y="{cy + 15}" text-anchor="middle" font-size="42" font-weight="300" letter-spacing="-1" fill="{C["txt"]}">{esc(c["monogram"])}</text>')
    m.append(f'<circle cx="{cx + 30}" cy="{cy - 30}" r="4" fill="{C["cyan"]}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    m.append("</g>")
    out.extend(m)
    out.append("</svg>")
    return "\n".join(out)


def build_about() -> str:
    p = "about"
    h = 420
    c = CONTENT
    label = "About: " + " ".join(f"{cmd} → {res}." for cmd, res in c["about_lines"]) + " " + \
            " ".join(f"{k.title()}: {v} ({d})." for k, v, d in c["about_cards"])
    extra = f".{p}-blink{{animation:{p}-blink 1.1s steps(2,start) infinite}}@keyframes {p}-blink{{to{{visibility:hidden}}}}"
    out = [head(W, h, label), panel(p, W, h, 0.95, 0.9), style(p, extra)]
    # terminal
    out.append(f'<g class="{p}-in">{card(40, 40, 762, 340, p, accent=False)}'
               f'<path d="M40 86 H802" stroke="{C["line"]}"/>'
               f'<circle cx="66" cy="63" r="5" fill="{C["cyan"]}" opacity=".9"/><circle cx="84" cy="63" r="5" fill="{C["cyan"]}" opacity=".5"/><circle cx="102" cy="63" r="5" fill="{C["cyan"]}" opacity=".25"/>'
               + mono(p, 421, 67, f"{c['handle'].lower()}@github: ~", 11.5, C["dim"], 2.2, "middle") + "</g>")
    y = 118
    for i, (cmd, res) in enumerate(c["about_lines"]):
        out.append(f'<g class="{p}-in {p}-d{min(i + 1, 8)}">'
                   f'<text class="{p}-mono" x="70" y="{y}" font-size="15" fill="{C["cyan"]}">$ <tspan fill="{C["txt"]}">{esc(cmd)}</tspan></text>'
                   f'<text class="{p}-mono" x="70" y="{y + 25}" font-size="14.5" fill="{C["cyan"]}">→ <tspan fill="{C["muted"]}">{esc(res)}</tspan></text></g>')
        y += 52
    out.append(f'<rect class="{p}-blink" x="70" y="{y - 14}" width="8" height="16" fill="{C["cyan2"]}"/>')
    # side cards
    for i, (k, v, d) in enumerate(c["about_cards"]):
        cy = 40 + i * 116
        out.append(f'<g class="{p}-in {p}-d{i + 3}">{card(838, cy, 322, 100, p, accent=False)}'
                   f'<path d="M838.5 {cy + 22} V{cy + 78}" stroke="{C["cyan"]}" stroke-width="3" stroke-linecap="round"/>'
                   + mono(p, 862, cy + 32, k, 10.5, C["cyan"], 2.6)
                   + f'<text class="{p}-serif" x="862" y="{cy + 64}" font-size="29" fill="{C["txt"]}">{esc(v)}</text>'
                   + f'<text class="{p}-sans" x="862" y="{cy + 86}" font-size="12.5" fill="{C["muted"]}">{esc(d)}</text></g>')
    out.append("</svg>")
    return "\n".join(out)


def hexagon(cx: float, cy: float, r: float, p: str, i: int) -> str:
    pts = " ".join(f"{cx + r * math.cos(math.radians(60 * k - 30)):.1f},{cy + r * math.sin(math.radians(60 * k - 30)):.1f}" for k in range(6))
    inner = " ".join(f"{cx + r * .55 * math.cos(math.radians(60 * k - 30)):.1f},{cy + r * .55 * math.sin(math.radians(60 * k - 30)):.1f}" for k in range(6))
    return (f'<polygon points="{pts}" fill="{C["surf2"]}" stroke="{C["cyan"]}" stroke-opacity=".7"/>'
            f'<polygon points="{inner}" fill="none" stroke="{C["cyan2"]}" stroke-opacity=".9">'
            f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="{18 + i * 4}s" repeatCount="indefinite"/></polygon>'
            f'<circle cx="{cx}" cy="{cy}" r="3" fill="{C["cyan2"]}"/>')


def build_credentials() -> str:
    p = "cred"
    h = 280
    c = CONTENT
    label = "Credentials: " + " ".join(f"{a} {b} ({d})." for _, a, b, d in c["credentials"])
    out = [head(W, h, label), panel(p, W, h, 0.5, 1.2), style(p)]
    xs = [40, 419, 798]
    for i, (k, l1, l2, d) in enumerate(c["credentials"]):
        x = xs[i]
        out.append(f'<g class="{p}-in {p}-d{i + 1}">{card(x, 40, 362, 200, p)}'
                   + mono(p, x + 28, 74, k, 10.5, C["cyan"], 2.6)
                   + hexagon(x + 318, 70, 20, p, i)
                   + f'<text class="{p}-serif" x="{x + 28}" y="{131}" font-size="30" fill="{C["txt"]}">{esc(l1)}</text>'
                   + f'<text class="{p}-serif" x="{x + 28}" y="{167}" font-size="24" font-style="italic" fill="{C["cyan2"]}">{esc(l2)}</text>'
                   + f'<text class="{p}-sans" x="{x + 28}" y="{208}" font-size="12.5" fill="{C["muted"]}">{esc(d)}</text></g>')
    out.append(rule(40, 1160, 258, p))
    out.append("</svg>")
    return "\n".join(out)


# ---- project motifs (right-hand panel, x 760..1160, y 40..340)

def motif_tenants(p: str) -> str:
    rows = [("tenant · acme", "clearance: internal"), ("tenant · globex", "clearance: restricted"), ("tenant · initech", "clearance: public")]
    s = [mono(p, 800, 78, "ONE DATABASE · ROW-LEVEL SECURITY", 10.5, C["cyan"], 2.6)]
    for i, (t, cl) in enumerate(rows):
        y = 96 + i * 62
        s.append(f'<rect x="800" y="{y}" width="330" height="48" rx="12" fill="{C["surf2"]}" stroke="{C["line2"]}">'
                 f'<animate attributeName="stroke" values="{C["line2"]};{C["cyan"]};{C["line2"]}" keyTimes="0;.5;1" dur="6s" begin="{i * 2}s" repeatCount="indefinite"/></rect>')
        s.append(f'<rect x="800" y="{y + 12}" width="3" height="24" rx="1.5" fill="{C["cyan"]}" opacity=".9"/>')
        s.append(f'<text class="{p}-mono" x="818" y="{y + 29}" font-size="13" fill="{C["txt"]}">{esc(t)}</text>')
        s.append(f'<text class="{p}-mono" x="1116" y="{y + 29}" font-size="11" text-anchor="end" fill="{C["muted"]}">{esc(cl)}</text>')
        # lock
        s.append(f'<rect x="{1070}" y="{y + 19}" width="10" height="8" rx="2" fill="none" stroke="{C["cyan2"]}" opacity=".0"/>')
    s.append(f'<text class="{p}-mono" x="800" y="300" font-size="11" fill="{C["cyan2"]}">WHERE tenant_id = :tenant <tspan fill="{C["muted"]}">AND</tspan> clearance ≤ :principal</text>')
    s.append(note(p, 800, 322, ["not cleared → never retrieved → never inside a prompt"]))
    return "".join(s)


def note(p: str, x: float, y: float, lines: list[str]) -> str:
    return "".join(f'<text class="{p}-sans" x="{x}" y="{y + i * 17}" font-size="12" fill="{C["dim"]}">{esc(t)}</text>'
                   for i, t in enumerate(lines))


def motif_pipeline(p: str) -> str:
    boxes = [("JIRA", "ticket + context"), ("LLM", "cloud · local"), ("DOC", "Google Docs · Confluence")]
    s = [mono(p, 800, 78, "FETCH → GENERATE → SCORE → PUBLISH", 10.5, C["cyan"], 2.6)]
    xs = [800, 930, 1060]
    for i, (t, d) in enumerate(boxes):
        x = xs[i]
        s.append(f'<rect x="{x}" y="118" width="92" height="64" rx="14" fill="{C["surf2"]}" stroke="{C["line2"]}"/>')
        s.append(f'<text class="{p}-serif" x="{x + 46}" y="150" text-anchor="middle" font-size="22" fill="{C["txt"]}">{esc(t)}</text>')
        s.append(f'<text class="{p}-sans" x="{x + 46}" y="169" text-anchor="middle" font-size="9.5" fill="{C["muted"]}">{esc(d)}</text>')
        if i < 2:
            s.append(f'<path d="M{x + 92} 150 H{x + 130}" stroke="{C["line2"]}" stroke-width="1.5"/>'
                     f'<path d="M{x + 124} 145 L{x + 131} 150 L{x + 124} 155" fill="none" stroke="{C["line2"]}" stroke-width="1.5"/>')
    s.append(f'<circle r="5" fill="url(#{p}-dot)" opacity=".95"><animateMotion dur="4s" repeatCount="indefinite" path="M800 150 H1152" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .6 1"/></circle>')
    # eval gate
    s.append(f'<rect x="800" y="214" width="352" height="54" rx="12" fill="none" stroke="{C["line2"]}" stroke-dasharray="4 5"/>')
    s.append(mono(p, 818, 236, "EVAL GATE · CI", 10, C["cyan2"], 2.4))
    s.append(f'<text class="{p}-sans" x="818" y="256" font-size="12" fill="{C["muted"]}">faithfulness · completeness · structure, scored against the ticket</text>')
    s.append(note(p, 800, 300, ["re-runs skip unchanged tickets; a changed ticket", "updates the same document in place and logs the diff"]))
    return "".join(s)


def motif_checks(p: str) -> str:
    checks = [("line items  ==  printed total", "± $0.05"), ("OCR mean confidence", "≥ 65"), ("provider · invoice # · date", "present"), ("date parseable", "8 formats")]
    s = [mono(p, 800, 78, "TRUST MODEL · LOCAL, DETERMINISTIC", 10.5, C["cyan"], 2.6)]
    for i, (t, v) in enumerate(checks):
        y = 104 + i * 44
        s.append(f'<circle cx="812" cy="{y}" r="9" fill="none" stroke="{C["line2"]}"/>')
        s.append(f'<path class="{p}-tick" style="animation-delay:{1 + i * .35:.2f}s" d="M807 {y} L811 {y + 4} L818 {y - 4}" fill="none" stroke="{C["teal"]}" '
                 f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="20"/>')
        s.append(f'<text class="{p}-mono" x="834" y="{y + 5}" font-size="13" fill="{C["txt"]}">{esc(t)}</text>')
        s.append(f'<text class="{p}-mono" x="1150" y="{y + 5}" font-size="12" text-anchor="end" fill="{C["cyan2"]}">{esc(v)}</text>')
        s.append(f'<path d="M834 {y + 16} H1150" stroke="{C["line"]}"/>')
    y = 104 + 4 * 44
    s.append(f'<rect x="800" y="{y - 14}" width="352" height="36" rx="10" fill="{C["amber"]}" fill-opacity=".1" stroke="{C["amber"]}" stroke-opacity=".5"/>')
    s.append(f'<text class="{p}-mono" x="816" y="{y + 9}" font-size="12.5" fill="{C["amber"]}">anything unverified → <tspan font-weight="700">NEEDS_REVIEW</tspan></text>')
    s.append(note(p, 800, y + 48, ["one corrupt file never aborts the batch ·", "every reviewer save is kept as a revision"]))
    return "".join(s)


def motif_funnel(p: str) -> str:
    steps = [("query → multi-query variants", 352), ("hybrid: dense + BM25 (Qdrant)", 316), ("RRF merge → top-50", 280), ("cross-encoder rerank → top-5", 248), ("parent expand → cited answer", 222)]
    s = [mono(p, 800, 78, "RETRIEVAL FUNNEL · FULLY LOCAL", 10.5, C["cyan"], 2.6)]
    for i, (t, w) in enumerate(steps):
        y = 96 + i * 40
        x = 800 + (352 - w) / 2
        op = .3 + i * .14
        s.append(f'<rect class="{p}-bar" style="animation-delay:{.4 + i * .2:.1f}s" x="{x:.0f}" y="{y}" width="{w}" height="30" rx="8" '
                 f'fill="{C["cyan"]}" fill-opacity="{op:.2f}" stroke="{C["cyan"]}" stroke-opacity=".35"/>')
        s.append(f'<text class="{p}-mono" x="976" y="{y + 19.5}" text-anchor="middle" font-size="11.5" fill="{C["txt"]}">{esc(t)}</text>')
    s.append(note(p, 800, 314, ["the same pipeline from this laptop to a sharded cluster —", "only the infrastructure changes"]))
    return "".join(s)


MOTIFS = {"tenants": motif_tenants, "pipeline": motif_pipeline, "checks": motif_checks, "funnel": motif_funnel}


def build_project(pr: dict) -> str:
    p = pr["file"].replace("project-", "pj-")
    h = 380
    extra = (f".{p}-tick{{animation:{p}-tick .5s ease-out both}}@keyframes {p}-tick{{from{{stroke-dashoffset:20}}to{{stroke-dashoffset:0}}}}"
             f".{p}-bar{{transform-box:fill-box;transform-origin:center;animation:{p}-bar .7s cubic-bezier(.16,1,.3,1) both}}"
             f"@keyframes {p}-bar{{from{{transform:scaleX(0)}}to{{transform:none}}}}"
             f"@media (prefers-reduced-motion:reduce){{.{p}-tick,.{p}-bar{{animation:none}}}}")
    out = [head(W, h, pr["alt"]), panel(p, W, h, 0.72, 0.5), style(p, extra)]
    out.append(f'<path d="M28 .5 H560" stroke="{C["cyan"]}" stroke-opacity=".6" stroke-width="2"/>')
    out.append(f'<path d="M740 52 V330" stroke="{C["line"]}"/>')
    out.append(f'<g class="{p}-in">' + mono(p, 56, 62, pr["eyebrow"], 11, C["cyan"], 3) + "</g>")
    out.append(f'<g class="{p}-in {p}-d1"><text class="{p}-serif" x="56" y="112" font-size="46" font-weight="300" letter-spacing="-1" fill="{C["txt"]}">{esc(pr["title"])}</text></g>')
    y = 148
    sub = [f'<g class="{p}-in {p}-d2">']
    for line in pr["subtitle"]:
        sub.append(f'<text class="{p}-sans" x="56" y="{y}" font-size="17.5" fill="{C["muted"]}">{esc(line)}</text>')
        y += 24
    sub.append("</g>")
    out.extend(sub)
    y += 10
    b = [f'<g class="{p}-in {p}-d3">']
    for i, line in enumerate(pr["built"]):
        prefix = f'<tspan fill="{C["cyan"]}" font-weight="600">BUILT ›</tspan> ' if i == 0 else ""
        b.append(f'<text class="{p}-sans" x="56" y="{y}" font-size="13" fill="{C["cyan3"]}">{prefix}{esc(line)}</text>')
        y += 19
    b.append("</g>")
    out.extend(b)
    y += 46
    st = [f'<g class="{p}-in {p}-d4">']
    x = 56
    for v, l in pr["stats"]:
        st.append(f'<text class="{p}-serif" x="{x}" y="{y}" font-size="40" font-weight="300" letter-spacing="-1" fill="{C["txt"]}">{esc(v)}</text>')
        st.append(f'<text class="{p}-sans" x="{x}" y="{y + 22}" font-size="12.5" fill="{C["muted"]}">{esc(l)}</text>')
        x += max(176, text_w(v, 40, "serif") + 40, text_w(l, 12.5) + 36)
    st.append("</g>")
    out.extend(st)
    y += 44
    ch = [f'<g class="{p}-in {p}-d5">']
    x = 56
    for label in pr["chips"]:
        w, s = chip(x, y, label, p)
        ch.append(s)
        x += w + 8
    ch.append("</g>")
    out.extend(ch)
    out.append(f'<g class="{p}-in {p}-d3">{MOTIFS[pr["motif"]](p)}</g>')
    out.append("</svg>")
    return "\n".join(out)


def build_toolkit() -> str:
    p = "kit"
    h = 500
    c = CONTENT
    label = "Toolkit. " + " ".join(f"{k.split(' ', 1)[1].title()}: {a}, {b}, {d}." for k, a, b, d in c["toolkit"])
    out = [head(W, h, label), panel(p, W, h, 0.5, 0.5), style(p)]
    xs = [40, 419, 798]
    for i, (k, a, b, d) in enumerate(c["toolkit"]):
        x, y = xs[i % 3], 40 + (i // 3) * 220
        out.append(f'<g class="{p}-in {p}-d{i + 1}">{card(x, y, 362, 200, p)}'
                   + mono(p, x + 28, y + 36, k, 10.5, C["cyan"], 2.6)
                   + f'<text class="{p}-serif" x="{x + 28}" y="{y + 90}" font-size="29" fill="{C["txt"]}">{esc(a)}</text>'
                   + (f'<text class="{p}-mono" x="{x + 28 + text_w(a, 29, "serif") + 14:.0f}" y="{y + 80}" font-size="9.5" letter-spacing="2" fill="{C["cyan2"]}">PRIMARY</text>' if i == 0 else "")
                   + f'<text class="{p}-serif" x="{x + 28}" y="{y + 130}" font-size="24" fill="{C["cyan3"]}">{esc(b)}</text>'
                   + f'<text class="{p}-serif" x="{x + 28}" y="{y + 166}" font-size="22" fill="{C["muted"]}">{esc(d)}</text></g>')
    for (x, y) in [(410.5, 250), (789.5, 250)]:
        out.append(f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" transform="rotate(45 {x} {y})" fill="none" stroke="{C["cyan"]}" stroke-opacity=".7"/>')
    out.append("</svg>")
    return "\n".join(out)


def build_footer() -> str:
    p = "foot"
    h = 230
    c = CONTENT
    out = [head(W, h, f"{c['footer_name']} — {c['footer_tagline']}"), panel(p, W, h, 0.1, 0.9), style(p)]
    out.append(f'<g class="{p}-in"><text class="{p}-serif" x="56" y="150" font-size="112" font-weight="300" letter-spacing="-4" fill="{C["txt"]}">{esc(c["footer_name"])}<tspan fill="{C["cyan"]}">.</tspan></text></g>')
    out.append(f'<g class="{p}-in {p}-d2">'
               + sheen(p, f'class="{p}-serif" x="1144" y="118" text-anchor="end" font-size="27"', "", esc(c["footer_tagline"]), C["cyan2"], C["txt"])
               + mono(p, 1144, 150, c["footer_meta"], 11, C["dim"], 2.6, "end") + "</g>")
    out.append(rule(56, 1144, 192, p))
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"hero.svg": build_hero(), "about.svg": build_about(), "credentials.svg": build_credentials(),
             "toolkit.svg": build_toolkit(), "footer.svg": build_footer()}
    for t in CONTENT["titles"]:
        files[f"title-{t[1].lower().replace(' ', '-')}.svg"] = build_title(*t)
    for pr in CONTENT["projects"]:
        files[f"{pr['file']}.svg"] = build_project(pr)
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote assets/{name} ({len(svg.encode()) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
