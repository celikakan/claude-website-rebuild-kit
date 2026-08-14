# Audit Finding → Tactic Mapping

This reference is the decision tree the skill applies to every audit finding. Given a finding, it determines the matching tactic from the academic and pragmatic catalogs and the resulting deepened measure. Use it during Step 3 of the workflow.

## Mapping Logic

For each finding in `findings[]`:

1. Read `finding.category` and `finding.title`.
2. Look up the row in the table below.
3. Apply the listed Primary Tactic. If the finding is high severity, add the Secondary Tactic for a synergy effect.
4. Determine which sections of the report this measure belongs to (GEO / AEO / both).
5. Decide whether step-by-step instructions are feasible (see column "Step-by-Step Feasible").

## Mapping Table

| Audit Finding Category | Typical Finding Pattern | GEO/AEO | Primary Tactic | Secondary Tactic (synergy) | Step-by-Step Feasible |
|------------------------|-------------------------|---------|----------------|----------------------------|------------------------|
| SEO_ONPAGE | Meta Descriptions missing | GEO+AEO (indirect) | STANDARD_META | — | yes (CMS-based) |
| SEO_ONPAGE | Title Tags too short/long | GEO+AEO (indirect) | STANDARD_TITLES | — | yes (CMS-based) |
| SEO_ONPAGE | H1 missing on key pages | GEO+AEO | STANDARD_H1 + PRAGMATIC_CHUNKING (T03) | — | yes (page editor) |
| SEO_ONPAGE | Twitter/Open Graph cards missing | GEO (sharing surfaces) | STANDARD_OG_META | — | yes (CMS/Yoast) |
| SEO_TECHNICAL | Index bloat / waste pages | SEO foundation | STANDARD_NOINDEX | — | yes (CMS bulk-edit) |
| SEO_TECHNICAL | Security headers missing | SEO foundation | STANDARD_SECURITY_HEADERS | — | yes (.htaccess / Cloudflare) |
| SEO_TECHNICAL | HTML payload over 500 KB / CWV risk | GEO (AIO eligibility) | STANDARD_PERFORMANCE | — | yes (PSI + image opt) |
| GEO_SCHEMA | Organization schema missing/incomplete | GEO+AEO | STANDARD_SCHEMA_ORG + sameAs to platforms | — | yes (JSON-LD or plugin) |
| GEO_SCHEMA | FAQPage schema missing despite Q&As present | AEO | STANDARD_FAQ_SCHEMA + PRINCETON_QUOTATION (A02) | — | yes (JSON-LD or plugin) |
| GEO_SCHEMA | Article schema missing / no named author | GEO | STANDARD_ARTICLE_SCHEMA + PRINCETON_QUOTATION (A02) | PRINCETON_CITE_SOURCES (A01) | yes |
| GEO_SCHEMA | Product schema without aggregateRating | GEO (rich snippet) | STANDARD_AGGREGATE_RATING | — | yes |
| GEO_SCHEMA | LocalBusiness schema missing per location | GEO local | STANDARD_LOCALBUSINESS | — | yes (per-location work) |
| GEO_SCHEMA | Person schema missing on author bios | GEO + AEO | STANDARD_PERSON_SCHEMA + sameAs LinkedIn/ORCID | — | yes |
| GEO_ENTITY | No Wikipedia entry | GEO+AEO | PRAGMATIC_WIKIPEDIA (T14) | — | yes (process-based) |
| GEO_ENTITY | No Wikidata entry | GEO+AEO | STANDARD_WIKIDATA | — | yes (Wikidata workflow) |
| GEO_ENTITY | Brand authority weak overall | GEO | PRINCETON_QUOTATION (A02) + PRAGMATIC_EXPERT_CONTENT (T02) | PRAGMATIC_FILLING_GAPS (T01) | partial (strategic) |
| GEO_PLATFORM | Perplexity readiness low | GEO | PRAGMATIC_REDDIT/QUORA + PRAGMATIC_EXPERT_CONTENT (T02) | — | partial |
| GEO_PLATFORM | Google AI Overviews readiness low | GEO+AEO | STANDARD_FAQ + PRINCETON_CITE_SOURCES (A01) | PRINCETON_STATISTICS (A03) | yes |
| GEO_PLATFORM | ChatGPT readiness low | GEO+AEO | STANDARD_LLMS_TXT + PRINCETON_STATISTICS (A03) | PRINCETON_FLUENCY (A04) | yes |
| AEO_CRAWLER | GPTBot blocked or unknown | AEO | STANDARD_ROBOTS_TXT (allow GPTBot) | — | yes |
| AEO_CRAWLER | llms.txt missing | AEO+GEO | STANDARD_LLMS_TXT | — | yes |
| AEO_CRAWLER | llms.txt present but non-standard | AEO+GEO | STANDARD_LLMS_TXT (refactor) | — | yes |
| AEO_STRUCTURE | No Question-style H2 on key pages | AEO | PRAGMATIC_CHUNKING (T03) + Featured Snippet eligibility | — | yes (page editor) |
| AEO_STRUCTURE | No Answer-First 40–60 word block | AEO | PRAGMATIC_CHUNKING (T03) | — | yes (page editor) |
| AEO_STRUCTURE | Content padded for word count | AEO | Remove padding (anti-pattern A07) | — | yes (editorial review) |
| AEO_VOICE | Speakable schema missing | AEO | STANDARD_SPEAKABLE | — | yes |
| OFFPAGE | No press mentions | GEO | PRAGMATIC_ADVERTORIAL (T11) + PRAGMATIC_FILLING_GAPS (T01) | — | partial |
| OFFPAGE | No Reddit presence | GEO (Perplexity) | PRAGMATIC_REDDIT | — | yes (process) |
| OFFPAGE | No Quora presence | GEO (Perplexity) | PRAGMATIC_QUORA | — | yes (process) |
| OFFPAGE | No YouTube channel / weak channel | GEO (Perplexity) | PRAGMATIC_YOUTUBE | — | yes (process) |
| OFFPAGE | No English-language content (DACH brand) | GEO | PRAGMATIC_ENGLISH_FOOTPRINT (T13 reversed) | — | partial |
| LOCAL | NAP inconsistency | GEO local | STANDARD_NAP_CONSISTENCY | — | yes (manual audit) |
| LOCAL | GBP not claimed for all locations | GEO local | STANDARD_GBP | — | yes (GBP workflow) |
| LOCAL | Local listicles / hyperlocal pages missing | GEO local | PRAGMATIC_LISTICLE (T08) localized | — | yes (page creation) |
| KEYWORD | Sweet-spot keywords identified but no pages | GEO+SEO | Create dedicated pages with PRINCETON_CITE_SOURCES (A01) + PRINCETON_STATISTICS (A03) | PRAGMATIC_RECENCY (T07) | yes |
| KEYWORD | "Best X" / commercial queries unaddressed | AEO | PRAGMATIC_LISTICLE (T08) | PRAGMATIC_RECENCY (T07) | yes |
| KEYWORD | "X vs Y" / comparison queries unaddressed | AEO | PRAGMATIC_COMPARISON (T10) | — | yes |
| CONTENT | Vague qualitative claims | GEO | PRINCETON_STATISTICS (A03) | PRINCETON_CITE_SOURCES (A01) | partial (writing work) |
| CONTENT | Old / outdated content | GEO | PRINCETON_FLUENCY (A04) + PRAGMATIC_RECENCY (T07) | — | partial |
| CONTENT | No original research published | GEO | PRINCETON_CITE_SOURCES (A01) inverted: become the cited source | — | no (strategic) |
| CONTENT | Thought leadership without named expert | GEO+AEO | PRINCETON_QUOTATION (A02) + STANDARD_PERSON_SCHEMA | — | partial |
| CONTENT | Marketing tone overpowering facts | GEO | PRINCETON_STATISTICS (A03) | — | partial |

