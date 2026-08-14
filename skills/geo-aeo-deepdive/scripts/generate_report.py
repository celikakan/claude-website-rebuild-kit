#!/usr/bin/env python3
"""
generate_report.py — Render the GEO/AEO Action Report HTML from derived data.

Inputs:
  - --parsed-audit PATH      JSON in the canonical audit-schema (output of parse_audit.py).
  - --measures PATH          JSON with the agent-derived measures, anti-patterns,
                             platform strategies, timeline, and step-by-step instructions.
                             Schema: see "Expected --measures schema" below.
  - --template PATH          Optional override for assets/report-template.html.
                             Defaults to the bundled template.
  - --out PATH               Output HTML file. Defaults to
                             ./geo-aeo-action-report-{audit_date}.html.

Expected --measures schema (all fields optional unless marked required):
{
  "geo_measures":     [ MeasureObj, ... ],     # required, list of GEO measures
  "aeo_measures":     [ MeasureObj, ... ],     # required, list of AEO measures
  "anti_patterns":    [ AntiPatternObj, ... ],
  "platform_strategy": {
      "perplexity":   "<HTML snippet>",
      "gemini":       "<HTML snippet>",
      "chatgpt":      "<HTML snippet>",
      "other":        "<HTML snippet>"
  },
  "step_instructions": [ StepInstrObj, ... ],  # only measures with feasible steps
  "timeline": {
      "p0": [ TimelineObj, ... ],
      "p1": [ TimelineObj, ... ],
      "p2": [ TimelineObj, ... ]
  },
  "executive": {
      "top3_geo": ["...", "...", "..."],
      "top3_aeo": ["...", "...", "..."],
      "expected_impact_html": "<p>...</p>",
      "executive_recommendation_html": "<p>...</p>",
      "effort_range_hours": "120-180",
      "timeline_months": 6
  }
}

MeasureObj:
{
  "id": "M-001",
  "title": "FAQPage Schema implementieren",
  "priority": "KRITISCH|HOCH|MITTEL|NIEDRIG",
  "what": "...",
  "why": "...",                                # cite Princeton/source here
  "impact": "...",
  "effort_hours": "2-3",
  "tactic_source": "PRINCETON_QUOTATION | PRAGMATIC_LISTICLE | ... | SKILL_AUGMENTATION",
  "augmentation": true|false                   # true = skill added, false = audit-derived
}

StepInstrObj:
{
  "id": "M-001",
  "title": "FAQPage Schema implementieren",
  "tool": "WordPress + SASWP",
  "steps": ["1. ...", "2. ...", ...],
  "validation": "Google Rich Results Test → URL eingeben → FAQ bestätigt",
  "alternative": "Bei Yoast Premium: ..."     # optional
}

TimelineObj:
{
  "id": "M-001",
  "title": "FAQPage Schema",
  "priority": "KRITISCH",
  "effort_hours": "2-3"
}

AntiPatternObj:
{
  "title": "Content Padding",
  "description": "...",
  "evidence": "Princeton KDD 2024 anti-pattern A07"
}
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from html import escape
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_ROOT / "assets" / "report-template.html"


def grade_for_score(score: int | None) -> str:
    if score is None:
        return "—"
    if score >= 80:
        return "Sehr gut"
    if score >= 55:
        return "Ausbaufähig"
    if score >= 40:
        return "Handlungsbedarf"
    return "Kritisch"


def _format_visibility_confidence(vc) -> str:
    """Render visibility_confidence as a pill string (default + per-platform deltas)."""
    if vc is None:
        return ""
    if isinstance(vc, str):
        return f'<span class="pill confidence-{vc.lower()}">Sichtbarkeit: {escape(vc)}</span>'
    if isinstance(vc, dict):
        default = vc.get("default", "")
        pills = []
        if default:
            pills.append(f'<span class="pill confidence-{default.lower()}">Sichtbarkeit: {escape(default)}</span>')
        by_platform = vc.get("by_platform") or {}
        for platform, val in by_platform.items():
            pills.append(
                f'<span class="pill confidence-{val.lower()}">{escape(platform)}: {escape(val)}</span>'
            )
        return "".join(pills)
    return ""


def _format_extension_pills(m: dict) -> str:
    pills = []
    speed = m.get("speed_impact")
    if speed:
        pills.append(f'<span class="pill speed">Wirkung: {escape(speed)}</span>')
    track = m.get("track")
    if track:
        pills.append(f'<span class="pill track">{escape(track)}</span>')
    platforms = m.get("platform_impact") or []
    if platforms:
        pills.append(f'<span class="pill platforms">Plattformen: {escape(", ".join(platforms))}</span>')
    if m.get("quickwin"):
        pills.append('<span class="pill quickwin">Quick Win</span>')
    return "".join(pills)


def render_measures(measures: list[dict]) -> str:
    """Render a list of MeasureObj as HTML cards."""
    if not measures:
        return "<p><em>Keine Maßnahmen identifiziert in dieser Kategorie.</em></p>"
    out = []
    for m in measures:
        prio = m.get("priority", "MITTEL")
        klass = prio.lower()
        is_aug = m.get("augmentation", False) or m.get("tactic_source") == "SKILL_AUGMENTATION"
        extension_pills = _format_extension_pills(m)
        confidence_html = _format_visibility_confidence(m.get("visibility_confidence"))
        out.append(f"""
