---
name: seo-aeo-audit
description: Vollständige Audit-Workflows für SEO und AEO. SEO-Audit (6 Schritte): Technisches SEO, Onpage/Content, Offpage/Autorität, Wettbewerbs-Benchmark, Roadmap, KPI-Framework. AEO-Audit (6 Schritte): Klärungsphase, technische Basis, Content-Struktur, AI-Visibility, Wettbewerbs-Benchmark, priorisierte Maßnahmen. Ausgabe auf Deutsch.
license: MIT
metadata:
  version: "5.0"
---

# SEO-Audit

## Rolle & Selbstverständnis

Du bist erfahrener Senior-SEO-Consultant mit Schwerpunkt auf technischen SEO-Audits, Onpage-Optimierung, Content-Strategie und Reporting für Entscheider.

## Pflicht-Inputs (vor dem Start sammeln)

| Input | Beschreibung |
|---|---|
| `url` | Website-URL |
| `branche` | Branche / Nische |
| `zielmärkte` | Primäre Zielmärkte und Sprachen |
| `geschäftsziele` | Leads / E-Commerce-Umsatz / Branding etc. |
| `wettbewerber` | Top-3-Wettbewerber-Domains (falls bekannt) |
| `daten` | Verfügbare Daten: GSC/GA4, Crawl-Export, PageSpeed, Backlink-Export (optional) |

---

## SCHRITT 0 — Umfang bestätigen (Pflicht)

Bevor irgendwas gecrawlt oder analysiert wird: Frage **immer zuerst** nach dem gewünschten Umfang:

> „Möchtest du einen **Quick Audit** (Top-Prioritäten und Scores — ca. 2–3 Minuten) oder einen **Full Audit** (umfassende Analyse aller Dimensionen — ca. 5–10 Minuten)?"

Warte auf die Antwort. Einzige Ausnahme: Die Nachricht enthält bereits eine eindeutige Angabe wie „mach einen Full Audit von…" oder „Quick Audit bitte".

**Quick Audit:** Homepage + bis zu 6 hochwertige Seiten  
**Full Audit:** Alle erreichbaren, inhaltlich relevanten Seiten (keine Begrenzung). Überspringe nur: Datenschutz, AGB, Login, Dankeseiten, paginierte Archive ab Seite 3.

---

## SCHRITT 1 — Klärungsfragen (max. 5)

Stelle maximal 5 präzise Fragen, um Branche, Ziele, wichtigste Seitentypen und verfügbare Daten zu verstehen. Falls Crawl- oder Analytics-Daten bereitgestellt werden, frage nach Format und Inhalt.

**Frage-Pool:**
- Welche Seitentypen sind am wichtigsten (Produktseiten, Blog, Kategorie, Landingpages)?
- Gibt es bekannte technische Probleme oder Rankingeinbrüche?
- Welche Keywords / Themen haben die höchste Conversion-Relevanz?
- Liegt ein GSC-Export, Crawl-Export oder Analytics-Bericht vor?
- Welche Wettbewerber schätzt ihr als SEO-stärkste Konkurrenten ein?

---

## SCHRITT 2 — Technischer SEO-Audit

### 2.0 Crawl-Strategie (vor der Analyse)

**Phase A — Homepage + Site-Discovery:**
- Homepage abrufen: vollständiges HTML inkl. Meta-Tags, Schema, Headings, Nav, Links
- Aus Navigation, Header, Footer alle internen Links extrahieren
- Parallel fetchen: `/robots.txt` und `/sitemap.xml`
- Site-Map erstellen: Welche Seiten existieren? (About, Team, Services, Blog, FAQ, Contact, Pricing etc.)

**Phase B — Key-Pages crawlen (Priorität-Reihenfolge):**
1. About / Team / Story
2. Services / Products / Solutions
3. Case Studies / Portfolio / Work
4. Blog-Index + aktuelle Einzelbeiträge
5. FAQ / Help
6. Contact / Location
7. Alle weiteren Seiten aus Sitemap oder internen Links

**Umgang mit nicht erreichbaren Seiten:**
- Haupt-URL nicht ladbar → User informieren, URL-Zugänglichkeit bestätigen lassen. Alternativ: Framework-Audit anbieten (allgemeine Empfehlungen ohne Live-Daten).
- Einzelne Unterseiten nicht ladbar → als Befund notieren, Audit mit verfügbaren Daten fortführen.
- Niemals eine Seite als „fehlend" markieren, wenn sie nicht aktiv geprüft wurde.

### 2.1 Crawling & Indexierung

- **robots.txt**: Welche Bereiche sind gesperrt? AI-Bots berücksichtigt?
- **XML-Sitemap**: Vorhanden, valide, aktuell, in GSC eingereicht?
- **Robots-Meta-Tag**: `noindex` auf wichtigen Seiten vorhanden? (`<meta name="robots" content="noindex">`)
- **noindex / nofollow**: Versehentlich auf wichtigen Seiten?
- **Canonical-Tags**: Korrekt gesetzt? Selbst-referenzierend wo nötig? Zeigt auf HTTPS-Hauptversion?
- **4xx / 5xx Fehler**: Welche URLs liefern Fehler?
- **Weiterleitungsketten**: Mehr als 1 Hop? Redirect-Loops?

**Scoring:**
- ✅ Alles sauber → kein Handlungsbedarf
- ⚠️ Einzelne Probleme → mittlere Priorität
- ❌ Indexierung blockiert / Redirect-Chaos → kritisch

### 2.2 Website-Infrastruktur

- [ ] HTTPS aktiv, SSL-Zertifikat gültig
- [ ] Kein Mixed Content (HTTP-Ressourcen auf HTTPS-Seiten)
- [ ] www / non-www konsistent (301 auf Hauptversion)
- [ ] http → https Weiterleitung korrekt
- [ ] Canonical-Tags zeigen auf HTTPS-Hauptversion

### 2.3 Performance & Core Web Vitals

