# Putting Plate & Barbell on your own domain

End state: `https://yourdomain.com` serves the app, both of you sign in, and one
shared log follows you across every device.

Everything here is free except the domain (~$10–12/year at cost from Cloudflare).
Budget about 40 minutes the first time.

The app picks its storage at boot, so the same file works three ways:

| Where it runs | Storage | Login |
|---|---|---|
| claude.ai artifact | artifact document store | claude.ai account |
| **your domain** | **your Supabase Postgres** | **email + password** |
| opened from disk, or unconfigured | `localStorage` | none |

---

## 1. Create the database (~10 min)

1. Sign up at <https://supabase.com> and create a project. Any region near you;
   the free tier is plenty (500 MB — this app uses a few MB a year).
2. Save the database password it gives you somewhere safe. You will not need it
   for the app, but you cannot recover it later.
3. Open **SQL Editor** → **New query**.
4. Paste the whole of [`supabase/schema.sql`](supabase/schema.sql), but **first
   edit the last block** — replace `madhu@example.com` and `aravind@example.com`
   with the two real addresses. Only addresses in that table can read or write
   anything.
5. Run it. It creates the tables, the row-level security policies, and turns on
   realtime so one phone updates while the other is logging.

## 2. Close the door behind you (~2 min)

**Authentication** → **Sign In / Providers**:

- Turn **off** "Allow new users to sign up". There is no public sign-up for this
  app; you create both accounts by hand.
- Leave **Email** enabled. You can turn off "Confirm email" — you are creating
  the accounts yourself, so there is nothing to confirm.

The allowlist in step 1 already blocks strangers even if this toggle is wrong.
This step means they cannot create an account at all. Do both.

## 3. Create the two accounts (~3 min)

**Authentication** → **Users** → **Add user** → **Create new user**, twice:

- Madhu's email + a password
- Aravind's email + a password

Use the same addresses as the allowlist. Put the passwords in a password
manager — there is no "forgot password" email flow set up, so resets happen
here in the dashboard.

## 4. Point the app at it (~3 min)

**Project Settings** → **API**, copy two values:

- **Project URL** — looks like `https://abcdefgh.supabase.co`
- **anon / public** key — a long `eyJ…` string

Put them in [`docs/config.js`](docs/config.js), replacing the placeholders, then
commit and push.

The anon key belongs in public code — it names the project, it does not grant
access. Row-level security decides who reads what. **Never** put the
`service_role` key here: that one bypasses every policy.

## 5. Buy the domain (~5 min)

Cloudflare sells domains at wholesale with WHOIS privacy included:
**Domain Registration** → **Register Domains** in the Cloudflare dashboard.

A `.com` runs about $10–12/year. Nothing else on this list costs money.

## 6. Deploy it (~10 min)

Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
**Connect to Git** → pick `skills-and-projects`.

| Setting | Value |
|---|---|
| Production branch | `claude/wizardly-noether-2cbh0z` |
| Framework preset | None |
| Build command | `node tools/build-standalone.mjs` |
| Build output directory | `docs` |

Save and deploy. You get a `*.pages.dev` URL within a minute — check the app
loads and the sign-in screen appears before moving on.

Then **Custom domains** → **Set up a domain** → your domain. If you bought it
through Cloudflare, DNS is configured for you and HTTPS is automatic.

## 7. Tell Supabase the address (~1 min)

**Authentication** → **URL Configuration** → set **Site URL** to
`https://yourdomain.com`. Add the `*.pages.dev` URL under **Redirect URLs** too
if you want to keep using it for testing.

## 8. Move your data across (~2 min)

If you have been logging in the artifact:

1. Artifact → **Settings** → **Full backup (JSON)** → save the file.
2. Your domain → sign in → **Settings** → **Import backup** → pick that file.

Import writes every day, profile and custom food into Supabase, so both of you
see it immediately.

---

## Checking it actually works

- Sign in on a laptop, log something, then sign in on a phone. The entry should
  be there, and appear live if both are open.
- Sign in with an address that is *not* on the allowlist (make a throwaway user
  if you disabled sign-ups — or just trust step 1). The app signs you straight
  back out with "That account is not on the allowlist for this log."
- Open the site in a private window without signing in. You should see the
  sign-in screen and nothing else.

## Running costs

| | |
|---|---|
| Domain | ~$10–12/year |
| Cloudflare Pages | free — unlimited requests on the free plan |
| Supabase | free tier; pauses after a week of no activity and wakes on the next visit |

If Supabase's free-tier pause annoys you, their paid tier is $25/month — but for
two people logging daily, the project never goes idle long enough to pause.

## Things worth knowing

- **The repo is public.** The committed `config.js` is safe (anon key only), but
  anyone can read the source. If you would rather it were private: GitHub →
  Settings → change visibility. Cloudflare Pages works with private repos.
- **The GitHub Action** (`build-check.yml`) fails if `docs/index.html` drifts
  from `plate-and-barbell/index.html`. Run `node tools/build-standalone.mjs` and
  commit when you change the app.
- **Offline**, the app shows the sign-in screen and cannot reach the log. It is
  not a local-first app; the `localStorage` mode is a separate fallback for the
  unconfigured build, not an offline cache for this one.
- **Backups**: Settings → Full backup (JSON) whenever you want one. The three
  CSV exports are there for pulling the data into a notebook.
