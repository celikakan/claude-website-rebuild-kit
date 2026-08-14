# Visibility Confidence Matrix

Every measure produced by the deepening workflow receives a `visibility_confidence` value (HOCH / MITTEL / NIEDRIG). This file is the canonical decision table. Controlling rule C-14 requires every confidence value in the rendered report to map to one of the rows below.

The confidence is **platform-conditional**: a measure with HOCH confidence for Perplexity may have NIEDRIG confidence for ChatGPT, depending on which platform's grounding behavior it addresses. The agent must record a `visibility_confidence` object with per-platform values where divergence exists:

```json
"visibility_confidence": {
  "default": "HOCH",
  "by_platform": {
    "perplexity": "HOCH",
    "gemini": "HOCH",
    "chatgpt": "MITTEL"
  }
}
```

When a measure addresses a single platform exclusively, only `default` is needed.

## Confidence anchors

### HOCH — strong empirical evidence

Assign HOCH when at least one of the following anchors applies:

| Anchor | Reason for HOCH |
|--------|-----------------|
| Princeton KDD 2024 effective tactic (A01–A04) on a page that already ranks Top-10 organic | Empirical lift documented: +30 to +115 % relative on Rank-5 pages. Combined with existing rankings, the page is in the grounding set. |
| Standard schema fix (Organization/Article/FAQPage/Product) on a Google-AIO-target market | AIO citations overlap ~76 % with organic; schema directly increases extractability. |
| `llms.txt` standardization on ChatGPT-target market | ChatGPT operates as a substantially independent ecosystem; llms.txt is a direct identity signal. |
| Reddit/Quora expert seeding on a Perplexity-target market | Reddit alone provides ~47 % of Perplexity's Top-10 cited sources on average. |
| ChatGPT-Shopping feed via Google Merchant Center on an e-commerce brand | ~99 % of ChatGPT-Shopping listings derive from organic Google Shopping. |
| Fixing a BLOCKED GPTBot in robots.txt for any brand active on ChatGPT | Direct unblocking of the dominant AI referrer (87,4 % of AI traffic). |
| Adding the current year to titles where annual relevance is plausible | Fan-out queries reliably append the year; documented industry pattern. |

### MITTEL — defensible mechanism, less direct evidence

Assign MITTEL when the mechanism is sound but the magnitude is uncertain, OR the lever is shared with many other brands and competitive pressure dilutes the effect:

| Anchor | Reason for MITTEL |
|--------|-------------------|
| Wikipedia entry creation (incl. temporary ones) | Documented lift for months even after deletion, but creation risk and Wikipedia editorial gates are real. |
| Wikidata entry creation | Useful for entity recognition but not directly tied to citation; adds confidence to the entity graph rather than driving citations alone. |
| Self-promotional listicles (Best X 2026) in a low-saturation category | Effective in industry observation, but high-saturation categories see diminishing returns. |
| Princeton Quotation Addition (A02) on a Commercial/Product page | Commercial pages benefit less than People & Society pages from quotation tactics. |
| Comparison pages (X vs. Y) for narrow B2B niches | Works in SaaS / B2B; less reliable for general consumer brands. |
| Paid advertorials on tier-1 publishers | Citation lift is observed, but ROI depends on the publisher's index strength and the buyer's market. |
| Authoritative voice (A05) in commercial contexts | Limited effect overall; niche wins in Debate/History/Science only. |

### NIEDRIG — speculative or marginal lift

Assign NIEDRIG when the lever is speculative for the target market, OR when the audience profile excludes the tactic:

| Anchor | Reason for NIEDRIG |
|--------|-------------------|
| Grok strategy (X posts) for non-US / non-EN markets | Grok's market share is small outside US/English-speaking dev/finance/crypto verticals. |
| Per-paragraph summaries (T04 anti-pattern variant) | Documented as ineffective; degrades human readability. |
| Wikipedia paraphrase content (T05 anti-pattern) | LLMs prefer the original; rewritten page rarely earns citation. |
| Knowledge-Graph API for `audience_profile == KMU_MID_MARKET` | Enterprise-only complexity; ROI rarely justifies on KMU budgets. |
| Custom entity-distribution pipeline for a single-domain brand | High build cost; the same lift can be achieved with sameAs + Wikidata + Wikipedia for a fraction of the effort. |
| Open-data publishing strategy without owned proprietary data | Without primary research as input, the program produces low-citability material. |

## Cross-platform divergence rules

When the same measure has different confidence per platform, follow these rules:

1. **AIO**: HOCH for schema, FAQ, Article, BLUF chunk, fluency cleanup. MITTEL for community plays. NIEDRIG for X posts.
2. **ChatGPT**: HOCH for llms.txt, Organization/sameAs, statistics density, Wikipedia/Wikidata. MITTEL for community plays. NIEDRIG for X posts.
3. **Perplexity**: HOCH for Reddit/Quora/YouTube, llms.txt, expert content. MITTEL for schema (Perplexity less SEO-coupled). NIEDRIG for X posts.
4. **Grok**: HOCH for X posts (US-EN markets only). MITTEL for nothing else. NIEDRIG for most non-X levers.
5. **Copilot**: HOCH for Bing Webmaster registration, LinkedIn presence. MITTEL for general AIO levers (transfer well). NIEDRIG for community plays (Copilot less community-grounded).

## When no anchor applies

If a proposed measure does not fit any row above, set `visibility_confidence: NIEDRIG` and flag the measure with `confidence_anchor: UNANCHORED`. Controlling rule C-14 treats UNANCHORED measures as warnings — the measure is allowed but the report displays a "not yet empirically anchored" note next to the confidence pill.

The agent must NOT invent its own confidence values. If a strong intuition disagrees with the matrix, propose an update to this file rather than override it at runtime.

## Maintenance

Update this file when new empirical evidence becomes available. Specifically:

- New Princeton-style academic studies → add anchors.
- Updated Perplexity / ChatGPT citation overlap data → adjust HOCH/MITTEL boundaries.
- Platform deprecations or API changes → remove obsolete anchors.

Every change to this file requires a corresponding bump of `EXTENSION_VERSION` (see `extension-tactic-mapping.md`), so previously generated reports remain auditable against the version that produced them.
