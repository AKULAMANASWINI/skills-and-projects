# skills-and-projects

| Project | What it is |
|---|---|
| [`plate-and-barbell/`](plate-and-barbell/) | Two-person food, nutrition and gym tracker — single-page app with plan, log, trends and CSV export. |
| [`hobby-ledger/`](hobby-ledger/) | Hobby time tracker — sessions, streaks, weekly goals, a consistency grid, milestones and CSV export. |

Each project runs in two places from one source: a **claude.ai artifact**, with
data in the artifact document store and synced across devices, and **GitHub
Pages**, with data in `localStorage`, per browser, no sync. Each app detects
which runtime it is in and says so in a banner.

| Project | Artifact | GitHub Pages |
|---|---|---|
| Plate & Barbell | <https://claude.ai/artifact/QFgnBt4yFivKUjJo93nJCw> | <https://akulamanaswini.github.io/skills-and-projects/> |
| Hobby Ledger | <https://claude.ai/artifact/JKUVm3koWQbheqgfrKhJvz> | <https://akulamanaswini.github.io/skills-and-projects/hobby-ledger/> |

`tools/build-standalone.mjs` wraps each artifact page into `docs/`;
`.github/workflows/build-check.yml` fails the build if a committed copy drifts
from its source. Pages serves `/docs` straight from the branch. Plate & Barbell
keeps the root of the site so the URL already handed out stays valid; every
project added since gets its own directory.