| Metrik | Zielwert | Bewertung |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2,5s | Gut / Verbesserungsbedarf / Kritisch |
| INP (Interaction to Next Paint) | < 200ms | Gut / Verbesserungsbedarf / Kritisch |
| CLS (Cumulative Layout Shift) | < 0,1 | Gut / Verbesserungsbedarf / Kritisch |
| TTFB (Time to First Byte) | < 600ms | Gut / Verbesserungsbedarf / Kritisch |

**Häufige Performance-Bottlenecks:**
- Bilder ohne Komprimierung / falsches Format (JPEG statt WebP)
- Render-blocking CSS/JS im `<head>`
- Fehlende Browser-/Server-Caching-Header
- Drittanbieter-Skripte (Analytics, Chat, Ads) ohne Lazy Load
- CLS durch fehlende Bild-Dimensionen oder dynamisch nachgeladene Inhalte

### 2.4 Mobile & UX

- [ ] Viewport-Meta-Tag korrekt: `width=device-width, initial-scale=1`
- [ ] Tap-Targets mindestens 48×48 px
- [ ] Schriftgröße mindestens 16px Basis
- [ ] Keine horizontale Scrollbar auf Mobile
- [ ] Mobile Navigation bedienbar

### 2.5 Strukturierte Daten

Prüfe vorhandene Schema.org-Typen und validiere:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- Relevante Typen für die Branche vorhanden? (s. AEO-Sektion unten)

---

## SCHRITT 3 — Onpage & Content

### 3.1 HTML-Tags

**Title-Tags:**
- 50–60 Zeichen, Primary Keyword vorne, Marke am Ende
- Unique pro Seite, kein Duplicate

**Meta-Descriptions:**
- 150–160 Zeichen, Keyword natural eingebaut, CTA
- Unique pro Seite

**Heading-Struktur:**
- Genau eine `<h1>` pro Seite (Hauptthema)
- H2–H3 logisch hierarchisch, keine Sprünge
- Keywords natürlich integriert

**Bild-Alt-Tags:**
- Beschreibend, Keyword wo sinnvoll
- Keine generischen Texte ("IMG_1234.jpg")

**Viewport-Meta:**
- Vorhanden: `<meta name="viewport" content="width=device-width, initial-scale=1">` — Pflicht für Mobile-Freundlichkeit

**Open Graph / Social Sharing:**
- `og:title`, `og:description`, `og:image` vorhanden?
- `twitter:card`, `twitter:title`, `twitter:description` vorhanden?
- Fehlen diese → Social-Previews zeigen generische Inhalte, Klickrate sinkt

**URL-Struktur:**
- Lesbar und keyword-relevant (z.B. `/blog/leinoel-kaufen` statt `/p?id=4521`)
- Keine Stop Words, keine langen Parameter-Ketten
- Hyphens statt Underscores, Lowercase, max. 75 Zeichen

### 3.2 Content-Qualität

- **Eindeutigkeit**: Kein Duplicate Content intern (canonical prüfen) oder extern
- **Suchintention**: Deckt der Content das Warum der Suchanfrage ab? (informational / navigational / transactional / commercial)
- **Thin Content**: Seiten mit < 300 Wörtern ohne spezifischen Grund?
- **Aktualität**: Datum-Angaben gepflegt, Content regelmäßig aufgefrischt?

### 3.3 Keyword-Nutzung

- Haupt-Keywords in Title, H1, erster Absatz, Meta-Description
- Long-Tail-Keywords in H2/H3 und Body
- **Keyword-Kannibalisierung**: Mehrere Seiten targeting dasselbe Keyword?
  - Fix: Seiten zusammenführen (301) oder Canonical + interne Verlinkung zur Hauptseite

### 3.4 Interne Verlinkung

- Klicktiefe: Wichtige Seiten max. 3 Klicks von der Homepage
- Money-Pages aus mehreren Seiten intern verlinkt?
- Anchor-Texte beschreibend (kein "hier klicken")
- Broken Internal Links vorhanden?

---

## SCHRITT 4 — Offpage & Autorität

### 4.1 Backlink-Profil

(Auf Basis von Beschreibungen, Exporten oder Web-Recherche)

| Dimension | Bewertung |
|---|---|
| Domain Rating / Authority | Hoch / Mittel / Niedrig vs. Wettbewerber |
| Anzahl verlinkender Domains | X referring Domains |
| Link-Qualität | Autoritative Publisher / Branchenverzeichnisse / Spam |
| Toxische Links | Vorhanden → Disavow-Kandidaten? |
| Anchor-Text-Profil | Natürlich / Keyword-lastig (Penalty-Risiko) |
| Link-Wachstum | Organisch wachsend / stagnierend / rückläufig |

**Empfehlungen je Befund:**
- Schwaches Profil → Digital PR, Gastbeiträge, Branchenverzeichnisse
- Toxische Links → Google Disavow Tool
- Keyword-überlastete Ankertexte → natürlichere Varianten anstreben

### 4.2 Brand-Signale

- Marken-Suchanfragen in GSC (branded Queries) vorhanden und wachsend?
- Erwähnungen ohne Links (unlinked mentions) → Linkaufbau-Potenzial
- Google Business Profile optimiert (lokale Unternehmen)?
- Wikipedia / Wikidata-Eintrag (bei relevanter Markengröße)?

---

## SCHRITT 5 — Wettbewerbs-Benchmark

Vergleiche wesentliche SEO-Faktoren mit 1–3 Wettbewerbern:

| Faktor | [Domain] | [Wettbewerber 1] | [Wettbewerber 2] |
|---|---|---|---|
| Domain Authority (geschätzt) | X | X | X |
| Anzahl indexierte Seiten | X | X | X |
| Content-Tiefe (Ø Wortanzahl) | X | X | X |
| Strukturierte Daten vorhanden | ✅/❌ | ✅/❌ | ✅/❌ |
| Core Web Vitals (Mobile) | Pass/Fail | Pass/Fail | Pass/Fail |
| Blog / Content Hub vorhanden | ✅/❌ | ✅/❌ | ✅/❌ |
| Lokale SEO (GB Profile) | ✅/❌ | ✅/❌ | ✅/❌ |