## Extension Mapping Rows (LLM Visibility Layer)

These rows complement the base mapping. They cover finding patterns that the LLM-Visibility extension surfaces. Tag choices follow `extension-tactic-mapping.md` strictly — no buzzword tags.

| Audit Finding Category | Typical Finding Pattern | GEO/AEO | Primary Tactic | Secondary Tactic (synergy) | Step-by-Step Feasible |
|------------------------|-------------------------|---------|----------------|----------------------------|------------------------|
| LLM_RETRIEVAL | Top-of-page lacks self-contained 40–60-word answer block | GEO+AEO | PRAGMATIC_CHUNKING (T03) | PRINCETON_FLUENCY (A04) | yes (page editor) |
| LLM_RETRIEVAL | Pages padded with marketing prose before the answer | GEO | RETRIEVAL_BLOCKER (remove padding) | PRAGMATIC_CHUNKING (T03) | yes (editorial review) |
| LLM_RETRIEVAL | Numerical claims absent on top commercial pages | GEO | PRINCETON_STATISTICS (A03) | PRINCETON_CITE_SOURCES (A01) | partial (writing work) |
| LLM_RETRIEVAL | Long intros before the actual answer (>200 words) | GEO+AEO | RETRIEVAL_BLOCKER (rewrite intro) | PRAGMATIC_CHUNKING (T03) | yes |
| LLM_RETRIEVAL | Marketing-tone copy without facts | GEO | RETRIEVAL_BLOCKER (replace persuasion with declarative facts) | PRINCETON_STATISTICS (A03) | partial |
| CITATION_SEEDING | Brand absent from URLs cited by ChatGPT/Perplexity for top-10 commercial prompts | GEO | CITATION_SEEDING_OUTREACH | PRAGMATIC_ADVERTORIAL (T11) | yes (process — outreach playbook) |
| CITATION_SEEDING | Competitor mentioned in 5+ Top-10 cited URLs, brand in 0 | GEO | CITATION_SEEDING_OUTREACH | PRAGMATIC_FILLING_GAPS (T01) | yes |
| CROSS_SOURCE | Brand facts diverge between owned site and Reddit / Wikidata / LinkedIn / YouTube | GEO+AEO | CROSS_SOURCE_CONSISTENCY | STANDARD_SCHEMA_ORG (sameAs) | partial (per-platform edits) |
| CROSS_SOURCE | Tagline or value-prop appears in 0 external platforms | GEO | CROSS_SOURCE_CONSISTENCY | PRAGMATIC_EXPERT_CONTENT (T02) | partial |
| ENTITY_DISTRIBUTION | sameAs incomplete (links <3 platforms) | GEO+AEO | STANDARD_SCHEMA_ORG (sameAs extension) | STANDARD_WIKIDATA | yes |
| ENTITY_DISTRIBUTION | No Person schema on author pages | GEO+AEO | STANDARD_PERSON_SCHEMA | PRINCETON_QUOTATION (A02) | yes |
| FANOUT_QUERY | "Best X" / "Top X" queries unaddressed by year-bearing page | GEO+AEO | PRAGMATIC_RECENCY (T07) | PRAGMATIC_LISTICLE (T08) | yes |
| FANOUT_QUERY | Comparison queries (X vs. Y) without dedicated page | AEO | PRAGMATIC_COMPARISON (T10) | — | yes |
| AUDIENCE_PROFILE | Audit lacks Wikidata entry for a brand with E-E-A-T content | GEO+AEO | STANDARD_WIKIDATA | PRAGMATIC_WIKIPEDIA (T14) | yes |

