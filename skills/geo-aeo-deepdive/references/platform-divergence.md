# Platform Divergence — Citation Behavior per AI Platform

There is no single "AI Search" optimization. Major Answer Engines and Generative Search systems behave differently in how they ground answers, which sources they prefer, and how their citation overlap with classical SEO results plays out. A deepened report must translate generic recommendations into platform-specific actions.

Use this reference to populate Section 5 (Platform Strategy) of the report.

## Snapshot Table

| Platform | Avg. citations/answer | Overlap with Google Organic | Strongest source bias |
|----------|----------------------|------------------------------|------------------------|
| Perplexity AI | 6.61 | 28 % | Reddit (46.7 %), YouTube (13.9 %), other community/UGC |
| Google AI Overviews (Gemini) | 6.10 | 76 % | Classical SEO + structured data + bullet/list formats |
| ChatGPT | 2.62 | 8 % | Information-dense, well-structured, llms.txt-friendly content |
| Grok | varies | low | X (Twitter) posts heavily |
| Microsoft Copilot | ~5 (varies) | moderate | Bing index + enterprise content |

## Perplexity AI — Community-First Architecture

**Core behavior:** Aggressive use of community/UGC content. Reddit alone provides ~47 % of Perplexity's Top-10 cited sources on average.

**What works:**
- Active brand presence in topical subreddits.
- Substantive Quora answers from a recognized expert account.
- YouTube videos with descriptive titles, transcripts, and topical tagging.
- Digital PR placements in industry publications and news sites.
- `llms.txt` (Perplexity actively crawls and uses it as identity signal).

**What does not work:**
- Corporate-only domain strategy.
- Pure SEO optimization without community footprint.
- One-off Reddit/Quora accounts with low karma/credibility — accounts are weighted by community signals.

**Audit findings to flag:**
- `offpage.reddit_presence: false` → critical for Perplexity.
- `offpage.quora_presence: false` → critical for Perplexity.
- `offpage.youtube_presence: false` or weak channel → high impact.
- `crawler_access.llms_txt: MISSING` → critical (Perplexity uses it).

**Step-by-step entry plan (default recommendation when the audit lacks community presence):**
1. Identify 3–5 most active subreddits for the brand's topic (use Reddit search + sort by activity).
2. Create a senior expert account; comment substantively for 2–4 weeks before posting any brand-related content.
3. Publish 2–3 highly substantive long-form posts addressing common community questions, citing the brand transparently as the expert source.
4. Mirror on Quora — answer 10 top questions in the brand's topic over 4 weeks.
5. Track citation lift in Perplexity using monthly test prompts.

## Google AI Overviews (Gemini) — SEO Continuation Layer

**Core behavior:** AI Overviews are built on top of a healthy classical SEO foundation. Citation overlap with same-SERP organic rankings has grown from ~32 % (May 2024) to ~55 % (Sept 2025).

**What works:**
- Strong classical SEO (technical, crawlability, on-page, backlinks).
- Bulleted/list content (40–61 % of AI Overviews contain lists).
- Structured data, especially FAQPage, HowTo, Product with aggregateRating, Article, BreadcrumbList.
- Unmistakable E-E-A-T signals (named authors with `Person` schema, citations to authoritative sources, fresh `dateModified` timestamps).
- Answer-First content (BLUF) with question-style H2 headings.

**What does not work:**
- Technically unhealthy pages (poor Core Web Vitals, render-blocking, crawl errors).
- Unstructured prose without schema.
- Content lacking a clear authority signal (anonymous author, no citations, no entity linkage).

**Audit findings to flag:**
- `scores.seo.technical < 60` → blocks AIO eligibility.
- `scores.seo.schema < 40` → low extractability.
- `findings` matching pattern "FAQPage schema missing" → critical for AIO list-style answers.
- `pages[].schema_types` lacking `FAQPage`/`Article`/`Product` → fix per page.

**Step-by-step entry plan (default when AIO readiness is weak):**
1. Run Lighthouse on the top 10 pages; resolve any LCP/INP issues over thresholds.
2. Add `FAQPage` schema to the top 3 question-heavy pages.
3. Add `Article` schema with named author (linked to `Person` schema) to all blog/insight pages.
4. Rewrite H2 headings as questions on top informational pages.
5. Add a 40–60 word answer block immediately after each question-H2.
6. Validate via Google Rich Results Test.
7. Request re-indexing in Google Search Console.

