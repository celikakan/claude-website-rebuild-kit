# Pragmatic GEO/AEO Tactics

Industry-tested tactics with verdicts. Use these to deepen audit findings into concrete, evidence-backed measures. Each tactic includes when to apply, why it works, the mechanism, the risk, and a neutral example pattern.

When mapping audit findings to these tactics, prefer the tactic with the strongest evidence and the clearest tool path. Do not stack contradictory tactics on the same measure.

## Index

- **T01** — Filling the SERP/AIO Gaps ✅
- **T02** — Original Expert Content On-Site ✅
- **T03** — Top-of-Page Self-Contained Chunk (50 words, declarative) ✅
- **T04** — Per-Paragraph Summaries ❌
- **T05** — Rewriting Existing Content (e.g., Wikipedia paraphrase) ❌
- **T06** — Matching the Prompt Intent (informational vs. commercial vs. transactional) ✅
- **T07** — Year-in-Title (Recency Bias / Fan-out Queries) ✅
- **T08** — Self-Promotional Listicles ("Best X 2026" with own brand ranked) ✅
- **T09** — Mass-Scaled AI-Generated Listicles ❌
- **T10** — Competitor Comparison Pages (X vs. Y) ✅
- **T11** — Paid Advertorials on High-Authority Domains ✅
- **T12** — ChatGPT-Shopping Inclusion (via organic Google Shopping feed) ✅
- **T13** — German-Only Strategy for DACH Markets ❌
- **T14** — Wikipedia Entry — even temporary / deleted ones ✅
- **T15** — X (Twitter) Posts to Influence Grok ✅
- **T16** — Pure SEO Without On-Site Positioning ❌

---

## T01 — Filling the SERP/AIO Gaps ✅

**When to apply:** When competitors appear as sources in target LLM answers but the audited brand does not.

**Mechanism:** LLMs ground answers in a small set of retrieved sources. If a brand is absent from those sources, it is invisible regardless of brand strength. Getting added to the source corpus directly inserts the brand into the AI's grounding context.

**How:** Identify the URLs cited by ChatGPT/Perplexity/Gemini for the brand's top 10 commercial prompts. Cross-reference where competitors are mentioned and the brand is not. Then: write a polite email to the publisher, leave a substantive comment, sponsor the article, or otherwise earn inclusion.

**Risk:** Low if outreach is honest. Medium if comments are spam-like or sponsorship is hidden.

**Evidence:** Industry-confirmed tactic; reported as "very, very effective" in multi-client agency observations.

**Neutral example:**
> Pattern: For each top-10 prompt in the target industry, identify Top-5 cited URLs across ChatGPT/Perplexity/Gemini. List which Top-5 URLs lack a mention of the audited brand. For each gap, define an outreach action (email, sponsored update, comment).

---

## T02 — Original Expert Content On-Site ✅

**When to apply:** When the brand has subject-matter expertise but limited LLM citation rate.

**Mechanism:** When a brand publishes original, defensible expert content, LLMs gain a high-trust source to cite. Citation rate of the brand's own pages rises, and brand mentions in adjacent prompts rise even faster (the brand becomes the canonical source for its topic cluster).

**How:** Publish original analyses, primary research, methodology pieces, opinion-led perspectives that no competitor has. Bind to a named expert with credentials.

**Risk:** None at modest publishing volume. Avoid AI-generated bulk publishing — Google rankings can suffer.

**Evidence:** Documented multi-client increase from ~3% to ~60% citation rate on monitored prompts following a focused expert-content publishing program; correlated ~1100% brand-mention growth.

**Tag:** `PRAGMATIC_EXPERT_CONTENT`

---

## T03 — Top-of-Page Self-Contained Chunk ✅

**When to apply:** Almost universally on content pages.

**Mechanism:** LLMs do not load full pages. They retrieve and reason over chunks. A 40–60-word self-contained block, placed high on the page, in clear declarative language, with relevant entities named, is the chunk most likely to be selected as the answer-grounding fragment.

**How:** Above the first H2 (or directly after the H1), insert a 2–3 sentence block that answers the page's primary question definitively. Name the entities (product, methodology, brand, location, condition) directly.

**Risk:** None.

**Evidence:** Aligns with retrieval-augmented generation architecture used across ChatGPT, Perplexity, Gemini, Bing Chat, and Copilot.

**Tag:** `PRAGMATIC_CHUNKING`

---

## T04 — Per-Paragraph Summaries ❌