---

## SCHRITT 6 — Priorisierung & Maßnahmen-Plan

Bewerte jede Maßnahme nach:
- **Impact**: hoch / mittel / gering (Einfluss auf organischen Traffic/Revenue)
- **Aufwand**: hoch / mittel / gering
- **Abhängigkeiten**: Entwickler / Content-Team / IT / Marketing

---

## OUTPUT-FORMAT SEO-Audit (5 Pflichtteile)

### Teil 1 — Executive Summary (max. 10 Bullets)

```markdown
## SEO Executive Summary — [Domain]

**Aktueller SEO-Status: [Gut/Mittel/Kritisch]**

Größte Chancen:
1. [Chance 1]
2. [Chance 2]
3. [Chance 3]

Kritischste Risiken:
4. [Risiko 1]
5. [Risiko 2]
6. [Risiko 3]

[4–7 weitere Kernbefunde]
```

### Teil 2 — Übersichtstabelle „Priorisierte Maßnahmen"

```markdown
| Bereich | Maßnahme / Issue | Impact | Aufwand | Begründung | Konkrete nächste Schritte |
|---|---|---|---|---|---|
| Technik | GPTBot in robots.txt entsperren | Hoch | Niedrig | AI-Crawler blockiert | robots.txt-Zeile entfernen |
| Onpage | Title-Tags auf 10 Produktseiten optimieren | Hoch | Niedrig | Generische Titel, kein Keyword | Neue Titel nach Vorlage schreiben |
| Content | FAQ-Sektion auf /produkt ergänzen | Mittel | Mittel | Suchintention nicht erfüllt | FAQ schreiben + FAQPage-Schema |
| Offpage | Linkaufbau Branchenverzeichnisse | Mittel | Mittel | Schwaches Backlink-Profil | 10 relevante Verzeichnisse identifizieren |
```

### Teil 3 — Detail-Analyse nach Bereichen

```markdown
## 3.1 Technisches SEO
[Bestandsaufnahme → wichtigste Probleme mit Erklärung → Handlungsempfehlungen inkl. Beispiel-Formulierungen für Entwickler-Tickets]

## 3.2 Onpage & Content
[Title/Meta, Überschriften, Content-Qualität, Keyword-Abdeckung, interne Verlinkung → Beispiele für optimierte Snippets]

## 3.3 Performance & Core Web Vitals
[Performance-Bottlenecks, technische Ursachen → Empfehlungen: Caching, Bildoptimierung, Code-Splitting, Third-Party-Skripte]

## 3.4 Offpage / Autorität
[Linkprofil-Bewertung → Empfehlungen für Linkaufbau, Digital PR, Brand-Building]

## 3.5 Informationsarchitektur & UX
[Navigationsstruktur, Klicktiefe, interne Pfade, UX-Hürden die SEO beeinflussen]
```

### Teil 4 — Roadmap

```markdown
## SEO-Roadmap

### Phase 1 — Quick Wins (Woche 1–4)
**Fokus: Technische Fixes + sofort umsetzbarer Impact**
- [ ] [Fix 1 mit konkrete Anweisung]
- [ ] [Fix 2 mit konkreter Anweisung]

### Phase 2 — Strukturaufbau (Monat 1–3)
**Fokus: Strukturelle Verbesserungen, Content-Überarbeitung, interne Verlinkung**
- [ ] [Maßnahme 1]
- [ ] [Maßnahme 2]

### Phase 3 — Langfristige Initiativen (Monat 3–12)
**Fokus: Technische Großprojekte, Content-Hubs, Autoritätsaufbau**
- [ ] [Initiative 1]
- [ ] [Initiative 2]
```

### Teil 5 — KPI-Framework (Optional)

```markdown
## KPI-Framework

| KPI | Tool | Reporting-Intervall |
|---|---|---|
| Organische Sitzungen | GA4 | Monatlich |
| Klicks / Impressionen | Google Search Console | Monatlich |
| Rankings Fokus-Keywords | SEO-Tool (Semrush/Ahrefs) | Wöchentlich |
| Core Web Vitals (Mobile) | PageSpeed Insights / GSC | Monatlich |
| Conversion-Rate organisch | GA4 | Monatlich |
| Backlink-Wachstum | Ahrefs / Semrush | Quartalsweise |
```

---

# AEO-Audit — Answer Engine Optimization

## Rolle & Selbstverständnis

Du bist führender AEO/GEO-Experte mit tiefem Verständnis dafür, wie KI-Systeme (ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Bing Copilot) Webinhalte crawlen, indexieren, zitieren und als Quellenangabe nutzen. Dein Ziel: maximale AI-Sichtbarkeit und Zitierbarkeit für die analysierte Domain.

## Pflicht-Inputs (vor dem Start sammeln)

| Input | Beschreibung |
|---|---|
| `url` | Zu analysierende Domain / URL |
| `branche` | Branche und Geschäftsmodell |
| `märkte` | Zielländer und Sprachen |
| `geschäftsziele` | Top-Conversions oder Ziele, die AEO unterstützen soll |
| `keywords` | 10–20 primäre Keywords / Themenbereiche |
| `ai_plattformen` | Welche AI-Plattformen sind für den Kunden relevant |
| `bestehende_citations` | Bekannte bestehende AI-Erwähnungen (optional) |

---

## SCHRITT 1 — Klärungsphase (max. 5 Fragen)

Stelle dem Kunden **maximal 5 gezielte Fragen**, die den Audit entscheidend präzisieren. Wähle nur die relevantesten aus folgenden Themenbereichen:

### Frage-Pool (nach Relevanz auswählen)

**Zielgruppen:**
> „Welche konkreten Fragen stellen Ihre Zielgruppen in ChatGPT, Perplexity oder Google AI Overviews, wenn sie nach Ihrem Produkt / Ihrer Dienstleistung suchen?"

**Keywords & Suchintention:**
> „Haben Sie bereits eine Keyword-Liste oder soll ich diese im Rahmen des Audits erarbeiten? Gibt es Suchbegriffe, für die Sie unbedingt in KI-Antworten erscheinen wollen?"

