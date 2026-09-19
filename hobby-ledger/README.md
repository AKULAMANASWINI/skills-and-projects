# Hobby Ledger

A ledger for the hours you actually spend on your hobbies. One page, no build
step: `index.html` is the whole application.

Its own look, deliberately not Plate & Barbell's: a cool grey ledger ground,
Bricolage Grotesque headings, Hanken Grotesk body, DM Mono for every number and
label. The chrome is kept quiet — one deep petrol accent, `#0E4552` — so the
hobby inks are the only strong colour on the page.

Two places it runs:

| Where | URL | Storage |
|---|---|---|
| claude.ai artifact | https://claude.ai/artifact/JKUVm3koWQbheqgfrKhJvz | Artifact document store — syncs across your devices |
| GitHub Pages | https://akulamanaswini.github.io/skills-and-projects/hobby-ledger/ | `localStorage` — per browser, no sync |

Same code. The app detects which runtime it is in and says so in a banner.

## What it does

**Today** — the working surface.
- A session timer that survives a reload: the running timer is a stored
  document, not a variable, so closing the tab does not lose it. `Stop & log`
  writes the session immediately rather than staging it in the form.
- Log by hand too: hobby, minutes, start time, how it went (1–5), a note, and —
  if the hobby counts its own thing — pages, kilometres, loaves, whatever.
- Four tiles: logged today, this week, the all-hobby day streak, and how many
  hobbies you have touched, with the one you have neglected longest called out.
- The day's entries, each editable in place, and every weekly goal's progress.

**Hobbies** — one card each: lifetime hours, sessions, weeks running, this
week against the goal, a twelve-week sparkline, and when you last did it. A
hobby untouched for a fortnight is marked **Cold**. Archive rather than delete
when you drift away from something, and the history stays.

**Trends** — 30 / 90 / 365 days.
- Minutes a week, stacked by hobby, with a key you can click to drop a series.
- Where the hours went, direct-labelled.
- Days you showed up: a 52-week consistency grid, filterable to one hobby, each
  cell clickable straight through to that day.
- When you do it: sessions by the hour they started.
- `Show table` swaps the weekly stack for the same numbers as rows, and the
  lifetime table is always there below.

**Milestones** — the long game. Hours banked against 10 / 25 / 50 / 100 / 250 /
500 / 1000 per hobby, with how many more sessions at your usual length it takes
to reach the next one. Longest streak, longest session, biggest week, best day.
Projects — the half marathon, the novel, the table — carry a status and collect
the hours logged against them.

**Settings** — week start, theme, exports, restore, and a way to wipe it.

## Why weeks running, not a day streak

A day streak is the wrong measure for most hobbies. Something you do three
times a week never holds one, so the number reads `0` forever and stops meaning
anything. Each hobby card counts **consecutive weeks carrying at least one
session** instead. The all-hobby day streak still appears on Today and
Milestones, where it does move.

## Chart colour

Series colours are the data-viz skill's validated categorical palette, checked
against this app's own card surfaces rather than the reference ones —
`#FAFBFB` light, `#181F22` dark:

- **Light**: worst adjacent CVD ΔE 9.1, worst adjacent normal-vision ΔE 19.6.
  Three inks (aqua, yellow, magenta) sit under 3:1 against the light card, so
  the relief rule applies and is honoured — a key is always present, the bars
  carry direct labels, and every chart has a table view.
- **Dark**: worst adjacent CVD ΔE 8.4, normal-vision ΔE 19.3, all eight clear
  3:1.

Inks are handed out in fixed order as hobbies are created and never recycled by
rank, so hiding three series in the key does not repaint the rest.

## Data

Stored in the artifact's document store (`db` capability):

```
config/app              week start and other preferences
hobbies/<hid>           one document per hobby, with its projects
sessions/<YYYY-MM>      one document per month, holding that month's sessions
timer/current           the running timer
```

Sessions are bucketed by month rather than stored one document each. The store
caps an artifact at 5,000 documents, and a document per session would spend that
in a couple of years of honest logging; a month document holds roughly 1,500
sessions inside the 256 KiB body limit, which is far past what a month can
physically contain. Opened outside the artifact runtime it falls back to
`localStorage` and says so in a banner.

One row per session is the only thing stored. Streaks, goals, milestones and the
grid are all computed from those rows, so nothing is held twice and an export is
the whole truth.

Exports, from Settings: `hobby-sessions.csv` (one row per session),
`hobby-summary.csv` (one row per hobby), `hobby-weekly.csv` (one row per
hobby-week, with the goal alongside the actual) and a JSON backup that imports
back, merging by id so restoring twice changes nothing. ISO dates, minutes,
snake_case headers. Inside the artifact the file goes through the `downloads`
capability; anywhere else it is an ordinary browser download.

## The example ledger

With nothing logged, the app builds four months of plausible pottery, sewing and
journal-writing sessions so the charts have something to show, labels them in a
banner, and keeps them in memory — they are never written to storage. Those three
take inks 1, 2 and 3, the slots the palette validates on all pairs rather than
only adjacent ones, so with three series every comparison on screen clears the
gates. The first real entry clears them but keeps
the hobbies, since the action that cleared them was almost certainly logging
against one.

## Building the hostable copy

`hobby-ledger/index.html` omits `<!doctype>`, `<html>`, `<head>` and `<body>` —
the artifact runtime supplies them plus a small reset. Anywhere else the page
needs that shell itself, so it is generated:

```sh
node tools/build-standalone.mjs   # -> docs/index.html and docs/hobby-ledger/index.html
```

That output is what GitHub Pages serves, and it opens straight from disk too.
`.github/workflows/build-check.yml` rebuilds both pages on every push and fails
if a committed copy is stale.

Pages serves the tree directly from the branch — **Settings -> Pages -> Source:
"Deploy from a branch", branch `claude/wizardly-noether-2cbh0z`, folder
`/docs`**. That one setting has to be set by hand; see the Plate & Barbell
README for why a workflow-based deploy cannot bootstrap itself.

Edit `hobby-ledger/index.html` — never `docs/hobby-ledger/index.html`, which is
overwritten.
