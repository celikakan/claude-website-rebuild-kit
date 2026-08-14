# Controlling Checklist — Final QA Pass

This is the canonical checklist applied in Step 6 of the skill workflow. The script `scripts/verify_report.py` enforces it programmatically. The same checklist is also useful for a manual human review.

A report that does not pass every rule below must NOT be handed to the user. The cost of a wrong number in a C-level deliverable far exceeds the cost of fixing it before delivery.

## Rule Index

| ID | Rule | Severity if violated |
|----|------|---------------------|
| C-01 | Coverage of audit findings | BLOCKER |
| C-02 | Sourcing of every "why" line | BLOCKER |
| C-03 | No fabricated statistics | BLOCKER |
| C-04 | Step-by-step integrity | BLOCKER |
| C-05 | Validation step present | BLOCKER |
| C-06 | Neutrality of skill internals | BLOCKER |
| C-07 | Placeholder closure | BLOCKER |
| C-08 | Verification consistency | BLOCKER |
| C-09 | Anti-pattern conflict check | BLOCKER |
| C-10 | Tool-stack consistency | WARN |
| C-11 | Priority distribution sanity | WARN |
| C-12 | Effort estimate realism | WARN |
| C-13 | Extension scores have formula-traceable inputs | BLOCKER |
| C-14 | Visibility-Confidence values match the anchor matrix | BLOCKER |
| C-15 | Total measures within hard limits | BLOCKER |
| C-16 | SEO-Foundation guard — no "drop SEO" recommendations | BLOCKER |

BLOCKER violations exit the verifier with non-zero status. WARN violations are surfaced but do not block delivery — they require explicit user acknowledgment when present.

Rules C-13 to C-16 are added by the LLM-Visibility extension (see `llm-visibility-extension.md`). They apply only when the extension is active (any of `extension_scores`, `quickwin`, `visibility_confidence`, or `audience_profile` is present in `measures.json`).

---

## C-01 — Coverage

**Requirement:** Every finding in `parsed-audit.json` with severity `KRITISCH` or `HOCH` must be represented in `measures.json` (either as a derived measure or with `skip_reason` and a verification-log entry justifying the skip).

**Why it matters:** Silent drops of audit findings make the deepening unreliable. Clients lose trust if a flagged issue from their audit disappears with no explanation.

**Check method:**
```python
audit_kritisch_hoch_ids = {f.id for f in audit.findings if f.severity in ("KRITISCH", "HOCH")}
covered_ids = {m.source_finding_id for m in measures.geo_measures + measures.aeo_measures}
skipped_ids = {s.finding_id for s in measures.skipped}
missing = audit_kritisch_hoch_ids - covered_ids - skipped_ids
assert not missing
```

---

## C-02 — Sourcing

**Requirement:** Every measure's `why` field must declare a `tactic_source`. Allowed values:
- `PRINCETON_CITE_SOURCES`, `PRINCETON_QUOTATION`, `PRINCETON_STATISTICS`, `PRINCETON_FLUENCY`, `PRINCETON_AUTHORITY`
- `PRAGMATIC_*` (T01-T16 tags)
- `STANDARD_*` (Schema, robots.txt, llms.txt standards, NAP, GBP)
- `SKILL_AUGMENTATION` — but only if backed by a verification-log entry that surfaced the issue

**Why it matters:** "Because I said so" is not an acceptable justification in a paid deliverable. Every recommendation must be traceable.

---

## C-03 — No Fabricated Statistics

**Requirement:** Every number in measures, executive summary, anti-patterns, and platform-strategy sections must trace to one of:
- `references/market-data.md`
- `references/tactics-academic.md` (Princeton lifts)
- the parsed audit JSON
- the verification-log

**Check method:** The verifier scans the rendered HTML for patterns matching `\d+(\.\d+)?%`, `\d+([,.]\d+)?\s*(M|Mrd|EUR|USD)`, `\d+x` and asserts each match appears in the source materials.

**Why it matters:** A fabricated "+40 %" looks credible until a client asks for the source. Then trust collapses.

---

## C-04 — Step-by-step Integrity

**Requirement:**
- Every entry in `step_instructions` must reference an existing measure ID from `geo_measures` or `aeo_measures`.
- Every measure marked `step_by_step_feasible: true` must have a corresponding `step_instructions` entry.
- Orphan step instructions (no matching measure) are defects.

**Why it matters:** Inconsistencies between the measures sections and the steps section signal a sloppy workflow and undermine the report's credibility.