**When to avoid:** Whenever it would degrade human readability.

**Why it fails:** Aggressive per-paragraph summarization hurts the human reading experience without proportionate citation gains. The model has no problem extracting from coherent prose if the BLUF block (T03) is in place.

**Tag:** `ANTI_PATTERN_OVER_SUMMARIZATION`

---

## T05 — Rewriting Existing Content (Wikipedia Paraphrase) ❌

**When to avoid:** When the only differentiator is paraphrasing of public-domain text.

**Why it fails:** LLMs detect near-duplicate semantics and prefer the original (typically Wikipedia or the primary publisher). The rewritten page rarely earns citation.

**Action:** Always inject at least one unique factual claim, dataset, quote, or interpretation per page. Princeton GEO study confirms statistical and citation richness as the dominant differentiator.

**Tag:** `ANTI_PATTERN_PARAPHRASE`

---

## T06 — Matching the Prompt Intent ✅

**When to apply:** When mapping content types to commercial funnel stages.

**Mechanism:** LLMs select source types that match prompt intent — informational prompts pull from articles, commercial top-of-funnel prompts pull from listicles and category pages, transactional prompts pull from product pages, home pages, and brand-owned comparison pages.

**How:** Audit which prompt stage each page targets and align the page type accordingly. A product page poorly suited to an informational prompt will not be cited.

**Risk:** None.

**Tag:** `PRAGMATIC_INTENT_MATCH`

---

## T07 — Year-in-Title (Recency Bias / Fan-out Queries) ✅

**When to apply:** On any page where annual relevance is plausible (best-of lists, comparisons, market analyses, statistics roundups).

**Mechanism:** LLM fan-out query expansion frequently appends the current or previous year (e.g., "best CRM 2026"). Pages with the year in the title intercept these fan-out queries.

**How:** Add the current year to titles where natural. Update annually.

**Risk:** Low. Looks dated by Q1 of next year — schedule an annual refresh.

**Tag:** `PRAGMATIC_RECENCY`

---

## T08 — Self-Promotional Listicles ✅

**When to apply:** When the brand competes in a commercial category with active LLM-driven research (CRM, SEO tools, agencies, sleep systems, SaaS in general).

**Mechanism:** LLMs frequently issue fan-out queries like "top 10 X 2026", "best X for use case Y". Listicles ranking the brand at #1 in its own category are pulled into the answer context.

**How:** Publish "Best X" articles that rank the brand at #1 (or #2/#3 in some variants for credibility), with substantive criteria. Cover use-case variants ("best X for startups", "best X for enterprise", "best X for regulated industries").

**Risk:** Medium — at scale, can trigger Google ranking penalties for self-referential content. Cap volume; mix with neutral listicles citing third parties.

**Evidence:** Documented industry pattern in SaaS, CRM, SEO tools, agencies, and sleep/health. Self-promotional rate of cited listicles reaches ~20% in Professional Services.

**Tag:** `PRAGMATIC_LISTICLE`

---

## T09 — Mass-Scaled AI-Generated Listicles ❌

**When to avoid:** Always at scale.

**Why it fails:** Google can detect spam at volume and penalize the entire domain. When organic rankings collapse, AI grounding visibility collapses with them (LLMs do not see uncrawlable or de-indexed content).

**Tag:** `ANTI_PATTERN_LISTICLE_SCALE`

---

## T10 — Competitor Comparison Pages (X vs. Y) ✅

**When to apply:** When the brand has identifiable competitors that prospects evaluate side-by-side.

**Mechanism:** When a user queries "Brand A vs. Brand B", LLMs frequently cite "A vs. B" comparison pages — including pages owned by either brand. The brand controlling the comparison page controls the framing.

**How:** Publish own-brand-vs-each-major-competitor comparisons. Optionally, also publish competitor-A-vs-competitor-B pages with the brand inserted as an alternative in the conclusion. Use honest, defensible claims to avoid backlash.

**Risk:** Medium — overly aggressive framing risks brand reputation and may breach competitor trademark/comparison advertising rules in some jurisdictions. Keep claims factual.

**Evidence:** Pattern observed in SaaS, file-storage, marketing automation, e-commerce platforms, and B2B services.

**Tag:** `PRAGMATIC_COMPARISON`

---

## T11 — Paid Advertorials on High-Authority Domains ✅

**When to apply:** When the brand has budget for paid placements on tier-1 publishers.