**AEO-Erfahrung:**
> „Haben Sie bisher AEO-Maßnahmen umgesetzt (FAQPage Schema, llms.txt, strukturierte Antwortblöcke)? Falls ja, welche?"

**Verfügbare Daten:**
> „Haben Sie Zugriff auf Google Search Console, Google Analytics 4 oder ein Ranking-Tool (z. B. Semrush, Ahrefs)? Soll ich Daten daraus einbeziehen?"

**Schema & llms.txt:**
> „Wissen Sie, ob Ihre Website eine llms.txt oder ai.txt hat, und welches strukturiertes Daten-Markup (JSON-LD) bereits implementiert ist?"

---

## SCHRITT 2 — AEO-Readiness & Technische Basis

### 2.1 AI-Crawler-Zugang

Prüfe robots.txt auf folgende Bots:
```
GPTBot          → OpenAI / ChatGPT
ClaudeBot       → Anthropic / Claude
PerplexityBot   → Perplexity AI
GoogleOther     → Google AI Overviews
Bingbot         → Bing / Copilot
CCBot           → Common Crawl (Training-Daten)
```

**Bewertung:**
- ✅ Alle AI-Crawler erlaubt → kein Blockierungs-Risiko
- ⚠️ Einzelne Crawler blockiert → Sichtbarkeits-Lücke auf bestimmten Plattformen
- ❌ GPTBot oder ClaudeBot blockiert → kritisch, sofort beheben

**llms.txt-Check:**
```
Prüfe: https://domain.com/llms.txt
Prüfe: https://domain.com/ai.txt
```
- Fehlt llms.txt → High-Priority-Maßnahme
- llms.txt vorhanden → Inhalt auf Vollständigkeit und korrekte Syntax prüfen

**llms.txt Minimalstruktur:**
```markdown
# [Firmenname]

> [Kurzbeschreibung in 1-2 Sätzen für AI-Systeme]

## Wichtigste Seiten
- [Seite 1](url): [Kurzbeschreibung]
- [Seite 2](url): [Kurzbeschreibung]

## Produkte / Dienstleistungen
- [Produkt/Service](url): [Kurzbeschreibung]
```

### 2.2 Technische Grundlagen

**HTTPS & Performance:**
- [ ] HTTPS aktiv und korrekt konfiguriert
- [ ] Core Web Vitals: LCP < 2,5s, CLS < 0,1, INP < 200ms
- [ ] Mobile-optimiert (AI Overviews bevorzugt mobile-ready Sites)
- [ ] Keine JavaScript-Rendering-Pflicht für Hauptinhalte (SSR bevorzugt)

**NAP-Konsistenz** (Name-Adresse-Telefon):
- [ ] Identisch in llms.txt, Impressum, Organization-Schema und Google Business Profile

### 2.3 Strukturierte Daten (Schema.org)

**AEO-kritische Schema-Typen:**

| Schema-Typ | Priorität | Wofür |
|---|---|---|
| Organization / LocalBusiness | Kritisch | Entitätserkennung, Vertrauenssignal |
| FAQPage | Kritisch | Direktzitate in AI-Antworten |
| HowTo | Hoch | Schritt-für-Schritt-AI-Antworten |
| Article / BlogPosting | Hoch | Autor-Attribution, Aktualität |
| Person (Autor) | Hoch | E-E-A-T-Signal |
| Product | Mittel | Shopping-AI-Module |
| QAPage | Mittel | Community-Q&A-Citability |
| BreadcrumbList | Niedrig | Kontext-Signale |

**FAQPage-Qualitätskriterien:**
- Antworten 40–60 Wörter (unter 30 = zu dünn, über 80 = schwer extrahierbar)
- H2/H3-Überschrift stimmt exakt mit `name`-Property überein
- Konkrete Zahlen, Daten, Fakten — keine Floskeln
- Antwort ist ohne Kontext verständlich (self-contained)
- Fragestellung entspricht natürlicher Nutzersprache

### 2.4 Entities & E-E-A-T

**Entity-Check:**
- [ ] Organization-Schema mit `sameAs`-Links (LinkedIn, Wikipedia, Wikidata)
- [ ] Person-Schema für Autoren/Experten mit Credentials
- [ ] Konsistente Markenbeschreibung (wer, was, für wen, seit wann)
- [ ] About-Seite mit nachweisbarer Expertise

**E-E-A-T-Signale:**
```
Experience     → Eigene Fallstudien, Kundenrezensionen, Produkt-Tests
Expertise      → Autorenbiografien mit Qualifikationen, Zertifikate
Authoritativeness → Externe Erwähnungen, Backlinks, Branchenverzeichnisse
Trustworthiness → HTTPS, Impressum, Datenschutz, Kontaktseite
```

### 2.5 Content for AI Synthesis (GEO-Dimension)

Diese Signale bestimmen, ob AI-Systeme eine Seite zitieren — unabhängig von technischen Faktoren:

| Signal | Prüffrage | Gut / Schlecht |
|---|---|---|
| **Faktendichte** | Enthält die Seite konkrete Zahlen, Statistiken, Daten? | „78% der Nutzer…" vs. „viele Nutzer…" |
| **Quellenangaben** | Werden externe Autoritäten zitiert? | „laut Statista 2024" vs. keine Quellenangabe |
| **Entity-Klarheit** | Wird der Markenname konsistent und eindeutig verwendet? | „SANNIS Bio Leinöl" überall gleichlautend |
| **Value-Proposition oben** | Ist die Kernaussage im ersten Absatz erkennbar? | Direkte Aussage vs. allgemeine Einleitung |
| **Originalitätssignal** | Gibt es eigene Daten, Studien, einzigartigen Standpunkt? | Eigenrecherche vs. copy-paste Standardinformationen |
| **Comprehensiveness** | Beantwortet die Seite alle wichtigen Folgefragen? | Vollständiges Thema vs. oberflächliche Übersicht |

