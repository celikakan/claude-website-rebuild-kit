# LLM Visibility Extension — Retrieval / Citability / Cross-Source Layer

This file is the master reference for the LLM-Visibility extension of the GEO/AEO Deepdive skill. It defines the scope, principles, additive workflow, and guardrails. It does NOT replace any existing reference — it augments them.

## Why this extension exists

Classical GEO/AEO mixed SEO foundations with citation hygiene. By 2026 the dominant question for many brands is no longer "Do we rank in Google?" but "Do ChatGPT, Perplexity, Gemini, and AI Overviews cite us?". This extension answers that question with operative levers, measurable scores, and platform-specific confidence ratings.

The extension is **additive**. Every existing tactic, controlling rule, and template section remains in force. SEO foundations remain load-bearing for Google AI Overviews (76 % organic overlap) and ChatGPT-Shopping (~99 % Google Merchant Center sourced). Do not downgrade SEO work — re-prioritize it relative to retrieval levers.

## Operating principles

1. **Retrieval-First, SEO-Load-Bearing.** Retrieval logic drives prioritization; SEO foundation remains a prerequisite for the platforms that depend on it. Recommending "drop SEO" is a BLOCKER.
2. **Anti-Duplication.** Every new tactic class maps to an existing Princeton/Pragmatic/Standard tag where overlap exists. Only three genuinely new tactic_source values are introduced (see `extension-tactic-mapping.md`).
3. **Evidence over Buzzwords.** Every new score has a formula. Every Visibility-Confidence value comes from a matrix entry. No "AI-theoretical" prose in the rendered report.
4. **Hard limits.** Max 25 total measures, max 10 Quick Wins, max 3 new scores, max 2 new report sections. See `controlling-checklist.md` rules C-13 to C-16.
5. **Business-readable.** Technical terms appear only where they earn their place. No jargon without definition.

## What changes vs. base skill

| Aspect | Base skill | Extended skill |
|--------|-----------|----------------|
| tactic_source allowlist | PRINCETON_*, PRAGMATIC_*, STANDARD_*, SKILL_AUGMENTATION | Above + 3 new: `CITATION_SEEDING_OUTREACH`, `CROSS_SOURCE_CONSISTENCY`, `RETRIEVAL_BLOCKER` |
| Per-measure fields | priority, what, why, impact, effort_hours, tactic_source | Above + `visibility_confidence`, `speed_impact`, `platform_impact[]`, `track` (TAKTISCH/STRATEGISCH) |
| Scores in scoreboard | SEO, GEO, AEO | Above + AI_Citability, Retrieval_Readiness, Cross_Source_Consistency |
| Report sections | 0–9 (existing) | Above + 3a "LLM Visibility Quick Wins" and 3b "LLM Visibility Blockers" embedded inside section 3 |
| Controlling rules | C-01 to C-12 | Above + C-13 to C-16 |
| Audience switch | none | `audience_profile`: KMU/Mid-Market vs. Enterprise — gates Enterprise-only tactics |

## What does NOT change

- Princeton KDD 2024 academic spine.
- 16 pragmatic tactics catalog (T01–T16).
- Anti-pattern conflict checks (C-09).
- Neutrality of skill internals (C-06).
- Live-Verification (Step 2.5).
- Output contract sections 0–9.

## Audience profile

The extension introduces `audience_profile` to the parsed audit. Allowed values:

- `KMU_MID_MARKET` — default. Limits recommendations to Quick Wins, simple Schema work, content rewrites, Reddit/Quora seeding, advertorial placements, Wikipedia/Wikidata workflows. Excludes Knowledge-Graph APIs, custom Entity-Distribution pipelines, open-data publishing.
- `ENTERPRISE` — unlocks: Knowledge Graph strategies, structured-data networks, Entity APIs, open-data publishing, multi-domain entity-distribution pipelines.
- `UNKNOWN` — treated as `KMU_MID_MARKET` for safety.

The audience profile is read in Step 3 (Derive Measures). Enterprise-only tactics that surface in a `KMU_MID_MARKET` audit must be downgraded to NIEDRIG or excluded entirely.

## Quick-Wins-First engine

Quick Wins are measures with **all** of these properties:

1. `effort_hours` ≤ 4 (single sit-down).
2. `speed_impact ∈ {SOFORT, 1–4_WOCHEN}`.
3. `visibility_confidence` ≥ MITTEL.
4. No external dependency on third-party publishers, editors, or community moderators.

Quick Wins receive `priority` re-stamped to KRITISCH or HOCH regardless of the audit's classification. Up to 10 Quick Wins go into the dedicated Section 3a. Excess Quick Wins remain in the regular measure list with `quickwin: true`.

## Strategisch vs. Taktisch

Every measure receives a `track` field:

- `TAKTISCH` — operative on-site fixes: chunking, FAQ, definition blocks, tables, schema, llms.txt, robots, semantic clarity, page rewrites. Implementable by the brand's content/tech team without external dependencies.
- `STRATEGISCH` — long-lever visibility work: Reddit/Quora seeding, Wikipedia/Wikidata, citation seeding outreach, paid advertorials, Original Research, entity-distribution programs, English-footprint build-out.

Mapping to existing P0/P1/P2 timeline: `TAKTISCH` measures dominate P0+P1; `STRATEGISCH` measures dominate P2. The two axes are complementary, not redundant.

## Tool activation matrix

External tools are invoked only when their preconditions are met. The skill MUST NOT default to "run everything".

| Tool | Activate when |
|------|---------------|
| Firecrawl (scrape) | `findings` contain CHUNK_BLOCKER signal, OR Top-3 pages need full-content extraction for retrieval-density analysis. |
| Apify (Reddit/Quora/SERP) | `target_platforms` includes `perplexity` AND (`offpage.reddit_presence == false` OR `offpage.quora_presence == false`), OR SERP snapshots needed for competitor citation analysis. |
| Perplexity Deep Research | Always run for Top-10 commercial prompts. Empirical citation data outweighs theoretical GEO assumptions. |
| OpenAI ChatGPT visibility tests | Run for brand-mention queries, comparison queries, recommendation queries. Validates Sichtbarkeit and Entity recognition. |
| Google AI Overview check | Run for query clusters where AIO presence is plausible (informational + commercial intent overlap). |

Tool selection is enforced via `scripts/tool_orchestrator.py` (optional helper; not BLOCKER-gated).

## What the extension is NOT

- **Not a replacement** for the audit pipeline. The base audit (`seo-audit` / `geo-audit` / `geo-citability`) still produces the input.
- **Not a Knowledge-Graph builder** for KMU clients. Enterprise-only tactics gate-keep with the audience profile.
- **Not a permission to fabricate.** Every new score, every confidence value, every tactic mapping has a source. See `scoring-methodology.md`, `visibility-confidence-matrix.md`, `extension-tactic-mapping.md`.

## When to apply the extension

Apply the extension by default for any audit dated 2025 or later. For older audits, apply the base workflow only — modern retrieval patterns may have shifted since the audit was taken.

If `audience_profile == ENTERPRISE`, also surface the Cross-Source-Consistency Score prominently. For `KMU_MID_MARKET`, prefer AI_Citability and Retrieval_Readiness as the headline scores.

## Read order

When the agent runs the deepening workflow, the read order for extension references is:

1. `llm-visibility-extension.md` (this file — orientation).
2. `extension-tactic-mapping.md` (anti-doubling rules).
3. `scoring-methodology.md` (score formulas).
4. `visibility-confidence-matrix.md` (confidence anchors).
5. Existing base references (Princeton, Pragmatic, Platform-Divergence, Audit-Mapping, Controlling-Checklist).
