# Tools Catalog — Step-by-Step Instruction Sources

This catalog lists the tools the skill references when generating Section 7 (Step-by-Step Instructions). Each entry includes the typical click path, validation method, and audit signals that point to that tool.

When the parsed audit's `detected_stack` is `UNKNOWN`, default to the **WordPress + Yoast + SASWP** stack for step-by-steps, plus one alternative (Custom HTML/JSON-LD).

## CMS Layer

### WordPress (default for unknown stacks)

| Sub-Tool | Typical Use | Path |
|----------|-------------|------|
| Yoast SEO | Titles, Meta Descriptions, Organization Schema, sameAs, Breadcrumbs | Dashboard → SEO → Settings → tabs (Search Appearance / Social) |
| Yoast SEO Premium | FAQ, HowTo, Product Schema blocks, advanced schema | Page editor → Yoast box → Schema tab |
| Rank Math | Alternative SEO plugin; covers same surfaces as Yoast | Dashboard → Rank Math |
| AIOSEO | Alternative SEO plugin | Dashboard → All in One SEO |
| SASWP (Schema and Structured Data for WP) | Full schema-type library, FAQ, Product, Article, Person, LocalBusiness | Dashboard → Structured Data → Add New |
| Schema Pro | Premium alternative for advanced schemas | Dashboard → Schema Pro |
| Elementor | Page editor for headings, blocks, custom HTML | Pages → Edit with Elementor |
| Gutenberg | Default page editor | Pages → Edit |
| Custom Fields (ACF) | Custom content fields for tailored schema | Custom Fields → Field Groups |
| functions.php | Server-side JSON-LD injection in `<head>` | Appearance → Theme Editor (or via SFTP) |
| .htaccess | Security headers (HSTS, CSP, X-Frame-Options) | SFTP/cPanel → root → `.htaccess` |

### Shopify

| Sub-Tool | Use | Path |
|----------|-----|------|
| Theme Code Editor | Insert JSON-LD in `theme.liquid` `<head>` | Online Store → Themes → Edit code |
| JSON-LD for SEO (app) | Adds Product/Organization schema | App Store → install → configure |
| Schema App (Total Schema Markup) | Full schema library | App Store → install → configure |
| Metafields | Brand-level facts (founder, founding date) | Settings → Custom data |

### Webflow

| Sub-Tool | Use | Path |
|----------|-----|------|
| Custom Code Embed | JSON-LD per page | Page Settings → Inside `<head>` tag |
| CMS Collections | Structured data for collection items | CMS → Collection → fields |

### Custom / Headless

| Method | Use |
|--------|-----|
| Direct `<script type="application/ld+json">` in HTML head | Universal fallback |
| Build-time schema injection (Next.js, Astro, Nuxt) | For static-generated sites |

## Validation Layer

| Tool | URL | Use |
|------|-----|-----|
| Google Rich Results Test | `search.google.com/test/rich-results` | Validate any schema markup against Google's parser |
| Schema.org Validator | `validator.schema.org` | Standards-compliance check |
| Bing Markup Validator | `bing.com/webmaster/help/markup-validator` | Bing-specific schema validation |
| Google Search Console — URL Inspection | GSC → URL Inspection | Request re-crawl, see Google's rendered view |
| llmstxt.org | `llmstxt.org` | Reference for `llms.txt` syntax |

## Analytics & Tracking

| Tool | Use | Path / Setup |
|------|-----|--------------|
| Google Search Console | Impressions, position, CTR per query, Core Web Vitals report | `search.google.com/search-console` |
| Google Analytics 4 | Sessions, conversion events, custom channel groups for AI traffic | `analytics.google.com` → Admin → Channel Groups |
| Google Tag Manager | Centralized tag deployment | `tagmanager.google.com` |
| **Google Clarity** | Free heatmaps and session recordings — useful to verify Answer-First block placement above the fold | `clarity.microsoft.com` |
| Bing Webmaster Tools | Bing index visibility, sitemap submission | `bing.com/webmasters` |
| Brand24 / Mention.com / Google Alerts | Brand mention monitoring | brand-specific configuration |
| Plausible / Matomo / Fathom | Privacy-first analytics alternatives | site-specific |

## Performance

| Tool | Use |
|------|-----|
| Google PageSpeed Insights | LCP/INP/CLS measurement per URL |
| Lighthouse (Chrome DevTools) | Local performance + Agentic Browsing audit |
| Cloudflare | CDN, security headers, image optimization, bot management |
| TinyPNG / Squoosh | Image compression (lossy/lossless) |
| ImageOptim | Local image optimization batch |

## Local SEO

