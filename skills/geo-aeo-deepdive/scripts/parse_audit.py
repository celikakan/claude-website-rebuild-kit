#!/usr/bin/env python3
"""
parse_audit.py — Parse an SEO/GEO/AEO audit into the canonical schema.

Input: a file path to an audit in one of these formats:
  - .pdf  (uses pdftotext or PyPDF2 if available; otherwise asks user to convert)
  - .html (parsed with BeautifulSoup if available, else regex fallback)
  - .md   (read raw)
  - .txt  (read raw)
  - .json (assumed already in canonical schema, copies through)

Output: parsed-audit.json next to the input file (or in /tmp/).

The parser does its best to populate the canonical schema. Any field it cannot
detect remains absent or set to "UNKNOWN". The skill workflow expects the
calling agent (Claude) to fill remaining gaps from the original audit text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


SCHEMA_VERSION = "1.0"


# ------------------------ PII Sanitization ------------------------ #

PII_PATTERNS = [
    # International phone numbers — be conservative to avoid swallowing schema IDs.
    (re.compile(r"\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,5}"), "[PHONE]"),
    # Domestic phone patterns (longer than 7 digits with separators).
    (re.compile(r"\b\d{3,5}[\s.-]\d{3,5}[\s.-]\d{2,5}\b"), "[PHONE]"),
    # Email addresses.
    (re.compile(r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b"), "[EMAIL]"),
    # German/AT/CH titled person names.
    (re.compile(r"\b(?:Prof\.?|Dr\.?|Mag\.?|Dipl\.-Ing\.?|Mr\.?|Mrs\.?|Ms\.?)\s+(?:[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)?\s+)+[A-ZÄÖÜ][a-zäöüß-]+"), "[PERSON]"),
    # IBAN.
    (re.compile(r"\b[A-Z]{2}\d{2}\s?(?:\d{4}\s?){3,7}\d{1,4}\b"), "[IBAN]"),
    # Credit card numbers.
    (re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"), "[CARD]"),
]


def sanitize_pii(text: str) -> str:
    """Strip common PII patterns from free text before logging or storing.

    Returns text with phone numbers, emails, person names, IBANs, and credit
    card numbers replaced by neutral placeholders. Domain names, URLs, and
    business-relevant identifiers (SKUs, audit IDs) remain untouched.

    Use this on any text written to verification-log.json or other persisted
    files. Do NOT use on the audit's findings array — those are the user's
    business content and the user owns them. Use only on incidental text
    that might contain stray PII from a PDF copy/paste."""
    if not text:
        return text
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text

# Stack detection patterns — case-insensitive substrings.
STACK_PATTERNS = {
    "cms": {
        "WORDPRESS": ["wordpress", "wp-admin", "wp-content", "yoast", "elementor"],
        "SHOPIFY": ["shopify", "shopify cli", "theme.liquid"],
        "WEBFLOW": ["webflow"],
    },
    "seo_plugin": {
        "YOAST_PREMIUM": ["yoast premium", "yoast seo premium"],
        "YOAST": ["yoast"],
        "RANK_MATH": ["rank math", "rankmath"],
        "AIOSEO": ["aioseo", "all in one seo"],
    },
    "schema_plugin": {
        "SASWP": ["saswp", "schema and structured data for wp"],
        "SCHEMA_PRO": ["schema pro"],
    },
    "page_builder": {
        "ELEMENTOR": ["elementor"],
        "GUTENBERG": ["gutenberg", "block editor"],
        "DIVI": ["divi"],
        "WPBAKERY": ["wpbakery", "visual composer"],
    },
    "hosting": {
        "CLOUDFLARE": ["cloudflare"],
        "APACHE": ["apache", ".htaccess"],
        "NGINX": ["nginx"],
        "VERCEL": ["vercel"],
        "NETLIFY": ["netlify"],
    },
}

ANALYTICS_PATTERNS = {
    "GA4": ["ga4", "google analytics 4", "g-"],
    "GTM": ["gtm", "google tag manager"],
    "CLARITY": ["google clarity", "clarity.microsoft", "clarity.ms"],
    "MATOMO": ["matomo"],
    "PLAUSIBLE": ["plausible"],
    "FATHOM": ["fathom analytics"],
}

# Crawler indicators from typical audit phrasing.
CRAWLER_PATTERNS = {
    "gptbot": [
        ("ALLOWED", ["gptbot erlaubt", "gptbot allowed", "gptbot: allowed"]),
        ("BLOCKED", ["gptbot blockiert", "gptbot blocked", "gptbot: blocked", "disallow: /\n.*gptbot", "user-agent: gptbot\ndisallow: /"]),
    ],
    "claudebot": [
        ("ALLOWED", ["claudebot erlaubt", "claudebot allowed"]),
        ("BLOCKED", ["claudebot blockiert", "claudebot blocked"]),
    ],
    "perplexitybot": [
        ("ALLOWED", ["perplexitybot erlaubt", "perplexitybot allowed"]),
        ("BLOCKED", ["perplexitybot blockiert", "perplexitybot blocked"]),
    ],
    "googlebot": [
        ("ALLOWED", ["googlebot erlaubt", "googlebot allowed"]),
        ("BLOCKED", ["googlebot blockiert", "googlebot blocked"]),
    ],
}

LLMS_TXT_PATTERNS = [
    ("STANDARD_COMPLIANT", ["llms.txt standardkonform", "llms.txt llmstxt.org-format", "llms.txt standard compliant"]),
    ("PRESENT", ["llms.txt vorhanden", "llms.txt present", "llms.txt aktiv"]),
    ("MISSING", ["llms.txt fehlt", "llms.txt missing", "kein llms.txt"]),
]


def read_text(path: Path) -> str:
    """Extract textual content from supported file types."""
    suffix = path.suffix.lower()

    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="replace")

    if suffix == ".html":
        raw = path.read_text(encoding="utf-8", errors="replace")
        try:
            from bs4 import BeautifulSoup
            return BeautifulSoup(raw, "html.parser").get_text("\n")
        except ImportError:
            return re.sub(r"<[^>]+>", " ", raw)

    if suffix == ".pdf":
        # Try pdftotext via subprocess first; fall back to PyPDF2.
        import subprocess
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        try:
            pypdf2 = __import__("PyPDF2")
            reader = pypdf2.PdfReader(str(path))
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        except ImportError:
            print(
                "ERROR: pdftotext not found and PyPDF2 not installed.\n"
                "Install one of:\n"
                "  brew install poppler   (provides pdftotext)\n"
                "  pip install PyPDF2",
                file=sys.stderr,
            )
            sys.exit(2)

    if suffix == ".json":
        # Assume already canonical; copy through.
        return path.read_text(encoding="utf-8", errors="replace")

    raise ValueError(f"Unsupported audit file extension: {suffix}")


def detect_stack(text: str) -> dict:
    """Detect CMS, plugins, analytics, hosting from audit text."""
    lower = text.lower()
    stack = {
        "cms": "UNKNOWN",
        "seo_plugin": "UNKNOWN",
        "schema_plugin": "UNKNOWN",
        "page_builder": "UNKNOWN",
        "analytics": [],
        "hosting": "UNKNOWN",
    }
    for category in ("cms", "seo_plugin", "schema_plugin", "page_builder", "hosting"):
        for value, needles in STACK_PATTERNS[category].items():
            if any(needle in lower for needle in needles):
                stack[category] = value
                break
    for tool, needles in ANALYTICS_PATTERNS.items():
        if any(needle in lower for needle in needles):
            stack["analytics"].append(tool)
    if not stack["analytics"]:
        stack["analytics"] = ["NONE"]
    return stack


def detect_crawler_access(text: str) -> dict:
    """Detect crawler permissions and llms.txt status."""
    lower = text.lower()
    result = {
        "gptbot": "UNKNOWN",
        "claudebot": "UNKNOWN",
        "perplexitybot": "UNKNOWN",
        "googlebot": "UNKNOWN",
        "llms_txt": "MISSING",
    }
    for crawler, rules in CRAWLER_PATTERNS.items():
        for state, needles in rules:
            if any(needle.lower() in lower for needle in needles):
                result[crawler] = state
                break
    for state, needles in LLMS_TXT_PATTERNS:
        if any(needle in lower for needle in needles):
            result["llms_txt"] = state
            break
    return result


def extract_scores(text: str) -> dict:
    """Best-effort score extraction.

    Matches patterns like "SEO Score 59/100", "GEO 58/100", "AEO: 59 of 100".
    Returns a partially populated structure; agent fills gaps from the source.
    """
    scores = {"seo": {}, "geo": {}, "aeo": {}}

    patterns = [
        (r"seo[^\n]*?(\d{1,3})\s*/\s*100", "seo", "overall"),
        (r"geo[^\n]*?(\d{1,3})\s*/\s*100", "geo", "overall"),
        (r"aeo[^\n]*?(\d{1,3})\s*/\s*100", "aeo", "overall"),
    ]
    for pattern, group, field in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if 0 <= value <= 100:
                scores[group][field] = value
    return scores


def stub_findings() -> list:
    """Return a minimal placeholder findings array.

    The agent fills detailed findings by reading the source audit. This stub
    ensures the schema is structurally valid even before deep parsing.
    """
    return [{
        "id": "F-AUTO-001",
        "severity": "HOCH",
        "category": "SEO_ONPAGE",
        "title": "Findings need to be filled from source audit",
        "description": "parse_audit.py created a schema skeleton. The calling agent must extract concrete findings from the source audit text.",
    }]


def derive_meta(text: str, path: Path) -> dict:
    """Best-effort meta extraction."""
    meta = {
        "audit_name": path.stem.replace("_", " ").replace("-", " ").strip(),
        "audit_date": date.today().isoformat(),
        "target_domain": "UNKNOWN",
        "language": "de" if any(word in text.lower() for word in ["und", "der", "die", "das", "schritt"]) else "en",
    }

    domain_match = re.search(r"\b([a-z0-9-]+\.(?:com|de|at|ch|io|ai|org|net|app|co))\b", text, flags=re.IGNORECASE)
    if domain_match:
        meta["target_domain"] = domain_match.group(1).lower()

    date_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", text)
    if date_match:
        meta["audit_date"] = "-".join(date_match.groups())
    else:
        de_date_match = re.search(r"(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})", text)
        if de_date_match:
            d, m, y = de_date_match.groups()
            meta["audit_date"] = f"{y}-{int(m):02d}-{int(d):02d}"

    pages_match = re.search(r"(\d{1,3})\s+seiten?\s+(?:analysiert|geprüft|gescannt)", text, flags=re.IGNORECASE)
    if pages_match:
        meta["pages_analyzed"] = int(pages_match.group(1))

    return meta


def parse(path: Path) -> dict:
    """Top-level parse: returns canonical audit dict."""
    if path.suffix.lower() == ".json":
        # Passthrough — already canonical.
        return json.loads(path.read_text(encoding="utf-8"))

    text = read_text(path)
    return {
        "_schema_version": SCHEMA_VERSION,
        "meta": derive_meta(text, path),
        "scores": extract_scores(text),
        "findings": stub_findings(),
        "crawler_access": detect_crawler_access(text),
        "detected_stack": detect_stack(text),
        "_raw_text_excerpt": text[:4000],  # First 4 KB for the agent to use as fill-in context.
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("audit_path", help="Path to the source audit (PDF/HTML/MD/JSON/TXT)")
    parser.add_argument("--out", help="Output path for parsed-audit.json (default: alongside source)")
    args = parser.parse_args()

    src = Path(args.audit_path).expanduser().resolve()
    if not src.exists():
        print(f"ERROR: audit file not found: {src}", file=sys.stderr)
        return 2

    parsed = parse(src)

    out_path = Path(args.out).expanduser().resolve() if args.out else src.with_suffix(".parsed-audit.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"OK parsed → {out_path}")
    print(f"   meta.target_domain  = {parsed['meta'].get('target_domain')}")
    print(f"   detected_stack.cms  = {parsed['detected_stack']['cms']}")
    print(f"   crawler.llms_txt    = {parsed['crawler_access']['llms_txt']}")
    print(f"   findings count      = {len(parsed['findings'])} (skeleton — agent must enrich)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
