# GBP Limits and Policy Traps

## Character limits (check with scripts/check_limits.py)

| Field | Limit | Notes |
|---|---|---|
| Business description | 750 chars | lodging profiles: bulk import rejects the field entirely ("Beschreibung von Unterkünften nicht bearbeitbar") while the search-UI editor still offers it with a 730-char cap; write for 730 when the category is lodging. First ~250 shown before "more", front-load the core |
| Post body | 1500 chars | aim 150-350; first ~100 chars visible in card |
| Post title (event/offer) | 58 chars | |
| Product name | 58 chars | |
| Product description | 1000 chars | |
| Service description | 300 chars | |
| Q&A question / answer | ~440 / ~4000 chars | keep answers 2-4 sentences |
| Review reply | 4096 chars | 2-4 sentences is the sweet spot |
| Business name | 100 chars | but see naming rule below, shorter is safer |

## Content rules for the description

- No prices, no URLs, no phone numbers, no promo language ("best", "#1", "Sale")
- No ALL CAPS, no emoji stuffing
- Describe what the business is and does, where, for whom; weave primary keyword + city
  in naturally, once or twice
- Google rejects or strips violating descriptions silently

## Policy traps that cause suspensions (not just weak rankings)

1. **Keyword-stuffed business name.** Profile name = real-world name exactly.
   "Rheintal Business Apartment Götzis Ferienwohnung günstig" gets suspended.
   Multi-location: same name on every profile, differentiated only by address.
2. **Fake or ineligible locations.** Address must be a place where staff or the owner
   can receive customers (or use service-area mode). Virtual offices, mailboxes,
   apartments nobody attends: suspension risk. Multi-location only where a real
   presence exists (sign, reachable person, key handover).
3. **Review incentives.** No discounts, gifts, or coupons in exchange for reviews,
   no review gating (asking only happy customers). Violations can wipe ALL reviews.
4. **Bulk-imported review bursts.** Asking hundreds of past customers at once looks
   synthetic. Ask continuously, per transaction/stay.
5. **Self-serving AggregateRating schema.** Marking up your own rating (from Booking,
   Trustpilot, or your own site) on your own website violates Google's structured-data
   policy, will not render, and risks a manual action. Ratings belong in visible text.
6. **Attribute lies.** Only set attributes that are true (accessibility especially).
   False attributes generate 1-star reviews, which cost more than a missing checkbox.
7. **Preview/staging URLs in the profile.** Website field must be the final production
   domain. A vercel.app link in the profile leaks and sticks in caches.

## Review handling rules

- Reply to every review within 48h, positive and negative
- Positive: thank by name if shown, reference one specific detail, invite back.
  May be automated.
- Negative: NEVER auto-publish. Draft only, human approves. Calm, non-defensive,
  no fault admission, no public discussion of visit details (privacy: guests/patients/
  clients may not want their presence confirmed), route to phone/email.
- Naturally mention city + service in replies ("your apartment in Götzis"), it is a
  minor relevance signal; never stuff.

## Verification reality

- New profiles: video verification (usually 2-5 days) or postcard (1-2 weeks) to the
  actual address. No API path exists for this. Ever.
- Nothing entered before verification is guaranteed to persist or show publicly.
- Bulk verification exists only for 10+ locations.

## Ranking levers, in impact order

1. Complete profile (every field filled) + correct primary category
2. Review count, recency, and reply rate
3. NAP consistency across website, profile, and citations (char-for-char)
4. Photos: 20+ total, fresh uploads monthly (2-3/month suffices)
5. Posts every 7-14 days (activity signal)
6. Website schema confirming the profile (same NAP, geo, hours)
7. Citations: Bing Places, Apple Business Connect, plus country-local directories
   (AT: Herold.at, firmenabc.at; DE: gelbeseiten.de, 11880; CH: local.ch, search.ch)
