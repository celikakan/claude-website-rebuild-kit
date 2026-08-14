---
name: geo-aeo-deepdive
description: Use this skill when the user has an existing SEO/GEO/AEO audit, compass, or assessment report and wants to derive a detailed, deepened GEO+AEO action report with step-by-step tool instructions. Ideal when the user says "vertiefe diesen Audit", "Maßnahmen aus dem Compass ableiten", "Action Report aus GEO/AEO Audit", "detaillierter Maßnahmen-Report mit Tools", "Schritt-für-Schritt Anleitung aus Audit", or provides a PDF/HTML/MD audit and asks for actionable next steps. The skill ingests an existing audit, maps findings to academic (Princeton GEO Study) and pragmatic (industry-tested) tactics, applies platform-specific strategies (ChatGPT/Perplexity/Gemini), and produces a polished HTML report with: Management Summary, separate detailed GEO and AEO measure lists, platform strategy, step-by-step tool instructions (WordPress/Yoast/SASWP/Google Clarity/Google Business Profile etc.), anti-patterns, prioritized timeline, and monitoring setup. Always use this skill whenever an existing audit document is the input and deepened actionable measures with tool guidance are the desired output, even if the user does not explicitly name the skill.
---

# GEO/AEO Audit Deepener

A skill that transforms an existing SEO/GEO/AEO audit into a deep, actionable GEO+AEO measures report — enriched with academic evidence (Princeton KDD 2024), pragmatic industry tactics, platform-specific strategies, and step-by-step tool instructions.

## When to Use

Invoke this skill when:
- The user provides or references an existing audit/compass/assessment document.
- The user wants to derive concrete next steps, not run a new audit.
- The user wants deepened recommendations beyond what the audit already contains.
- The user wants step-by-step tool-based instructions (WordPress, Google tools, Schema plugins, etc.).
- The user wants a management-ready HTML report with executive summary, separated GEO/AEO sections, and prioritized timelines.

Do **not** use this skill to crawl websites or perform a new audit — for that, use dedicated audit skills (`seo-audit`, `geo-audit`, `geo-citability`, etc.).

## Output Contract

The skill produces a single HTML file at a user-specified output path (default: `./geo-aeo-action-report.html`). The HTML must contain these sections, in this exact order:

```
0.  MANAGEMENT SUMMARY (1 page, C-level)
1.  AUDIT INPUT OVERVIEW
2.  MARKET CONTEXT
3.  GEO MEASURES — DETAILED
3a. LLM VISIBILITY QUICK WINS              (extension, max 10 entries)
3b. LLM VISIBILITY BLOCKERS                (extension)
4.  AEO MEASURES — DETAILED
5.  PLATFORM STRATEGY
6.  ANTI-PATTERNS
7.  STEP-BY-STEP INSTRUCTIONS
8.  ACTION-PLAN TIMELINE (P0/P1/P2)
9.  MONITORING SETUP
```

Sections 3a and 3b are added by the LLM-Visibility extension. They are embedded inside the GEO measures block to avoid sprawling the contract. When the extension is inactive (no `quickwin: true` measures and no `RETRIEVAL_BLOCKER` measures), the sections may be empty placeholders ("Keine Quick Wins / Blockers identifiziert.") but must still appear so the report structure stays predictable.

The output must remain neutral — no client/brand/person names embedded in the skill itself. All brand-specific content is injected at runtime from the parsed audit. Placeholders such as `{{ TARGET_DOMAIN }}`, `{{ INDUSTRY }}`, `{{ AUDIT_NAME }}` are resolved from the audit input.

## Workflow

Follow these steps. Do not skip steps.

### Step 1 — Parse the Audit

1. Read the audit document the user provided (PDF, HTML, Markdown, or already-structured JSON).
2. For PDF audits, extract text using a parsing approach available in your environment (e.g., `pdftotext`, `PyPDF2`, or simply read the raw text the user supplied).
3. Map extracted content to the `audit-schema.json` structure stored in `assets/audit-schema.json`. Required fields: `meta.audit_name`, `meta.target_domain`, `scores.*.overall` (at least one), `findings[]` (at least 1).
4. If the audit mentions concrete tools (e.g., "Yoast SEO", "SASWP", "Elementor"), populate `detected_stack` accordingly. If unknown, leave fields as `UNKNOWN`.
5. Write the parsed result to `parsed-audit.json` next to the audit file (or in `/tmp/` if no write path is given). Confirm with the user before proceeding if any required field is missing.