---

## C-05 — Validation Step Present

**Requirement:** Every step-instruction must end with a `validation` field. Allowed validations include:
- "Google Rich Results Test: <expected outcome>"
- "GSC URL-Inspection: indexed / refreshed"
- "llmstxt.org structural check: pass"
- "Manual prompt-test in <platform>: brand cited"
- "Lighthouse score before vs. after"
- Equivalent platform-specific verification methods

**Why it matters:** A step without a validation cannot be confirmed as done. The user has no way to know whether the implementation succeeded.

---

## C-06 — Neutrality

**Requirement:** The skill directory (`SKILL.md`, all files in `references/`, `assets/`, `scripts/`) must contain no client-specific names, brand names, or person names taken from any audit ever processed.

**Check method:** The verifier reads the target_domain from `parsed-audit.json`, derives plausible brand-name variants (capitalized, lowercased, hyphenated), and greps every skill-internal file. Matches anywhere outside the parsed-audit JSON or the rendered output file are violations.

**Why it matters:** The skill is intended to be reusable across many audits. Leaking client data into the skill itself is a confidentiality breach and a contamination risk for future clients.

---

## C-07 — Placeholder Closure

**Requirement:** The rendered HTML must contain zero `{{ ... }}` placeholders.

**Check method:** Regex scan the HTML for `\{\{\s*\w+\s*\}\}`. Any match is a defect.

**Why it matters:** Unfilled placeholders in a C-level deliverable are immediately obvious and devastating to perceived quality.

---

## C-08 — Verification Consistency

**Requirement:**
- Every finding with `verification_status: CONFIRMED` must have a matching entry in `verification-log.json` with the same finding_id.
- Findings with `WORSENED` status must have visibly escalated priority in their derived measure.
- Findings with `RESOLVED` status must NOT appear in the active GEO/AEO measure lists; they appear only in the "Resolved since audit" call-out.
- Findings with `NEW` status (discovered by live checks beyond the audit) must be marked as `SKILL_AUGMENTATION` and have a verification-log evidence link.

**Why it matters:** Live verification is meaningless if its outcomes are not faithfully reflected in the report.

---

## C-09 — Anti-pattern Conflict

**Requirement:** No measure's recommendation may match a known anti-pattern. The verifier checks recommendation text against the descriptions of:
- Princeton anti-patterns A06 (keyword stuffing), A07 (content padding), A08 (persuasion only), A09 (over-simplification)
- Pragmatic anti-patterns T04 (per-paragraph summaries), T05 (Wikipedia paraphrase), T09 (mass listicle scaling), T13 (German-only DACH), T16 (pure SEO without on-page positioning)

If a measure recommends e.g. "increase keyword density" — flag as conflict.

**Why it matters:** Recommending a tactic that the skill's own knowledge base classifies as harmful is internally contradictory.

---

## C-10 — Tool-stack Consistency

**Requirement:**
- When `detected_stack.cms == WORDPRESS`, step instructions for schema/SEO measures should use WordPress paths (Yoast, SASWP, Elementor) as the primary tool.
- When `detected_stack.cms == UNKNOWN`, every step-instruction must include both a default path (WordPress + Yoast + SASWP) AND one alternative (Custom HTML/JSON-LD, or Shopify, or Webflow).
- When stack is Shopify or Webflow, the WordPress default must NOT appear; instead use the platform-specific tools.

**Severity:** WARN. Inconsistencies are surfaced for review but do not block delivery.

---

## C-11 — Priority Distribution Sanity

**Requirement:** The distribution of priorities across all measures should look plausible:
- KRITISCH measures: 10-30 % of total
- HOCH measures: 30-50 %
- MITTEL measures: 20-40 %
- NIEDRIG measures: ≤10 %

Distributions where >50 % of measures are KRITISCH suggest priority inflation; where <5 % are KRITISCH despite KRITISCH findings in the audit suggest under-translation.

**Severity:** WARN.

---

## C-12 — Effort Realism

**Requirement:** Sum of `effort_hours` across all P0 measures should fit within a single sprint (≤40 hours). P1 within 3-4 weeks (40-160 h). P2 within several months. Outliers (single measure with `effort_hours > 80`) require a comment explaining why the effort is justified.

**Severity:** WARN.

---

## C-13 — Extension Scores Have Formula-Traceable Inputs

**Requirement:** Every score in `measures.extension_scores` (AI_Citability_Score, Retrieval_Readiness_Score, Cross_Source_Consistency_Score) must include:

