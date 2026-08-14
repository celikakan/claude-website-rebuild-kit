# Design-Checkliste: Premium statt Template · Stand 2026

## Was 2026 Standard ist (Messlatte für jedes Rebuild)

- **Performance:** LCP < 2,5 s, CLS < 0,1 – Bilder mit Breite/Höhe, moderne
  Formate (webp/avif), Videos lazy + Poster, kein Renderblocker-JS.
- **Barrierefreiheit (WCAG 2.2 AA als Ziel):** Kontraste ≥ 4,5:1,
  Fokus-Zustände sichtbar, Formulare mit Labels + Fehlermeldungen,
  Touch-Ziele ≥ 24 px, `prefers-reduced-motion` UND `prefers-color-scheme`
  respektiert.
- **Maschinenlesbarkeit:** semantisches HTML, strukturierte Daten (JSON-LD:
  Organization/LocalBusiness, FAQ, Breadcrumb), saubere Meta- und OG-Daten –
  auch KI-Suchsysteme lesen die Seite.
- **UX-Muster, die User erwarten:** Sticky-Header mit Scroll-Verhalten,
  mobiles Vollbild-Menü, Micro-Interactions auf allem Klickbaren,
  Skeleton/Blur-Platzhalter statt Layout-Sprüngen, klare Formular-States.
- **Ehrlichkeit:** Demo-Projekte als Demo kennzeichnen, `noindex` bis Launch.

## Warum Seiten "nach KI" aussehen – und die Gegenmittel

| Generisch                                   | Premium                                                        |
| ------------------------------------------- | -------------------------------------------------------------- |
| Violett-Blau-Verlauf auf Weiß               | Marken-Farbwelt, dunkle Basis oder bewusst editorial hell       |
| Drei gleiche Feature-Cards mit Schatten     | Wechselnde Layouts: Splits, volle Bildflächen, asymmetrische Grids |
| Emoji als Icons                             | Typografische Labels, Nummern (01/02/03), feine SVG-Linien      |
| Alles zentriert, gleiche Abstände           | Klarer Rhythmus: enge Gruppen, große Pausen, linksbündige Blöcke |
| Headline "Willkommen bei …"                 | Eine Haltung als Headline ("Tempo ist eine Entscheidung.")      |
| Buttons "Mehr erfahren" überall             | Spezifische CTAs ("Probetraining sichern", "Drop 01 ansehen")   |
| Lorem Ipsum / Platzhalterkästen             | Echte Texte; fehlende Bilder als gestylte Marken-Platzhalter    |

## Typografie-Hebel

- Headlines groß denken: `clamp(2.5rem, 8vw, 7rem)`, Zeilenhöhe ~0.9–1.05,
  uppercase + negatives Tracking für technisch/sportlich.
- Hierarchie über Kontrast: Mono-Eyebrow (klein, gesperrt, Akzentfarbe) →
  Display-Headline → gedämpfter Fließtext. Drei Ebenen reichen.
- Tabellarische Ziffern für Zahlen/Countdowns (`font-variant-numeric`).

## Farbe & Textur

- 1 Basis (fast schwarz oder fast weiß), 1 Fläche (Surface), 1–2 Akzente.
  Akzent sparsam: Linien, Hover, Labels – nicht ganze Flächen.
- Tiefe ohne Schatteninflation: hauchdünne Borders (`rgba(255,255,255,.08)`),
  Radial-Gradients als Lichtquellen, CSS-Texturen (repeating-linear-gradient).

## Motion-Regeln

- Einmal einfaden beim ersten Sichtbarwerden, danach Ruhe. Stagger (60–100 ms
  Versatz) für Listen. Easing `cubic-bezier(0.22,1,0.36,1)`.
- Hover überall dort, wo man klicken kann – Scale auf Bildern (1.03–1.05,
  700 ms), Farbwechsel auf Links, Pfeile, die sich bewegen.
- `prefers-reduced-motion: reduce` → alles statisch, Videos als Poster.

## Abnahme (vor "fertig")

- [ ] Kein Lorem Ipsum, keine leeren Platzhalter, keine TODO-Reste
- [ ] Jede Seite erreichbar, Navigation + Footer verlinken korrekt
- [ ] Genau eine H1 pro Seite, Title + Description individuell
- [ ] Alt-Texte gesetzt; fehlende Assets fallen auf Marken-Platzhalter zurück
- [ ] Mobile: keine horizontalen Scroller, Menü funktioniert, Text lesbar
- [ ] Reduced Motion getestet (Emulation reicht)
- [ ] Interaktionen funktionieren (Formulare validieren, Filter filtern)
- [ ] Fiktive Projekte klar als Demo gekennzeichnet, keine echten Marken