<div class="measure {klass}">
  <h4>{escape(m.get('id', ''))} — {escape(m.get('title', ''))}</h4>
  <div class="row">
    <span class="pill {klass}">{escape(prio)}</span>
    <span class="pill">Aufwand: {escape(str(m.get('effort_hours', '—')))} h</span>
    <span class="pill">Quelle: {escape(m.get('tactic_source', '—'))}</span>
    {'<span class="pill augmentation">SKILL_AUGMENTATION</span>' if is_aug else ''}
    {extension_pills}
    {confidence_html}
  </div>
  <p><strong>Was:</strong> {escape(m.get('what', ''))}</p>
  <p><strong>Warum:</strong> {escape(m.get('why', ''))}</p>
  <p><strong>Impact:</strong> {escape(m.get('impact', ''))}</p>
</div>""")
    return "\n".join(out)


def render_quickwins(measures: dict) -> str:
    """Render the LLM-Visibility Quick Wins section (max 10).

    Looks for measures with `quickwin: true` AND `in_quickwin_section: true`,
    falling back to all `quickwin: true` measures sorted by visibility_confidence + effort.
    """
    candidates: list[dict] = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            if m.get("quickwin"):
                candidates.append(m)
    if not candidates:
        return "<p><em>Keine Quick Wins in dieser Audit-Konfiguration identifiziert.</em></p>"
    # Prefer those explicitly flagged for the section; else fallback to first 10.
    flagged = [m for m in candidates if m.get("in_quickwin_section")]
    if flagged:
        ranked = flagged[:10]
    else:
        ranked = candidates[:10]
    return render_measures(ranked)


def render_blockers(measures: dict) -> str:
    """Render the LLM-Visibility Blockers section.

    Surfaces measures with tactic_source == 'RETRIEVAL_BLOCKER' (negative findings to fix).
    """
    blockers = []
    for measure_list_key in ("geo_measures", "aeo_measures"):
        for m in measures.get(measure_list_key, []):
            if m.get("tactic_source") == "RETRIEVAL_BLOCKER":
                blockers.append(m)
    if not blockers:
        return "<p><em>Keine Retrieval-Blocker identifiziert.</em></p>"
    return render_measures(blockers)


def render_extension_scores(scores: dict | None) -> str:
    """Render the optional extension-score cards. Suppressed scores show '—'."""
    if not scores:
        return ""
    cards = []
    labels = {
        "AI_Citability_Score": "AI Citability",
        "Retrieval_Readiness_Score": "Retrieval Readiness",
        "Cross_Source_Consistency_Score": "Cross-Source Consistency",
    }
    for key, label in labels.items():
        payload = scores.get(key)
        if not payload:
            continue
        value = payload.get("value")
        display = f"{value}/100" if isinstance(value, int) else "—"
        grade = grade_for_score(value) if isinstance(value, int) else "Datenbasis unzureichend"
        cards.append(f"""
