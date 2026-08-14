#!/usr/bin/env python3
"""Validate GBP deliverable HTML: copyblock char limits, dash policy, JSON-LD sanity.

Usage: python3 check_limits.py <file.html> [more.html ...]
Exit 0 = all good, 1 = violations found.
"""
import html
import json
import re
import sys

# em dash, en dash, horizontal bar (escapes only, the literals are banned repo-wide)
FORBIDDEN_DASHES = "—–―"

COPYBLOCK_RE = re.compile(
    r'<div class="copyblock[^"]*" id="([^"]+)"(?:\s+data-max="(\d+)")?>(.*?)</div>',
    re.S,
)
JSONLD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def check_file(path: str) -> list[str]:
    errors = []
    src = open(path, encoding="utf-8").read()

    for ch in FORBIDDEN_DASHES:
        if ch in src:
            errors.append(f"forbidden dash U+{ord(ch):04X} found ({src.count(ch)}x)")

    seen_ids = set()
    for block_id, max_str, body in COPYBLOCK_RE.findall(src):
        if block_id in seen_ids:
            errors.append(f"duplicate copyblock id '{block_id}'")
        seen_ids.add(block_id)
        text = strip_tags(body).strip()
        if max_str:
            n, limit = len(text), int(max_str)
            if n > limit:
                errors.append(f"copyblock '{block_id}': {n} chars > limit {limit}")
        if "application/ld+json" in text:
            json_body = re.sub(r"</?script[^>]*>", "", text).strip()
            try:
                json.loads(json_body)
            except json.JSONDecodeError as e:
                errors.append(f"copyblock '{block_id}': invalid JSON-LD ({e})")

    for i, raw in enumerate(JSONLD_RE.findall(src)):
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"inline JSON-LD block {i}: invalid JSON ({e})")

    for ref in re.findall(r'class="count" data-for="([^"]+)"', src):
        if ref not in seen_ids:
            errors.append(f"counter references missing copyblock '{ref}'")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    failed = False
    for path in sys.argv[1:]:
        errors = check_file(path)
        status = "FAIL" if errors else "OK"
        print(f"{status}  {path}")
        for e in errors:
            print(f"      {e}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
