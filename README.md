# skills-and-projects

| Project | What it is |
|---|---|
| [`plate-and-barbell/`](plate-and-barbell/) | Two-person food, nutrition and gym tracker — single-page app with plan, log, trends and CSV export. |
| [`de-foundations/`](de-foundations/) | SQL and Python from zero for the Data & AI Engineering roadmap's Phase 1 — 15 lessons, 60 auto-checked SQL problems, 47 Python tests, and an ingestion capstone against a flaky local API. |

**Plate & Barbell** runs from one source file with three storage backends,
picked at boot:

- **claude.ai artifact** — <https://claude.ai/artifact/QFgnBt4yFivKUjJo93nJCw> — artifact
  document store, synced.
- **Your own domain** — Supabase Postgres behind an email/password login, synced and
  realtime across devices and between both people. See **[SETUP.md](SETUP.md)**.
- **Anywhere else** — `localStorage`, this browser only.

`tools/build-standalone.mjs` wraps the artifact page into `docs/index.html`;
`.github/workflows/build-check.yml` fails if that committed copy drifts from its
source. `supabase/schema.sql` is the database, row-level security included.
