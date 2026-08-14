# Scoring Methodology — LLM Visibility Extension

This file defines the formulas, inputs, and reproducibility rules for the three new scores introduced by the LLM-Visibility extension. Every score is computed deterministically from inputs that exist in `parsed-audit.json`, `verification-log.json`, or the rendered measures. No subjective inputs.

Scoring rule C-13 (controlling-checklist) requires that every score appearing in the report be computable from the formulas below. Scores without traceable inputs fail controlling.

## Scope

Three new scores. No more. The Brief's "max 5 zusätzliche Scores" cap is interpreted conservatively to prevent score bloat. `Chunk_Engineering` and `Entity_Distribution` are sub-components of AI_Citability, not standalone scores.

| Score | Range | Purpose |
|-------|-------|---------|
| AI_Citability_Score | 0–100 | How likely is a page chunk to be cited by an LLM as the grounding source? |
| Retrieval_Readiness_Score | 0–100 | How accessible and structurally extractable is the site for AI crawlers? |
| Cross_Source_Consistency_Score | 0–100 | How consistent are brand facts across the web, Reddit, Wikidata, LinkedIn, and YouTube? |

## AI_Citability_Score

Weighted composite. Range 0–100. Inputs read from the parsed audit and the verification log.

```
AI_Citability_Score = round(
    0.25 * chunk_density_subscore        +   # T03 / PRAGMATIC_CHUNKING signal
    0.20 * entity_clarity_subscore       +   # named-entity density + schema coverage
    0.20 * schema_coverage_subscore      +   # Organization, Article, FAQPage, Person
    0.15 * source_citation_subscore      +   # Princeton A01 — inline citations present
    0.10 * statistical_density_subscore  +   # Princeton A03 — numerical-claim density
    0.10 * fluency_subscore                  # Princeton A04 — readability/structure
)
```

### Sub-scores (each 0–100)

- **chunk_density_subscore**: share of top-10 audited pages that contain a self-contained answer block (40–60 words) within the first 600 chars. Source: page-level findings or `firecrawl-scrape` output. Formula: `(pages_with_answer_block / total_audited_pages) * 100`.
- **entity_clarity_subscore**: share of pages naming the primary entity (brand/product) AND a secondary entity (location/methodology/persona) within the first 600 chars. Formula: `(pages_with_2_named_entities / total_audited_pages) * 100`.
- **schema_coverage_subscore**: share of strategic schema types present on the relevant pages. Counts: Organization on homepage, Article on insight pages, FAQPage on Q&A pages, Person on author bios. Formula: `(schema_types_present / 4) * 100`.
- **source_citation_subscore**: share of factual claims on top-10 pages backed by an inline citation (link, footnote, named source). Formula: `(claims_with_citation / total_claims_sampled) * 100`. If sampling is not feasible, fall back to a 3-bucket estimate from audit text: `0/50/100` for `none/some/many`.
- **statistical_density_subscore**: numerical claims per 1,000 words, normalized. Formula: `min(100, (numbers_per_1000_words / 4) * 100)`. A density of ≥4 numbers per 1,000 words saturates at 100.
- **fluency_subscore**: derived from existing audit `scores.geo.content_quality` if present; otherwise 50 (neutral). Never invented.

### Defaults when inputs missing

Any sub-score whose inputs are missing defaults to `null` and is **excluded** from the weighted average. The remaining weights are renormalized. If <3 sub-scores have inputs, the AI_Citability_Score is suppressed entirely and the report shows `—` for this card with a note "insufficient input data".

## Retrieval_Readiness_Score

Weighted composite. Range 0–100. All inputs are binary or directly measurable.

```
Retrieval_Readiness_Score = round(
    0.30 * llms_txt_subscore          +   # standard-compliant llms.txt
    0.25 * crawler_access_subscore    +   # GPTBot / ClaudeBot / PerplexityBot allowed
    0.20 * speed_subscore             +   # Core Web Vitals on Top-10 pages
    0.15 * schema_org_subscore        +   # Organization + sameAs completeness
    0.10 * answer_first_subscore          # H2-as-question pattern on key pages
)
```

