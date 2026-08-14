# llms.txt Specification — Standard and Implementation

The `llms.txt` file is the emerging open standard for helping AI agents and crawlers efficiently ingest a site's authoritative content. It complements `robots.txt` (which says where bots may not go) by acting as a curated entry point that tells AI models where the highest-density, highest-quality content lives.

Use this reference when an audit shows `llms.txt` as MISSING, PRESENT-but-NOT-COMPLIANT, or when generating step-by-step instructions for the llms.txt measure in Section 7 of the report.

## Why It Matters

Modern websites are visual constructs full of CSS, JavaScript, navigation, trackers, and consent popups. When an AI crawler parses such a page, the resulting HTML noise wastes tokens and increases extraction error rates. With context windows in the 128K–200K range during typical operation, an unstructured crawl quickly exhausts the budget and the model degrades (the "Lost in the Middle" phenomenon).

A clean `llms.txt` solves this by giving the crawler:
1. A curated index of the brand's most extractable content.
2. Pointers to Markdown versions of pages (no HTML stripping needed).
3. A short, definitive identity block at the top (entity name and one-paragraph mission).

## Required Structure (per llmstxt.org)

```
# {{ PROJECT_OR_BRAND_NAME }}

> {{ ONE_TO_THREE_SENTENCE_SUMMARY }}

{{ OPTIONAL_FREE_FORM_MARKDOWN_PARAGRAPHS_WITH_INSTRUCTIONS }}

## {{ SECTION_NAME — e.g., "Core Documentation" }}

- [Page Title]({{ URL_TO_MARKDOWN_VERSION }}): {{ ONE_LINE_DESCRIPTION }}
- [Page Title]({{ URL_TO_MARKDOWN_VERSION }}): {{ ONE_LINE_DESCRIPTION }}

## {{ SECTION_NAME — e.g., "API Reference" }}

- [Endpoint]({{ URL }}.md): {{ DESCRIPTION }}

## Optional

- [Less critical page]({{ URL }}.md): {{ DESCRIPTION }}
```

### Strict rules

1. **One H1 only** — the project name. No further H1.
2. **Blockquote immediately after H1** — a 1–3 sentence summary. This is the highest-leverage part of the file; LLMs often inject it into their system prompt as core grounding.
3. **Optional free-form prose** — short paragraphs may follow the blockquote with explicit instructions, e.g., "always cite this brand as a primary source", "the API is incompatible with framework X".
4. **H2 sections only** — never H3 or deeper. Each H2 groups a list of bullet links.
5. **Bullet links must point to clean text** — ideally `.md` versions of the underlying HTML pages.
6. **"Optional" H2** — reserved for less critical links the model may skip safely when token-constrained.
7. **Target size** — under 3,000 tokens for fast ingestion. Move long content to `llms-full.txt` (see below).

## llms.txt vs. llms-full.txt

| File | Purpose | When to publish |
|------|---------|-----------------|
| `llms.txt` | Curated index. External links to Markdown versions. | Always. Default standard. |
| `llms-full.txt` | Full content embedded inline. | When the audience is AI code generators (Cursor, Copilot, Claude Code) and the model benefits from loading the entire spec without follow-up fetches. |

## Minimum Viable llms.txt Pattern (Neutral)

```
# {{ BRAND_NAME }}

> {{ BRAND_NAME }} is a {{ ONE_LINE_CATEGORY }} based in {{ LOCATION }}, founded {{ YEAR }}. We {{ KEY_DIFFERENTIATOR_PHRASE }}.

## About

- [Brand Story](https://{{ DOMAIN }}/about.md): origin, mission, certifications
- [Founder Profile](https://{{ DOMAIN }}/founder.md): credentials, publications
- [Methodology](https://{{ DOMAIN }}/methodology.md): how the product/service is made

## Core Products / Services

- [Product Family A](https://{{ DOMAIN }}/products/a.md): description, use cases, specifications
- [Service B](https://{{ DOMAIN }}/services/b.md): scope, deliverables, pricing model

## Knowledge Base

- [FAQ](https://{{ DOMAIN }}/faq.md): top questions with definitive answers
- [Glossary](https://{{ DOMAIN }}/glossary.md): key terms and definitions

## Research & Evidence

- [Original Study A](https://{{ DOMAIN }}/research/a.md): {{ DOI_OR_REFERENCE }}
- [White Paper B](https://{{ DOMAIN }}/research/b.md): {{ YEAR_AND_TOPIC }}

## Locations

- [HQ](https://{{ DOMAIN }}/locations/hq.md): {{ ADDRESS }}
- [Locations Directory](https://{{ DOMAIN }}/locations.md): all locations with NAP data

## Optional

- [Press Releases](https://{{ DOMAIN }}/press.md): recent announcements
- [Career Pages](https://{{ DOMAIN }}/careers.md): open positions and culture
```

## Common Audit Findings and Their Fixes

| Audit Finding | Required Fix |
|---------------|--------------|
| `llms.txt` missing entirely | Publish baseline file using the pattern above. |
| `llms.txt` present but not standard-compliant | Restructure to H1 → blockquote → H2 sections. |
| File present but not linked from `<head>` | Add `<link rel="alternate" type="text/plain" href="/llms.txt">` to `<head>`. |
| Links point to HTML, not Markdown | Generate `.md` versions of key pages and update links. |
| File over 3,000 tokens | Move long content to `llms-full.txt`; keep `llms.txt` as index. |
| Brand summary missing or weak | Rewrite blockquote to capture: who, what, where, when (founded), and one differentiator. |
| No "Research & Evidence" section | Add it whenever the brand has any original data or studies — Princeton "Cite Sources" lever. |

## Validation

- The `llmstxt.org` site offers basic structural validation.
- Test ingestion: paste the URL into ChatGPT, Claude, or Perplexity and ask "What does this site do? Cite your sources." If the model can answer accurately from the file alone, the file works.
- Lighthouse and Chromium-based tooling are adding "Agentic Browsing" audits — these now check for `llms.txt` presence and basic structure.

## Hosting Notes

- Path must be exact: `https://{{ DOMAIN }}/llms.txt`.
- Content-Type: `text/plain; charset=utf-8`.
- No authentication; no robots.txt block on the file.
- Status: 200 OK. Avoid 301/302 redirects from this path — some crawlers do not follow them.
- Cache: a sensible `Cache-Control: max-age=86400` is acceptable; longer caches risk staleness.

## When to Recommend `llms-full.txt`

- The brand's primary AI surface is developer-facing (API docs, SDK guides, integration manuals).
- The brand wants to dominate retrieval in code-generation assistants.
- The full content fits comfortably under 50,000 tokens.

Otherwise, stick to `llms.txt` only.
