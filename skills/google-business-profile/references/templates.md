# German Text Templates for GBP

All guest/customer-facing text in Sie-Form unless the brand demonstrably uses Du.
Fill [BRACKETS] from the gathered business data, never leave brackets in the final
deliverable without marking them as open items.

## Description skeleton (max 750 chars)

Structure: what + where (1 sentence), offering details (1-2), equipment/USPs (1-2),
target groups (1), personal/trust element (1), closing capability (1).

Example pattern:
> [NAME] bietet [ANGEBOT] in [ORT/REGION]. Die [EINHEITEN] mit [GRÖSSE/UMFANG] bieten
> [KERNMERKMALE]. [AUSSTATTUNGSLISTE]. Ideal für [ZIELGRUPPEN]. [PERSÖNLICHES
> TRUST-ELEMENT, z.B. Inhabergeführt, persönliche Betreuung durch NAME].
> [ABSCHLUSS: Buchung/Terminvereinbarung, Besonderheit wie Firmenrechnung].

No prices, no URLs, no superlatives (policy).

## Post templates (rotate every 7-14 days, max 1500 chars, aim 150-350)

1. **Angebot/Verfügbarkeit**: hook with concrete availability or entry price, 3-4
   equipment/benefit points, CTA to booking/contact page.
2. **Zielgruppe**: address one segment directly (Monteure, Familien, Firmenkunden...),
   their specific pain, how the business solves it, CTA.
3. **Standort/Region**: seasonal or local hook (See, Messe, Markt, Saison), one
   genuinely useful local tip, tie back to the business, CTA.
4. **Vertrauen**: review score from any platform (in text, never in schema), what
   guests/customers praise, personal note from the owner, CTA.

Every post CTA links with UTM: `?utm_source=google&utm_medium=organic&utm_campaign=gbp_<zweck>`

## Review reply, positive (may be automated)

> Vielen Dank, [NAME], für die schöne Bewertung! Es freut uns sehr, dass [KONKRETES
> DETAIL AUS DER BEWERTUNG] Ihnen gefallen hat. Wir freuen uns, Sie bald wieder in
> [ORT] begrüßen zu dürfen.

2-3 sentences, one concrete detail, city mention where natural.

## Review reply, negative (DRAFT ONLY, human approves)

> Vielen Dank für Ihre Rückmeldung, [NAME]. Es tut uns leid, dass Ihr [AUFENTHALT/
> BESUCH/TERMIN] nicht Ihren Erwartungen entsprochen hat. Bitte melden Sie sich direkt
> bei uns unter [TELEFON] oder [E-MAIL], damit wir gemeinsam eine Lösung finden.

Never: fault admission, public detail discussion, defensiveness, visit-detail
confirmation (privacy).

## Departure/follow-up message (review request)

> Hallo [NAME],
>
> vielen Dank für [Ihren Aufenthalt/Ihren Besuch] bei [FIRMA]. [Ich hoffe/Wir hoffen],
> Sie waren zufrieden.
>
> Wenn ja, würden Sie [mir/uns] mit einer kurzen Google-Bewertung sehr helfen,
> das dauert keine Minute: [BEWERTUNGSLINK]
>
> Herzliche Grüße
> [INHABER], [TELEFON], [E-MAIL]

Send per transaction, continuously. Never in bulk to the backlog (looks synthetic).
QR code with the same link on-site.

## Q&A starter set (self-post and self-answer, allowed and recommended)

Generate 8-10 from these universal buckets, concretized with real business facts:
parking, hours/check-in, core amenity 1-3 (WLAN, Küche...), payment/invoicing
(Firmenrechnung!), restrictions (Haustiere, Rauchen), capacity/size, location/
directions, price entry point, booking/appointment process.

Mirror the same set as on-site FAQ with FAQPage schema, answers consistent
word-for-word where possible.

## Operating prompt pack (for a connected MCP like PostProxy)

When the user wants recurring AI operation, generate a German prompt document with:

1. **Setup prompt** (paste once): business facts block (name, locations with
   "ask which profile or run for both" for multi-location, area, phone, mail, website),
   brand voice, always-mention list, never-say list (no price promises beyond "ab X",
   no availability promises, nothing about individual customers), Sie-Form rule,
   1500-char cap.
2. **Auto-allowed tasks**: positive review replies, regular posts.
3. **Approval-gated tasks** (draft, wait for "freigeben"): negative reviews, anything
   involving complaints, money, prices, cancellations, individual customers.
4. **Standing guardrail prompt** the user can paste to enforce the split.
