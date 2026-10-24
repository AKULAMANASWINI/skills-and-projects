# 08 — Linux, Bash and Git for data teams

Roadmap item: *shell pipelines, cron, file permissions, SSH, branching strategy,
conventional commits, PR review etiquette*. Do this **in week 1 alongside Python 01**,
15–20 minutes a day — it's practice, not study. Windows: install WSL (Ubuntu) or use
Git Bash.

## Navigating

```bash
pwd                         # where am I
ls -la                      # list, including hidden, with permissions
cd de-foundations ; cd ..   # into / up
mkdir -p data/clean         # make folders (and parents)
cp a b ; mv a b ; rm a      # copy, move/rename, delete (no recycle bin!)
cat f ; less f ; head -n 5 f ; tail -f log.txt   # read files; tail -f follows a growing log
```

## Shell pipelines — the original data pipeline

Each command reads input, writes output; `|` connects them.

```bash
wc -l data/raw/customers_export.csv                                    # count lines
cut -d, -f4 data/raw/customers_export.csv | sort | uniq -c | sort -rn  # value counts of column 4
grep -c "N/A" data/raw/customers_export.csv                            # rows containing N/A
python sql/run.py "SELECT status FROM orders" | sort | uniq -c
command > out.txt     # overwrite;   >> appends;   2> errors only
```

Exploring a 5 GB file with `head`, `wc -l`, `grep` before loading it anywhere is a
real, daily skill.

## Permissions

`ls -l` shows `-rwxr-x---`: owner / group / others × read, write, execute.

```bash
chmod +x run_pipeline.sh     # make a script executable
chmod 600 ~/.ssh/id_ed25519  # private key: only you can read — ssh refuses otherwise
```

## Scripts and cron

```bash
#!/usr/bin/env bash
set -euo pipefail            # stop on error, on unset variables, on failures inside pipes
cd "$(dirname "$0")"
python ingest.py --date "$(date +%F)" >> logs/ingest.log 2>&1
```

`crontab -e` schedules it. Format: `minute hour day month weekday command`.

```
15 2 * * *  /home/me/pipeline/run_pipeline.sh     # 02:15 every day
```

Cron is the ancestor of Airflow (Phase 2). Knowing its limits — no retries, no
dependencies, no backfills, silent failures — is exactly why orchestrators exist.

## SSH

```bash
ssh-keygen -t ed25519 -C "you@example.com"   # key pair: private stays, .pub is shared
ssh user@server                               # log into a remote machine
scp file.csv user@server:/data/               # copy over ssh
```

Add the `.pub` key to GitHub (Settings → SSH keys) to push without passwords.

## Git

```bash
git clone <url>
git status                         # ALWAYS before committing
git switch -c feat/clean-customers # new branch per change
git add path/to/file               # stage (prefer specific files over "git add .")
git commit -m "feat: clean customer export dates and emails"
git push -u origin feat/clean-customers
git pull --rebase                  # update from remote
git log --oneline --graph
git diff ; git diff --staged
```

**Branching strategy:** `main` is always deployable. Short-lived feature branches,
merged by pull request after review. (GitFlow with develop/release branches exists;
most data teams use this simpler "trunk-based" style.)

**Conventional commits:** `type: what changed`, imperative mood.
`feat:` new behaviour, `fix:` bug fix, `refactor:`, `test:`, `docs:`, `chore:`.
`fix: handle N/A lifetime value in customer export` — not `"updates"` or `"final v2"`.

Never commit: secrets/passwords/API keys, `.venv/`, large data files. Use `.gitignore`.

**PR etiquette:**
- Small PRs (< 400 lines) get real reviews; huge ones get rubber stamps.
- Description says *what*, *why*, and *how you tested it* (paste row counts!).
- As reviewer: ask questions ("what happens if amount is NULL here?"), distinguish
  blocking from nit, review within a day.
- Don't take comments personally; don't leave them unanswered either.

## Tasks

1. Put this `de-foundations` folder in your own GitHub repo. Commit your exercise
   answers daily with conventional commit messages — your commit graph becomes
   evidence of consistent work.
2. Do every new exercise set on its own branch and merge it through a PR to yourself.
3. Write `run_checks.sh` that runs the SQL and Python checkers and appends the
   summary with a timestamp to `logs/progress.log`. Schedule it with cron (or Task
   Scheduler on Windows) for 21:00 daily.
4. Using only shell commands, find how many rows in `customers_export.csv` have an
   empty email.