### Sub-scores

- **llms_txt_subscore**: 0 (missing), 50 (present non-standard), 100 (standard-compliant per `llmstxt-spec.md`).
- **crawler_access_subscore**: average of binary allowed/blocked across GPTBot, ClaudeBot, PerplexityBot, Googlebot. Each crawler counts 25 points.
- **speed_subscore**: 100 if Top-10 pages pass CWV thresholds; 50 if 50–80 % pass; 0 if <50 % pass. Source: `scores.seo.performance` or Lighthouse data.
- **schema_org_subscore**: 100 if Organization schema present AND `sameAs` includes ≥3 platforms; 50 if Organization present but `sameAs` incomplete; 0 if missing.
- **answer_first_subscore**: share of top informational pages with H2-as-question pattern. `(pages_with_question_h2 / total_informational_pages) * 100`.

## Cross_Source_Consistency_Score

Range 0–100. Compares brand facts across platforms. Inputs come from Apify Reddit/Quora scrapes, Wikidata API, LinkedIn company page, and YouTube channel description.

```
Cross_Source_Consistency_Score = round(
    0.25 * core_facts_match_subscore     +   # name, founding year, HQ, founder
    0.20 * messaging_alignment_subscore  +   # tagline/value-prop alignment across owned + earned
    0.20 * sameAs_completeness_subscore  +   # platforms linked from Organization schema
    0.15 * wikidata_subscore             +   # Wikidata entity exists + linked
    0.10 * reddit_consistency_subscore   +   # Reddit mentions consistent with site claims
    0.10 * youtube_consistency_subscore      # YouTube descriptions consistent with site claims
)
```

### Sub-scores

- **core_facts_match_subscore**: count of brand facts (name spelling, founding year, HQ city, founder name) consistent across at least 3 sources. `(consistent_facts / 4) * 100`.
- **messaging_alignment_subscore**: 100 if tagline/value-prop appears verbatim or near-verbatim on ≥3 platforms; 50 if 1–2; 0 if 0.
- **sameAs_completeness_subscore**: `(linked_platforms / 6) * 100` where the 6 reference platforms are LinkedIn, Wikipedia, Wikidata, YouTube, X/Twitter, GitHub (replace last with industry-specific if irrelevant).
- **wikidata_subscore**: 100 if Wikidata entity exists AND links to homepage; 50 if exists but unlinked; 0 if absent.
- **reddit_consistency_subscore**: 0 if no Reddit mentions; 50 if mentions exist but contradict site facts; 100 if mentions exist and align with site facts.
- **youtube_consistency_subscore**: equivalent logic for YouTube channel description and pinned video.

### When to skip

If `audience_profile == KMU_MID_MARKET` AND fewer than 2 sub-scores have inputs, suppress the Cross_Source_Consistency_Score from the scoreboard. Smaller brands rarely have measurable cross-source signals, and a low score caused by lack of measurement (rather than lack of consistency) is misleading. Display `—` and a footnote.

## Score-to-grade mapping

Use the same grade scale as the existing SEO/GEO/AEO scores (defined in `generate_report.py`):

- ≥ 80 → "Sehr gut"
- ≥ 55 → "Ausbaufähig"
- ≥ 40 → "Handlungsbedarf"
- <  40 → "Kritisch"

## Reproducibility

A second run of the deepening workflow on the same `parsed-audit.json` and `verification-log.json` MUST produce identical scores. The skill MUST NOT randomize, weight by recency, or apply unspecified heuristics. If you find yourself wanting to add a heuristic — write it into this file first, then implement it.

## Anti-fabrication

Scores written into the report MUST be computable by following the formulas above with inputs traceable to either `parsed-audit.json`, `verification-log.json`, or sub-agent output logs. Controlling rule C-13 enforces this: every score in the rendered HTML must appear in `measures.json` under `extension_scores.{score_name}.value` with a `inputs_hash` for reproducibility.

If a score cannot be computed, write `null` and surface "—" in the report. Never estimate a score "from feel".
