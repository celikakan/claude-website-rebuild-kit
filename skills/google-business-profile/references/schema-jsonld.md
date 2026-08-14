# Schema JSON-LD Patterns for GBP Linkage

The website confirms the profile: same NAP char-for-char, same hours, same geo.
Deliver as `<script type="application/ld+json">` blocks for the site's `<head>`.

## Before writing: inspect what exists

Fetch the live pages and extract existing `application/ld+json` blocks first.
Extend or replace surgically; never duplicate a type that already exists on a page
(two LodgingBusiness nodes with different data is worse than one incomplete node).

## Main entity pattern

Pick the most specific LocalBusiness subtype (LodgingBusiness, Dentist, Electrician,
Restaurant, ...; schema.org/LocalBusiness lists them). One `@graph` with:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "<Subtype>",
      "@id": "https://<domain>/#business",
      "name": "...", "url": "...", "telephone": "+43 ...", "email": "...",
      "priceRange": "ab €80",
      "address": { "@type": "PostalAddress", "streetAddress": "...", "postalCode": "...",
                   "addressLocality": "...", "addressRegion": "...", "addressCountry": "AT" },
      "geo": { "@type": "GeoCoordinates", "latitude": 0.0, "longitude": 0.0 },
      "hasMap": "https://www.google.com/maps/search/?api=1&query=<url-encoded address>",
      "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","..."], "opens": "08:00", "closes": "20:00" }],
      "areaServed": [{ "@type": "Place", "name": "..." }],
      "amenityFeature": [{ "@type": "LocationFeatureSpecification", "name": "...", "value": true }],
      "containsPlace": [{ "@id": "https://<domain>/<page>#<child-id>" }],
      "image": "...", "logo": "..."
    }
  ]
}
```

Negative facts are valuable too: `"petsAllowed": false`, `"smokingAllowed": false`,
amenityFeature with `"value": false`.

## Multi-location

One node per real address in the same `@graph`. Secondary locations get
`"parentOrganization": { "@id": ".../#business" }` and their own `@id`
(`#business-<ort>`), address, hasMap, containsPlace. Same business name on all.

## Child entities (products, rooms, offerings)

On the listing page, one node per offering (Apartment, Product, Service...) with its
own `@id`, name, image, description, real specs (floorSize with unitCode MTK,
occupancy with unitCode C62, numberOfRooms...), address, and
`"containedInPlace": { "@id": "<parent>" }`. Parent lists them via `containsPlace`.
This is what AI search reads for "X mit Y in ORT" queries.

## Deliberately omit (policy or maintenance traps)

- **AggregateRating from any source about the own business**: self-serving, will not
  render, manual-action risk. Scores go in visible text.
- **sameAs with guessed URLs**: only add platform profiles (Booking, social) with
  confirmed exact URLs.
- **Offer/price markup with static prices**: diverges from live prices, markup/visible
  mismatch is a violation. Only wire prices when they come from the booking system.

## Validation (mandatory before delivering)

1. Every block parses as JSON (script it, do not eyeball).
2. Every `{"@id": ...}` reference resolves to a defined node across all delivered
   blocks. Count defined vs. referenced, zero unresolved.
3. All URLs point at the production domain, not previews (vercel.app, *.pages.dev,
   staging). If the final domain is not live yet, deliver anyway but flag deploy order:
   domain first, then schema.
4. Point the user at search.google.com/test/rich-results and validator.schema.org
   for post-deploy checks; Search Console "Verbesserungen" confirms indexing.
