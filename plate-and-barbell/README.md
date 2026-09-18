# Plate & Barbell

Madhu and Aravind's food and training log. One page, no build step: `index.html`
is the whole application.

Styled to the couple's 12-week plan document: bone ground, Fraunces headings,
Work Sans body, Space Mono for every label and number, moss green structure with
coral for Madhu and teal for Aravind. Square-cornered bordered cards, a 3px
left rule for person identity, and hairline `--line` separators throughout.

Two places it runs:

| Where | URL | Storage |
|---|---|---|
| claude.ai artifact | https://claude.ai/artifact/QFgnBt4yFivKUjJo93nJCw | Artifact document store — syncs across devices and between both people |
| GitHub Pages | https://akulamanaswini.github.io/skills-and-projects/ | `localStorage` — per browser, no sync |

Same code. The app detects which runtime it is in and says so in a banner.

## What it does

**Today** — the day's plate and the day's session, side by side.
- Calorie ring and macro bars against targets. Protein and fibre are treated as
  floors (green tick when cleared); calories, carbs and fat as ceilings (red when
  exceeded).
- Meals split into breakfast / lunch / dinner / snacks. Search 80+ foods with
  per-100 g macros, one-tap portions (`1 roti`, `½ cup`), or type a one-off entry.
- Training: exercises with per-set reps × weight, a done toggle, running volume,
  estimated 1RM (Epley) and an automatic PR badge when a set beats every earlier
  session. Cardio logs minutes, distance and a MET-based calorie estimate.
- `Load <session>` pulls the day's planned session in, pre-filled with last
  session's loads. `Repeat last session` copies the previous workout.
- Bar-loading calculator using IWF competition plate colours.
- Water, body weight and steps.

**Plan** — the Mon / Wed / Fri / Sun split (Lower + Core, Upper Push, Upper Pull,
Conditioning) built from the gym's own kit: squat rack, cable machine, assisted
pull-up/dip station, kettlebells, TRX, RowErg, Peloton, elliptical, treadmills.
Rest days carry the 10,000-step target. Alongside it a weekly meal plan per
person, each day showing planned calories against that person's target so a
mismatch is visible. `Use plan` on a meal drops the planned foods into the log.

**Trends** — 14 / 30 / 90 days: calories against target, macro stack, body weight
(both people overlaid), volume by muscle group, and a consistency grid. A `Table`
toggle shows the same numbers as rows.

**Library** — the food table (per 100 g) and the exercise table, plus your own
additions.

**Settings** — per person: sex, age, height, weight, activity, goal. Madhu is set
to 4'10" / 58.5 kg on a fat-loss target, Aravind to 5'11" / 79 kg on a lean-gain
target; ages are starter values. Targets come
from Mifflin-St Jeor → TDEE → goal adjustment → 1.8–2.0 g/kg protein, 25% fat,
carbs as the remainder; override any of them manually.

## Chart colour

Series colours were re-stepped into the plan's own family and validated against
the bone card surface with the data-viz validator: light `#C4562F / #008C81 /
#7B4F9B` passes lightness, chroma, CVD separation, normal-vision separation and
contrast on all pairs. The dark steps `#D2703F / #1F9E92 / #9A80C4` pass every
gate with CVD separation in the 6–8 warn band, which the always-present legend,
the 2px gaps between stacked segments and the table view cover.

## Data

Stored in the artifact's document store (`db` capability), shared across the
owner's devices:

```
config/app                      units, active profile
library/custom                  your own foods and exercises
profiles/<pid>                  person, targets, training plan, meal plan
profiles/<pid>/days/<YYYY-MM-DD>  one document per person per day
```

One document per person per day keeps the store well inside the 5,000-document
cap (~730/year for two people). Opened outside the artifact runtime it falls back
to `localStorage` and says so in a banner.

Exports, from Settings: `nutrition-log.csv` (one row per food entry),
`training-log.csv` (one row per set), `daily-summary.csv` (one row per person-day,
with targets alongside actuals) and a full JSON backup that imports back. ISO
dates, metric units, snake_case headers.

## Building the hostable copy

`plate-and-barbell/index.html` omits `<!doctype>`, `<html>`, `<head>` and
`<body>` — the artifact runtime supplies them plus a small reset. Anywhere else
the page needs that shell itself, so it is generated:

```sh
node tools/build-standalone.mjs   # -> docs/index.html
```

That output is what GitHub Pages serves, and it opens straight from disk too.
`.github/workflows/build-check.yml` rebuilds it on every push and fails if the
committed copy is stale.

Pages serves it directly from the branch — **Settings -> Pages -> Source:
"Deploy from a branch", branch `claude/wizardly-noether-2cbh0z`, folder
`/docs`**. That one setting has to be set by hand: a workflow-based deploy
cannot bootstrap itself, because `GITHUB_TOKEN` may deploy to Pages but may not
create the Pages site, so `actions/configure-pages` with `enablement: true`
fails with `Resource not accessible by integration` until Pages exists.

Edit `plate-and-barbell/index.html` — never `docs/index.html`, which is
overwritten.
