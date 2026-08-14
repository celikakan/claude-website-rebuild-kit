---
name: brand-board
description: Builds a professional Brand Board for any client from two fixed inputs, the client website and client documents (fonts, logos, PDF/Word). Extracts the brand DNA (colors, typography, logo, imagery, tone) into brand-dna.md, then runs a builder plus three fresh-context blind critics on every section until all three agree the board is accurate and looks professional. Industry agnostic. Triggers on "/brand-board", "brand board", "erstelle Brand Board", "Design Board fuer Kunden", "brand board loop".
---

# Brand Board Loop

Turns a client website plus client documents into a rendered HTML Brand Board, then judges it in fresh contexts that never saw it being built. Adapted from The Design Loop (Gauntlet Loop, Matt Shumer). The judge must never share memory with the builder.

The two inputs are always the same, no matter the industry:
1. The client website (live URL)
2. Client documents (PDF, Word, brand files) carrying fonts, logos, colors, claims

Everything the board contains is derived from those two sources. Do not invent brand attributes the sources do not support.

Four phases: intake, preflight, extraction, loop. Do not skip ahead. Do not build the board during phases 1 to 3.

## Phase 1: Intake

Ask exactly these three, together, then stop and wait.

1. Client website URL, and any subpages that carry the brand best (about, product, imprint).
2. Which documents should I work from? Give paths to PDFs, Word files, logo files, existing brand guidelines. If none exist, say none, I will pull everything from the site.
3. Optional: name a brand board you consider excellent, a page or an image I can open, as the quality bar. If nothing comes to mind, say skip and I will propose three.

If the reference bar is vague ("a clean brand board"), push once for a specific example. A vague bar is the number one reason the loop approves weak work on round one. If they say skip, propose three concrete reference boards, one line each on why, and wait. No answer, take the strongest.

## Phase 2: Preflight

A check, not a question. Run it before any work and report in one block.

- Fetch the website now. Screenshot the homepage and the named subpages. If blocked, say so and ask for another entry point.
- Read every named document. Extract raw material only at this stage: embedded font names, logo files, color values, taglines, imagery.
- Confirm you can render the board output as a screenshot. No render means no craft critic.
- Confirm any generation tools the board needs are connected (only if the client has no usable logo or imagery and assets must be generated).

Then print: what is available, what is missing, and which critic goes blind if something is missing. Never carry on quietly with a critic that cannot see.

## Phase 3: Extraction (Brand DNA)

Read the two sources properly and write the brand DNA to `brand-dna.md`, starting from the scaffold `assets/brand-dna.template.md`. This file replaces the pre made design system, it is built from the client, not assumed. Capture only what the sources actually show:

- **Logo**: primary logo, variants found, file formats available, clear space if documented, smallest safe size.
- **Colors**: every color pulled from site CSS and documents. Record HEX, and RGB. Mark one primary, supporting colors, neutrals. Note where each is used.
- **Typography**: exact font families found in the site stylesheet and documents. Headline font, body font, weights in use, observed size relationships (for example headline about 4x body).
- **Imagery**: photography or illustration style observed (subject, treatment, crop, color grade). One line, checkable, not "nice photos".
- **Tone of voice**: three to five adjectives evidenced by real copy from the site or docs, each with a short quote as proof.
- **Graphic elements**: shapes, icons, patterns, borders, corner radius, shadow style actually present.

Every line must be checkable by looking at the source. Show `brand-dna.md` to the user before continuing. Flag gaps openly (for example "no CMYK found, print values not confirmed").

Then write `bar.md`: 5 to 7 mechanisms that make a brand board look professional, torn down from the reference bar. See `assets/bar.example.md` for the required format. Mechanisms, not adjectives.

Useless: feels premium, clean layout, good hierarchy.
Checkable:
- color swatches sit in one aligned row, equal size, HEX label under each
- exactly two type specimens, headline and body, shown at real display size
- one accent color, used at most twice on the whole board
- logo shown on both light and dark ground
- generous margin, board content uses at most 80% of the frame width

Show `bar.md` to the user before continuing.

## Phase 4: Loop

Split the board into the smallest sections that can be built and judged on their own. Standard sections: logo, color palette, typography, imagery, tone of voice, application. Keep it to three or four sections per round unless told otherwise, because every extra section multiplies the run.

Start from `assets/brand-board-template.html`. Fill the CSS variables and section content from `brand-dna.md`. Never leave placeholder tokens in a section a critic will judge.

For each section: fan out a builder, then three critics, each with fresh context and no knowledge of how the builder worked.

- **Brief critic** judges accuracy against the two sources only. Does the board represent this client truthfully? Are the colors, fonts, logo the real ones from the site and documents, not invented? Ignore aesthetics.
- **System critic** judges against `brand-dna.md` only. Mechanical adherence: exact HEX values, exact font families, correct logo variants. No drift from the extracted DNA.
- **Craft critic** judges against `bar.md` and the rendered screenshot only. Put the board next to the reference blind, labels stripped, say which looks more professional, name the single biggest gap. Never reads the HTML.

Write each critic brief yourself, adapted to the section. A logo section and a tone section are not judged the same way.

Rules:
- Critics are harsh. Praise is not useful.
- Critics judge rendered output, never the code. Reading the HTML makes a critic grade intent instead of result.
- Binary verdicts, not scores. Scores drift upward every round.
- All three must pass. Any fail goes back to the builder with the single biggest gap named.
- No fixed round count. The exit is winning, or the user stopping the run.

Keep a live progress note updating as work evolves: section status, each critic verdict, gap history, round count.

Final output: one self contained `brand-board.html` per client (all CSS inline, fonts and logo embedded or linked, prints clean to PDF).

## Model tiering (critics)

| Critic | Judges against | Model | Why |
| --- | --- | --- | --- |
| Brief | The two client sources only | Sonnet | Accuracy check, light vision |
| System | brand-dna.md only | Haiku | Mechanical value matching |
| Craft | bar.md and rendered board, never the code | Strongest available | Never downgrade. A cheap craft critic approves everything and the loop dies on round one. |

## Cost

Reserve this for the real client deliverable, not a quick mockup. Every round is a build plus three judgments, it is token hungry. Controls, in order of what works:
- Watch it and stop it. You are the brake.
- Cap sections to three or four, not rounds.
- Let your weekly limit be the hard stop.

There is no reliable self reported token cost. Show round count and section status instead.

## What breaks this

- A vague quality bar. By far the most common failure.
- Inventing brand attributes the website and documents do not support.
- The builder judging its own work. Critics need fresh context.
- A soft craft critic. Binary job, not a score.
- A fixed round count. The exit is winning.
- Over specifying. Every extra instruction is one fewer decision the model makes with its own judgment.

The one thing to remember: a critic that shares memory with the builder is grading its own homework. Everything else is detail.
