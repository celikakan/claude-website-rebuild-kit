# Extension Tactic Mapping — Anti-Doubling Rules

This file prevents tactic duplication. The original extension brief proposed 10 new `tactic_source` classes; many overlap with existing Princeton/Pragmatic/Standard tags. This file resolves the overlap: where a proposed class duplicates an existing tag, use the existing tag. Only three genuinely new classes are introduced.

Controlling rule C-15 enforces this mapping. Using a proposed class instead of its existing equivalent is a BLOCKER violation.

EXTENSION_VERSION: 1.0.0 (bump when this file changes).

## Resolution table — proposed → existing

| Proposed class (brief) | Resolved tactic_source | Reason |
|------------------------|------------------------|--------|
| `LLM_RETRIEVAL` | `PRAGMATIC_CHUNKING` (T03) + `PRINCETON_FLUENCY` (A04) | Retrievability = self-contained chunk + fluent prose. Both tags exist. |
| `CHUNK_ENGINEERING` | `PRAGMATIC_CHUNKING` (T03) | Identical scope. Use T03 with extended description in the measure body. |
| `FANOUT_QUERY_MAPPING` | `PRAGMATIC_RECENCY` (T07) + `PRAGMATIC_LISTICLE` (T08) | Year-in-title and listicles are the fan-out intercept levers. Use both, depending on the page type. |
| `ENTITY_DISTRIBUTION` | `STANDARD_WIKIDATA` + `STANDARD_SCHEMA_ORG` (sameAs) + `PRAGMATIC_WIKIPEDIA` (T14) | Entity distribution = Wikidata + Wikipedia + sameAs. All exist. |
| `SEMANTIC_DENSITY` | `PRINCETON_STATISTICS` (A03) + `PRINCETON_FLUENCY` (A04) | Density = stats + cleanly written. Both Princeton tactics. |
| `RETRIEVAL_FIRST_CONTENT` | `PRAGMATIC_CHUNKING` (T03) + `PRINCETON_STATISTICS` (A03) | Same lever as chunking + stats density. |
| `AI_CONTENT_STRUCTURE` | `PRAGMATIC_CHUNKING` (T03) + `STANDARD_FAQ_SCHEMA` | Structure = chunks + FAQ markup. Both exist. |
| `AI_CITABILITY` | — | Composite *score*, not a tactic. Reserve for the score output, NOT for `tactic_source`. |
| `CITATION_SEEDING` | **NEW** → `CITATION_SEEDING_OUTREACH` | Operational outreach to third-party publishers is a distinct workflow not covered by T01/T11/T14. See "Genuinely new" below. |
| `CROSS_SOURCE_VALIDATION` | **NEW** → `CROSS_SOURCE_CONSISTENCY` | Fact alignment across Reddit / Wikidata / LinkedIn / YouTube vs. owned site is not covered by existing tags. |
| (extension addition) | **NEW** → `RETRIEVAL_BLOCKER` | Negative findings (marketing tone, long intros, missing definitions, semantic noise) require a tag for the "what to remove" measures, distinct from positive tags. |

## Genuinely new tactic_source values

Three values join the controlling allowlist (rule C-02):

### CITATION_SEEDING_OUTREACH

**Scope:** Operational program to earn inclusion in URLs already cited by ChatGPT / Perplexity / Gemini for the brand's top-10 commercial prompts. Distinct from T01 (which is the strategic intent), T11 (paid advertorials), and T14 (Wikipedia).

**Workflow shape:**
1. Pull cited URLs per prompt from Perplexity Deep Research.
2. Cross-reference where competitors are mentioned and the brand is not.
3. For each gap, define an outreach action: polite publisher email, substantive comment, sponsored update, or paid placement.
4. Track inclusion via monthly re-prompt and citation diff.

**Why a new class:** T01 names the *concept* of filling gaps. CITATION_SEEDING_OUTREACH names the *operational program* — with cadence, outreach templates, tracking. Reports benefit from the distinction because the latter has measurable status (contacted / responded / included / cited).

**Anti-pattern guards:** Spammy comments, undisclosed sponsorships, and impersonation are excluded. The measure body must explicitly require honesty and disclosure where legally relevant.

### CROSS_SOURCE_CONSISTENCY

**Scope:** Programmatic alignment of brand facts (name spelling, founding year, HQ, founder, value-prop, taglines) across Reddit, Wikidata, LinkedIn, YouTube descriptions, Quora answers, and owned site. Distinct from sameAs (which is a schema field) — this addresses the *content* of those linked sources, not just the existence of the link.

