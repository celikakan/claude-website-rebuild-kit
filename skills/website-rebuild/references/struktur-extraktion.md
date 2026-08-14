# Struktur-Extraktion und Selbst-Rekonstruktion der Vorlage

Zweck: Die Vorlage strukturell 1:1 kopieren, nicht aus Tokens nachempfinden.
Anbieterunabhaengig (egal womit die Vorlage gebaut wurde). PRIMAERWEG: selbst
extrahieren und Sektion fuer Sektion nachbauen, ohne externe Hilfsmittel.
SEKUNDAERWEG: fertige Vorlagen-Dateien nutzen, falls der User sie liefert.

## 1. PRIMAERWEG - selbst extrahieren (Standard)
Vorlage im Browser (Chrome-Erweiterung) oeffnen, VOLLSTAENDIG durchscrollen
(Lazy-Sektionen, Scroll-Effekte laden), dann erheben. URLs im Output immer mit
.split("?")[0] kuerzen (sonst Privacy-Filter).

Sektions-Skelett (Tags + Klassen + Grid-Spalten, Tiefe 4):
```js
function skel(el,d,max){ if(!el||d>max)return null;
  const cls=(''+el.className).split(/\s+/).filter(c=>c&&!/^w-/.test(c)).slice(0,3).join('.');
  const g=getComputedStyle(el); const n={el:el.tagName.toLowerCase()+(cls?'.'+cls:'')};
  if(g.display==='grid')n.cols=g.gridTemplateColumns.replace(/px/g,'');
  if(g.display==='flex')n.flex=g.flexDirection;
  const k=[...el.children]; if(k.length&&d<max)n.kids=k.map(x=>skel(x,d+1,max)).filter(Boolean);
  return n; }
JSON.stringify([...document.querySelectorAll('main>section,section,[class*="section"]')].map(s=>skel(s,0,4)));
```

Gemessene Werte je Komponente:
```js
const g=getComputedStyle,P=['fontFamily','fontSize','lineHeight','letterSpacing','textTransform','color'];
const m=(sel,pr)=>{const e=document.querySelector(sel);if(!e)return null;const c=g(e);const o={sel};pr.forEach(p=>o[p]=c[p]);return o;};
JSON.stringify({container:m('[class*="container"]',['maxWidth','paddingLeft']),
 header:m('header,[class*="nav"]',['height','backgroundColor','position','backdropFilter']),
 h1:m('h1',P),h2:m('h2',P),body:m('body',['backgroundColor','fontFamily','color'])});
```

Motion-Stack + Fonts:
```js
JSON.stringify({
 techniques:{smoothScroll:!!window.Lenis||!!window.__lenis, textReveal:!!window.SplitText,
   gsap:!!window.gsap, scrollTrigger:!!(window.gsap&&window.ScrollTrigger)},
 scripts:[...document.scripts].map(s=>s.src.split('?')[0]).filter(Boolean),
 fonts:[...document.fonts].map(f=>f.family).filter((v,i,a)=>a.indexOf(v)===i)});
```
Ablage: artefakte/struktur-map.md (Skelett) + artefakte/spec.md (Werte + Motion
+ Fonts). Danach in Schritt 8 jede Sektion strukturtreu nachbauen: gleiche DOM-
Gliederung, gleiche Spaltenzahl/-rollen, gleicher Motion-Stack (real einbinden
oder gleichwertig nachbauen).

## 2. SEKUNDAERWEG - fertige Dateien (optional)
Wenn der User Vorlagen-Dateien liefern kann (ZIP oder HTML/CSS/JS-Ordner, z. B.
ein Export oder gekauftes Theme): in <projekt>/eingang/vorlage/ ablegen,
entpacken nach artefakte/vorlage-code/, direkt als Bau-Basis nutzen. Das ist
eine Abkuerzung, keine Voraussetzung - ohne Dateien laeuft der Primaerweg.
Grosse Dateien landen ggf. im Downloads-Ordner (kein Sandbox-Zugriff): Zielordner
in Finder oeffnen (computer-use -> Cmd+Shift+G -> Pfad), User zieht sie hinein.

## 3. Demo-/Platzhalter-Listen fuellen
Viele Vorlagen zeigen in Listen/Repeatern nur Demo-Beispiele oder ein leeres
Muster-Item. Diese durch die ECHTEN N Eintraege des Originals im GLEICHEN Karten-
Markup ersetzen; Muster-/Leer-Item und "No items"-Reste entfernen. Keine leeren
Platzhalter stehen lassen.

