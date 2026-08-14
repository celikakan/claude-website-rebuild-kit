# Scraping-Playbook: Original & Vorlage erfassen

## Werkzeug-Kette (verbindliche Reihenfolge)

**Fuer ORIGINAL-Website und RECHERCHE (Wettbewerber, Bewertungen, Quellen):**

1. **Scrapling (Pflicht, erste Wahl):** Python-Scraping-Bibliothek —
   `pip install scrapling --break-system-packages`. Statische/serverseitige
   Seiten mit dem einfachen Fetcher; JS-gerenderte oder Bot-geschützte
   Seiten mit dem Stealth-/Dynamic-Fetcher (dafür einmalig
   `scrapling install` für die Browser-Abhängigkeiten; schlägt das fehl →
   Stufe 2, kein Abbruch). Grundmuster:
   ```python
   from scrapling.fetchers import Fetcher
   page = Fetcher.get('https://original-seite.tld/unterseite')
   text  = page.get_all_text(ignore_tags=('script','style'))
   links = [a.attrib['href'] for a in page.css('a[href]')]
   imgs  = [i.attrib.get('src') for i in page.css('img')]
   # JS-/Bot-geschuetzt: from scrapling.fetchers import StealthyFetcher
   # page = StealthyFetcher.fetch(url)  # echte Browser-Engine
   ```
   Damit die komplette Original-Site systematisch abarbeiten: Startseite →
   alle internen Links → jede Seite als Text + Asset-URLs sichern.
2. **Chrome-Browser-Tools** (claude-in-chrome: navigate, get_page_text,
   read_page, javascript_tool, Screenshots) — für JS-lastige Reste, Seiten
   hinter Interaktion und alles, was Scrapling nicht sauber liefert.
3. **Apify-MCP** (wenn verbunden) — für große Crawls (> 10 Seiten),
   Bot-geschützte Seiten und Massen-Downloads von Bildern/Videos
   (z. B. Website Content Crawler Actor). Nutzt das Guthaben des Users.
4. **web_fetch** — letzter Fallback.

**Fuer die VORLAGE (Struktur-Extraktion):** Chrome-Browser-Tools bleiben
erste Wahl — die Selbst-Extraktion braucht getComputedStyle, echtes DOM und
den Motion-Stack im laufenden Browser (references/struktur-extraktion.md).
Scrapling/Playwright nur als Fallback, wenn kein Chrome verbunden ist.

Scheitert alles (Login, harter Bot-Schutz): nicht tricksen — User um
Export/Screenshots bitten oder Apify-Verbindung vorschlagen, mit markierten
Platzhaltern weiterarbeiten. Niemals Inhalte erfinden.

Seitenauswahl: Startseite zuerst, dann ALLE Seiten aus Navigation, Footer
und Sitemap — vollständig, kein Limit (Kernregel 3: 100 % des Originals).
Nur bei sehr großen Sites (> ~25 Seiten) eine Priorisierung VORSCHLAGEN und
die User-Freigabe abwarten; ausgelassene Seiten mit Begründung in der
url-liste dokumentieren. **Rechtsseiten immer zusätzlich.**

## A) Content-Inventar (Original)

Ziel: Die Substanz vollständig sichern → `artefakte/content-inventar.md`.
Pro Seite:

```markdown
## Seite: /leistungen  (Zweck: Leistungsübersicht → Anfrage)
- Alte URL: https://…/leistungen.html   ← für die Redirect-Map
- H1: "…"
- Sektion "…": [Text wörtlich]
- CTAs: "…" → Ziel
- Bilder: dateiname/URL + Beschreibung · Videos: URL + Beschreibung
- Fakten: Telefon, Mail, Adresse, Öffnungszeiten, Preise, Zahlen ("seit 1998")
- Lücken/Auffälligkeiten: …
```

Regeln: Texte wörtlich (gekürzt wird erst beim Mapping). Zahlen, Namen,
Preise exakt. Alle alten URLs in `artefakte/url-liste.md` sammeln.

**Rechtsseiten (Pflichtblock):** Impressum, Datenschutzerklärung, AGB,
Widerruf, Storno, Hausordnung, Cookie-Richtlinie — was existiert, wird im
**Volltext wörtlich** gesichert (eigener Abschnitt im Inventar oder eigene
Dateien `artefakte/recht/…`). Diese Texte werden später 1:1 übernommen,
nie umformuliert. **Fehlen Impressum oder Datenschutz:** sofort die
Pflicht-Frage aus der Footer-Pflicht an den User (Texte nachliefern /
gekennzeichnetes Platzhalter-Gerüst) — Rechtstexte niemals selbst erfinden.