| Tool | Use |
|------|-----|
| Google Business Profile | Claim, verify, configure each location | `business.google.com` |
| Bing Places for Business | Bing's GBP equivalent | `bingplaces.com` |
| Apple Business Connect | Apple Maps presence | `businessconnect.apple.com` |
| Whitespark / BrightLocal | Citation building, NAP consistency monitoring | subscription-based |

## Off-Site / Entity Building

| Tool | Use | Path |
|------|-----|------|
| Wikipedia | Brand or expert entity entry | `wikipedia.org` → Create account → Sandbox first → Submit |
| Wikidata | Structured entity record | `wikidata.org` → Create new item → Add statements |
| Reddit | Subreddit presence, expert account | `reddit.com` → identify topical subs → comment → post |
| Quora | Authoritative answers on key questions | `quora.com` → expert profile → topic-focused answers |
| YouTube Studio | Channel optimization, video SEO | `studio.youtube.com` |
| LinkedIn Company Page | Brand presence, employee advocacy | `linkedin.com/company` admin |
| Trustpilot / Google Reviews / Yelp | Review aggregation feeds aggregateRating | platform-specific |
| ORCID | Researcher entity ID for `Person` schema | `orcid.org` |

## Content / Workflow

| Tool | Use |
|------|-----|
| Claude / ChatGPT / Gemini | Drafting, fluency optimization (Princeton A04) |
| DeepL / Trados | Multi-language translation |
| Hunter.io / Apollo | Email discovery for outreach (Filling Gaps tactic) |
| Lemlist / Mailshake / Smartlead | Cold-email sequences |
| Notion / ClickUp / Trello | Editorial calendar |
| Google Docs | Collaborative drafting |

## AEO-Specific Tracking

| Tool | Use |
|------|-----|
| Manual prompt-testing in ChatGPT/Claude/Perplexity/Gemini | Monthly Citation Score measurement |
| AthenaHQ / Rankability / Otterly.ai / Profound | Paid AEO tracking platforms |
| GA4 Custom Channel Group "AI Search" | Isolate AI-referred traffic for conversion comparison |
| Spreadsheet template (Google Sheets / Excel) | Citation Score log per month and platform |

## Advertorial Contacts (PR Channel for Pragmatic T11)

| Region | Channels |
|--------|----------|
| DACH general | Bild.de Brandstudio, Handelsblatt Live, Wirtschaftswoche Brandstudio |
| Trade press | Industry-specific publishers — identify per brand's vertical |
| US/Global | Forbes BrandVoice, Inc.com Sponsored, WSJ Custom Studios |

The skill should not name a specific publisher unless the audit's industry maps cleanly to a known vertical.

## Mapping Tool → Audit Finding

When generating step-by-steps, use this map:

| Audit Finding | Tool Path |
|---------------|-----------|
| Meta Descriptions missing | WP + Yoast SEO Admin |
| Title Tags fixes | WP + Yoast SEO Admin |
| Open Graph / Twitter Cards | WP + Yoast SEO → Social |
| Schema (Organization / FAQ / Article / Person / Product / LocalBusiness) | WP + SASWP or Yoast Premium or direct JSON-LD via functions.php |
| H1 fixes on key pages | WP + Elementor (page editor) |
| Answer-First block | WP + Elementor (page editor) — content rewrite |
| Question-style H2 | WP + Elementor — content rewrite |
| Speakable Schema | SASWP (or direct JSON-LD) |
| llms.txt creation | SFTP / cPanel / GitHub — text editor |
| llms.txt validation | llmstxt.org spec + ChatGPT ingestion test |
| robots.txt updates (GPTBot allow) | SFTP / hosting panel → root → `robots.txt` |
| Security headers | .htaccess (Apache) or Cloudflare → Security → Settings |
| Core Web Vitals improvements | PageSpeed Insights → TinyPNG → CDN |
| Google Business Profile per location | GBP backend |
| NAP consistency | Manual review across GBP / footer / schema / llms.txt |
| GSC + GA4 setup | Google Search Console / Google Analytics 4 |
| Google Clarity setup | Clarity backend → install script |
| AI-traffic channel group | GA4 → Admin → Channel Groups |
| Wikipedia entry | Wikipedia editor workflow |
| Wikidata entry | Wikidata editor workflow |
| Reddit presence | Reddit account + topical subreddits |
| Quora presence | Quora expert profile |
| YouTube channel | YouTube Studio |
| Backlink outreach (Filling Gaps) | Hunter.io + cold-email sequencer |
| Listicle creation | CMS page editor + research outline |
| Comparison-page creation | CMS page editor + competitor research |
| Advertorial purchase | Direct contact with publisher's brandstudio |

For each measure in the final report, instructions should pick the relevant tool from this catalog, present the click path in numbered steps, and end with a validation step (e.g., Rich Results Test for schema, ChatGPT prompt for llms.txt, GSC for crawl-side changes).