## ChatGPT — Decoupled Information-Density Engine

**Core behavior:** Largest user base (>87 % of all AI referral traffic). However, only 8 % overlap with classical Google rankings — ChatGPT operates as a substantially independent ecosystem.

**What works:**
- Highest possible information density per chunk (BLUF at top, named entities, precise statistics).
- `llms.txt` and `llms-full.txt` with clean Markdown.
- Direct, emotionless, encyclopedia-style framing.
- Original data and unique facts (the model has no alternative source for them, so citation odds rise).
- Domain authority signals like Wikipedia entity link, sameAs in `Organization` schema.

**What does not work:**
- Persuasive marketing copy without facts (Princeton anti-pattern A08).
- Pages padded for SEO word count (anti-pattern A07).
- Content that competes head-to-head with Wikipedia on encyclopedic ground — ChatGPT will prefer Wikipedia.

**Audit findings to flag:**
- `crawler_access.gptbot: BLOCKED` → emergency-level critical.
- `crawler_access.llms_txt: MISSING` or `PRESENT` (not `STANDARD_COMPLIANT`) → critical.
- `offpage.wikidata_entry: false` → high.
- Findings matching "marketing tone", "vague claims", "no statistics" → apply Princeton A03 + A04.

**Step-by-step entry plan:**
1. Verify GPTBot is allowed in `robots.txt`.
2. Publish standard-compliant `llms.txt` (see `llmstxt-spec.md`).
3. Audit the top 10 commercial pages: add at least one precise, cited statistic per page (Princeton A03).
4. Add `Organization` schema with `sameAs` to LinkedIn, Wikipedia (if applicable), Wikidata, and key social profiles.
5. Create a Wikidata entity if missing (low-cost, high-leverage).
6. Test monthly with a fixed prompt set, scoring citation rate.

## Grok — X-Centric

**Relevant only if:** the brand's market overlaps with Grok user base (US-heavy, dev/finance/crypto, English-first).

**What works:** Active substantive X presence. A single high-quality long-thread on the brand's specialty can dominate Grok answers in the topic.

**What does not work:** Anything off-X. Grok ignores most non-X sources for most queries.

**Step-by-step entry plan:** Open or revive a substantive X profile, post 1 long thread weekly for 8 weeks on the brand's topic, link the brand transparently.

## Microsoft Copilot — Bing + Enterprise

**Core behavior:** Mixed grounding from Bing index + enterprise Microsoft Graph (when used inside M365). For public Copilot, Bing is the primary index.

**What works:**
- Bing Webmaster Tools registration.
- Same on-page work as Google AI Overviews.
- Enterprise discoverability (clear brand presence on LinkedIn — Microsoft owned, indexed deeply).

**Step-by-step entry plan:**
1. Register and verify the domain in Bing Webmaster Tools.
2. Submit the XML sitemap to Bing.
3. Maintain a complete, regularly updated LinkedIn Company Page with rich brand content.

## Cross-Platform Strategy Pattern

For a brand with limited budget that wants the highest ROI:

1. **Phase 1 (Foundation):** Standard-compliant `llms.txt`, `Organization` schema with `sameAs`, `FAQPage` schema on Q&A pages, `Article` schema with named `Person` on insights pages. Resolves the lowest-hanging fruit across all platforms.
2. **Phase 2 (Volume Plays):** Listicle and Comparison pages targeting fan-out queries (helps ChatGPT and Perplexity in commercial categories; helps AIO via lists).
3. **Phase 3 (Community):** Reddit + Quora + YouTube expert presence (Perplexity-critical).
4. **Phase 4 (Entity Strengthening):** Wikipedia + Wikidata + named-expert publications (ChatGPT and Gemini both reward this).
5. **Phase 5 (Original Research):** Publish proprietary data — earns "primary source" status across all platforms; Princeton A01 + A03 multiplier.

The skill should map every audit finding to the earliest phase in which it makes sense.