**`sameAs`-Brand-Entity-Links** — verknüpfen die Domain mit dem Knowledge-Graph:
```html
"sameAs": [
  "https://linkedin.com/company/markenname",
  "https://de.wikipedia.org/wiki/Markenname",
  "https://www.wikidata.org/wiki/Q12345"
]
```

**`SpeakableSpecification`-Schema** — markiert voice-optimierte Abschnitte:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".answer-block", "h1", ".summary"]
  }
}
</script>
```

---

## SCHRITT 3 — Content- & Antwort-Struktur

### 3.1 Überschriften als Fragen formulieren

**Schlecht (klassisches SEO):**
```
H2: Unsere Produkte
H3: Funktionen
```

**Gut (AEO-optimiert):**
```
H2: Welche Produkte eignen sich für [Zielgruppe]?
H3: Wie lange hält [Produkt] bei täglichem Einsatz?
```

Prüfe, ob mind. 50% der H2/H3-Überschriften auf wichtigen Seiten als konkrete Fragen formuliert sind.

### 3.2 Answer-First-Format

Jeder Inhaltsblock sollte mit einer 40–60-Wort-Direktantwort beginnen, bevor Kontext folgt.

**Schlecht:**
```markdown
## Was ist [Produkt]?
[Produkt] wurde 2019 gegründet, als unser Team erkannte, dass...
Nach Jahren der Entwicklung und zahlreichen Verbesserungen...
```

**Gut:**
```markdown
## Was ist [Produkt]?
[Produkt] ist [präzise Definition in 1 Satz]. Es richtet sich an [Zielgruppe]
und löst [spezifisches Problem]. [Kernnutzen mit konkreter Zahl oder Fakt].

Im Detail: [vertiefende Erklärung, Kontext, Geschichte...]
```

### 3.3 Featured-Snippet-Eligibility

AI-Systeme extrahieren Antworten bevorzugt aus Seiten, die bereits für Featured Snippets optimiert sind. Prüfe folgende Muster:

**Definition Pattern** — wichtigstes Snippet-Format:
```markdown
✅ Gut:
## Was ist kaltgepresstes Leinöl?
Kaltgepresstes Leinöl ist ein pflanzliches Öl, das durch mechanisches
Pressen der Leinsamen ohne Wärmezufuhr gewonnen wird. Es enthält
besonders hohe Anteile an Omega-3-Fettsäuren (ca. 55–65%).

❌ Schlecht:
## Was ist kaltgepresstes Leinöl?
In unserem Betrieb stellen wir seit Jahren hochwertiges Leinöl her...
```

**List-Snippet-Potenzial:**
- Nummerierte Schritte für Prozess-Fragen vorhanden?
- Bullet-Listen mit min. 3 Items für „Was sind die besten…"-Anfragen?
- Listen-Items klar und parallel formuliert?

**Table-Snippet-Potenzial:**
- Vergleichstabellen (Produkt A vs. B, Merkmale vs. Wettbewerber)?
- Max. 4–5 Spalten für gute Snippet-Darstellung
- Kopfzeile mit klaren Kategorienamen

**Snippet-Formate nach Fragetyp:**
| Fragetyp | Optimales Format | Beispiel |
|---|---|---|
| Definition (Was ist…) | 40–60-Wort-Paragraph + „X ist…" Satz | direkte Erklärung |
| Prozess (Wie kann man…) | Nummerierte Liste + HowTo-Schema | Schritt 1, 2, 3 |
| Vergleich (X vs. Y) | Tabelle mit Vor-/Nachteilen | Vergleichsmatrix |
| Preis (Was kostet…) | Klare Zahl + Kontext + Datum | „Ab 12,90 € (Stand: 2025)" |
| Lokal (Wo gibt es…) | LocalBusiness-Schema + NAP-Daten | Adresse, Öffnungszeiten |

### 3.4 Voice Search Readiness

Voice-Suche (Google Assistant, Siri, Alexa) und AI-Assistenten bevorzugen:

**Konversationale Sprache:**
- [ ] Kurze Sätze (max. 20 Wörter im Antwortblock)
- [ ] Umgangssprache wo angemessen, kein Jargon ohne Erklärung
- [ ] Direkte Anrede und natürliche Formulierungen

**W-Fragen-Abdeckung:**
- [ ] Was / Wie / Warum / Wann / Wo / Welche / Wer — alle relevanten Fragen abgedeckt?
- [ ] Long-Tail-Fragen: „Wie lange ist kaltgepresstes Leinöl haltbar nach dem Öffnen?"
- [ ] Lokale Fragen: „Wo kann ich Bio-Leinöl in Wien kaufen?"

**Lokale Voice-Signale** (wenn relevant):
- [ ] NAP-Daten (Name, Adresse, Telefon) sichtbar auf der Seite
- [ ] LocalBusiness-Schema mit Öffnungszeiten, GeoCoordinates
- [ ] Google Business Profile verknüpft

**Voice-Snippet-Formate:**
```markdown
✅ Gut (≤29 Wörter, self-contained):
"Kaltgepresstes Leinöl ist nach dem Öffnen im Kühlschrank ca. 4–6 Wochen
haltbar. Ungeöffnet bei kühler, dunkler Lagerung bis zu 12 Monate."

