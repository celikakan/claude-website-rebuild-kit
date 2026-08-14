# QA-Checkliste (Schritt 9) — erst wenn alles ✓, kommt Gate 3

Vier Blöcke: Vorlagentreue, Inhalt, Technik/Barrierefreiheit, Übergabe.
Jeder Punkt wird mit ✓/✗ + Beleg im `artefakte/qa-bericht.md` dokumentiert.

## Block 1: Vorlagentreue-Beweis

- [ ] Screenshots neue Website vs. Vorlage, nebeneinander, pro Seitentyp,
      Desktop UND Mobil → `artefakte/vergleich-screenshots/`
- [ ] Farben identisch mit design-tokens.css (Stichprobe per Computed Style)
- [ ] Typografie: gleiche Hierarchie-Sprache (Display/Body/Label), Größenskala
- [ ] Sektionsabfolge und Layout-Typen entsprechen der Blaupause
- [ ] Header-, Menü- und Footer-Verhalten wie Vorlage (Scroll, Mobil-Menü)
- [ ] Motion-Charakter wie Vorlage (Easing, Reveals, Hover)
- [ ] Jede Abweichung gelistet + begründet (Inhalts-Bann / Barrierefreiheit /
      Seitenplan) — unbegründete Abweichungen werden behoben

## Block 2: Inhalts-Abgleich & Vorlagen-Leak (BLOCKER-Block)

- [ ] **Leak-Scan gelaufen (struktur-extraktion.md Abschnitt 7): 0 Treffer**
      über ALLE Dateien in website/ — inkl. title/meta/alt/og. Jeder
      Treffer ist ein Blocker; Ausnahmen einzeln begründet im qa-bericht
- [ ] KEIN Logo, Foto, Video, Text, Headline oder Button-Label der Vorlage
      im Ergebnis — gilt AUSNAHMSLOS, auch bei gekauften/lizenzierten
      Templates (Kernregel 2); jede Unterseite einzeln von Hand geöffnet
- [ ] seitenplan.md komplett abgehakt: jede Original-Seite hat ihr Ziel
      erreicht, jede Vorlagen-Seite ist GEFÜLLT / UMGEWIDMET / GESTRICHEN —
      keine mitkopierte Vorlagen-Seite übrig, Navigation/Footer bereinigt
- [ ] NEU-Inhalte entsprechen exakt der Gate-2-Freigabe (nichts ungefragt
      dazu, nichts Freigegebenes vergessen)
- [ ] mapping.md komplett abgehakt — kein Original-Inhalt verloren
      (Coverage: 100 % der content-inventar-Zeilen zugeordnet)
- [ ] medien-plan.md komplett abgehakt: jedes ÜBERNOMMEN-Bild/-Video sitzt
      an seinem freigegebenen Platz (Seite + Sektion), kein Bestands-Medium
      stillschweigend weggelassen; NICHT-ÜBERNOMMEN nur mit Gate-2-Freigabe
- [ ] animations-plan.md umgesetzt: freigegebene Scroll-Motion-/
      Video-Animations-/Neu-Animations-Einsatzorte gebaut, nichts
      Ungefragtes darüber hinaus
- [ ] Fakten stichprobengeprüft: Telefon, Adresse, Öffnungszeiten, Preise,
      Zahlen exakt wie im Content-Inventar
- [ ] **Footer-Pflichtblock** auf jeder Seite: Impressum + Datenschutz
      verlinkt (eigene Seiten), ggf. AGB/Über uns wie mit dem User geklärt;
      Rechtsseiten vorhanden, **Texte wörtlich identisch** mit dem Original
      (bzw. gekennzeichnetes Platzhalter-Gerüst laut Freigabe)
- [ ] FAQ vorhanden, Fragen in Kundensprache, Antworten mit zitierfähigem
      Kern, FAQPage-Schema deckungsgleich mit sichtbarem Text
- [ ] Nichts erfunden: keine ausgedachten Kundenstimmen, Zahlen, Siegel
- [ ] Kein Lorem Ipsum, keine TODO-Reste, keine leeren Platzhaltertexte
- [ ] Sprachprofil eingehalten (Stichprobe gegen voice-profile.md), keine
      KI-Floskeln (disallow-Liste), keine Gedankenstriche als Stilmittel

## Block 3: Technik, Barrierefreiheit, Performance

