# skills-and-projects

| Project | What it is |
|---|---|
| [`plate-and-barbell/`](plate-and-barbell/) | Two-person food, nutrition and gym tracker — single-page app with plan, log, trends and CSV export. |

**Plate & Barbell** runs in two places from one source:

- **claude.ai artifact** — <https://claude.ai/artifact/QFgnBt4yFivKUjJo93nJCw> — data in the
  artifact document store, synced across devices and shared between both people.
- **GitHub Pages** — <https://akulamanaswini.github.io/skills-and-projects/> — data in
  `localStorage`, per browser, no sync.

`tools/build-standalone.mjs` wraps the artifact page into `docs/index.html`, which
`.github/workflows/pages.yml` builds and deploys on every push.