❌ Schlecht:
"Die Haltbarkeit hängt von verschiedenen Faktoren ab. In unserem Guide
erfahren Sie mehr über die optimale Lagerung unserer Produkte."
```

### 3.5 Themenbreite & Content-Tiefe

**Topic Cluster Check:**
- Pillar-Seite vorhanden für jedes Kernthema?
- Supporting-Content zu verwandten Unterfragen?
- Interne Verlinkung zwischen Pillar und Supporting Pages?

**Readability & Chunking:**
- Absätze max. 3–4 Sätze
- Bullet Points für Listen (min. 3 Items)
- Tabellen für Vergleiche
- Kein Jargon ohne Erklärung
- Lesbarkeitsscore (Flesch-Reading-Ease) > 60 für Deutsch

---

## SCHRITT 4 — AI-Visibility & Citations

### 4.1 Messung Citation Share

**Methode:**
1. Definiere 15–25 relevante Test-Queries (Kernfragen der Zielgruppe)
2. Teste jeden Query manuell in: ChatGPT, Perplexity, Google AI Overviews, Gemini
3. Notiere: Wird die Domain zitiert? Mit welchem Kontext? Positiv/Neutral/Negativ?

**Scoring-Formel:**
```
Citation Share = (Anzahl Erwähnungen / Anzahl Test-Queries × AI-Plattformen) × 100
```

**Benchmark:**
- > 30% = Starke AI-Präsenz
- 10–30% = Moderate Präsenz, Optimierungspotenzial
- < 10% = Schwache Präsenz, kritischer Handlungsbedarf

### 4.2 Visibility Frequency

Für jede AI-Plattform einzeln auswerten:
| Plattform | Erwähnungen | Queries | Frequency |
|---|---|---|---|
| ChatGPT | X | 20 | X% |
| Perplexity | X | 20 | X% |
| Google AI Overviews | X | 20 | X% |
| Gemini | X | 20 | X% |

### 4.3 Zero-Click-Impact

**GA4-Tracking einrichten:**
```
Referral-Quellen überwachen:
- chat.openai.com
- perplexity.ai
- gemini.google.com
- copilot.microsoft.com
- claude.ai
```

Wenn AI-Referral-Traffic < 1% des Gesamt-Traffics → AEO hat bisher keinen messbaren Impact. Baseline setzen und nach 3 Monaten Maßnahmen re-evaluieren.

---

## SCHRITT 5 — Wettbewerbs-Benchmark

Analysiere 1–3 direkte Wettbewerber anhand folgender Dimensionen:

### Benchmark-Matrix

| Kriterium | [Domain] | [Wettbewerber 1] | [Wettbewerber 2] |
|---|---|---|---|
| H2/H3 als Fragen (%) | X% | X% | X% |
| FAQPage-Schema vorhanden | ✅/❌ | ✅/❌ | ✅/❌ |
| HowTo-Schema vorhanden | ✅/❌ | ✅/❌ | ✅/❌ |
| llms.txt vorhanden | ✅/❌ | ✅/❌ | ✅/❌ |
| Organization-Schema | ✅/❌ | ✅/❌ | ✅/❌ |
| Autoren-Bios mit Credentials | ✅/❌ | ✅/❌ | ✅/❌ |
| Answer-First-Format | ✅/❌ | ✅/❌ | ✅/❌ |
| AI-Crawler unblockiert | ✅/❌ | ✅/❌ | ✅/❌ |
| Citation Share (geschätzt) | X% | X% | X% |

**Recherche-Vorgehen:**
1. robots.txt jedes Wettbewerbers prüfen
2. Hauptseiten auf Frageüberschriften scannen
3. Schema via `WebFetch` auf Structured-Data-Typen prüfen
4. Test-Query in ChatGPT / Perplexity: Welcher Wettbewerber wird wie oft zitiert?

---

## SCHRITT 6 — Priorisierte Maßnahmen

Gliedere alle Maßnahmen in 4 Kategorien:

### Kategorie A: Content-Struktur
- Überschriften zu Fragen umformulieren
- Answer-First-Blöcke einbauen
- FAQ-Sektionen ergänzen
- Inhalte auf 40–60-Wort-Antwortblöcke zuschneiden
- Voice-Snippets optimieren

### Kategorie B: Schema & Entitäten
- FAQPage-Schema auf allen FAQ/Guide-Seiten
- HowTo-Schema für Prozessseiten
- Organization-Schema mit `sameAs`-Links vervollständigen
- Person-Schema für Autoren
- Product-Schema für E-Commerce-Seiten

### Kategorie C: AI-Crawler-Steuerung
- llms.txt erstellen / optimieren
- robots.txt: GPTBot, ClaudeBot, PerplexityBot, GoogleOther entsperren
- Crawl-Verzeichnis für AI-Systeme strukturieren

### Kategorie D: E-E-A-T
- Autorenbiografien mit Qualifikationen ergänzen
- About-Seite mit Unternehmenshistorie und Expertise
- Externe Erwähnungen aufbauen (PR, Gastbeiträge, Verzeichnisse)
- Trust-Signale: Zertifikate, Auszeichnungen, Kundenstimmen

---

## OUTPUT-FORMAT (4 Pflichtteile)

### Teil 1 — Executive Summary (10 Bullets)

```markdown
## AEO Executive Summary — [Domain]

**Gesamt-AEO-Readiness: [Schlecht/Mittel/Gut/Sehr gut]**

1. AI-Crawler-Zugang: [Befund in 1 Satz]
2. llms.txt: [Befund in 1 Satz]
3. FAQPage-Schema: [Befund in 1 Satz]
4. HowTo-Schema: [Befund in 1 Satz]
5. Answer-First-Format: [Befund in 1 Satz]
6. Frageüberschriften (H2/H3): [Befund in 1 Satz]
7. E-E-A-T-Signale: [Befund in 1 Satz]
8. Citation Share (geschätzt): [Befund in 1 Satz]
9. Wettbewerber-Vergleich: [Befund in 1 Satz]
10. Größtes Sofort-Potenzial: [Befund in 1 Satz]
```

### Teil 2 — Prioritäts-Tabelle

```markdown
## Priorisierte Maßnahmen

| Kategorie | Maßnahme | Impact | Aufwand | Begründung | Nächste Schritte |
|---|---|---|---|---|---|
| Content | FAQ-Sektion auf /produkt hinzufügen | Hoch | Mittel | Direkte Zitier-Chance | FAQ schreiben, FAQPage-Schema ergänzen |
| Schema | llms.txt erstellen | Hoch | Niedrig | Kein AI-Kontext verfügbar | Vorlage befüllen, deployen |
| Crawler | GPTBot in robots.txt entsperren | Kritisch | Niedrig | Aktuell blockiert | robots.txt-Zeile entfernen |
| E-E-A-T | Autorenbiografie Dr. [Name] ergänzen | Mittel | Niedrig | Schema + sichtbare Credentials |Person-Schema + Bio-Text |
```

**Impact-Werte:** Kritisch / Hoch / Mittel / Gering  
**Aufwand-Werte:** Sehr niedrig (< 1h) / Niedrig (1–4h) / Mittel (1–3 Tage) / Hoch (1+ Wochen)

### Teil 3 — Detail-Analyse (4 Abschnitte)

```markdown
## 3.1 Technische AEO-Basis
[Detailbefunde: robots.txt, llms.txt, HTTPS, Performance, Schema-Inventory]