## 4. Sprach-/Typo-Guard (Pflicht bei DE u. langen Woertern)
Zerlegt die Vorlage Headlines fuer Text-Reveal-Animationen, brechen lange
Woerter mitten im Wort. Gegenmittel als CSS-Override:
.section-title,.hero-title{overflow-wrap:normal;word-break:keep-all;hyphens:none;
text-wrap:balance;font-size:clamp(28px,3.6vw,56px)!important}
Immer das LAENGSTE Wort jeder grossen Headline gegen die Spaltenbreite testen.

## 5. Verifikation (nach JEDER Sektion, nicht erst am Ende)
- Lokale Datei rendern: Finder -> Rechtsklick -> "Oeffnen mit" -> Browser (der
  Standard-Handler fuer .html ist oft ein Editor). Dann computer-use Screenshot.
- Die Chrome-Erweiterung kann keine file://-Seiten oeffnen (Navigate haengt
  https:// davor). Fuer Scroll/Interaktion: Playwright headless
  (pip install playwright --break-system-packages && playwright install chromium)
  auf die lokale Datei; Motion-Libraries brauchen ggf. Netz, sonst lokal vendorn.
- Pruefen: Container-Breite, Header, Typo-Skala, Sektions-Struktur, Motion und
  IMMER die Textanordnung (keine Mitten-Wort-Umbrueche, keine Ueberlaeufe).
- Gegen die Vorlage nebeneinander vergleichen, Abweichungen fixen statt
  begruenden.

## 6. Unterseiten der Vorlage + Text-Inventar (Pflicht in beiden Wegen)
ALLE Unterseiten der Vorlage erfassen: Navigation, Footer, Sitemap durchgehen,
jede Seite oeffnen und vollstaendig durchscrollen. Ergebnis:
artefakte/vorlagen-seitenliste.md (URL, Zweck/Thema, Sektions-Typen je Seite).
Skelett-/Werte-/Motion-Erhebung (Abschnitt 1) fuer JEDEN Seitentyp wiederholen.

Text-Inventar je Seite sichern (Basis des Leak-Scans):
```js
JSON.stringify({url:location.href.split('?')[0],
 title:document.title,
 text:document.body.innerText,
 alts:[...document.images].map(i=>i.alt).filter(Boolean),
 metas:[...document.querySelectorAll('meta[name="description"],meta[property^="og:"]')]
   .map(m=>m.content).filter(Boolean)});
```
Ablage: artefakte/vorlagen-text-inventar/<seite>.txt (Rohtext genuegt).

## 7. Leak-Scan: kein Vorlagen-Text im Ergebnis (Blocker)
Nach JEDER gebauten Seite (Schritt 8) und einmal komplett in der QA
(Schritt 9). Prinzip: alle Wortfolgen ab 4 Woertern aus dem Vorlagen-
Text-Inventar duerfen NICHT in website/ vorkommen (sichtbarer Text UND
title/meta/alt/og-Attribute). Referenz-Implementierung:
```python
import re, pathlib, html, json
def norm(t): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',t)).lower()
def grams(t,n=4):
    w=re.findall(r'[a-z0-9äöüß]+',norm(t))
    return {' '.join(w[i:i+n]) for i in range(len(w)-n+1)}
inv=set()
for f in pathlib.Path('artefakte/vorlagen-text-inventar').glob('*'):
    inv|=grams(f.read_text(errors='ignore'))
hits=[]
for f in pathlib.Path('website').rglob('*.html'):
    src=f.read_text(errors='ignore')
    for g in grams(src)&inv: hits.append((str(f),g))
print(json.dumps(hits[:50],ensure_ascii=False), 'TREFFER:',len(hits))
```
Erwartung: TREFFER: 0. Ausnahmen gibt es nur fuer Texte, die zwangslaeufig
identisch sind (z. B. gemeinsame Ortsnamen, generische Rechtsbegriffe) -
jede Ausnahme wird einzeln geprueft und im QA-Bericht begruendet. Eigene
Marken-/Ortsnamen der Vorlage sind NIE eine Ausnahme.

## 8. Vorlagen-Seiten ohne Original-Pendant
Jede Vorlagen-Seite hat im seitenplan.md genau einen Zustand: GEFUELLT,
UMGEWIDMET oder GESTRICHEN. Beim Bauen heisst das: Seiten ohne Plan-Eintrag
loeschen (inkl. Nav-/Footer-Links), umgewidmete Seiten komplett mit dem
freigegebenen NEU-Inhalt befuellen. Eine Vorlagen-Seite, die "einfach
mitkommt", ist ein Fehler - egal wie huebsch sie ist.
