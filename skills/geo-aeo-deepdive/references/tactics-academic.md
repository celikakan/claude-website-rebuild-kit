# Academic GEO Tactics — Princeton KDD 2024

Evidence-based tactics from the Princeton/Georgia Tech/IIT Delhi/Allen Institute for AI paper "GEO: Generative Engine Optimization" (KDD 2024). These tactics have been empirically validated on the GEO-bench benchmark of 10,000 queries across 8 domains, then re-validated on Perplexity.ai.

Use these as the **academic spine** of any deepened audit report. Whenever an audit recommendation can be aligned with a Princeton tactic, cite the tactic explicitly in the Why-line.

## Method Notes

The Princeton team developed two new metrics, because traditional ranking position became meaningless in generated answers:

- **Position-Adjusted Word Count** — number of words from a given source used in the AI's answer, weighted by their position and prominence within the answer.
- **Subjective Impression** — holistic visibility and authority projection of a source within the generated answer.

Strategies that lifted these metrics by ≥30% across multiple domains are listed below as **Effective**. Strategies that produced no lift or negative lift are listed under **Anti-Pattern**.

---

## Effective Tactics

### A01 — Cite Sources ✅ +30 % to +40 %

**Modification:** Embed inline references to external, verifiable, authoritative sources (peer-reviewed studies, institutional reports, government data).

**Mechanism:** Inline citations function as a per-claim trust signal. Generative engines are conditioned to weight claims that rest on verifiable foundations more heavily during synthesis.

**Lift for Rank-5 pages:** +115.1 % relative — the strongest lever for under-ranked pages.

**Best fit for audit findings:**
- Pages with low E-E-A-T scores
- Pages making factual or numerical claims without sources
- Content covering regulated topics (health, finance, legal)

**Tag:** `PRINCETON_CITE_SOURCES`

---

### A02 — Quotation Addition ✅ +30 % to +41 %

**Modification:** Insert named expert quotations using explicit formats like "According to [Author/Source], …".

**Mechanism:** Named-expert quoting allows the LLM to complete a Credibility Chain — content → expert → institution → trust. Particularly dominant in soft domains: People & Society, Explanation, History.

**Lift for Rank-5 pages:** +99.7 % relative.

**Best fit for audit findings:**
- Thought-leadership pages without attributed expertise
- Pages on subjective or interpretive topics
- Pages targeting prompts that invite "expert opinion"

**Tag:** `PRINCETON_QUOTATION`

---

### A03 — Statistics Addition ✅ +30 % to +40 %

**Modification:** Replace vague qualitative claims with precise numerical evidence, ideally cited with year and source.

**Mechanism:** LLMs favor information-dense content. A datum like "21 percent of US workers use AI daily (Pew Research, 2025)" is treated as extractable, high-quality grounding material. The same idea expressed as "many workers use AI" is filler.

**Lift for Rank-5 pages:** +97.9 % relative.

**Best fit for audit findings:**
- Marketing pages full of qualitative claims ("many customers", "leading", "premium")
- FAQ pages with vague answers
- Pages on legal, regulatory, or opinion-heavy topics

**Tag:** `PRINCETON_STATISTICS`

---

### A04 — Fluency Optimization ✅ +15 % to +30 %

**Modification:** Improve readability, grammatical flow, and sentence-level clarity without altering underlying claims.

**Mechanism:** LLMs prefer structurally clean, semantically coherent text because it tokenizes more efficiently and integrates into the response with fewer rewriting steps.

**Universal applicability:** Works across all 8 domains in the study. Combine with A03 for synergy gains beyond either tactic alone.

**Best fit for audit findings:**
- Pages with awkward translations
- Auto-generated copy without editorial pass
- Old SEO-era content with keyword-stuffed sentences

**Tag:** `PRINCETON_FLUENCY`

---

### A05 — Authoritative Voice ✅ +10 % to +20 % (niche only)

**Modification:** Use a confident, declarative tone that asserts subject-matter authority.