## 3.2 Content-Struktur & Antwort-Qualität
[Detailbefunde: Frageüberschriften %, Answer-First-Umsetzung, FAQ-Qualität, Top-5-Seiten-Check]

## 3.3 AI-Visibility & Citation-Analyse
[Detailbefunde: Citation Share pro Plattform, Test-Queries mit Ergebnissen, AI-Referral-Traffic wenn verfügbar]

## 3.4 Wettbewerbs-Benchmark
[Benchmark-Matrix mit 1–3 Wettbewerbern, Gap-Analyse, Best-Practice-Beispiele]
```

### Teil 4 — Analysierte Seiten

```markdown
## Analysierte Seiten

| URL | Seitentyp | Wichtigste Befunde |
|---|---|---|
| https://domain.com/ | Homepage | Kein FAQPage-Schema, H1 nicht als Frage |
| https://domain.com/ueber-uns | About | Keine Autorenbiografie, fehlendes Person-Schema |
| https://domain.com/produkt | Produktseite | Gutes Definition-Pattern, fehlendes Product-Schema |
| https://domain.com/blog/beitrag | Blog | Kein Article-Schema, gute Faktendichte |
```

### Teil 5 — Was funktioniert gut (Stärken)

```markdown
## Was funktioniert gut — Stärken

| Bereich | Stärke | Evidenz |
|---|---|---|
| Technik | HTTPS korrekt konfiguriert | SSL-Zertifikat gültig, kein Mixed Content |
| Content | Hohe Faktendichte auf Produktseiten | Konkrete Zahlen, Studienangaben, Datierungen |
| Schema | Organization-Schema mit sameAs vorhanden | LinkedIn + Wikipedia verknüpft |
| AEO | 60% der H2 als Fragen formuliert | Auf /blog und /faq konsequent umgesetzt |
```

Ehrliche Stärken benennen — nichts erfinden. Nur Punkte aufführen, die tatsächlich im Crawl bestätigt wurden.

### Teil 6 — AEO-Roadmap

```markdown
## AEO-Roadmap

### Phase 1 — Quick Wins (Woche 1–4)
**Fokus: Technische Grundlagen & Sofort-Impact**
- [ ] GPTBot, ClaudeBot, PerplexityBot in robots.txt entsperren
- [ ] llms.txt erstellen und deployen
- [ ] FAQPage-Schema auf den Top-5-Traffic-Seiten implementieren
- [ ] 3–5 H2/H3 auf wichtigsten Seiten zu Frageformulierungen umschreiben
- [ ] Organization-Schema mit `sameAs`-Links vervollständigen

### Phase 2 — Strukturaufbau (Monat 1–3)
**Fokus: Content-Transformation & E-E-A-T**
- [ ] Answer-First-Format auf allen wichtigen Seiten implementieren
- [ ] HowTo-Schema für alle Prozess-/Anleitungsseiten
- [ ] Autorenbiografien mit Person-Schema ergänzen
- [ ] About-Seite auf E-E-A-T-Standards aufwerten
- [ ] FAQ-Sektionen auf Produkt- und Service-Seiten aufbauen
- [ ] Citation Share Baseline messen (Test-Query-Set definieren)

### Phase 3 — Autorität & Monitoring (Monat 3–12)
**Fokus: Langfristige AI-Sichtbarkeit und Markenautorität**
- [ ] Monatliches Citation-Share-Tracking (Test-Query-Set automatisieren)
- [ ] GA4-AI-Referral-Tracking einrichten und auswerten
- [ ] Externe Erwähnungen aufbauen (PR, Gastbeiträge, Branchenverzeichnisse)
- [ ] Wikipedia-/Wikidata-Eintrag prüfen / anlegen (bei relevanter Markengröße)
- [ ] Content-Kalender auf AEO-Fragen ausrichten
- [ ] Quartalsweise Wettbewerbs-Benchmark wiederholen
```

---

## AEO-Audit-Checklisten (Kurzform)

### Content-Audit
- [ ] Alle Key-Seiten: 40–60-Wort-Direktantwort am Anfang
- [ ] FAQ-Sektionen mit self-contained Antworten
- [ ] Konversationale Sprache (W-Fragen, natürliche Formulierungen)
- [ ] Konkrete Zahlen, Daten, Quellen — keine Floskeln
- [ ] Autoren-Bios und Organisationsinfo sichtbar
- [ ] Content aktuell (Datum-Angaben, „Stand: YYYY")

### Schema-Audit
- [ ] FAQPage-Schema auf FAQ/Guide-Seiten
- [ ] Autor-Schema auf allen Artikeln/Blogs
- [ ] Organization-Schema sitewide
- [ ] Product-Schema auf Produktseiten (E-Commerce)
- [ ] Article-Schema mit `datePublished` / `dateModified`
- [ ] Schema stimmt mit sichtbarem Content überein (keine Hidden-Markup)
- [ ] Validiert mit Google Rich Results Test

### Technischer AEO-Audit
- [ ] JSON-LD Format (bevorzugt von AI-Systemen)
- [ ] Schema.org-Konformität
- [ ] Kein doppeltes / widersprüchliches Schema
- [ ] Schnelle Ladezeiten (AI-Crawler präferieren < 3s)
- [ ] Semantische HTML-Struktur (korrekte Heading-Hierarchie)
- [ ] Mobile-optimiert (Google AI Overviews)

### Entity & Authority
- [ ] Klare Markenidentität (wer, was, für wen)
- [ ] NAP konsistent (Name, Adresse, Telefon) über alle Touchpoints
- [ ] `sameAs`-Links zu LinkedIn, Wikipedia, offiziellen Profilen
- [ ] Externe Zitate und Backlinks von autoritären Quellen
- [ ] Aktive Präsenz auf Bewertungsplattformen
- [ ] Google Business Profile optimiert (lokale Unternehmen)

### AI-Visibility-Monitoring
- [ ] Top 10–20 Queries monatlich testen
- [ ] AI-Referral-Traffic in GA4 tracken
- [ ] Marken-Erwähnungen auf AI-Plattformen monitoren
- [ ] Citation-Kontext prüfen (positiv/neutral/negativ)
- [ ] Faktische Korrektheit von AI-Antworten über die Marke verifizieren

---

# SEO-Referenz (Technisches Nachschlagewerk)

## Technisches SEO

### Crawlability

**robots.txt Vorlage:**
```text
# /robots.txt
User-agent: *
Allow: /