### Step 2 — Load Knowledge References

Read these reference files in this order. They are the analytical lens applied to the parsed findings:

1. `references/llm-visibility-extension.md` — extension scope, operating principles, audience profile, Quick-Wins gating.
2. `references/extension-tactic-mapping.md` — anti-doubling rules; valid extension tactic_source values.
3. `references/scoring-methodology.md` — formulas for AI_Citability, Retrieval_Readiness, Cross_Source_Consistency scores.
4. `references/visibility-confidence-matrix.md` — anchored HOCH/MITTEL/NIEDRIG decision table.
5. `references/tactics-pragmatic.md` — 16 industry-tested tactics with ✅/❌ verdicts.
6. `references/tactics-academic.md` — Princeton KDD 2024 GEO study (5 effective + 2 anti-pattern tactics).
7. `references/market-data.md` — Verified market statistics (Gartner, traffic data, conversion benchmarks).
8. `references/llmstxt-spec.md` — llms.txt standard and best practices.
9. `references/platform-divergence.md` — Citation behavior per platform (Perplexity / Gemini / ChatGPT).
10. `references/audit-mapping.md` — Decision rules for mapping audit findings to deepening tactics (including extension rows).
11. `references/tools-catalog.md` — Tool inventory for step-by-step instructions.
12. `references/controlling-checklist.md` — Final QA-checklist applied in Step 6 (now C-01 to C-16).

### Step 2.5 — Live-Verification (Mandatory)

Before deriving measures, verify the audit's findings against live data. Audits are point-in-time snapshots and may be stale by the time the deepening runs. Skipping this step risks recommending fixes for problems that have already been resolved (or missing problems the audit did not catch).

Perform these checks in parallel where possible. Log every fetched URL and the resulting status into `verification-log.json` next to `parsed-audit.json`.

**A. Direct fetches (always run):**

1. `WebFetch https://{{ target_domain }}/llms.txt` → record `present | missing | structured | non_standard`.
2. `WebFetch https://{{ target_domain }}/robots.txt` → parse `User-agent: GPTBot / ClaudeBot / PerplexityBot / Googlebot` blocks; record allow/block per crawler.
3. `WebFetch https://{{ target_domain }}/` → check `<head>` for `<link rel="alternate" type="text/plain" href="/llms.txt">`, presence of `<script type="application/ld+json">` blocks, Open Graph and Twitter Card meta tags.
4. For each page in `audit.pages[]` flagged as KRITISCH/HOCH: re-fetch the URL and verify the specific finding (e.g., "FAQPage schema missing" → check JSON-LD for `@type: FAQPage`).

**B. Sub-agent calls (run when relevant):**

Use the `Agent` tool to spawn these specialized skills. Run them in parallel by sending multiple Agent calls in a single message:

- `geo-crawlers` — for full crawler-access audit beyond the basic `robots.txt` check.
- `geo-llmstxt` — for standards-compliance check of an existing `llms.txt`.
- `geo-citability` — for page-level AI-citability scoring on top 3 pages from the audit.
- `geo-brand-mentions` — for current brand-mention status across AI-cited platforms (Wikipedia, Wikidata, Reddit, Quora).
- `firecrawl-scrape` — when a page needs full content extraction for chunking/Princeton-tactic application.

**C. Discrepancy handling:**

For every audit finding, decide:

- `CONFIRMED` — live check matches audit. Keep the finding as-is.
- `RESOLVED` — live check shows the issue has been fixed since the audit. Mark the measure as `skip_reason: "already resolved per live check on {date}"` and exclude it from the report; mention it in the audit-input-overview section as "resolved between audit date and report date".
- `WORSENED` — live check shows the issue is more severe than the audit indicates. Escalate the severity in the measure and add a note.
- `NEW` — live check found a new issue not in the audit. Add it as a SKILL_AUGMENTATION measure.

