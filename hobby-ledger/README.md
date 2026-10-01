# Hobby Ledger

A ledger for the hours you actually spend on your hobbies. One page, no build
step: `index.html` is the whole application.

## The look

All three hobbies this was built around — pottery, sewing, journal writing — are
handwork, so the page takes its cues from the bench rather than the office.

**Indigo and oat.** The ground is oat `#E7E5DF`, the ink indigo-black `#1A1B2E`,
the structural accent a deep indigo `#2A2E6E`; dark mode is a near-black indigo
`#101124` with a periwinkle accent. Indigo because it is the dyer's and the
writer's colour, and because it sits far enough from every hobby ink to read as
structure rather than data. The chrome stays quiet so the inks are the only
strong colour on the page.

**The ground is woven.** A one-pixel warp every 4px and weft every 7px, at the
edge of visibility — different pitches, the way real cloth is, so it reads as
texture and never as a grid you might measure against. The consistency grid
carries the same weave, so untouched days look like bare cloth and logged ones
like dye taken up.

**Type.** Bricolage Grotesque for headings, Hanken Grotesk for body, DM Mono for
every number and label — deliberately not Plate & Barbell's Fraunces/Work
Sans/Space Mono, so the two read as siblings rather than clones. Hero figures
are set in the mono, never the display face.

**Today opens on the day's thread.** One segment per session, in that hobby's
ink, carrying a warp texture, laid in a track. Its length is measured against a
four-hour day rather than against the day's own total — normalising to itself
would draw a full bar for a ten-minute morning, which reads as "done". The rule
across the top of the hero is the hobby inks themselves, in order.

**Motion that knows when to stay still.** The view is rebuilt on every
interaction, so an unconditional entrance animation would re-animate the page
every time you touched a control. `animateNext` is raised only on arrival —
boot, a tab change, a different day — so cards rise, meters sweep, bars grow and
the day's figure counts up when you get somewhere new, and nothing moves at all
while you are typing into a form. All of it is behind
`prefers-reduced-motion: no-preference`, and the count-up falls straight to the
final value whenever it is skipped, so a figure is never left wrong.

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
Projects — the dinner set, the linen shirt, the book — carry a credit, a status
and a finish date, and collect the hours logged against them.

**Settings** — week start, theme, exports, restore, and a way to wipe it.

## Books are projects with an author

A book being read is exactly what a project already is: a named thing a hobby
works through over many sessions. So rather than bolt on a separate reading
list, a project carries a **by** — the author of a book, the designer of a
sewing pattern, whoever's form a pot copies — and the vocabulary follows the
hobby's category:

| Hobby category | The thing | The credit | Statuses |
|---|---|---|---|
| Reading | Book | Author | To read · Reading · Finished · Abandoned |
| Everything else | Project | By | Idea · In progress · Finished · Shelved |

`Reading` and `Writing` are separate categories for this reason — a journal
volume is not a book with an author. A hobby saved under the old combined
`words` category migrates to `Writing` on load.

Finishing something sets a date you can edit, so a book finished last week can
be logged today. Attach sessions to a book and its hours, session count and
first/last dates all accrue to it; `hobby-projects.csv` is the reading log as a
table. The board is reachable before anything is logged — you line up what you
are going to read before you have read any of it.

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

- **Light** (`#F7F6F2`): worst adjacent CVD ΔE 9.1, worst adjacent
  normal-vision ΔE 19.6. Four inks (orange, aqua, yellow, magenta) sit under
  3:1 against the oat card, so the relief rule applies and is honoured — a key
  is always present, the bars carry direct labels, and every chart has a table
  view.
- **Dark** (`#1A1C32`): worst adjacent CVD ΔE 8.4, normal-vision ΔE 19.3, all
  eight clear 3:1.

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

Exports, from Settings: `hobby-sessions.csv` (one row per session, carrying the
book or project and its author), `hobby-summary.csv` (one row per hobby),
`hobby-weekly.csv` (one row per hobby-week, with the goal alongside the actual),
`hobby-projects.csv` (one row per book or project, with credit, status, finish
date and the hours logged against it) and a JSON backup that imports back,
merging by id so restoring twice changes nothing. ISO dates, minutes,
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
