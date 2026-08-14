# Next.js-Variante: Setup, Fallen, Verifikation

Nur lesen, wenn der Stack Next.js ist (gefordert oder Produktionsprojekt).

## Setup ohne create-next-app

Scaffolde manuell (schneller, deterministischer): `package.json` mit
`next react react-dom` + Dev-Deps `typescript tailwindcss postcss autoprefixer
@types/*`, dazu `tsconfig.json` (Next-Standard mit `@/*`-Pfaden),
`next.config.mjs`, `tailwind.config.ts` (Brand-Farben unter `theme.extend`),
`postcss.config.mjs`, `app/layout.tsx`, `app/globals.css`. App Router
verwenden, eine Route pro Seite (`app/<slug>/page.tsx`).

## Die drei häufigsten Fallen

1. **Server/Client-Grenze:** Alles mit State, Effekten oder Browser-APIs
   bekommt `"use client"`. Aber: Daten/Konstanten NIE aus einer
   Client-Datei in Server-Komponenten importieren – beim Prerendern werden
   solche Importe zu Client-Referenzen und Methodenaufrufe wie `.slice()`
   schlagen fehl ("Attempted to call X from the server"). Gemeinsame Daten
   (Navigation, Inhalte) gehören in eigene datei ohne `"use client"`
   (z. B. `data/nav.ts`), aus der Server- UND Client-Komponenten importieren.
2. **Hydration-Mismatch:** Alles Zeitabhängige (Countdown, Datum) erst nach
   dem Mount berechnen (`useEffect` + State, vorher Platzhalter rendern).
3. **Bilder ohne Garantie:** Wenn Asset-Dateien fehlen können, kein
   `next/image` mit statischem Import, sondern `<img>` in einer
   Client-Komponente mit `onError`-Fallback auf einen gestylten Platzhalter.

## Metadaten

Pro Seite `export const metadata: Metadata` mit `title`, `description`,
`openGraph.images` aus der Asset-Map. Im Root-Layout `metadataBase`,
Title-Template und für Demos `robots: { index: false }`.

## Build-Verifikation

`npm install && npx next build` muss mit Exit 0 durchlaufen und alle Routen
statisch generieren. Typische Fehlerquelle ist Falle 1 – die Fehlermeldung
nennt die Seite, die Ursache ist fast immer ein Import aus einer
Client-Datei. In Sandbox-Umgebungen mit Kommando-Timeouts: Install/Build
detached starten (`setsid -f`) und Log pollen; bei gesperrten
`.next`-Verzeichnissen ein frisches `distDir` setzen oder in `/tmp` bauen.