<div class="score-card">
  <div class="label">{escape(label)}</div>
  <div class="value">{escape(display)}</div>
  <div class="grade">{escape(grade)}</div>
</div>""")
    return "\n".join(cards)


def render_steps(step_instructions: list[dict]) -> str:
    """Render step-by-step blocks. Skips any with no steps."""
    if not step_instructions:
        return "<p><em>Keine Maßnahmen mit Tool-basierten Schritten identifiziert.</em></p>"
    out = []
    for s in step_instructions:
        steps_list = s.get("steps") or []
        if not steps_list:
            continue
        steps_html = "".join(f"<li>{escape(step)}</li>" for step in steps_list)
        validation = s.get("validation")
        alt = s.get("alternative")
        out.append(f"""
<h3>{escape(s.get('id', ''))} — {escape(s.get('title', ''))}</h3>
<div class="steps">
  <span class="tool-tag">Tool: {escape(s.get('tool', 'WordPress + Yoast + SASWP (Default)'))}</span>
  <ol>{steps_html}</ol>
  {f'<div class="validation"><strong>Validierung:</strong> {escape(validation)}</div>' if validation else ''}
  {f'<div class="validation"><strong>Alternative:</strong> {escape(alt)}</div>' if alt else ''}
</div>""")
    return "\n".join(out) or "<p><em>Alle Maßnahmen sind rein strategisch — keine Tool-Schritte erforderlich.</em></p>"


def render_anti_patterns(items: list[dict]) -> str:
    if not items:
        return "<p><em>Keine Anti-Patterns flagiert.</em></p>"
    rows = []
    for it in items:
        rows.append(f"""
<div class="measure">
  <h4>{escape(it.get('title', ''))}</h4>
  <p>{escape(it.get('description', ''))}</p>
  <p><strong>Evidenz:</strong> {escape(it.get('evidence', ''))}</p>
