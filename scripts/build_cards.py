#!/usr/bin/env python3
"""Build the profile README cards (assets/*.svg) — "Schematic" design.

The profile is drawn as an engineering drawing: blueprint grid, drafting title
blocks, numbered callouts, dimension lines, and each project rendered as its
real architecture rather than a list of technologies.

Everything the cards say lives in CONTENT below. Edit it, run

    python scripts/build_cards.py

and commit the regenerated SVGs. Standard library only.
The contribution heatmap is built separately by scripts/build_heatmap.py.
"""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
W = 1200

C = dict(
    bg0="#06172A", bg1="#0A2238", grid="#123A5E", grid2="#1B4E79",
    ink="#DCEAF8", muted="#86A9CB", dim="#5E809F",
    cy="#5EEAD4", cy2="#99F6E4", amber="#FCD34D", panel="#081D31",
)
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# --------------------------------------------------------------------------- primitives

def sheet(p: str, w: int, h: int, label: str, extra_css: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">
<defs>
<linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>
<pattern id="{p}-g1" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0 V20 M0 20 H20" stroke="{C['grid']}" stroke-width=".5" opacity=".55"/></pattern>
<pattern id="{p}-g2" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0 V100 M0 100 H100" stroke="{C['grid2']}" stroke-width=".7" opacity=".5"/></pattern>
<linearGradient id="{p}-sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
</defs>
<style>
.{p}-m{{font-family:{MONO}}}.{p}-s{{font-family:{SANS}}}
.{p}-i{{animation:{p}-i .9s cubic-bezier(.16,1,.3,1) both}}
.{p}-d1{{animation-delay:.1s}}.{p}-d2{{animation-delay:.2s}}.{p}-d3{{animation-delay:.3s}}.{p}-d4{{animation-delay:.4s}}.{p}-d5{{animation-delay:.5s}}.{p}-d6{{animation-delay:.6s}}
.{p}-dr{{stroke-dasharray:1200;animation:{p}-dr 1.8s cubic-bezier(.65,0,.35,1) .3s both}}
.{p}-band{{animation:{p}-band 8s cubic-bezier(.4,0,.6,1) 1.6s infinite}}
@keyframes {p}-i{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes {p}-dr{{from{{stroke-dashoffset:1200}}to{{stroke-dashoffset:0}}}}
@keyframes {p}-band{{0%{{transform:translateX(0)}}45%{{transform:translateX(1700px)}}100%{{transform:translateX(1700px)}}}}
@media (prefers-reduced-motion:reduce){{.{p}-i,.{p}-dr,.{p}-band{{animation:none}}}}
{extra_css}</style>
<rect width="{w}" height="{h}" fill="url(#{p}-bg)"/>
<rect width="{w}" height="{h}" fill="url(#{p}-g1)"/>
<rect width="{w}" height="{h}" fill="url(#{p}-g2)"/>
<rect x="8.5" y="8.5" width="{w-17}" height="{h-17}" fill="none" stroke="{C['grid2']}"/>
<rect x="14.5" y="14.5" width="{w-29}" height="{h-29}" fill="none" stroke="{C['grid']}" stroke-width=".6"/>'''


def mono(p, x, y, s, size=11, fill=None, ls=1.8, anchor="start"):
    return (f'<text class="{p}-m" x="{x}" y="{y}" font-size="{size}" letter-spacing="{ls}" '
            f'fill="{fill or C["dim"]}" text-anchor="{anchor}">{esc(s)}</text>')


def sans(p, x, y, s, size=13, fill=None, anchor="start", weight=None, style=None):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' font-style="{style}"' if style else ""
    return (f'<text class="{p}-s" x="{x}" y="{y}" font-size="{size}" fill="{fill or C["muted"]}" '
            f'text-anchor="{anchor}"{a}>{esc(s)}</text>')


def callout(p, n, x, y, r=11):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C["bg0"]}" stroke="{C["cy"]}" stroke-width="1.2"/>'
            f'<text class="{p}-m" x="{x}" y="{y+4.5}" text-anchor="middle" font-size="12" fill="{C["cy"]}">{n}</text>')


_SHEEN = [0]


def sheen(p: str, attrs: str, text: str, base: str) -> str:
    _SHEEN[0] += 1
    cid = f"{p}-sc{_SHEEN[0]}"
    return (f'<text {attrs} fill="{base}">{text}</text>'
            f'<clipPath id="{cid}"><text {attrs}>{text}</text></clipPath>'
            f'<g clip-path="url(#{cid})"><rect class="{p}-band" x="-380" y="0" width="380" height="100%" fill="url(#{p}-sheen)"/></g>')


def table(p, x, y, cols, rows, rh=30, head_h=28):
    """Drafting register table. cols = [(label, width, align)]; rows = [[(text, fill, kind)]]."""
    out, total = [], sum(c[1] for c in cols)
    out.append(f'<rect x="{x}" y="{y}" width="{total}" height="{head_h}" fill="{C["cy"]}" fill-opacity=".08"/>')
    cx = x
    for label, cw, _ in cols:
        out.append(mono(p, cx + 12, y + head_h - 9, label, 9.5, C["cy"], 1.9))
        cx += cw
    out.append(f'<path d="M{x} {y+head_h} h{total}" stroke="{C["cy"]}" stroke-opacity=".45"/>')
    ry = y + head_h
    for i, row in enumerate(rows):
        if i % 2:
            out.append(f'<rect x="{x}" y="{ry}" width="{total}" height="{rh}" fill="{C["panel"]}" fill-opacity=".5"/>')
        cx = x
        for (_, cw, align), (val, fill, kind) in zip(cols, row):
            tx = cx + 12 if align == "l" else (cx + cw - 12 if align == "r" else cx + cw / 2)
            anc = "start" if align == "l" else ("end" if align == "r" else "middle")
            if kind == "m":
                out.append(mono(p, round(tx), ry + rh / 2 + 4, val, 11.5, fill, 1.2, anc))
            else:
                out.append(sans(p, round(tx), ry + rh / 2 + 4.5, val, 13, fill, anc))
            cx += cw
        out.append(f'<path d="M{x} {ry+rh} h{total}" stroke="{C["grid2"]}" stroke-width=".6" opacity=".8"/>')
        ry += rh
    out.append(f'<rect x="{x}" y="{y}" width="{total}" height="{ry-y}" fill="none" stroke="{C["grid2"]}"/>')
    cx = x
    for _, cw, _a in cols[:-1]:
        cx += cw
        out.append(f'<path d="M{cx} {y} V{ry}" stroke="{C["grid2"]}" stroke-width=".6" opacity=".8"/>')
    return "".join(out), ry


def box(p, x, y, bw, bh, title, sub="", accent=False):
    col = C["cy"] if accent else C["grid2"]
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="3" fill="{C["bg0"]}" fill-opacity=".62" '
         f'stroke="{col}" stroke-width="{1.3 if accent else .9}"/>')
    cy = y + bh / 2
    if sub:
        s += sans(p, round(x + bw / 2), round(cy - 2), title, 12.5, C["ink"], "middle")
        s += mono(p, round(x + bw / 2), round(cy + 14), sub, 9.5, C["dim"], 1, "middle")
    else:
        s += sans(p, round(x + bw / 2), round(cy + 4.5), title, 12.5, C["ink"], "middle")
    return s


def arrow(p, x1, y, x2, label="", dash=False):
    d = ' stroke-dasharray="4 4"' if dash else ""
    s = f'<path class="{p}-dr" d="M{x1:.0f} {y:.0f} H{x2:.0f}" stroke="{C["cy"]}" stroke-width="1" opacity=".85"{d}/>'
    s += (f'<path d="M{x2-7:.0f} {y-4:.0f} L{x2:.0f} {y:.0f} L{x2-7:.0f} {y+4:.0f}" fill="none" '
          f'stroke="{C["cy"]}" stroke-width="1" opacity=".85"/>')
    if label:
        s += mono(p, round((x1 + x2) / 2), round(y - 9), label, 9.5, C["muted"], 1, "middle")
    return s


def chain(p, items, y, bh=56, left=60, right=1140, labels=None):
    """Evenly place a left-to-right chain of boxes with arrows. Returns (svg, positions)."""
    n = len(items)
    gap = 36
    bw = min(150, (right - left - gap * (n - 1)) / n)
    total = n * bw + gap * (n - 1)
    x = left + (right - left - total) / 2
    out, pos = [], []
    for i, (t, sub, acc) in enumerate(items):
        out.append(box(p, x, y, bw, bh, t, sub, acc))
        pos.append((x, x + bw, y, y + bh))
        if i < n - 1:
            lbl = labels[i] if labels and i < len(labels) else ""
            out.append(arrow(p, x + bw + 4, y + bh / 2, x + bw + gap - 4, lbl))
        x += bw + gap
    return "".join(out), pos


def notes(p, y, items, left=60):
    """Numbered annotation strip under a diagram."""
    out = [f'<path d="M{left} {y-18} H1140" stroke="{C["grid2"]}" stroke-width=".7"/>']
    per = (1140 - left) / len(items)
    for i, (n, t) in enumerate(items):
        x = left + i * per
        out.append(mono(p, round(x), y + 6, f"({n})", 10.5, C["cy"], 1))
        out.append(sans(p, round(x + 26), y + 6, t, 12, C["muted"]))
    return "".join(out)


# --------------------------------------------------------------------------- content

CONTENT = {
    "name1": "Nikhil Chandra",
    "name2": "Sairam Tokala",
    "kicker": "DRAWING 01 — SYSTEMS ENGINEER",
    "role": "AI/ML · GENAI · DEVOPS",
    "tagline": "I draw the system before I write the code.",
    "titleblock": [("LOCATION", "DUBAI, UAE", 150), ("DISCIPLINE", "AI PLATFORMS · RETRIEVAL", 230),
                   ("SHEET", "01 OF 06", 100), ("REV", "2026.10", 100)],
    "stack": [("INTERFACE", "react · vite · streamlit"), ("SERVICE", "fastapi · pydantic"),
              ("AGENTS", "langgraph · tools · eval"), ("RETRIEVAL", "pgvector · qdrant · rerank"),
              ("PLATFORM", "docker · actions · aws")],
    "titles": [("01", "ABOUT", "Specification"), ("02", "CREDENTIALS", "Certification register"),
               ("03", "SELECTED WORK", "Four systems, drawn"), ("04", "TOOLKIT", "Parts list"),
               ("05", "COMMIT LOG", "Twelve months"), ("06", "CONNECT", "Say hello")],
    # 01 about — specification register
    "spec": [
        ("01", "language", "Python 3.11+ — FastAPI, SQLAlchemy 2.0 async, pytest-first"),
        ("02", "agents", "LangGraph runtime, tool calling, offline eval harness"),
        ("03", "retrieval", "pgvector + Qdrant, hybrid BM25 + dense, cross-encoder rerank"),
        ("04", "platform", "Docker, GitHub Actions, AWS, Temporal durable execution"),
        ("05", "principle", "Treat the model as untrusted — verify locally, ship with tests"),
    ],
    # 02 credentials — (ref, credential, issuer, date, status)
    "creds": [
        ("01", "Post Graduate Program in DevOps", "Edureka & Purdue University", "Jan 2026", "CURRENT"),
        ("02", "Data Science Capstone", "Johns Hopkins University", "Nov 2025", "CURRENT"),
        ("03", "Introduction to Retrieval Augmented Generation", "Duke University", "Oct 2025", "CURRENT"),
        ("04", "Generative AI for Data Science", "Microsoft", "Oct 2025", "CURRENT"),
        ("05", "Develop Generative AI Applications", "IBM", "Oct 2025", "CURRENT"),
        ("06", "Business Intelligence Professional Certificate", "Google", "Oct 2025", "CURRENT"),
        ("07", "Python for Everybody (specialization)", "University of Michigan", "Jul 2025", "CURRENT"),
        ("08", "AWS Certified Data Analytics – Specialty", "Amazon Web Services", "2022–2025", "LAPSED"),
        ("09", "AWS Certified Developer – Associate", "Amazon Web Services", "2022–2025", "LAPSED"),
        ("10", "AWS Certified Cloud Practitioner", "Amazon Web Services", "2022–2025", "LAPSED"),
    ],
    # 04 toolkit — parts list
    "parts": [
        ("A1", "Languages", "Python · TypeScript · SQL · Bash"),
        ("A2", "AI / LLM", "LangGraph · RAG · rerank · eval · Gemini · Claude · Ollama"),
        ("B1", "Backend", "FastAPI · Pydantic · SQLAlchemy · Alembic · JWT · RLS · ABAC"),
        ("B2", "Data", "PostgreSQL · pgvector · Qdrant · FAISS · Redis · SQLite"),
        ("C1", "Platform", "Docker · Compose · GitHub Actions · AWS · Temporal"),
        ("C2", "Quality", "pytest · ruff · mypy · coverage gates · RAGAS"),
    ],
    "footer_tag": "Building AI that holds up in production.",
    "footer_meta": "GITHUB.COM/NIKHIL-956653 · DUBAI, UAE",
}

PROJECTS = [
    dict(file="project-eap", fig="FIG. 01 — MULTI-TENANT AGENT PLATFORM", title="Enterprise Agent Platform",
         repo="NIKHIL-956653/enterprise-agent-platform", stats="162 tests · 10 migrations · 4 ADRs",
         stack="fastapi · sqlalchemy · pgvector · redis · temporal · react", kind="eap",
         notes=[("1", "not cleared for a chunk → never retrieved → never in a prompt"),
                ("2", "every run is a workflow — a crash resumes at the last step")],
         alt=("Enterprise Agent Platform, drawn as a schematic: a tenant client authenticates to a FastAPI service, "
              "requests cross a Postgres row-level-security boundary carrying tenant and clearance, and reach "
              "pgvector. Redis handles rate limits and queues; Temporal makes runs durable; Gemini and Anthropic "
              "sit behind one provider protocol. 162 tests, 10 migrations, 4 ADRs.")),
    dict(file="project-docgen", fig="FIG. 02 — DOCUMENT GENERATION PIPELINE", title="Document Writing Assistant",
         repo="NIKHIL-956653/GenAI-Document-Writing-Assistant", stats="368 tests · 95% coverage gate · 6 templates",
         stack="python · fastapi · jira rest · google docs · ollama · docker", kind="docgen",
         notes=[("1", "the eval gate scores faithfulness against the ticket"),
                ("2", "a re-run updates the same document in place, with a diff")],
         alt=("Document Writing Assistant, drawn as a pipeline: a Jira ticket is fetched, passed to a cloud or local "
              "model, scored by an evaluation gate for faithfulness, completeness and structure, then published to "
              "Google Docs or Confluence. 368 offline tests, a 95% coverage gate in CI, 6 document templates.")),
    dict(file="project-bill-ocr", fig="FIG. 03 — DOCUMENT AI / OCR PIPELINE", title="Medical Bill OCR",
         repo="NIKHIL-956653/medical-bill-ocr", stats="45 tests · ±$0.05 tolerance · 300 DPI",
         stack="opencv · tesseract 5 · gemini · fastapi · pandas · pytest", kind="ocr",
         notes=[("1", "local arithmetic re-checks every figure the model returned"),
                ("2", "anything unverified is flagged NEEDS_REVIEW, never guessed")],
         alt=("Medical Bill OCR, drawn as a pipeline: a scan is classified, preprocessed with OpenCV, read by "
              "Tesseract 5, extracted by Gemini, then re-verified by local arithmetic before export to Excel. "
              "Anything that fails validation is flagged NEEDS_REVIEW. 45 tests, ±$0.05 tolerance, 300 DPI.")),
    dict(file="project-rag", fig="FIG. 04 — HYBRID RETRIEVAL PIPELINE", title="Enterprise RAG Pipeline",
         repo="NIKHIL-956653/rag-curriculum", stats="~6,800 pages · ~20K chunks · 50 → 5 rerank",
         stack="qdrant · ollama · nomic-embed · bge reranker · ragas · streamlit", kind="rag",
         notes=[("1", "BM25 and dense results are merged by reciprocal rank fusion"),
                ("2", "fully local — no external API in the retrieval path")],
         alt=("Enterprise RAG Pipeline, drawn as a retrieval funnel: a query is expanded into variants, searched "
              "by BM25 and dense vectors in parallel, merged by reciprocal rank fusion, reranked by a cross-encoder "
              "from top-50 to top-5, expanded to parent chunks and answered with citations. About 6,800 pages and "
              "20,000 chunks, fully local.")),
]


# --------------------------------------------------------------------------- sheets

def build_hero() -> str:
    p, h = "hero", 440
    c = CONTENT
    label = (f"{c['name1']} {c['name2']} — AI/ML, GenAI and DevOps engineer in Dubai, UAE. "
             f"{c['tagline']} Stack, top to bottom: " +
             "; ".join(f"{k.lower()}: {v}" for k, v in c["stack"]) + ".")
    o = [sheet(p, W, h, label)]
    o.append(f'<g class="{p}-i">' + mono(p, 44, 64, c["kicker"], 11.5, C["cy"], 3.4) + "</g>")
    o.append(f'<g class="{p}-i {p}-d1">'
             + sans(p, 42, 140, c["name1"], 56, C["ink"], weight="300")
             + sheen(p, f'class="{p}-s" x="42" y="198" font-size="56" font-weight="300" letter-spacing="-1.6"',
                     esc(c["name2"]), C["ink"]) + "</g>")
    o.append(f'<path class="{p}-dr" d="M44 226 H560" stroke="{C["cy"]}" stroke-width="1.2"/>')
    o.append(f'<g class="{p}-i {p}-d3">' + mono(p, 44, 258, c["role"], 14, C["muted"], 3)
             + sans(p, 44, 290, c["tagline"], 17, C["dim"], style="italic") + "</g>")
    # drafting title block
    o.append(f'<g class="{p}-i {p}-d4">')
    x, ty = 44, 322
    for k, v, cw in c["titleblock"]:
        o.append(f'<rect x="{x}" y="{ty}" width="{cw}" height="54" fill="{C["panel"]}" fill-opacity=".5" stroke="{C["grid2"]}"/>'
                 + mono(p, x + 11, ty + 20, k, 9.5, C["dim"], 1.6)
                 + mono(p, x + 11, ty + 41, v, 12.5, C["ink"], 0.6))
        x += cw
    o.append("</g>")
    # layered stack, right
    ox, ly = 660, 66
    o.append(f'<g class="{p}-i {p}-d2">')
    for i, (k, v) in enumerate(c["stack"]):
        o.append(f'<rect x="{ox}" y="{ly}" width="420" height="52" fill="{C["bg0"]}" fill-opacity=".55" stroke="{C["grid2"]}"/>'
                 f'<path d="M{ox} {ly} h6 v52 h-6 z" fill="{C["cy"]}" opacity="{.25+i*.14:.2f}"/>'
                 + mono(p, ox + 20, ly + 22, k, 10.5, C["cy"], 2)
                 + mono(p, ox + 20, ly + 41, v, 12.5, C["muted"], 0.6)
                 + callout(p, i + 1, ox - 26, ly + 26))
        if i < len(c["stack"]) - 1:
            o.append(f'<path d="M{ox+210} {ly+52} v10" stroke="{C["grid2"]}" stroke-width="1"/>')
        ly += 62
    o.append(f'<path d="M{ox+440} 66 V{ly-10}" stroke="{C["cy"]}" stroke-width=".8" opacity=".7"/>'
             f'<path d="M{ox+435} 66 h10 M{ox+435} {ly-10} h10" stroke="{C["cy"]}" stroke-width=".8" opacity=".7"/>'
             f'<text class="{p}-m" transform="rotate(90 {ox+462} {(66+ly-10)/2:.0f})" x="{ox+462}" '
             f'y="{(66+ly-10)/2:.0f}" text-anchor="middle" font-size="10" letter-spacing="1.6" fill="{C["cy"]}">FULL STACK</text>')
    o.append("</g></svg>")
    return "\n".join(o)


def build_title(num, kicker, sub) -> str:
    p, h = f"t{num}", 96
    o = [sheet(p, W, h, f"{num} — {kicker}: {sub}")]
    o.append(f'<g class="{p}-i"><rect x="44" y="30" width="44" height="30" fill="{C["cy"]}" fill-opacity=".1" stroke="{C["cy"]}" stroke-opacity=".5"/>'
             + mono(p, 66, 50, num, 13, C["cy"], 1, "middle")
             + mono(p, 104, 50, kicker, 13, C["ink"], 3.6)
             + mono(p, 1156, 50, sub.upper(), 10.5, C["dim"], 2.2, "end"))
    o.append(f'<path class="{p}-dr" d="M44 72 H1156" stroke="{C["cy"]}" stroke-width=".9" opacity=".65"/>')
    for i in range(12):
        o.append(f'<path d="M{104+i*88} 72 v6" stroke="{C["grid2"]}" stroke-width=".7"/>')
    o.append("</g></svg>")
    return "\n".join(o)


def build_about() -> str:
    p, h = "ab", 376
    c = CONTENT
    label = "Specification. " + " ".join(f"{k}: {v}." for _, k, v in c["spec"])
    o = [sheet(p, W, h, label)]
    o.append(f'<g class="{p}-i">' + mono(p, 44, 54, "SPECIFICATION — WHAT I BUILD WITH", 11, C["cy"], 3) + "</g>")
    cols = [("REF", 70, "c"), ("SUBSYSTEM", 190, "l"), ("SPECIFICATION", 836, "l")]
    rows = [[(r, C["cy"], "m"), (k, C["ink"], "s"), (v, C["muted"], "s")] for r, k, v in c["spec"]]
    tbl, end = table(p, 44, 74, cols, rows, rh=42)
    o.append(f'<g class="{p}-i {p}-d2">{tbl}</g>')
    o.append(f'<g class="{p}-i {p}-d4">' + mono(p, 44, end + 34, "DUBAI, UAE", 10.5, C["dim"], 2)
             + mono(p, 1156, end + 34, "ALL FOUR SYSTEMS BELOW ARE PUBLIC REPOSITORIES", 10.5, C["dim"], 2, "end") + "</g>")
    o.append("</svg>")
    return "\n".join(o)


def build_credentials() -> str:
    p, h = "cr", 452
    c = CONTENT
    cur = sum(1 for r in c["creds"] if r[4] == "CURRENT")
    label = ("Certification register. " +
             " ".join(f"{n}, {iss}, {d}, {st.lower()}." for _, n, iss, d, st in c["creds"]))
    o = [sheet(p, W, h, label)]
    o.append(f'<g class="{p}-i">' + mono(p, 44, 54, "CERTIFICATION REGISTER", 11, C["cy"], 3)
             + mono(p, 1156, 54, f"{cur} CURRENT · {len(c['creds'])-cur} LAPSED · VERIFIABLE ON LINKEDIN", 10.5, C["dim"], 2, "end") + "</g>")
    cols = [("REF", 58, "c"), ("CREDENTIAL", 460, "l"), ("ISSUER", 330, "l"), ("DATE", 140, "l"), ("STATUS", 108, "c")]
    rows = []
    for ref, name, iss, date, st in c["creds"]:
        live = st == "CURRENT"
        rows.append([(ref, C["cy"] if live else C["dim"], "m"),
                     (name, C["ink"] if live else C["muted"], "s"),
                     (iss, C["muted"], "s"), (date, C["muted"], "m"),
                     (st, C["cy"] if live else C["amber"], "m")])
    tbl, end = table(p, 44, 72, cols, rows, rh=31)
    o.append(f'<g class="{p}-i {p}-d2">{tbl}</g>')
    o.append(f'<g class="{p}-i {p}-d4">'
             + sans(p, 44, end + 30, "Lapsed entries are shown with their real validity window rather than quietly dropped.", 12, C["dim"]) + "</g>")
    o.append("</svg>")
    return "\n".join(o)


# --------------------------------------------------------------------------- project diagrams

def diagram_eap(p):
    o, y = [], 168
    top, bot = y - 62, y + 74          # satellite rows, clear of the title line
    o.append(box(p, 60, y, 118, 56, "client", "tenant user"))
    o.append(arrow(p, 182, y + 28, 246, "JWT"))
    o.append(box(p, 250, y, 132, 56, "FastAPI", "async API", True))
    o.append(arrow(p, 386, y + 28, 450, "principal"))
    o.append(box(p, 454, y, 156, 56, "RLS boundary", "tenant + clearance", True))
    o.append(arrow(p, 614, y + 28, 678))
    o.append(box(p, 682, y, 146, 56, "Postgres", "pgvector"))
    o.append(box(p, 454, top, 156, 48, "Redis", "limits · queues"))
    o.append(box(p, 454, bot, 156, 48, "Temporal", "durable runs"))
    o.append(f'<path d="M316 {y} V{top+24} h134" stroke="{C["grid2"]}" stroke-width=".9" fill="none"/>')
    o.append(f'<path d="M316 {y+56} V{bot+24} h134" stroke="{C["grid2"]}" stroke-width=".9" fill="none"/>')
    o.append(box(p, 900, top, 146, 48, "Gemini", "provider"))
    o.append(box(p, 900, bot, 146, 48, "Anthropic", "provider"))
    o.append(f'<path d="M828 {y+28} h42 V{top+24} h30 M870 {y+28} V{bot+24} h30" stroke="{C["grid2"]}" stroke-width=".9" fill="none"/>')
    o.append(mono(p, 884, y + 22, "one protocol", 9.5, C["dim"], 1))
    o.append(callout(p, 1, 632, y - 16))
    o.append(callout(p, 2, 632, y + 100))
    return "".join(o)


def diagram_docgen(p):
    o, y = [], 168
    items = [("Jira", "ticket + context", False), ("docgen", "fetch · prompt", True),
             ("LLM", "cloud or local", False), ("eval gate", "scored in CI", True),
             ("Google Docs", "or Confluence", False)]
    ch, pos = chain(p, items, y, 56, 60, 1060, ["REST", "prompt", "draft", "pass"])
    o.append(ch)
    lx0, lx1, _, _ = pos[2]
    mid = (lx0 + lx1) / 2
    # both model backends sit above the LLM stage, on one bracket
    o.append(box(p, mid - 152, y - 62, 144, 46, "OpenRouter", "gemini"))
    o.append(box(p, mid + 8, y - 62, 144, 46, "Ollama", "fully local"))
    o.append(f'<path d="M{mid-80:.0f} {y-16} V{y-26} H{mid+80:.0f} V{y-16} M{mid:.0f} {y-26} V{y}" '
             f'stroke="{C["grid2"]}" stroke-width=".9" fill="none"/>')
    gx0, gx1, _, _ = pos[3]
    o.append(mono(p, round((gx0 + gx1) / 2), y + 80, "faithfulness · completeness · structure", 9.5, C["muted"], 1, "middle"))
    o.append(callout(p, 1, gx1 + 16, y - 16))
    o.append(callout(p, 2, pos[4][1] + 16, y + 28))
    o.append(f'<path d="M{pos[4][1]:.0f} {y+56} V{y+100} H{pos[1][0]:.0f} V{y+56}" stroke="{C["cy"]}" stroke-width=".9" '
             f'stroke-dasharray="4 4" opacity=".6" fill="none"/>')
    o.append(mono(p, round((pos[1][0] + pos[4][1]) / 2), y + 114, "re-run → updates the same document in place", 9.5, C["cy"], 1, "middle"))
    return "".join(o)


def diagram_ocr(p):
    o, y = [], 156
    items = [("scan", "pdf · photo", False), ("ingest", "classify", False), ("OpenCV", "deskew · threshold", False),
             ("Tesseract 5", "ocr + confidence", False), ("Gemini", "extract JSON", False),
             ("validate", "local arithmetic", True), ("Excel", "two sheets", False)]
    ch, pos = chain(p, items, y, 56, 60, 1140)
    o.append(ch)
    vx0, vx1, _, _ = pos[5]
    o.append(f'<path d="M{(vx0+vx1)/2:.0f} {y+56} v34" stroke="{C["amber"]}" stroke-width="1" opacity=".8"/>')
    o.append(f'<rect x="{vx0-56:.0f}" y="{y+90}" width="{(vx1-vx0)+112:.0f}" height="38" rx="4" '
             f'fill="{C["amber"]}" fill-opacity=".1" stroke="{C["amber"]}" stroke-opacity=".55"/>')
    o.append(mono(p, round((vx0 + vx1) / 2), y + 114, "NEEDS_REVIEW", 12, C["amber"], 1.6, "middle"))
    o.append(callout(p, 1, vx0 - 16, y - 16))
    o.append(callout(p, 2, vx1 + 70, y + 109))
    o.append(mono(p, 60, y + 114, "±$0.05 reconciliation · OCR confidence ≥ 65 · 8 date formats", 10, C["muted"], 1))
    return "".join(o)


def diagram_rag(p):
    o, y = [], 160
    o.append(box(p, 60, y, 124, 54, "query", "user question"))
    o.append(arrow(p, 188, y + 27, 248))
    o.append(box(p, 252, y, 140, 54, "multi-query", "variants", True))
    o.append(box(p, 452, y - 44, 150, 46, "BM25", "sparse"))
    o.append(box(p, 452, y + 52, 150, 46, "dense", "nomic-embed"))
    o.append(f'<path d="M396 {y+27} h28 v-21 h24 M424 {y+27} v48 h24" stroke="{C["cy"]}" stroke-width="1" opacity=".85" fill="none"/>')
    o.append(box(p, 650, y, 130, 54, "RRF merge", "top-50", True))
    o.append(f'<path d="M602 {y-21} h24 v48 h20 M602 {y+75} h24 v-48" stroke="{C["cy"]}" stroke-width="1" opacity=".85" fill="none"/>')
    o.append(arrow(p, 784, y + 27, 840))
    o.append(box(p, 844, y, 140, 54, "rerank", "cross-encoder", True))
    o.append(arrow(p, 988, y + 27, 1040))
    o.append(box(p, 1044, y, 96, 54, "top-5", "cited"))
    o.append(callout(p, 1, 715, y - 24))
    o.append(callout(p, 2, 914, y + 78))
    o.append(mono(p, 60, y + 120, "parent-child chunking · contextual retrieval · per-chunk ACL · RAGAS eval", 10, C["muted"], 1))
    return "".join(o)


DIAGRAMS = {"eap": diagram_eap, "docgen": diagram_docgen, "ocr": diagram_ocr, "rag": diagram_rag}


def build_project(pr: dict) -> str:
    p, h = pr["file"].replace("project-", "pj"), 384
    o = [sheet(p, W, h, pr["alt"])]
    o.append(f'<g class="{p}-i">' + mono(p, 44, 50, pr["fig"], 11, C["cy"], 3)
             + mono(p, 1156, 50, "SCALE 1:1 · REV 2026.10", 10.5, C["dim"], 2, "end") + "</g>")
    o.append(f'<g class="{p}-i {p}-d1">' + sans(p, 44, 90, pr["title"], 30, C["ink"], weight="300")
             + mono(p, 1156, 90, "github.com/" + pr["repo"].split("/", 1)[1], 11, C["muted"], 1, "end") + "</g>")
    o.append(f'<g class="{p}-i {p}-d3">{DIAGRAMS[pr["kind"]](p)}</g>')
    o.append(f'<g class="{p}-i {p}-d5">' + notes(p, 324, pr["notes"])
             + mono(p, 44, 356, pr["stats"], 11, C["ink"], 1)
             + mono(p, 1156, 356, pr["stack"], 11, C["dim"], 1, "end") + "</g>")
    o.append("</svg>")
    return "\n".join(o)


def build_toolkit() -> str:
    p, h = "kit", 352
    c = CONTENT
    label = "Parts list. " + " ".join(f"{k}: {v}." for _, k, v in c["parts"])
    o = [sheet(p, W, h, label)]
    o.append(f'<g class="{p}-i">' + mono(p, 44, 54, "PARTS LIST — BILL OF MATERIALS", 11, C["cy"], 3)
             + mono(p, 1156, 54, "6 ASSEMBLIES", 10.5, C["dim"], 2, "end") + "</g>")
    cols = [("ITEM", 78, "c"), ("ASSEMBLY", 180, "l"), ("COMPONENTS", 838, "l")]
    rows = [[(r, C["cy"], "m"), (k, C["ink"], "s"), (v, C["muted"], "s")] for r, k, v in c["parts"]]
    tbl, _ = table(p, 44, 74, cols, rows, rh=38)
    o.append(f'<g class="{p}-i {p}-d2">{tbl}</g>')
    o.append("</svg>")
    return "\n".join(o)


def build_footer() -> str:
    p, h = "ft", 220
    c = CONTENT
    o = [sheet(p, W, h, f"Nikhil Chandra Sairam Tokala — {c['footer_tag']}")]
    o.append(f'<g class="{p}-i">' + sans(p, 44, 112, "Nikhil", 76, C["ink"], weight="300")
             + f'<text class="{p}-s" x="236" y="112" font-size="76" font-weight="300" fill="{C["cy"]}">.</text></g>')
    o.append(f'<g class="{p}-i {p}-d2">'
             + sheen(p, f'class="{p}-s" x="1156" y="92" text-anchor="end" font-size="24" font-style="italic"',
                     esc(c["footer_tag"]), C["ink"])
             + mono(p, 1156, 122, c["footer_meta"], 10.5, C["dim"], 2.4, "end") + "</g>")
    o.append(f'<path class="{p}-dr" d="M44 148 H1156" stroke="{C["cy"]}" stroke-width=".9" opacity=".6"/>')
    x = 44
    for k, v, cw in [("DRAWN BY", "N. C. S. TOKALA", 230), ("SHEET", "06 OF 06", 110), ("REV", "2026.10", 110)]:
        o.append(f'<g class="{p}-i {p}-d4"><rect x="{x}" y="160" width="{cw}" height="40" fill="{C["panel"]}" '
                 f'fill-opacity=".5" stroke="{C["grid2"]}"/>'
                 + mono(p, x + 11, 175, k, 9, C["dim"], 1.6) + mono(p, x + 11, 193, v, 11.5, C["ink"], 0.6) + "</g>")
        x += cw
    o.append("</svg>")
    return "\n".join(o)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"hero.svg": build_hero(), "about.svg": build_about(), "credentials.svg": build_credentials(),
             "toolkit.svg": build_toolkit(), "footer.svg": build_footer()}
    for num, kicker, sub in CONTENT["titles"]:
        files[f"title-{kicker.lower().replace(' ', '-')}.svg"] = build_title(num, kicker, sub)
    for pr in PROJECTS:
        files[f"{pr['file']}.svg"] = build_project(pr)
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote assets/{name} ({len(svg.encode())/1024:.1f} KB)")


if __name__ == "__main__":
    main()