**Medien übernehmen (Kernregel 7 — Pflicht, vollständig):** ALLE Bild-/
Video-URLs aus dem Inventar herunterladen → `assets/bilder/`,
`assets/videos/`, sprechende Dateinamen, Alt-Texte aus dem Kontext. Vom
User gelieferte Bestände (Frage 6) dazu. Ergebnis:
`artefakte/asset-map.md` (Datei, Alt-Text, Herkunft, bisheriger Einsatzort
auf dem Original, bei Videos Poster). Die Asset-Map muss JEDES Medium
enthalten — sie ist die Basis des Medien-Plans (Schritt 5c), in dem jedes
Medium einen Platzierungs-Vorschlag bekommt oder mit Begründung zur
Nicht-Übernahme vorgeschlagen wird. Apify für Massen-Downloads. Nicht
ladbare Medien → Lückenliste.

## B) Vorlage erfassen (Design wird übernommen!)

Ziel: exakte, umsetzbare Design-Basis → `artefakte/vorlage-blaupause.md` +
`artefakte/design-tokens.css`.

**Zweig 1 — Live-Website als Vorlage:**

- Screenshots pro Seitentyp (Desktop + schmaler Viewport) zur Analyse.
- Exakte Tokens per Chrome javascript_tool erheben (getComputedStyle auf
  body, Headlines, Buttons, Cards, Header, Footer): Farben als Hex,
  font-family, Größenskala (H1/H2/Body/Label), Zeilenhöhen, letter-spacing,
  Abstände (Sektions-Padding), border-radius, Schatten, Breakpoint-Verhalten.
- Struktur: Sektionsabfolge pro Seitentyp mit Layout-Typ ("Hero: volle Höhe,
  Split 60/40, H1 links unten, 2 CTAs"), Navigations- und Footer-Aufbau,
  Scroll-/Hover-Verhalten, Interaktionen (Sticky-CTA, Akkordeon, Filter,
  Marquee, Zähler), Motion-Charakter (Easing, Dauer, Stagger).
- Skill `website-brand-analysis` unterstützt die Analyse — Telegram-Versand
  ignorieren, alles lokal speichern.
- **Alle Unterseiten erfassen:** Navigation + Footer + Sitemap durchgehen →
  `artefakte/vorlagen-seitenliste.md` (URL, Thema, Sektions-Typen). Pro
  Seite das Text-Inventar sichern → `artefakte/vorlagen-text-inventar/`
  (Basis des Leak-Scans, siehe struktur-extraktion.md Abschnitt 6/7).
- **Inhalts-Bann dokumentieren (Kernregel 2):** SÄMTLICHE Inhalte der
  Vorlage — Logos, Fotos, Videos, Illustrationen, Texte, Headlines,
  Button-/Label-Texte — werden NICHT übernommen; in der Blaupause als
  "ersetzen durch Original-Inhalt/NEU-Inhalt/Platzhalter" markieren.

**Zweig 2 — Template/Theme als Datei (gekauft):**

- Kein Scraping: Dateien direkt einlesen. Tokens aus dem CSS/Config
  übernehmen (bei Tailwind: theme-Konfiguration), Struktur aus den
  Template-Seiten. Lizenz liegt beim User (kurz bestätigen lassen).
  **Der Inhalts-Bann gilt trotzdem in voller Härte (Kernregel 2):** auch
  bei gekauften Templates werden ALLE Texte, Headlines, Bilder, Videos
  und Labels ersetzt — von der Vorlage bleibt nur Struktur, CSS/JS und
  Motion. Seitenliste + Text-Inventar auch hier Pflicht (aus den
  Template-Dateien statt per Browser).

**design-tokens.css Format:**

```css
:root {
  --bg: #…; --surface: #…; --text: #…; --muted: #…;
  --accent: #…; --accent-2: #…;
  --font-display: …; --font-body: …; --font-mono: …;
  --radius-card: …; --radius-btn: …;
  --space-section: …; --maxw: …;
  /* + Schatten, Border, Easing, Dauer */
}
```

Die Blaupause endet mit einer Kurzfassung für Gate 1: Farbpalette (Swatches
als Hex-Liste), Typo-Stack, Sektionsliste pro Seitentyp, Interaktions-Liste.
