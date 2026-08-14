#!/usr/bin/env python3
"""
verify_report.py — Final controlling pass for the GEO/AEO Deepdive report.

Applies the canonical checklist in references/controlling-checklist.md
programmatically. Exits with non-zero status if any BLOCKER rule fails.

Usage:
  verify_report.py \
      --audit parsed-audit.json \
      --measures measures.json \
      --report report.html \
      [--verification-log verification-log.json] \
      [--out controlling-result.json] \
      [--skill-root /path/to/geo-aeo-deepdive]

Exit codes:
  0 — all BLOCKER rules pass (WARN may be present, see controlling-result.json)
  1 — at least one BLOCKER rule failed
  2 — verifier itself encountered an error (file not found, malformed JSON)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


SKILL_ROOT_DEFAULT = Path(__file__).resolve().parent.parent

ALLOWED_TACTIC_PREFIXES = (
    "PRINCETON_",
    "PRAGMATIC_",
    "STANDARD_",
    "SKILL_AUGMENTATION",
)

# Extension-v1.0 tactic_source values added by the LLM-Visibility extension.
EXTENSION_TACTIC_VALUES = (
    "CITATION_SEEDING_OUTREACH",
    "CROSS_SOURCE_CONSISTENCY",
    "RETRIEVAL_BLOCKER",
)

# Buzzword tags from the extension brief that are NOT valid tactic_source values.
# They are mapped to the existing taxonomy via extension-tactic-mapping.md.
# Using them is a BLOCKER violation (rule C-15).
REJECTED_BUZZWORD_TAGS = (
    "LLM_RETRIEVAL",
    "CHUNK_ENGINEERING",
    "FANOUT_QUERY_MAPPING",
    "ENTITY_DISTRIBUTION",
    "SEMANTIC_DENSITY",
    "RETRIEVAL_FIRST_CONTENT",
    "AI_CONTENT_STRUCTURE",
    "AI_CITABILITY",
    "CITATION_SEEDING",          # use CITATION_SEEDING_OUTREACH
    "CROSS_SOURCE_VALIDATION",   # use CROSS_SOURCE_CONSISTENCY
)

# C-14 — Visibility confidence values must come from the matrix.
ALLOWED_CONFIDENCE_VALUES = {"HOCH", "MITTEL", "NIEDRIG"}

# C-15 — Hard limits enforced by the extension.
EXT_LIMIT_TOTAL_MEASURES = 25
EXT_LIMIT_QUICKWIN_SECTION = 10
EXT_LIMIT_EXTENSION_SCORES = 3

# C-16 — SEO-Foundation guard. Forbidden phrases (case-insensitive substring match).
FORBIDDEN_SEO_DROP_PHRASES = (
    "drop seo",
    "skip seo",
    "seo is obsolete",
    "seo no longer matters",
    "ignore google rankings",
    "ignore organic seo",
    "seo ist obsolet",
    "seo nicht mehr relevant",
    "google rankings ignorieren",
)

ALLOWED_SCORE_NAMES = (
    "AI_Citability_Score",
    "Retrieval_Readiness_Score",
    "Cross_Source_Consistency_Score",
)

ANTI_PATTERN_KEYWORDS = {
    # Princeton anti-patterns
    "A06": ["keyword stuffing", "keyword-dichte erhöhen", "keyword density"],
    "A07": ["content padding", "aufblähen", "wordcount erhöhen", "word count inflation"],
    "A08": ["pure persuasion", "rein persuasiv", "marketing tone only"],
    "A09": ["over simplification", "vereinfachen ohne tiefe"],
    # Pragmatic anti-patterns
    "T04": ["per paragraph summaries", "jeden absatz zusammenfassen"],
    "T05": ["wikipedia paraphrase", "wikipedia umschreiben"],
    "T09": ["mass scaled listicles", "hunderte listicles", "ai bulk listicle"],
    "T13": ["only german", "rein deutsch", "no english footprint"],
    "T16": ["only seo without on-page positioning", "pure seo without positioning"],
}

NUMBER_PATTERN = re.compile(
    r"(?<!\d)("
    r"\d+(?:[.,]\d+)?\s*%|"           # percentages
    r"\d+(?:[.,]\d+)?\s*(?:M|Mrd|Mio|Milliarden|Millionen)(?:\s*(?:EUR|USD|€|\$))?|"
    r"\d+(?:[.,]\d+)?\s*(?:EUR|USD|€|\$)|"
    r"\d+x"
    r")(?!\w)",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_source_corpus(skill_root: Path) -> str:
    """Concatenate the text of all reference files plus the audit and verification log.
    Used by C-03 to verify every number in the report has a source."""
    chunks: list[str] = []
    for ref in (skill_root / "references").glob("*.md"):
        chunks.append(ref.read_text(encoding="utf-8", errors="replace"))
    return "\n\n".join(chunks)


# ------------------------------ Rules ------------------------------ #

def rule_c01_coverage(audit: dict, measures: dict) -> tuple[str, str] | None:
    """C-01 — Every KRITISCH/HOCH finding must be covered or explicitly skipped."""
    findings = audit.get("findings", [])
    must_cover = {f.get("id") for f in findings if f.get("severity") in ("KRITISCH", "HOCH")}
    covered = set()
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            sid = m.get("source_finding_id")
            if sid:
                covered.add(sid)
    skipped = {s.get("finding_id") for s in measures.get("skipped", [])}
    missing = must_cover - covered - skipped
    if missing:
        return ("C-01", f"Findings not covered: {sorted(missing)}")
    return None


def rule_c02_sourcing(measures: dict) -> tuple[str, str] | None:
    """C-02 — Every measure must have a valid tactic_source.

    Valid values:
      - Any tag starting with PRINCETON_, PRAGMATIC_, STANDARD_, SKILL_AUGMENTATION (base skill).
      - Extension v1.0 values: CITATION_SEEDING_OUTREACH, CROSS_SOURCE_CONSISTENCY, RETRIEVAL_BLOCKER.
    """
    offenders = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            tag = m.get("tactic_source", "")
            valid = (
                any(tag.startswith(prefix) for prefix in ALLOWED_TACTIC_PREFIXES)
                or tag in EXTENSION_TACTIC_VALUES
            )
            if not valid:
                offenders.append(f"{m.get('id')} ({tag or 'EMPTY'})")
    if offenders:
        return ("C-02", f"Measures without valid tactic_source: {offenders}")
    return None


def rule_c03_no_fabricated_stats(report_html: str, source_corpus: str, audit_text: str) -> tuple[str, str] | None:
    """C-03 — Every number in the report must trace to references, audit, or verification."""
    found_numbers = set(m.group(1).strip() for m in NUMBER_PATTERN.finditer(report_html))
    haystack = (source_corpus + "\n\n" + audit_text).lower()
    unsourced = []
    for number in found_numbers:
        # Normalize: lowercase, strip whitespace inside.
        norm = number.lower().replace(" ", "")
        # Also test without space variants in haystack.
        if norm not in haystack.replace(" ", ""):
            unsourced.append(number)
    if unsourced:
        return ("C-03", f"Numbers without source in references/audit/verification: {sorted(unsourced)[:10]} (showing up to 10)")
    return None


def rule_c04_step_integrity(measures: dict) -> tuple[str, str] | None:
    """C-04 — Step-instructions must reference existing measure IDs and vice versa."""
    measure_ids = set()
    feasible_ids = set()
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            mid = m.get("id")
            if mid:
                measure_ids.add(mid)
                if m.get("step_by_step_feasible"):
                    feasible_ids.add(mid)
    step_ids = {s.get("id") for s in measures.get("step_instructions", []) if s.get("id")}
    orphans = step_ids - measure_ids
    missing_steps = feasible_ids - step_ids
    if orphans or missing_steps:
        details = []
        if orphans:
            details.append(f"Orphan step instructions (no matching measure): {sorted(orphans)}")
        if missing_steps:
            details.append(f"Measures marked feasible but missing step-instructions: {sorted(missing_steps)}")
        return ("C-04", " | ".join(details))
    return None


def rule_c05_validation_present(measures: dict) -> tuple[str, str] | None:
    """C-05 — Every step-instruction must end with a validation field."""
    offenders = []
    for s in measures.get("step_instructions", []):
        if not s.get("validation"):
            offenders.append(s.get("id", "?"))
    if offenders:
        return ("C-05", f"Step instructions missing validation: {offenders}")
    return None


def rule_c06_neutrality(skill_root: Path, target_domain: str, auditor: str | None) -> tuple[str, str] | None:
    """C-06 — No client-specific names in skill internals."""
    if not target_domain or target_domain == "UNKNOWN":
        return None
    needles = {target_domain.lower()}
    # Derive brand-name variants from domain.
    brand_stem = target_domain.split(".")[0].lower()
    needles.add(brand_stem)
    needles.add(brand_stem.replace("-", ""))
    needles.add(brand_stem.replace("-", " "))
    if auditor:
        needles.update(part.lower() for part in auditor.split() if len(part) > 3)

    skill_files = []
    for sub in ("SKILL.md", "references", "assets", "scripts"):
        target = skill_root / sub
        if target.is_dir():
            skill_files.extend(target.rglob("*"))
        elif target.is_file():
            skill_files.append(target)

    violations = []
    for f in skill_files:
        if not f.is_file():
            continue
        # Skip the verifier itself and any cache files.
        if f.name in ("__pycache__", "verify_report.py") or "__pycache__" in str(f):
            continue
        # Skip the audit-schema.json (legitimate schema definition).
        if f.name == "audit-schema.json":
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        for needle in needles:
            if len(needle) >= 4 and needle in text:
                violations.append(f"{f.relative_to(skill_root)}: contains '{needle}'")
                break
    if violations:
        return ("C-06", f"Neutrality breach — skill internals contain client identifiers: {violations[:5]}")
    return None


def rule_c07_placeholders(report_html: str) -> tuple[str, str] | None:
    """C-07 — No unfilled {{ ... }} placeholders in the rendered HTML."""
    unfilled = re.findall(r"\{\{\s*[\w_]+\s*\}\}", report_html)
    if unfilled:
        unique = sorted(set(unfilled))
        return ("C-07", f"Unfilled placeholders ({len(unfilled)} occurrences): {unique[:10]}")
    return None


def rule_c08_verification_consistency(measures: dict, audit: dict, verification_log: dict | None) -> tuple[str, str] | None:
    """C-08 — Verification statuses must be reflected in measures and log."""
    if not verification_log:
        # If skill ran in --no-network mode, every measure must be marked as not_verified_local_mode.
        all_unverified = True
        for measure_list_key in ("geo_measures", "aeo_measures"):
            for m in measures.get(measure_list_key, []):
                if m.get("verification_status") not in (None, "not_verified_local_mode"):
                    all_unverified = False
                    break
        if not all_unverified:
            return ("C-08", "verification-log.json missing but some measures claim verification status — inconsistent.")
        return None

    log_finding_ids = {c.get("finding_id") for c in verification_log.get("checks", []) if c.get("finding_id")}
    log_statuses = {c.get("finding_id"): c.get("result") for c in verification_log.get("checks", [])}

    offenders = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            vstatus = m.get("verification_status")
            sid = m.get("source_finding_id")
            if vstatus == "CONFIRMED" and sid not in log_finding_ids:
                offenders.append(f"{m.get('id')}: claims CONFIRMED but no log entry for {sid}")
            if vstatus == "RESOLVED":
                offenders.append(f"{m.get('id')}: marked RESOLVED but still appears in active GEO/AEO measures — should be in 'resolved since audit' callout only")
    if offenders:
        return ("C-08", "; ".join(offenders[:10]))
    return None


def rule_c09_anti_pattern_conflict(measures: dict) -> tuple[str, str] | None:
    """C-09 — No measure recommendation may match a known anti-pattern."""
    violations = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            text_blob = " ".join(filter(None, [m.get("what"), m.get("why"), m.get("title")])).lower()
            for ap_id, keywords in ANTI_PATTERN_KEYWORDS.items():
                for kw in keywords:
                    if kw in text_blob:
                        violations.append(f"{m.get('id')} matches anti-pattern {ap_id} ('{kw}')")
    if violations:
        return ("C-09", "; ".join(violations[:10]))
    return None


# WARN-level rules

def rule_c10_tool_stack(audit: dict, measures: dict) -> tuple[str, str] | None:
    cms = audit.get("detected_stack", {}).get("cms", "UNKNOWN")
    if cms == "UNKNOWN":
        # Expect each step-instruction to have an alternative.
        missing = [s.get("id") for s in measures.get("step_instructions", []) if not s.get("alternative")]
        if missing:
            return ("C-10", f"Stack UNKNOWN but step instructions without alternative path: {missing[:5]}")
    return None


def rule_c11_priority_distribution(measures: dict) -> tuple[str, str] | None:
    counts = {"KRITISCH": 0, "HOCH": 0, "MITTEL": 0, "NIEDRIG": 0}
    total = 0
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            prio = m.get("priority")
            if prio in counts:
                counts[prio] += 1
            total += 1
    if total < 3:
        return None
    kritisch_share = counts["KRITISCH"] / total
    if kritisch_share > 0.5:
        return ("C-11", f"{int(kritisch_share*100)}% of measures flagged KRITISCH — priority inflation suspected")
    if counts["KRITISCH"] == 0 and any(f.get("severity") == "KRITISCH" for f in measures.get("source_findings", [])):
        return ("C-11", "Audit has KRITISCH findings but no measure marked KRITISCH — under-translation risk")
    return None


def rule_c12_effort_realism(measures: dict) -> tuple[str, str] | None:
    def parse_hours(value) -> float | None:
        if value is None:
            return None
        s = str(value).replace(",", ".")
        match = re.findall(r"\d+(?:\.\d+)?", s)
        if not match:
            return None
        nums = [float(n) for n in match]
        return sum(nums) / len(nums)

    p0_total = 0.0
    outliers = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            h = parse_hours(m.get("effort_hours"))
            if h is None:
                continue
            if h > 80:
                outliers.append(f"{m.get('id')} ({h:.0f} h)")
            if m.get("priority") == "KRITISCH":
                p0_total += h
    issues = []
    if p0_total > 60:
        issues.append(f"P0 (KRITISCH) effort sum is {p0_total:.0f} h — exceeds single-sprint capacity")
    if outliers:
        issues.append(f"Single-measure outliers >80 h: {outliers[:5]}")
    if issues:
        return ("C-12", "; ".join(issues))
    return None


# ------------------------------ Extension rules (C-13..C-16) ------------------------------ #


def extension_active(measures: dict) -> bool:
    """The extension rules only fire when the extension layer is present in measures.json."""
    if measures.get("extension_scores"):
        return True
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            if any(k in m for k in ("visibility_confidence", "quickwin", "speed_impact", "platform_impact", "track")):
                return True
    if measures.get("audience_profile"):
        return True
    return False


def rule_c13_extension_scores(measures: dict) -> tuple[str, str] | None:
    """C-13 — Extension scores must include value, sub_scores, inputs_hash, methodology_ref."""
    scores = measures.get("extension_scores")
    if not scores:
        return None
    offenders = []
    for name, payload in scores.items():
        if name not in ALLOWED_SCORE_NAMES:
            offenders.append(f"{name}: not in allowlist {ALLOWED_SCORE_NAMES}")
            continue
        if not isinstance(payload, dict):
            offenders.append(f"{name}: payload not a dict")
            continue
        value = payload.get("value")
        sub_scores = payload.get("sub_scores")
        inputs_hash = payload.get("inputs_hash")
        methodology_ref = payload.get("methodology_ref")
        if value is None:
            # Score suppressed; still require methodology_ref so future renders know why.
            if methodology_ref != "scoring-methodology.md":
                offenders.append(f"{name}: value=null but methodology_ref missing")
            continue
        if not isinstance(value, int) or not (0 <= value <= 100):
            offenders.append(f"{name}: value must be int 0-100, got {value!r}")
        if not isinstance(sub_scores, dict) or not sub_scores:
            offenders.append(f"{name}: sub_scores missing or empty")
        if not inputs_hash:
            offenders.append(f"{name}: inputs_hash missing — score not reproducible")
        if methodology_ref != "scoring-methodology.md":
            offenders.append(f"{name}: methodology_ref must be 'scoring-methodology.md'")
    if offenders:
        return ("C-13", "; ".join(offenders[:10]))
    return None


def rule_c14_visibility_confidence(measures: dict) -> tuple[str, str] | None:
    """C-14 — visibility_confidence values must be HOCH/MITTEL/NIEDRIG (per matrix)."""
    offenders = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            vc = m.get("visibility_confidence")
            if vc is None:
                continue
            if isinstance(vc, str):
                if vc not in ALLOWED_CONFIDENCE_VALUES:
                    offenders.append(f"{m.get('id')}: '{vc}' not in {ALLOWED_CONFIDENCE_VALUES}")
                continue
            if isinstance(vc, dict):
                default = vc.get("default")
                if default and default not in ALLOWED_CONFIDENCE_VALUES:
                    offenders.append(f"{m.get('id')}: default='{default}' not allowed")
                for platform, val in (vc.get("by_platform") or {}).items():
                    if val not in ALLOWED_CONFIDENCE_VALUES:
                        offenders.append(f"{m.get('id')}: by_platform[{platform}]='{val}' not allowed")
                continue
            offenders.append(f"{m.get('id')}: visibility_confidence has unexpected type {type(vc).__name__}")
    if offenders:
        return ("C-14", "; ".join(offenders[:10]))
    return None


def rule_c15_hard_limits(measures: dict) -> tuple[str, str] | None:
    """C-15 — Hard limits + buzzword-tag rejection."""
    geo = measures.get("geo_measures", [])
    aeo = measures.get("aeo_measures", [])
    total = len(geo) + len(aeo)
    issues = []
    if total > EXT_LIMIT_TOTAL_MEASURES:
        issues.append(f"Total measures {total} exceeds limit {EXT_LIMIT_TOTAL_MEASURES}")
    quickwin_section_count = sum(
        1 for m in geo + aeo
        if m.get("quickwin") and m.get("in_quickwin_section")
    )
    if quickwin_section_count > EXT_LIMIT_QUICKWIN_SECTION:
        issues.append(f"Quick-Wins section {quickwin_section_count} exceeds limit {EXT_LIMIT_QUICKWIN_SECTION}")
    scores = measures.get("extension_scores") or {}
    if len(scores) > EXT_LIMIT_EXTENSION_SCORES:
        issues.append(f"extension_scores count {len(scores)} exceeds limit {EXT_LIMIT_EXTENSION_SCORES}")
    # Reject buzzword tactic_source values.
    buzzwords = []
    for m in geo + aeo:
        tag = m.get("tactic_source", "")
        if tag in REJECTED_BUZZWORD_TAGS:
            buzzwords.append(f"{m.get('id')} uses rejected tag '{tag}' — see extension-tactic-mapping.md")
    if buzzwords:
        issues.extend(buzzwords)
    if issues:
        return ("C-15", "; ".join(issues[:10]))
    return None


def rule_c16_seo_foundation_guard(measures: dict, report_html: str) -> tuple[str, str] | None:
    """C-16 — No "drop SEO" recommendations anywhere in the report."""
    haystacks = []
    # Scan measure bodies.
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            for field in ("title", "what", "why", "impact"):
                v = m.get(field)
                if v:
                    haystacks.append(str(v).lower())
    # Scan executive summary HTML snippets.
    exec_block = measures.get("executive") or {}
    for v in exec_block.values():
        if isinstance(v, str):
            haystacks.append(v.lower())
    # Scan rendered report (covers strings inserted by the template).
    haystacks.append(report_html.lower())
    found = set()
    for phrase in FORBIDDEN_SEO_DROP_PHRASES:
        if any(phrase in h for h in haystacks):
            found.add(phrase)
    if found:
        return ("C-16", f"SEO-Foundation guard tripped — forbidden phrases: {sorted(found)}")
    return None


# ------------------------------ Runner ------------------------------ #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--audit", required=True, help="parsed-audit.json")
    parser.add_argument("--measures", required=True, help="measures.json")
    parser.add_argument("--report", required=True, help="rendered HTML report")
    parser.add_argument("--verification-log", help="verification-log.json (optional)")
    parser.add_argument("--out", help="controlling-result.json output path")
    parser.add_argument("--skill-root", default=str(SKILL_ROOT_DEFAULT), help="path to skill directory")
    args = parser.parse_args()

    try:
        audit = load_json(Path(args.audit).expanduser())
        measures = load_json(Path(args.measures).expanduser())
        report_html = Path(args.report).expanduser().read_text(encoding="utf-8", errors="replace")
        verification_log = load_json(Path(args.verification_log).expanduser()) if args.verification_log else None
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read inputs: {exc}", file=sys.stderr)
        return 2

    skill_root = Path(args.skill_root).expanduser()
    source_corpus = collect_source_corpus(skill_root)
    audit_text = json.dumps(audit, ensure_ascii=False)

    blockers: list[tuple[str, str]] = []
    warns: list[tuple[str, str]] = []

    target_domain = audit.get("meta", {}).get("target_domain", "")
    auditor = audit.get("meta", {}).get("auditor")

    blocker_checks = [
        rule_c01_coverage(audit, measures),
        rule_c02_sourcing(measures),
        rule_c03_no_fabricated_stats(report_html, source_corpus, audit_text),
        rule_c04_step_integrity(measures),
        rule_c05_validation_present(measures),
        rule_c06_neutrality(skill_root, target_domain, auditor),
        rule_c07_placeholders(report_html),
        rule_c08_verification_consistency(measures, audit, verification_log),
        rule_c09_anti_pattern_conflict(measures),
    ]

    # Extension-only rules — fire only when the extension layer is present.
    ext_active = extension_active(measures)
    if ext_active:
        blocker_checks.extend([
            rule_c13_extension_scores(measures),
            rule_c14_visibility_confidence(measures),
            rule_c15_hard_limits(measures),
            rule_c16_seo_foundation_guard(measures, report_html),
        ])

    for result in blocker_checks:
        if result:
            blockers.append(result)

    warn_checks = [
        rule_c10_tool_stack(audit, measures),
        rule_c11_priority_distribution(measures),
        rule_c12_effort_realism(measures),
    ]
    for result in warn_checks:
        if result:
            warns.append(result)

    rules_checked = 12 + (4 if ext_active else 0)

    summary = {
        "verified_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "rules_checked": rules_checked,
        "extension_active": ext_active,
        "blocker_violations": [{"rule": r, "detail": d} for r, d in blockers],
        "warn_violations": [{"rule": r, "detail": d} for r, d in warns],
        "pass": len(blockers) == 0,
        "target_domain": target_domain,
        "audit_date": audit.get("meta", {}).get("audit_date"),
        "report_path": str(Path(args.report).expanduser().resolve()),
    }

    out_path = Path(args.out).expanduser() if args.out else Path(args.report).expanduser().with_name("controlling-result.json")
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    if blockers:
        print(f"FAIL ({len(blockers)} blocker, {len(warns)} warn) → {out_path}")
        for rule, detail in blockers:
            print(f"  BLOCKER {rule}: {detail}")
        return 1
    print(f"PASS ({len(warns)} warn) → {out_path}")
    for rule, detail in warns:
        print(f"  WARN {rule}: {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