- `value`: integer 0–100 or `null`.
- `sub_scores`: dict of sub-score names → integers 0–100 or `null`.
- `inputs_hash`: deterministic hash over the inputs used to compute the score (so reruns are reproducible).
- `methodology_ref`: literal string `"scoring-methodology.md"`.

A score with `value` not `null` and missing/empty `sub_scores`, or `value` ≠ the formula applied to `sub_scores`, fails.

**Why it matters:** Scores are headline numbers in a C-level report. They must be reproducible. Anchoring them to a documented formula prevents drift across reruns and "feel-based" overrides.

---

## C-14 — Visibility-Confidence Values Match the Anchor Matrix

**Requirement:** Every `visibility_confidence` value (default and per-platform) in any measure must match a row of `references/visibility-confidence-matrix.md`. The verifier reads the matrix anchors and validates that the agent's chosen value is consistent.

Measures with `confidence_anchor: UNANCHORED` are allowed but counted as WARN, not BLOCKER.

**Why it matters:** Without a matrix anchor, confidence levels become subjective and inflate over time. The matrix keeps them empirically grounded.

---

## C-15 — Total Measures Within Hard Limits

**Requirement:** The extension introduces these hard limits:

- `len(geo_measures) + len(aeo_measures)` ≤ 25 (across all priorities).
- Quick Wins (`quickwin: true` AND appearing in the dedicated section) ≤ 10.
- `len(extension_scores)` ≤ 3.
- Newly added dedicated sections beyond the base output contract ≤ 2 (currently: LLM Visibility Quick Wins, LLM Visibility Blockers).

The verifier also rejects any `tactic_source` value that does not appear in the updated allowlist in `extension-tactic-mapping.md`. Specifically, the buzzword classes (`LLM_RETRIEVAL`, `CHUNK_ENGINEERING`, `FANOUT_QUERY_MAPPING`, `ENTITY_DISTRIBUTION`, `SEMANTIC_DENSITY`, `RETRIEVAL_FIRST_CONTENT`, `AI_CONTENT_STRUCTURE`, `AI_CITABILITY`, `CITATION_SEEDING`, `CROSS_SOURCE_VALIDATION`) are rejected — the agent must use the resolved tags.

**Why it matters:** Without hard limits, the deepening drifts into bloat. The extension brief explicitly caps these counts. Buzzword tags also bypass the existing taxonomy and produce duplicated measures.

---

## C-16 — SEO-Foundation Guard

**Requirement:** No measure or executive summary text may recommend dropping, skipping, or de-prioritizing classical SEO foundations. The verifier scans `measures.json` for forbidden phrases including:

- "drop SEO"
- "skip SEO"
- "SEO is obsolete"
- "SEO no longer matters"
- "ignore Google rankings"
- "ignore organic SEO"

**Why it matters:** Google AI Overviews cite organic-ranking pages ~76 % of the time; ChatGPT-Shopping is ~99 % sourced from Google Merchant Center. Dropping SEO collapses AI visibility through the back door. SEO is load-bearing for the LLM-Visibility extension, not optional.

---

## Verifier Output Contract

`verify_report.py` writes a JSON summary to `controlling-result.json`:

```json
{
  "verified_at": "2026-05-12T14:00:00Z",
  "rules_checked": 12,
  "blocker_violations": [],
  "warn_violations": [
    {"rule": "C-11", "detail": "78% of measures flagged KRITISCH — priority inflation suspected"}
  ],
  "pass": true,
  "target_domain": "example.com",
  "audit_date": "2026-05-01",
  "report_path": "/path/to/report.html"
}
```

Exit code:
- `0` — all BLOCKER rules pass (WARN may still be present)
- `1` — at least one BLOCKER rule failed
- `2` — verifier itself encountered an error (file not found, malformed JSON, etc.)

## Manual Review Companion

For high-stakes deliverables, run a manual review in addition to the script. The human reviewer should:

1. Read the Management Summary alone and assess whether the C-level reader would act on it.
2. Read 2-3 random measures and verify the `why` line is convincing without further context.
3. Pick one step-by-step and mentally walk through it — would a junior admin succeed?
4. Cross-check that the Action-Plan Timeline can plausibly be executed in the stated effort.
5. Confirm the report uses the client's own language (e.g., German if the audit is German) consistently.

Sign off the manual review by appending a `manual_review_passed_by` field to `controlling-result.json`.