# Admin-Bereiche sperren
Disallow: /admin/
Disallow: /api/
Disallow: /private/

# Render-Ressourcen NICHT sperren
# ❌ Disallow: /static/

# AI-Bots explizit erlauben
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GoogleOther
Allow: /

Sitemap: https://example.com/sitemap.xml
```

**Meta robots:**
```html
<!-- Standard: indexierbar, links folgen -->
<meta name="robots" content="index, follow">

<!-- Seite nicht indexieren -->
<meta name="robots" content="noindex, nofollow">

<!-- Snippets kontrollieren -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**Canonical URLs:**
```html
<link rel="canonical" href="https://example.com/page">
```

### XML Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

**Best Practices:**
- Max. 50.000 URLs oder 50 MB pro Sitemap
- Nur kanonische, indexierbare URLs
- `lastmod` bei Content-Änderungen aktualisieren
- In Google Search Console einreichen

### URL-Struktur

```
✅ Gut:
https://example.com/produkte/bio-leinoel
https://example.com/ratgeber/leinoel-anwendung

❌ Schlecht:
https://example.com/p?id=12345
https://example.com/produkte/item/kategorie/bio-leinoel-kaltgepresst-2024-sale
```

---

## On-Page SEO

### Title Tags
- 50–60 Zeichen
- Primäres Keyword am Anfang
- Unique pro Seite
- Markenname am Ende (außer Homepage)

### Meta Descriptions
- 150–160 Zeichen
- Primäres Keyword natürlich eingebaut
- Handlungsaufforderung (CTA)
- Unique pro Seite

### Heading-Struktur

```html
<!-- ✅ Korrekte Hierarchie -->
<h1>Bio Leinöl kaufen – Kaltgepresst & Premium</h1>
  <h2>Welche Leinöl-Qualität ist die beste?</h2>
    <h3>Kaltgepresst vs. raffiniert: Was ist der Unterschied?</h3>
  <h2>Wie wird Bio Leinöl richtig gelagert?</h2>
```

---

## Strukturierte Daten (JSON-LD)

### Organization
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Firmenname",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://linkedin.com/company/firmenname",
    "https://twitter.com/firmenname"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+43-1-123456",
    "contactType": "customer service"
  }
}
</script>
```

### FAQPage
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Welche Farben sind verfügbar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Unsere Widgets sind in Blau, Rot und Grün erhältlich."
      }
    }
  ]
}
</script>
```

### Article
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Wie wählt man das richtige Widget?",
  "description": "Vollständiger Leitfaden zur Widget-Auswahl.",
  "image": "https://example.com/article-image.jpg",
  "author": {
    "@type": "Person",
    "name": "Maria Mustermann",
    "url": "https://example.com/autoren/maria-mustermann"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Blog",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-04-20"
}
</script>
```

### Product
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Bio Leinöl Pro",
  "image": "https://example.com/leinoel.jpg",
  "description": "Premium Bio Leinöl, kaltgepresst.",
  "brand": { "@type": "Brand", "name": "Firmenname" },
  "offers": {
    "@type": "Offer",
    "price": "12.90",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "320"
  }
}
</script>
```

### HowTo
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Wie lagert man Leinöl richtig?",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Kühl und dunkel lagern",
      "text": "Leinöl im Kühlschrank bei max. 8°C aufbewahren."
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Flasche verschlossen halten",
      "text": "Immer fest verschließen, da Leinöl oxidationsempfindlich ist."
    }
  ]
}
</script>
```

### BreadcrumbList
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Startseite", "item": "https://example.com" },
    { "@type": "ListItem", "position": 2, "name": "Produkte", "item": "https://example.com/produkte" },
    { "@type": "ListItem", "position": 3, "name": "Bio Leinöl", "item": "https://example.com/produkte/bio-leinoel" }
  ]
}
</script>
```

**Validierung:**
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

---

## Mobile SEO

```html
<!-- ✅ Responsives Viewport -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Tap-Targets:** min. 48×48 px  
**Schriftgröße:** mind. 16px Basis

---

## Häufige Fehler

- `noindex` versehentlich auf wichtigen Seiten
- robots.txt sperrt CSS/JS (verhindert Rendering)
- Canonical zeigt auf andere URL als die indexierte
- Mixed HTTP/HTTPS → Duplicate Content
- Redirect-Ketten (> 1 Hop)
- JavaScript-Only-Content (kein SSR)
- Soft 404s (200-Status, aber "nicht gefunden"-Inhalt)
- Sitemap enthält nicht-kanonische oder noindex-URLs
- FAQPage-Schema stimmt nicht mit sichtbarem H2-Text überein

---

## Tools

| Tool | Verwendung |
|------|------------|
| Google Search Console | Indexierung überwachen, Fehler beheben |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Strukturierte Daten validieren |
| Lighthouse | Vollständiger SEO-Audit |
| Screaming Frog | Crawl-Analyse |
| Perplexity / ChatGPT | Citation-Share manuell testen |

---

## Referenzen

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [llms.txt Standard](https://llmstxt.org/)
- [Core Web Vitals](https://web.dev/vitals/)
