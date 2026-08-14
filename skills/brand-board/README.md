# Brand Board Loop

Wiederverwendbarer Skill, der aus **Kundenwebseite + Kundendokumenten** ein professionelles Brand Board (HTML) baut und in frischem Kontext blind gegenpruefen laesst. Branchenunabhaengig. Adaption von The Design Loop (Gauntlet Loop, Matt Shumer).

## Inhalt
```
brand-board/
  SKILL.md                        Kern, die 4-Phasen-Loop
  README.md                       diese Datei
  assets/
    brand-board-template.html     ausfuellbares Board, Output pro Kunde
    brand-dna.template.md         Scaffold fuer die Extraktion (Phase 3)
    bar.example.md                Beispiel-Teardown, zeigt Mechanismus-Format
```

## Installation
Ordner liegt unter `~/.claude/skills/brand-board/`, damit global in jedem Projekt verfuegbar. Fuer projektlokal stattdessen nach `.claude/skills/brand-board/` kopieren.

## Nutzung
```
/brand-board
```
Dann drei Fragen beantworten:
1. Website-URL (+ markenstarke Subpages)
2. Dokumentpfade (PDF, Word, Logo, bestehende Guidelines) oder "keine"
3. Optional Referenz-Board als Qualitaets-Bar, sonst "skip"

Der Skill:
1. **Intake** , die zwei Inputs + optionaler Bar
2. **Preflight** , Website screenshoten, Dokumente lesen, Render bestaetigen
3. **Extraction** , Brand-DNA nach `brand-dna.md` (aus `brand-dna.template.md`), Referenz nach `bar.md`
4. **Loop** , Builder fuellt `brand-board-template.html`, drei Blind-Critics pro Sektion bis alle passen

Output: ein self-contained `brand-board.html` pro Kunde, druckt sauber als PDF.

## Die drei Critics
| Critic | Prueft gegen | Modell |
|---|---|---|
| Brief | echte Quellen (Website + Docs), Genauigkeit | Sonnet |
| System | brand-dna.md, exakte HEX/Fonts/Logo | Haiku |
| Craft | bar.md + gerendertes Board, nie den Code | staerkstes verfuegbares |

## Kosten
Fuer echte Kunden-Deliverables, nicht fuer Quick-Mockups. Jede Runde = Build + drei Judgments, token-hungrig. Bremsen: Sektionen auf 3-4 cappen, zusehen und stoppen, Wochenlimit als harte Grenze.

## Kernregel
Ein Critic, der Speicher mit dem Builder teilt, benotet seine eigene Hausaufgabe. Deshalb frischer Kontext pro Critic. Alles andere ist Detail.