**Workflow shape:**
1. Identify the brand's owned source-of-truth facts.
2. Scrape Reddit (Apify), Wikidata API, LinkedIn company page, YouTube channel, Quora profile.
3. Diff facts; flag inconsistencies.
4. Issue corrections via the platform's owner-edit flow (Wikidata claim, LinkedIn admin, YouTube channel description, Reddit moderator outreach where appropriate).

**Why a new class:** Existing sameAs work checks whether platforms are *linked*, not whether the facts *match*. Cross-source consistency is a separate operational lever.

### RETRIEVAL_BLOCKER

**Scope:** Tag for measures that *remove* an obstacle to retrieval, rather than add something. Includes:

- Marketing-tone rewrites (replace persuasion-only copy with declarative facts).
- Long intro removal (move the answer above the fold).
- Defining undefined terms (add a glossary block).
- Removing semantic noise (filler paragraphs, navigation-style intros, redundant brand boilerplate).
- Resolving fact contradictions on owned content that confuse retrieval.

**Why a new class:** Existing Princeton anti-patterns (A06–A09) describe *what NOT to suggest*. RETRIEVAL_BLOCKER describes *what to fix on the existing site*. The report needs both: the prevention tag (A06–A09 used in anti-patterns section) and the remediation tag (RETRIEVAL_BLOCKER used in measures section).

**Anti-pattern guards:** A RETRIEVAL_BLOCKER measure must not introduce a new anti-pattern (e.g., do not suggest per-paragraph summaries when removing a long intro — use a top-of-page BLUF chunk instead).

## Updated allowlist

The full tactic_source allowlist for the extended skill is:

```
PRINCETON_CITE_SOURCES
PRINCETON_QUOTATION
PRINCETON_STATISTICS
PRINCETON_FLUENCY
PRINCETON_AUTHORITY
PRAGMATIC_FILLING_GAPS         (T01)
PRAGMATIC_EXPERT_CONTENT       (T02)
PRAGMATIC_CHUNKING             (T03)
PRAGMATIC_INTENT_MATCH         (T06)
PRAGMATIC_RECENCY              (T07)
PRAGMATIC_LISTICLE             (T08)
PRAGMATIC_COMPARISON           (T10)
PRAGMATIC_ADVERTORIAL          (T11)
PRAGMATIC_SHOPPING_FEED        (T12)
PRAGMATIC_WIKIPEDIA            (T14)
PRAGMATIC_X_POSTS              (T15)
PRAGMATIC_REDDIT
PRAGMATIC_QUORA
PRAGMATIC_YOUTUBE
PRAGMATIC_ENGLISH_FOOTPRINT
STANDARD_META
STANDARD_TITLES
STANDARD_H1
STANDARD_OG_META
STANDARD_NOINDEX
STANDARD_SECURITY_HEADERS
STANDARD_PERFORMANCE
STANDARD_SCHEMA_ORG
STANDARD_FAQ_SCHEMA
STANDARD_ARTICLE_SCHEMA
STANDARD_AGGREGATE_RATING
STANDARD_LOCALBUSINESS
STANDARD_PERSON_SCHEMA
STANDARD_SPEAKABLE
STANDARD_LLMS_TXT
STANDARD_ROBOTS_TXT
STANDARD_WIKIDATA
STANDARD_NAP_CONSISTENCY
STANDARD_GBP
CITATION_SEEDING_OUTREACH      (NEW — extension v1.0)
CROSS_SOURCE_CONSISTENCY       (NEW — extension v1.0)
RETRIEVAL_BLOCKER              (NEW — extension v1.0)
SKILL_AUGMENTATION
```

Tags introduced in the extension are versioned. Reports record the EXTENSION_VERSION used at render time so older deliverables remain auditable when this file evolves.

## Behavior when a brief class is still used

If a measure surfaces with `tactic_source: LLM_RETRIEVAL` (or any other proposed-but-resolved class), the verifier (`verify_report.py` rule C-15) rejects the report. The agent must rewrite the measure using the resolved tag(s) from the table above.

This is intentional: it prevents the report from carrying buzzword-only tags that look modern but duplicate existing taxonomy.

## Mapping cheat sheet for the agent

When deriving a measure in Step 3:

1. Read the audit finding.
2. Ask: "Does an existing Princeton/Pragmatic/Standard tag cover this?"
3. If yes → use the existing tag.
4. If no → check whether one of the three new tags applies.
5. If still no → flag as `SKILL_AUGMENTATION` with a verification-log entry.

Never invent a new tactic_source value at runtime. The allowlist above is the only valid set.