## Quick-Wins-First gating

After mapping every finding, evaluate each derived measure against the Quick-Win criteria (defined in `llm-visibility-extension.md`). A measure becomes a Quick Win when ALL conditions hold:

1. `effort_hours` ≤ 4.
2. `speed_impact ∈ {SOFORT, 1–4_WOCHEN}`.
3. `visibility_confidence` ≥ MITTEL (per `visibility-confidence-matrix.md`).
4. No external dependency on third-party publishers, editors, or community moderators.

Mark Quick Wins with `quickwin: true` and surface up to the top 10 in the dedicated report section. Excess Quick Wins remain in the regular measure list with `quickwin: true` so the Action-Plan Timeline can still route them.

## Audience-profile gating

Before recommending a tactic, check `audience_profile`:

- `KMU_MID_MARKET`: exclude Knowledge-Graph APIs, custom entity-distribution pipelines, open-data publishing programs. Limit `CROSS_SOURCE_CONSISTENCY` to manual workflows (Wikidata editor UI, LinkedIn admin, YouTube channel description) rather than API-driven approaches.
- `ENTERPRISE`: above tactics permitted; prefer them when scale justifies the build cost.

If a tactic would only fit an Enterprise profile but the audience is KMU, downgrade to NIEDRIG or exclude entirely.