**Mechanism:** LLMs treat indexed editorial content as a citation source regardless of whether it was paid. As long as the publisher domain is reputable and Google indexes the page, it can be retrieved as grounding material.

**How:** Buy brand-story / brandstudio placements on industry-leading publishers (large general-news outlets, sector-leading trade publications). Verify Google indexing post-publication.

**Risk:** Medium — depends on disclosure requirements in the publisher's jurisdiction and the buyer's market. Spend-heavy approach; track citation lift to justify ROI.

**Evidence:** Documented citation share on commercial prompts in insurance, finance, and B2B SaaS in DACH and US markets. Stable as of early 2026 — no LLM provider has filtered paid editorial.

**Tag:** `PRAGMATIC_ADVERTORIAL`

---

## T12 — ChatGPT-Shopping Inclusion ✅

**When to apply:** When the brand operates an e-commerce catalog.

**Mechanism:** ChatGPT-Shopping product listings are ~99% sourced from organic Google Shopping (Merchant Center, organic listings — not paid Shopping Ads).

**How:** Maintain a clean Google Merchant Center feed with the "organic listings" checkbox enabled. New products propagate to ChatGPT-Shopping within ~24 hours.

**Risk:** None beyond standard Merchant Center compliance.

**Tag:** `PRAGMATIC_SHOPPING_FEED`

---

## T13 — German-Only Strategy for DACH Markets ❌

**When to avoid:** When the target market is DACH (DE/AT/CH) and the brand has no English-language footprint.

**Why it fails:** LLMs issue English-language fan-out queries even for German prompts. Brands without English content (reviews, interviews, PR, expert profiles) are absent from English-language sources and lose share to international competitors with English footprints.

**Action:** Build a baseline English presence — at minimum: English homepage, 5–10 English explainer articles, English LinkedIn profile, English press mentions or interviews.

**Tag:** `ANTI_PATTERN_LANGUAGE_LOCK`

---

## T14 — Wikipedia Entry — Including Temporary Ones ✅

**When to apply:** When the brand is too small for a permanent Wikipedia entry but needs AI entity recognition.

**Mechanism:** LLMs ingest Wikipedia snapshots regularly. Even articles that are eventually deleted continue to be cited for months after deletion because the ingested snapshot persists in the model's training/grounding data.

**How:** Create an honest, factual Wikipedia entry. If it survives, perfect. If it is deleted, the brand still benefits from months of citation.

**Risk:** High reputational — creating low-quality or self-promotional entries can damage relationships with Wikipedia editors and prevent future legitimate entries. The brand may be flagged as a known abuser.

**Ethics:** Do not create negative entries about competitors. This is mentioned only so readers can defend against it.

**Tag:** `PRAGMATIC_WIKIPEDIA`

---

## T15 — X (Twitter) Posts to Influence Grok ✅

**When to apply:** When Grok visibility matters to the brand's market (US-heavy, English-speaking, dev/finance/crypto verticals).

**Mechanism:** Grok references X posts heavily. A single substantive X post can dominate Grok's answer to a related query, sometimes quoted near-verbatim.

**How:** Maintain an active X presence on relevant topics. Substantive threads beat short posts.

**Risk:** Low for Grok-specific influence; ROI in non-US/European markets is limited because Grok's market share is small.

**Tag:** `PRAGMATIC_X_POSTS`

---

## T16 — Pure SEO Without On-Site Positioning ❌

**When to avoid:** When relying on SEO alone to drive AI visibility.

**Why it fails:** Excellent SEO makes the brand's URL retrievable, but the on-page text determines what the LLM extracts. A retrieved page that lists competitors prominently and the brand modestly will produce an answer that prominently mentions competitors and modestly mentions the brand.

**Action:** Pair every high-ranking page with an explicit on-page positioning that places the brand as the primary entity (e.g., self-promotional headlines, brand at top of comparison tables, declarative claims of leadership where defensible).

**Tag:** `ANTI_PATTERN_SEO_ONLY`

---

## Tactic Categorization (for Audit-Mapping)

- **Off-Site:** T01, T11, T14, T15
- **On-Site Content:** T02, T03, T05, T06
- **Content Formats:** T08, T09, T10
- **Technical / Feed:** T07, T12, T13
- **Strategic Framing:** T04, T16

Anti-patterns: T04, T05, T09, T13, T16.

Pragmatic positives: T01, T02, T03, T06, T07, T08, T10, T11, T12, T14, T15.