</div>""")
    return "\n".join(rows)


def render_timeline_rows(items: list[dict]) -> str:
    if not items:
        return "<p><em>Keine Einträge in dieser Phase.</em></p>"
    rows = []
    rows.append("<table><tr><th>ID</th><th>Titel</th><th>Priorität</th><th>Aufwand (h)</th></tr>")
    for it in items:
        rows.append(
            f"<tr><td>{escape(it.get('id', ''))}</td>"
            f"<td>{escape(it.get('title', ''))}</td>"
            f"<td>{escape(it.get('priority', ''))}</td>"
            f"<td>{escape(str(it.get('effort_hours', '—')))}</td></tr>"
        )
    rows.append("</table>")
    return "".join(rows)


def render_top3(items: list[str]) -> str:
    if not items:
        return "<li><em>Keine Top-Maßnahmen identifiziert.</em></li>"
    return "".join(f"<li>{escape(s)}</li>" for s in items)


def render_test_prompts(prompts: list[dict]) -> str:
    if not prompts:
        return "<p><em>Keine Test-Prompts in der Eingabe — Standard-Prompts werden empfohlen.</em></p>"
    rows = ["<table><tr><th>#</th><th>Prompt</th><th>Ziel-Check</th></tr>"]
    for idx, p in enumerate(prompts, start=1):
        rows.append(
            f"<tr><td>{idx}</td>"
            f"<td>{escape(p.get('prompt', ''))}</td>"
            f"<td>{escape(p.get('target_check', ''))}</td></tr>"
        )
    rows.append("</table>")
    return "".join(rows)


def build_replacements(audit: dict, measures: dict) -> dict:
    meta = audit.get("meta", {})
    scores = audit.get("scores", {})
    stack = audit.get("detected_stack", {})
    test_prompts = audit.get("test_prompts", [])
    findings = audit.get("findings", [])

    seo_overall = scores.get("seo", {}).get("overall")
    geo_overall = scores.get("geo", {}).get("overall")
    aeo_overall = scores.get("aeo", {}).get("overall")

    geo_measures = measures.get("geo_measures", [])
    aeo_measures = measures.get("aeo_measures", [])
    step_instructions = measures.get("step_instructions", [])

    def count_priority(lst: list[dict], prio: str) -> int:
        return sum(1 for m in lst if m.get("priority") == prio)

    deepened = sum(1 for m in geo_measures + aeo_measures if not (m.get("augmentation") or m.get("tactic_source") == "SKILL_AUGMENTATION"))
    augmentation = sum(1 for m in geo_measures + aeo_measures if (m.get("augmentation") or m.get("tactic_source") == "SKILL_AUGMENTATION"))

    executive = measures.get("executive", {})
    platform = measures.get("platform_strategy", {})
    timeline = measures.get("timeline", {})

    return {
        "LANGUAGE": meta.get("language", "de"),
        "TARGET_DOMAIN": meta.get("target_domain", "UNKNOWN"),
        "AUDIT_NAME": meta.get("audit_name", "Audit"),
        "AUDIT_DATE": meta.get("audit_date", dt.date.today().isoformat()),
        "INDUSTRY": meta.get("industry", "—"),
        "PAGES_ANALYZED": str(meta.get("pages_analyzed", "—")),
        "AUDITOR": meta.get("auditor", "—"),
        "REPORT_GENERATED_AT": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),

        "SEO_OVERALL": str(seo_overall if seo_overall is not None else "—"),
        "GEO_OVERALL": str(geo_overall if geo_overall is not None else "—"),
        "AEO_OVERALL": str(aeo_overall if aeo_overall is not None else "—"),
        "SEO_GRADE": grade_for_score(seo_overall),
        "GEO_GRADE": grade_for_score(geo_overall),
        "AEO_GRADE": grade_for_score(aeo_overall),

        "GEO_MEASURE_COUNT": str(len(geo_measures)),
        "AEO_MEASURE_COUNT": str(len(aeo_measures)),
        "GEO_KRITISCH_COUNT": str(count_priority(geo_measures, "KRITISCH")),
        "AEO_KRITISCH_COUNT": str(count_priority(aeo_measures, "KRITISCH")),
        "STEP_COUNT": str(len(step_instructions)),

        "TOTAL_FINDINGS_COUNT": str(len(findings)),
        "KRITISCH_FINDINGS_COUNT": str(sum(1 for f in findings if f.get("severity") == "KRITISCH")),
        "HOCH_FINDINGS_COUNT": str(sum(1 for f in findings if f.get("severity") == "HOCH")),
        "MITTEL_FINDINGS_COUNT": str(sum(1 for f in findings if f.get("severity") == "MITTEL")),

        "DEEPENED_COUNT": str(deepened),
        "AUGMENTATION_COUNT": str(augmentation),

        "DETECTED_STACK_SUMMARY": f"CMS={stack.get('cms', 'UNKNOWN')}, SEO={stack.get('seo_plugin', 'UNKNOWN')}, Schema={stack.get('schema_plugin', 'UNKNOWN')}",
        "STACK_CMS": stack.get("cms", "UNKNOWN"),
        "STACK_SEO_PLUGIN": stack.get("seo_plugin", "UNKNOWN"),
        "STACK_SCHEMA_PLUGIN": stack.get("schema_plugin", "UNKNOWN"),
        "STACK_PAGE_BUILDER": stack.get("page_builder", "UNKNOWN"),
        "STACK_ANALYTICS": ", ".join(stack.get("analytics", ["UNKNOWN"])),
        "STACK_HOSTING": stack.get("hosting", "UNKNOWN"),

        "TOP_3_GEO_HTML": render_top3(executive.get("top3_geo", [])),
        "TOP_3_AEO_HTML": render_top3(executive.get("top3_aeo", [])),
        "EXPECTED_IMPACT_HTML": executive.get("expected_impact_html", "<p>Daten werden nach Pilot-Implementierung erhoben.</p>"),
        "EXECUTIVE_RECOMMENDATION_HTML": executive.get("executive_recommendation_html", "<p>Starten mit P0-Quick-Wins (Tag 1–7), dann Schema und Answer-First (Woche 2–4), dann strategische Hebel (Monat 2–6).</p>"),
        "SIMPLE_SUMMARY_HTML": executive.get("simple_summary_html", "<p><em>Keine einfache Zusammenfassung in measures.json hinterlegt. Eine laienverständliche Übersetzung des technischen Management Summary fehlt — siehe Sektion 0b.</em></p>"),
        "EFFORT_RANGE_HOURS": executive.get("effort_range_hours", "—"),
        "TIMELINE_MONTHS": str(executive.get("timeline_months", 6)),

        "GEO_MEASURES_HTML": render_measures(geo_measures),
        "AEO_MEASURES_HTML": render_measures(aeo_measures),

        "QUICKWINS_HTML": render_quickwins(measures),
        "BLOCKERS_HTML": render_blockers(measures),
        "EXTENSION_SCORES_HTML": render_extension_scores(measures.get("extension_scores")),
        "AUDIENCE_PROFILE": measures.get("audience_profile", "—"),

        "PERPLEXITY_STRATEGY_HTML": platform.get("perplexity", "<p><em>Plattform-Strategie für Perplexity wird ergänzt.</em></p>"),
        "GEMINI_STRATEGY_HTML": platform.get("gemini", "<p><em>Plattform-Strategie für Gemini wird ergänzt.</em></p>"),
        "CHATGPT_STRATEGY_HTML": platform.get("chatgpt", "<p><em>Plattform-Strategie für ChatGPT wird ergänzt.</em></p>"),
        "OTHER_PLATFORMS_HTML": platform.get("other", "<p><em>Weitere Plattformen optional je nach Zielmarkt.</em></p>"),

        "ANTI_PATTERNS_HTML": render_anti_patterns(measures.get("anti_patterns", [])),
        "STEP_INSTRUCTIONS_HTML": render_steps(step_instructions),

        "P0_TIMELINE_HTML": render_timeline_rows(timeline.get("p0", [])),
        "P1_TIMELINE_HTML": render_timeline_rows(timeline.get("p1", [])),
        "P2_TIMELINE_HTML": render_timeline_rows(timeline.get("p2", [])),

        "TEST_PROMPTS_TABLE_HTML": render_test_prompts(test_prompts),
    }


def fill_template(template_text: str, replacements: dict) -> str:
    """Replace {{ KEY }} placeholders. We do simple string substitution rather than
    using Python's Template class, because the template uses double-brace
    Jinja-like markers — keeps the template human-friendly."""
    out = template_text
    for key, value in replacements.items():
        out = out.replace("{{ " + key + " }}", str(value))
        out = out.replace("{{" + key + "}}", str(value))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--parsed-audit", required=True, help="parsed-audit.json from parse_audit.py")
    parser.add_argument("--measures", required=True, help="JSON with derived measures and strategies")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="HTML template override")
    parser.add_argument("--out", help="Output HTML path")
    args = parser.parse_args()

    audit = json.loads(Path(args.parsed_audit).expanduser().read_text(encoding="utf-8"))
    measures = json.loads(Path(args.measures).expanduser().read_text(encoding="utf-8"))
    template_path = Path(args.template).expanduser()
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        return 2

    template_text = template_path.read_text(encoding="utf-8")
    replacements = build_replacements(audit, measures)
    output_html = fill_template(template_text, replacements)

    audit_date = audit.get("meta", {}).get("audit_date", dt.date.today().isoformat())
    default_out = Path.cwd() / f"geo-aeo-action-report-{audit_date}.html"
    out_path = Path(args.out).expanduser() if args.out else default_out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output_html, encoding="utf-8")

    geo_count = len(measures.get("geo_measures", []))
    aeo_count = len(measures.get("aeo_measures", []))
    step_count = len(measures.get("step_instructions", []))
    print(f"OK report → {out_path}")
    print(f"   GEO measures      : {geo_count}")
    print(f"   AEO measures      : {aeo_count}")
    print(f"   Step instructions : {step_count}")
    print(f"   Replacements      : {len(replacements)} placeholders filled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