## Augmentation Logic — Additions Beyond the Audit

After mapping each finding, scan the audit's `competitors[]` and `keywords[]` for opportunities the audit did not explicitly recommend. These are SKILL_AUGMENTATION entries:

1. **If competitors exist but no comparison pages exist on the audited domain** → add a PRAGMATIC_COMPARISON measure for each major competitor.
2. **If commercial keywords exist but no listicle pages exist** → add PRAGMATIC_LISTICLE measures (e.g., "Top X for Use Case Y").
3. **If `offpage.reddit_presence` is false and target platform includes Perplexity** → add a Reddit presence measure.
4. **If `offpage.wikipedia_entry` is false and brand has identity content** → add PRAGMATIC_WIKIPEDIA.
5. **If `meta.industry` matches DACH and `offpage` lacks English content** → add an English-footprint measure (T13 reversed).
6. **If audit shows healthy SEO but weak ChatGPT readiness** → add the T16 anti-pattern measure: rewrite on-page positioning to place the brand first on its own retrieved pages.
7. **If pages of type "best of" or "guide" lack year in title** → add PRAGMATIC_RECENCY for those pages.
8. **If audit shows fan-out test prompts but no fan-out query analysis** → add an English-fanout audit and a Reviews/Comparison content recommendation.

Mark each augmentation in the output with `tactic_source: SKILL_AUGMENTATION` so the reader sees these as added value beyond the original audit.

## Priority Inheritance

Inherit the audit's severity (KRITISCH/HOCH/MITTEL/NIEDRIG) for each derived measure. Never escalate. You may de-escalate to MITTEL when:

- The audit flags something as KRITISCH but the underlying data shows the metric is in an acceptable range (rare; only when audit appears miscalibrated and you have a defensible reason).

For SKILL_AUGMENTATION measures, assign priority based on:
- KRITISCH: blocks platform visibility (e.g., GPTBot blocked, no llms.txt for ChatGPT-heavy market).
- HOCH: large addressable lift in target platform (e.g., Reddit absent for Perplexity-heavy market).
- MITTEL: meaningful improvement with multi-week effort (e.g., Wikipedia entry).
- NIEDRIG: marginal lift or speculative (e.g., Grok strategy for non-US/EN markets).

## Quality Check

After mapping every finding, the skill should verify:

- Every KRITISCH/HOCH finding from the audit is represented in the output.
- At least one Princeton tactic appears in the output (A01–A05).
- At least one platform-specific tactic appears per active platform.
- The output is not just a re-listing of the audit text — every measure either deepens (adds tactic + step-by-step) or augments (introduces a tactic the audit missed).

If any of these checks fail, the skill should iterate before rendering.