**Funktion**
- [ ] Alle Seiten erreichbar, interne Links + Anker treffen, 404-Seite da
- [ ] Formulare validieren (Fehlermeldungen inline, Fokus aufs erste Fehlerfeld),
      Success-State; ohne Backend als Demo gekennzeichnet
- [ ] Filter/Tabs/Akkordeons/Carousel funktionieren; Zustände mit aria
- [ ] Next.js: `next build` Exit 0, alle Routen generiert

**WCAG 2.2 (EAA-Pflichtniveau)**
- [ ] Kontrast: Text ≥ 4,5:1 (großer Text ≥ 3:1), UI-Komponenten ≥ 3:1
- [ ] Fokus sichtbar auf allem Interaktiven; Fokus nie verdeckt (2.4.11);
      logische Fokus-Reihenfolge; Skip-Link vorhanden
- [ ] Touch-/Klickziele ≥ 24×24 px (2.5.8); mobile Inputs ≥ 16px Schrift
- [ ] Volle Tastaturbedienung (Menü, Akkordeon, Formular, Modal ohne Falle)
- [ ] Labels an allen Feldern, autocomplete/type/inputmode korrekt,
      keine Redundanz-Abfragen (3.3.7), Paste nie blockiert
- [ ] Alt-Texte auf allen Inhaltsbildern; Dekoratives aria-hidden;
      Icon-Buttons mit aria-label; lang-Attribut gesetzt
- [ ] Statusinfos nicht nur über Farbe; aria-live für dynamische Meldungen
- [ ] prefers-reduced-motion: Reveals statisch, Videos nur Poster, Marquees
      stehen; keine Autoplay-Medien mit Ton; Zoom nicht deaktiviert

**Interface-Guidelines (Vercel-Essentials)**
- [ ] Nur transform/opacity animiert, kein `transition: all`, keine
      Layout-Prop-Animationen, kein scroll-Listener für Animation
- [ ] Skeletons/Platzhalter formstabil (kein Layout-Shift), width/height
      auf Bildern
- [ ] Lange Inhalte brechen sauber (truncate/break-words, min-w-0 in Flex)
- [ ] Zahlenvergleiche mit tabular-nums; Datums-/Zahlenformate lokalisiert
- [ ] Keine toten Links/`#`-Buttons; aktiver Nav-Punkt markiert

**Performance-Budget**
- [ ] LCP-Kandidat (Hero) optimiert: modernes Format, priorisiert geladen
- [ ] CLS < 0,1 plausibel (Maße reserviert, Fonts mit swap)
- [ ] Videos lazy + Poster; max. 3–4 prominent, eins pro Viewport
- [ ] Kein Renderblocker-JS; Gesamtgewicht der Startseite geprüft

**KI-Tells-Kurzcheck (aus taste-/redesign-skill)**
- [ ] Kein Violett-Verlauf-Default, keine drei identischen Feature-Cards,
      kein reines #000/#fff, keine Emoji-Icons, keine Fake-Screenshots aus
      Divs, keine erfundenen Präzisionszahlen, ein Akzent konsequent

## Block 4: SEO/GEO/AEO-Abnahme

- [ ] Title/Description/OG pro Seite (≤ 60/160), genau eine H1
- [ ] JSON-LD valide (Organization/LocalBusiness, FAQPage, Breadcrumb,
      Branchen-Schema) — Test: Schema-Parser wirft keine Fehler
- [ ] llms.txt im Root; robots-Entscheidung dokumentiert; Demo → noindex
- [ ] Redirect-Map vollständig (jede alte URL hat ein Ziel)
- [ ] seo-geo-aeo-audit-Selbstcheck gelaufen, Mängel behoben

## Übergabe-Doku (`artefakte/uebergabe-doku.md`)

Pflicht-Inhalte: gebaute Seiten · Herkunft aller Medien (Bestand / Original /
generiert / Platzhalter) · offene Platzhalter + Lücken · Abweichungen von
Vorlage und Original mit Begründung · Launch-Liste (Redirects aktivieren,
Formular-Backend, Rechtstexte juristisch prüfen lassen, noindex entfernen,
Hosting/CDN, Analytics + Consent) · Empfehlung für 3 A/B-Test-Hypothesen
nach Launch (aus page-cro).

**Gate 3:** QA-Bericht + Screenshots + Übergabe-Doku dem User zeigen.
Fertig ist das Projekt erst mit seiner Endabnahme.