Write the result to `verification-log.json`:

```json
{
  "verified_at": "2026-05-12T11:00:00Z",
  "audit_age_days": 30,
  "checks": [
    {"finding_id": "F-001", "check_type": "llms.txt", "result": "CONFIRMED", "source": "https://example.com/llms.txt", "fetched_at": "..."},
    {"finding_id": "F-002", "check_type": "FAQPage_schema", "result": "RESOLVED", "evidence": "JSON-LD with @type FAQPage found"}
  ]
}
```

**D. Data security:**

- Strip PII from logs (phone numbers, emails, person names) before writing `verification-log.json`. The `parse_audit.py` script provides `sanitize_pii()` — call it on text passed to logs.
- Never write API keys, credentials, or auth tokens into any audit-related file.
- All fetches run server-side. The report itself contains no remote-asset references — fonts, scripts, and styles are inlined.
- If the user requests local-only mode (`--no-network` flag), skip Step 2.5 entirely and mark every measure with `verification_status: "not_verified_local_mode"`.

### Step 3 — Derive Measures

For every audit finding (from `findings[]` and `existing_actionplan[]`):

1. Classify it as a **GEO concern**, an **AEO concern**, or **both**.
2. Apply `references/audit-mapping.md` to find the relevant pragmatic and academic tactics.
3. For each measure, capture:
   - `title` (short, action-oriented)
   - `priority` (KRITISCH/HOCH/MITTEL/NIEDRIG — inherit from audit, never escalate without evidence)
   - `what` (concrete action — what changes on the site)
   - `why` (the evidence — cite Princeton study, industry data, or the underlying mechanism in 1–2 sentences with a number where possible)
   - `impact` (expected effect on Citation-Score / AI-Traffic / specific KPI — quantified range when supported by references)
   - `effort_hours` (numeric range)
   - `tactic_source` (`PRINCETON_CITE_SOURCES`, `PRINCETON_QUOTATION`, `PRINCETON_STATISTICS`, `PRINCETON_FLUENCY`, `PRAGMATIC_LISTICLE`, `PRAGMATIC_COMPARISON`, `PRAGMATIC_WIKIPEDIA`, `PRAGMATIC_ADVERTORIAL`, `PRAGMATIC_FILLING_GAPS`, `PRAGMATIC_CHUNKING`, `PRAGMATIC_RECENCY`, `PRAGMATIC_FANOUT`, `PRAGMATIC_ENGLISH_FOOTPRINT`, `STANDARD_LLMS_TXT`, `STANDARD_SCHEMA`, etc.)
4. Add **additional measures from the knowledge base that the audit missed** — common omissions include: Listicle strategy, Comparison-page strategy, Reddit/Quora presence (Perplexity hook), English-language footprint, Advertorial budget, Wikipedia/Wikidata entry, Recency tactic (year-in-title), Fan-out-query mapping. Mark these clearly as `Source: SKILL_AUGMENTATION` so the reader knows they are not in the original audit.

5. **Extension fields per measure.** When the LLM-Visibility extension is active, every measure additionally carries:
   - `visibility_confidence` — `{default, by_platform}` with values `HOCH | MITTEL | NIEDRIG`, anchored to `visibility-confidence-matrix.md`.
   - `speed_impact` — `SOFORT | 1–4_WOCHEN | 1–3_MONATE | 3–12_MONATE`.
   - `platform_impact` — array of platforms expected to benefit: `chatgpt | gemini | perplexity | claude | aio | copilot | grok`.
   - `track` — `TAKTISCH | STRATEGISCH` (per `llm-visibility-extension.md`).
   - `quickwin` — boolean (set in Step 3.5).
   - `confidence_anchor` — matrix-row tag or `UNANCHORED` (rare).
6. Tactic-source compliance: use only the values in the allowlist of `extension-tactic-mapping.md`. Buzzword tags (`LLM_RETRIEVAL`, `CHUNK_ENGINEERING`, etc.) are rejected by C-15.

### Step 3.5 — Quick-Wins-First Gating

