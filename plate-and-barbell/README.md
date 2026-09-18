# Plate & Barbell

A two-person food and training log. One page, no build step: `index.html` is the
whole application.

Live (private to the owner's account): https://claude.ai/artifact/QFgnBt4yFivKUjJo93nJCw

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

**Plan** — a weekly training split and a weekly meal plan per person, both
editable. `Use plan` on a meal drops the planned foods straight into the log.

**Trends** — 14 / 30 / 90 days: calories against target, macro stack, body weight
(both people overlaid), volume by muscle group, and a consistency grid. A `Table`
toggle shows the same numbers as rows.

**Library** — the food table (per 100 g) and the exercise table, plus your own
additions.

**Settings** — per person: sex, age, height, weight, activity, goal. Targets come
from Mifflin-St Jeor → TDEE → goal adjustment → 1.8–2.0 g/kg protein, 25% fat,
carbs as the remainder; override any of them manually.

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

## Running it locally

The published page omits `<!doctype>`, `<html>`, `<head>` and `<body>` — the
artifact runtime supplies them. To open it in a browser directly, wrap it:

```sh
{ printf '<!doctype html><html><head><meta charset="utf-8">'
  printf '<meta name="viewport" content="width=device-width,initial-scale=1">'
  printf '</head><body>'; cat index.html; printf '</body></html>'; } > preview.html
```

`window.claude` is absent there, so it runs on `localStorage`.
