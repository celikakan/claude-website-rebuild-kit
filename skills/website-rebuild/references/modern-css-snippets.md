# Moderne CSS-Snippets im Rebuild — Einsatz-Matrix

Kurzreferenz für Schritt 8 (Build). Regelt, welche modernen CSS-Features im
Rebuild IMMER, BEDINGT oder NIE eingesetzt werden. Grundsatz aus Kernregel 0/1:
Die Vorlage ist gesetzt — diese Snippets liefern Umsetzungsqualität, treffen
keine Designentscheidungen.

## IMMER (reine Umsetzungsqualität, visuell vorlagentreu)

### 1. Dynamische Viewport-Höhe — Full-Height-Sektionen

```css
.hero {
  min-height: 100dvh; /* statt 100vh */
}
```

`dvh` passt sich an ein-/ausblendende Browser-UI an (mobile Adressleiste).
Desktop-Rendering identisch zur Vorlage, mobil robuster. Bei jeder
Full-Height-Sektion verwenden, auch wenn die Vorlage `100vh` nutzt.

### 2. Zeilenumbruch-Balance — Teil des Typo-Guards (Schritt 8.5)

```css
.section-title, .hero-title {
  text-wrap: balance;
}
```

Bereits Pflicht im Sprach-/Typo-Guard (zusammen mit `overflow-wrap:normal;
word-break:keep-all;hyphens:none`). Hier nur zur Vollständigkeit.

### 3. Seitenverhältnis für Medien-Slots

```css
.card img {
  aspect-ratio: 1;      /* Wert aus der Vorlage MESSEN, nicht raten */
  object-fit: cover;
}
```

Löst das Kernproblem des Medien-Tauschs: Original-Bilder haben andere Maße
als die Vorlagen-Bilder. Das gemessene `aspect-ratio` der Vorlagen-Slots
hält die Slot-Geometrie stabil (Vorlagentreue) und verhindert Layout-Shifts
(CLS-Budget der QA). Gehört als Messwert in spec.md (Schritt 3).

## BEDINGT (nur mit Leitplanke)

### 4. Fluide Schriftgrößen mit clamp()

```css
font-size: clamp(2.4rem, 7vw, 5.5rem); /* min, bevorzugt, max */
```

- ERLAUBT als Typo-Guard-Cap (Schritt 8.5): Maximum so wählen, dass das
  längste Wort in seine Spalte passt.
- ERLAUBT, wenn die Vorlage selbst fluide Typo nutzt (in spec.md gemessen).
- NICHT als genereller Ersatz fester, gemessener Vorlagen-Größen — exakte
  Werte aus spec.md haben Vorrang.

### 5. Scrollgesteuerte Animationen (CSS-only)

```css
.card {
  animation: fadeUp linear;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(50px) scale(0.8); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
```

- ERLAUBT als Umsetzungs-Technik für Scroll-Motion, die die VORLAGE hat —
  aber NUR mit `@supports (animation-timeline: view()) {}`-Wrapper plus
  gleichwertigem Fallback (Safari!). Ohne Fallback bricht "Motion 1:1 auf
  allen Geräten" (Kernregel 0).
- NIE als stiller Ersatz des echten Vorlagen-Motion-Stacks (GSAP, IX3, Lenis
  … werden real eingebunden, Schritt 8.3).
- Als NEUE Animation ausschließlich über den Animations-Plan +
  Gate-Freigabe (Schritt 7).

### 6. Auto-responsives Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
```

- ERLAUBT, wenn die Vorlage selbst so baut (struktur-map) ODER das
  Responsive-Verhalten der Vorlage nicht messbar war (Fallback, in der
  Übergabe-Doku vermerken).
- SONST: gemessene Spaltenzahl + echte Breakpoints der Vorlage exakt
  nachbauen — auto-fit verhält sich beim Umbruch anders als feste
  Breakpoints.

## NIE proaktiv (Designentscheidungen — nur wenn die Vorlage sie hat)

### 7. Gradient-Text

```css
background: linear-gradient(135deg, #0f172a 0%, #2563eb 35%, #7c3aed 70%, #06b6d4 100%);
background-clip: text;
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

### 8. Neumorphismus-Schatten

```css
box-shadow: 10px 10px 20px rgba(163, 177, 198, .6),
  -10px -10px 20px rgba(255, 255, 255, .9);
```

Beide verändern die Optik gegenüber der Vorlage (Kernregel 0: keine Features,
die die Vorlage nicht hat). Nutzt die VORLAGE einen dieser Effekte, kommt er
automatisch aus der Struktur-Extraktion (Schritt 3) mit den dort gemessenen
Werten — dann die Snippets oben als Umsetzungshilfe verwenden (Gradient-Text
immer mit Standard- UND `-webkit-`-Property).