After Step 3, evaluate every derived measure against the Quick-Win criteria from `llm-visibility-extension.md`:

- `effort_hours` ≤ 4.
- `speed_impact ∈ {SOFORT, 1–4_WOCHEN}`.
- `visibility_confidence` ≥ MITTEL.
- No external dependency on third-party publishers, editors, or community moderators.

Set `quickwin: true` on all measures that meet the criteria. Select the top 10 (by `visibility_confidence` desc, then by `effort_hours` asc) for the dedicated Section 3a. Excess Quick Wins keep `quickwin: true` and remain in the regular measure list.

If no measures qualify as Quick Wins, leave Section 3a empty with the note "Keine Quick Wins in dieser Audit-Konfiguration identifiziert".

### Step 3.6 — Compute Extension Scores

Using `scoring-methodology.md`:

1. Compute `AI_Citability_Score`, `Retrieval_Readiness_Score`, and (when inputs allow) `Cross_Source_Consistency_Score`.
2. Write each to `measures.extension_scores` with `value`, `sub_scores`, `inputs_hash` (sha256 over the input JSON), and `methodology_ref: "scoring-methodology.md"`.
3. If any sub-score has no input, suppress it (`null`) and renormalize remaining weights. Where insufficient inputs exist, suppress the entire score (`null`) with a footnote.

### Step 4 — Generate Step-by-Step Instructions

For each measure, decide whether a step-by-step instruction is feasible:

- **Include** when there is a clear tool path (CMS, Plugin, Cloud-Tool, Service) or a clear procedural sequence (e.g., "create page, write 5 Q&As, validate with Rich Results Test").
- **Omit** when the measure is purely strategic content production with no tool-anchored procedure (e.g., "publish original research", "build executive thought-leadership presence"). In this case, render only the strategic recommendation without a step section.

When tool-stack is detected: tailor instructions to that stack. When stack is `UNKNOWN`: provide the most common WordPress/Yoast/SASWP path as default, plus one alternative (Custom HTML/JSON-LD).

Step structure per measure:
```
1. <Tool/Location> → <Action>
2. <Tool/Location> → <Action>
...
N. Validation: <Verification tool + expected result>
```

Always end with a validation step where possible (Google Rich Results Test, llmstxt.org-validator, GSC URL-Inspection, manual prompt-test in target LLM, etc.).

### Step 5 — Render the HTML Report

1. Read the template `assets/report-template.html`.
2. Use `scripts/generate_report.py` to populate placeholders with the derived data.
3. Save the HTML to the user-specified output path (default: working directory, filename `geo-aeo-action-report-{{ audit_date }}.html`).
4. Confirm completion: report the output path, the number of GEO measures, the number of AEO measures, and the number of measures that include step-by-step instructions.

### Step 6 — Controlling / Final QA-Pass (Mandatory)

This step is non-negotiable. The report must not be handed to the user before passing a final controlling check. The cost of a wrong number in a C-level report is high. The cost of running the check is one minute.

Execute `scripts/verify_report.py --measures <measures.json> --audit <parsed-audit.json> --verification-log <verification-log.json> --report <report.html>`. The script returns a non-zero exit code if any controlling rule fails.

The controlling rules (see `references/controlling-checklist.md` for the canonical version):

1. **Coverage.** Every KRITISCH and HOCH finding from `parsed-audit.json` must be represented as a measure in `measures.json` OR explicitly marked `skip_reason` with a verification-log entry justifying the skip. No silent drops.
2. **Sourcing.** Every measure's `why` field must reference either:
   - a Princeton tactic tag (`PRINCETON_*`),
   - a pragmatic tactic tag (`PRAGMATIC_*`),
   - a standard tag (`STANDARD_*`), or
   - a verification-log entry (for SKILL_AUGMENTATION measures).
   No `why` lines without provenance.
