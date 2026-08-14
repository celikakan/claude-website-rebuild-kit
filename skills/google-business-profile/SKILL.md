---
name: google-business-profile
description: >
  Create, audit, optimize, and operate Google Business Profiles (Google Unternehmensprofil, GBP,
  formerly Google My Business). Covers profile setup, categories, 750-char descriptions, products,
  services, attributes, photos, posts, Q&A, review management, UTM tracking, multi-location logic,
  schema.org linkage, and what can/cannot be automated via API or MCP connectors. Use this skill
  whenever the user mentions Google Business Profile, GBP, Google My Business, Google Maps Eintrag,
  Unternehmensprofil, Local SEO, Map Pack, lokales Ranking, Google Bewertungen, Google Posts,
  NAP consistency, citations, "bei Google gefunden werden", or wants content written FOR a
  business profile (description, posts, review replies, Q&A), even if they never say "GBP".
---

# Google Business Profile

Help the user set up, fill, and run a Google Business Profile that ranks in the local
Map Pack and converts. Respond in the user's language (German for this user), keep
technical identifiers (field names, schema types) in English.

## Step 0: Pick the mode

| User intent sounds like | Mode | Go to |
|---|---|---|
| "Profil anlegen", "GBP erstellen", new business | CREATE | Step 1 → 2 → 3 |
| "Profil prüfen/verbessern", existing profile | AUDIT | Step 1 → 2 (gap-only) → 3 |
| "Bewertungen beantworten", "Post schreiben" | OPERATE | `references/templates.md` |
| "automatisieren", API, MCP, PostProxy, Pipedream | AUTOMATE | Step 4 |

## Step 1: Gather real data, never invent

Facts come from the business, not from you. Priority order:

1. **Live website** of the business (WebFetch every relevant page: home, offers/products,
   contact, imprint). Extract verbatim: name, address(es), phone, email, owner, offers,
   prices, amenities, hours, policies (pets, smoking...), review scores on other platforms.
2. **Existing audits/reports** in the project folder (grep for the business name first).
3. **Ask the user** for anything still missing. Mark unconfirmed values visibly as
   placeholders in the deliverable; never silently guess an opening hour, price, or PLZ.

Watch for contradictions between sources (e.g. street spelled two ways). Flag them,
the wrong variant kills NAP consistency.

**Multi-location check:** if the business has 2+ real addresses where customers show up,
plan one profile per address, same business name on each (no city suffix in the name,
that violates guidelines). Each needs its own verification.

## Step 2: Build the deliverable

Produce a self-contained HTML document (plus nothing else, no scattered .md files) using
`assets/doc-template.html` as the skeleton. Auto-open it in the browser after writing.
Sections, in this order:

1. **NAP** table (name, address, phone, email, website, geo) with per-field notes
2. **Categories** (1 primary + max 9 secondary, only truly fitting ones)
3. **Description** as a `copyblock` with `data-max="750"`
4. **Hours + service area** (service-area logic for businesses without walk-in storefront)
5. **Attributes** (set / explicitly negate / still to verify)
6. **Products** (one card per product/offering) and **Services** (keyword-style list)
7. **Photo plan** (logo 720x720+, cover 16:9, per-offering shots, owner photo, no stock)
8. **Posts**: 4 rotating templates as copyblocks with `data-max="1500"`
9. **Website link with UTM** (`utm_source=google&utm_medium=organic&utm_campaign=gbp_...`)
10. **Q&A**: 8-10 self-posted questions with owner answers (allowed and recommended;
    mirror them as on-site FAQ with FAQPage schema)
11. **Reviews**: request link/QR workflow, departure-message template, 48h reply rule
12. **How data gets in** (import reality, see below) + post-setup checklist
    (schema linkage, Maps embed, citations: Bing Places, Apple Business Connect,
    local directories, monthly stats check)

Every paste-ready text is a `<div class="copyblock" id="..." data-max="...">`, the
template's JS adds copy buttons and live character counters. German business texts use
Sie-Form unless the brand demonstrably uses Du.

**Validate before claiming done:** run `scripts/check_limits.py <file.html>`. It parses
all copyblocks, checks their `data-max`, and exits non-zero on violations. No green run,
no "fertig".

Hard content rules live in `references/limits-and-policies.md`. Read it before writing
the description and posts; the traps there (keyword-stuffed names, review incentives,
self-serving AggregateRating) cause suspensions, not just weak rankings.

## Step 3: Schema linkage (website side)

The profile ranks better when the website confirms it. Generate JSON-LD per
`references/schema-jsonld.md`: LocalBusiness subtype (LodgingBusiness, Dentist,
Electrician...) with geo, openingHoursSpecification, amenityFeature/offer data, hasMap,
plus child entities (rooms, products) with resolvable `@id` references. Validate JSON
parses and every `@id` reference resolves before delivering. All URLs must point at the
final production domain, never at previews (vercel.app, netlify.app, staging).

## Step 4: Automation, tell the truth about limits

Users regularly ask "can you import/do this automatically". The honest matrix:

| Channel | Can do | Cannot do, ever |
|---|---|---|
| Manual dashboard (recommended default) | everything | nothing |
| Bulk CSV upload | core fields only; bulk verification needs 10+ locations | products, posts, Q&A, photos |
| Business Profile API / MCP connectors (Pipedream, PostProxy, gbp-review-agent) | core fields, posts, review replies, locations list | **create profile, verify, photos-galleries*, products, Q&A, most attributes** |

*Some third-party connectors claim photo upload; verify against the connector's tool list
before promising it.

API access itself is gated: Google approval required (form:
support.google.com/business/contact/api_default, takes days to weeks), plus a verified
profile. OAuth flows run in the account owner's browser; never ask the user to paste
tokens. If no connector is live in the session, say so and deliver the copy-paste
document instead. The correct order is always: create + verify manually → move final
domain live → collect reviews → only then wire up automation.

A vetted self-hosted option: amirjahfar1/Google-Business-Profile-GBP-MCP (MIT, TypeScript,
42 tools, audited 2026-07: only official googleapis.com hosts, local credentials file,
scope business.manage only). Covers locations CRUD, attributes, categories, review replies,
performance metrics. Does NOT cover posts and Q&A (Google killed the Q&A API in Nov 2025)
or the Lodging API. Setup recipe and API-request fill-in help:
~/Documents/Antigraphity/Marketinganlyse/Ayhan/gbp-mcp/setup-anleitung.html

For recurring operation via a connected MCP, generate a German prompt pack per
`references/templates.md` section "Operating prompts" (setup prompt teaching the
business once, auto-allowed tasks vs. approval-gated tasks; negative reviews and
anything involving money are ALWAYS approval-gated).

## Reference files

- `references/limits-and-policies.md`: all character limits, naming rules, review and
  schema policy traps, suspension risks. Read before writing any profile content.
- `references/templates.md`: German text skeletons (description, 4 post types, review
  replies positive/negative, departure mail, Q&A starter set, operating prompt pack).
- `references/schema-jsonld.md`: JSON-LD patterns, multi-location graph, validation
  workflow, what to deliberately omit.
- `assets/doc-template.html`: deliverable skeleton with copy buttons + char counters.
- `scripts/check_limits.py`: validator, run on every deliverable before completion.
