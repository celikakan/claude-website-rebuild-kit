# SEO / GEO / AEO — Sichtbarkeit auf höchstem Niveau (Schritt 6)

Ziel: Die neue Seite wird von Google gerankt UND von KI-Suchsystemen
(ChatGPT, Perplexity, Google AI Overviews, Claude) gefunden, verstanden und
zitiert. Alles hier fließt in `artefakte/seo-plan.md` und wird in Schritt 8
umgesetzt.

## 1. Klassisches SEO (Basis)

- Pro Seite: Title ≤ 60 Zeichen (Marke + Kernnutzen), Description ≤ 160
  (konkret, mit Handlungsimpuls), genau eine H1, logische H2/H3.
- Open Graph: Title, Description, Bild aus der Asset-Map.
- Keywords aus Original-Themen + Branchen-Brief (Schritt 2). Wenn
  DataForSEO-/Ahrefs-/Semrush-MCP verbunden: Volumen und SERP-Daten ziehen;
  sonst Ableitung kennzeichnen als "ohne Volumendaten".
- Sprechende URLs, saubere interne Verlinkung (Skill `site-architecture`):
  jede Seite von mindestens einer anderen erreichbar, Kernseiten aus dem
  Footer, Breadcrumbs bei Tiefe > 1.

## 2. Redirect-Map (der meistvergessene Rankings-Schutz)

Aus `artefakte/url-liste.md`: jede alte URL → neue URL (301). Entfallene
Inhalte → nächstbeste Seite, nie pauschal auf die Startseite. Ergebnis:
`artefakte/redirect-map.md` mit fertiger Regel-Syntax (Kommentarblock je
Hosting: .htaccess / netlify.toml / vercel.json / next.config redirects).
Aktivierung ist Launch-Aufgabe → Übergabe-Doku.

## 3. Strukturierte Daten (JSON-LD, Skill `schema-markup`)

Pflicht pro Projekt:
- `Organization` oder `LocalBusiness` (Name, Adresse, Telefon, Öffnungszeiten,
  Geo — aus dem Content-Inventar, nichts erfinden) auf der Startseite.
- `FAQPage` auf jeder Seite mit FAQ-Sektion (Fragen/Antworten identisch mit
  dem sichtbaren Text — Google-Vorgabe).
- `BreadcrumbList` bei Unterseiten.
- Branchenabhängig: `Service`, `Product` (mit Preis nur wenn echt),
  `Event`, `Restaurant`, `MedicalBusiness` … passend zur Branche wählen.
- Alle Werte stammen aus dem Content-Inventar. Erfundene Bewertungssterne
  (`aggregateRating` ohne echte Quelle) sind verboten.

## 4. GEO/AEO: Für KI-Systeme zitierfähig werden (Skill `ai-seo`)

KI-Assistenten zitieren Seiten, die Antworten liefern statt Marketing:

- **Antwort-Blöcke:** Jede wichtige Seite beantwortet ihre Kernfrage in den
  ersten 1–2 Sätzen nach der H1 direkt und faktisch ("Wer / Was / Wo / Kosten
  / Ablauf"). Danach Details.
- **FAQ-Pflicht (Kernregel):** Fragen wörtlich so, wie Kunden sie stellen
  (Quelle: customer-research aus Schritt 2). Jede Antwort: erst der
  zitierfähige 1–2-Satz-Kern, dann Ausführung. 5–10 Fragen pro Seite-Typ.
- **Fakten maschinenlesbar:** Adresse, Telefon, Öffnungszeiten, Preise,
  Leistungsliste als klarer Text + Schema — nicht nur in Bildern/PDFs.
- **llms.txt** ins Website-Root: Kurzbeschreibung des Unternehmens, Kern-
  Leistungen, wichtigste Seiten mit URLs, Kontakt — als kompaktes Markdown.
- **robots-Freigabe für KI-Crawler** (GPTBot, PerplexityBot, ClaudeBot,
  Google-Extended) bewusst entscheiden: Standard = erlauben (Sichtbarkeit ist
  das Ziel); nur auf User-Wunsch blocken.
- Semantisches HTML ist die Grundlage: header/nav/main/section/footer,
  Listen als Listen, Tabellen als Tabellen.

## 5. Abschluss-Selbstcheck

Skill `seo-geo-aeo-audit` im **Live-Modus** auf die NEUE Website anwenden
(lokale Dateien bzw. Preview — ohne Tool-PDF-Pflicht): Meta, Schema,
Antwort-Blöcke, llms.txt, interne Links. Gefundene Mängel vor Gate 3 beheben
und im QA-Bericht abhaken. Wenn Ahrefs-MCP verbunden: Brand-Radar-Baseline
notieren (KI-Zitierungen), damit der Kunde den Effekt später messen kann.

## Demo vs. Launch

- Demo: `noindex` + Hinweis in der Übergabe-Doku ("vor Launch entfernen").
- Launch: index erlaubt, Sitemap.xml erzeugen, Redirect-Map aktivieren.