**Mechanism:** Limited overall effect; LLMs are robust to pure rhetoric. Niche wins in Debate, History, Science domains where authoritative phrasing aligns with reader expectation.

**Best fit for audit findings:**
- Debate or perspective-pieces
- Historical narratives
- Scientific explainers

Use only where natural — do not force authoritative tone on commercial or transactional pages.

**Tag:** `PRINCETON_AUTHORITY`

---

## Anti-Patterns (Tactics that Failed)

### A06 — Keyword Stuffing ❌

**Modification tested:** Artificially raising keyword density.

**Result:** No positive effect. In several configurations, mild negative effect.

**Why it fails:** LLMs reason semantically, not by surface lexical match. Keyword density is irrelevant to embedding similarity.

**Tag:** `ANTI_PATTERN_KEYWORD_STUFFING`

---

### A07 — Content Padding ❌

**Modification tested:** Inflating word count without adding new information.

**Result:** Negative effect. Visibility dropped because the padded sections diluted the embedding density of relevant content.

**Why it fails:** Generative engines reward information density. Padding lowers density, so the page is rated as less useful.

**Tag:** `ANTI_PATTERN_PADDING`

---

### A08 — Persuasive Language Without Facts ❌

**Modification tested:** Adding emotional/persuasive copy without factual underpinnings.

**Result:** No measurable lift.

**Tag:** `ANTI_PATTERN_PERSUASION_ONLY`

---

### A09 — Over-Simplification ❌

**Modification tested:** Reducing technical content to shallower phrasing.

**Result:** No measurable lift; in technical domains, negative effect.

**Tag:** `ANTI_PATTERN_SIMPLIFICATION`

---

## Synergies (Combine Tactics)

The KDD paper found that combining tactics produced disproportionate gains beyond the sum of single tactics.

| Combination | Reason |
|-------------|--------|
| A03 Statistics + A04 Fluency | Numerical density + clean prose = highest-information-density content the model can ingest. |
| A01 Cite Sources + A02 Quotation | Two independent trust signals on the same claim. |
| A03 Statistics + A01 Cite Sources | Every number gets a citation — the credibility chain is fully verifiable. |
| A02 Quotation + A05 Authoritative Voice (in Science/History domains) | Expert quote + confident framing — domain-appropriate stack. |

**Skill behavior:** When deepening a measure, prefer recommending a 2-tactic synergy over a single tactic when the page type supports it.

---

## Domain-Specific Notes

The Princeton dataset shows tactic effectiveness varies by domain. Adjust recommendations accordingly:

- **People & Society:** Quotation Addition strongest.
- **Law & Government:** Statistics Addition strongest.
- **Explanation / Education:** Quotation Addition + Fluency.
- **History:** Cite Sources + Authoritative Voice.
- **Science:** Cite Sources strongest, with Quotation second.
- **Debate / Opinion:** Authoritative Voice + Statistics.
- **Health (per Princeton-adjacent reviews):** Cite Sources + Statistics, with conservative Fluency edits.
- **Commercial / Product:** Cite Sources weakest (commercial pages rarely have appropriate external citations); Statistics + Fluency dominate.

When the audit's `meta.industry` field maps cleanly to one of these domains, prefer the domain-best combination.

---

## Quick-Reference Decision Table

| Audit Finding Pattern | Recommended Princeton Tactic(s) |
|----------------------|---------------------------------|
| Low E-E-A-T score | A01 + A02 |
| Vague marketing claims | A03 |
| FAQ page with weak answers | A03 + A04 |
| Auto-translated content | A04 |
| Thought leadership without expert | A02 |
| Old SEO-era copy | A04 (rewrite for flow) |
| Statistics quoted without source | A01 (add the source) |
| Numbers stated as ranges or "many" | A03 (specify with citation) |
| Page padded to hit word counts | Remove padding (A07 anti-pattern) — do **not** suggest adding more |
| Heavy keyword repetition | Reduce density (A06 anti-pattern) — clean up |