3. **No fabricated statistics.** Every numeric claim (e.g., "+30%", "12.5M EUR") must trace back to `references/market-data.md`, `references/tactics-academic.md`, or the audit itself. The verifier scans for `\d+(\.\d+)?%|\d+([,.]\d+)?\s*(M|Mrd|EUR|USD)` patterns and flags any number not appearing in the source materials.
4. **Step-by-step integrity.** Every entry in `step_instructions` must reference an existing measure `id`. Orphan step-instructions are a defect. Conversely, every measure marked `step_by_step_feasible: true` must have a corresponding entry in `step_instructions`.
5. **Validation step present.** Every step-instruction must end with a `validation` field (Rich Results Test, GSC, llmstxt.org, prompt-test, etc.). Steps without a validation are rejected — there is no way to verify success otherwise.
6. **Neutrality.** No skill-internal files (references, templates, scripts) may contain client/brand/person names from the audit. The verifier greps the skill directory for the target_domain and the auditor's name and fails if found in any file other than the parsed-audit JSON or the rendered output.
7. **Placeholder closure.** The rendered HTML must contain zero `{{ ... }}` placeholders. Any unfilled placeholder is a defect.
8. **Verification consistency.** Every finding with `verification_status: CONFIRMED` must have a matching entry in `verification-log.json`. Measures with `WORSENED` status must have their priority escalated visibly. Measures with `RESOLVED` status must not appear in the active GEO/AEO sections — they appear only in the "resolved since audit" call-out.
9. **Anti-pattern conflict.** No measure may recommend a Princeton anti-pattern (A06 Keyword Stuffing, A07 Content Padding, A08 Persuasion Only, A09 Over-Simplification) or a pragmatic anti-pattern (T04, T05, T09, T13, T16). The verifier matches recommendation text against the anti-pattern descriptions.
10. **Tool-stack consistency.** When `detected_stack.cms == WORDPRESS`, step-instructions should default to WordPress paths. When `UNKNOWN`, both a default and an alternative path must be present. Inconsistencies are flagged.

If `verify_report.py` fails any rule, do NOT hand the report to the user. Either fix the underlying data and re-render, or surface the failures to the user with a clear list of what cannot be auto-resolved.

When all rules pass, write a `controlling-passed.json` summary next to the report (timestamp, rules-checked count, target_domain, audit_date) and only then mark the deliverable as complete.

### Step 7 — Optional Hand-Off

If the user requests a PDF version, suggest converting the HTML via a headless browser (e.g., Playwright, wkhtmltopdf, or browser print-to-PDF). The skill does not bundle a PDF renderer to remain lightweight.

## Quality Rules

These rules are non-negotiable. They are what makes the deepened report defensible.

1. **Never duplicate** what the audit already says. If the audit already specifies a measure, *deepen* it (add Princeton evidence, add platform-specifics, add a step-by-step) but do not just repeat the audit text.
2. **Never invent statistics**. Numbers must come from `references/market-data.md` or `references/tactics-academic.md`. If a number is unknown, write "range not yet quantified — track post-implementation".
3. **Always cite the tactic source** in the Why-line so reviewers can verify (e.g., "Princeton KDD 2024 — Quotation Addition tactic, +41% citation lift on benchmark").
4. **Never insert client names, brand names, or person names into the skill files or templates**. Brand-specific content lives only in the parsed-audit JSON and gets injected at render time.
5. **When the audit lacks data for a section**, mark the section as "Data not present in source audit — recommended to collect: X" instead of fabricating content.
6. **Anti-pattern hygiene**: explicitly call out any audit recommendation that conflicts with Princeton findings (e.g., audit suggests "Content-Padding to hit word counts" → flag as Princeton-negative tactic).
7. **Step-by-step quality**: each step must be executable by someone with basic admin access. No "configure backend" without naming the tool, location, and click path.

## Common Pitfalls

- **Over-listing**: if the audit has 24 measures, derive 24–35 deepened measures — not 60. Quality over breadth.
- **Tool assumptions**: do not assume the user runs WordPress unless the audit confirms it. When uncertain, surface alternatives.
- **Princeton over-application**: not every measure needs a Princeton tag. Reserve academic tactics for content-quality and citation work. Schema and crawler tactics map to industry standards instead.
- **Lost neutrality**: if you find yourself writing a brand name into a reference file, stop and move that content into the parsed-audit JSON instead.

## When in Doubt

Re-read `references/audit-mapping.md` — it contains the decision tree for ambiguous findings.
