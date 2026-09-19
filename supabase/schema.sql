-- Plate & Barbell — Supabase schema
-- Run this once, whole, in the SQL editor of a fresh project.
-- It is idempotent: running it again is safe.

-- ---------------------------------------------------------------- membership
-- Who is allowed in. Two rows. Everything else keys off this, so that a
-- stranger who manages to sign up still reads and writes nothing.
create table if not exists public.allowed_emails (
  email text primary key,
  note  text
);

create or replace function public.is_member()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.allowed_emails a
    where lower(a.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

revoke all on function public.is_member() from public;
grant execute on function public.is_member() to authenticated;

-- ---------------------------------------------------------------- the data
-- One row per person, one row per person-day. Same shape the app already
-- uses, so the JSON round-trips with the artifact build and the exports.
create table if not exists public.app_config (
  id         text primary key default 'app',
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.library (
  id         text primary key default 'custom',
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.profiles (
  id         text primary key,          -- 'p1' = Madhu, 'p2' = Aravind
  data       jsonb not null,
  updated_at timestamptz not null default now()
);

create table if not exists public.days (
  profile_id text not null,
  day        date not null,
  data       jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (profile_id, day)
);

create index if not exists days_day_idx on public.days (day desc);

create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;

drop trigger if exists t_app_config_touch on public.app_config;
create trigger t_app_config_touch before update on public.app_config
  for each row execute function public.touch_updated_at();
drop trigger if exists t_library_touch on public.library;
create trigger t_library_touch before update on public.library
  for each row execute function public.touch_updated_at();
drop trigger if exists t_profiles_touch on public.profiles;
create trigger t_profiles_touch before update on public.profiles
  for each row execute function public.touch_updated_at();
drop trigger if exists t_days_touch on public.days;
create trigger t_days_touch before update on public.days
  for each row execute function public.touch_updated_at();

-- ---------------------------------------------------------------- row security
alter table public.allowed_emails enable row level security;
alter table public.app_config     enable row level security;
alter table public.library        enable row level security;
alter table public.profiles       enable row level security;
alter table public.days           enable row level security;

-- The allowlist itself is readable by members and writable by nobody through
-- the API — edit it here in the SQL editor.
drop policy if exists "members read the allowlist" on public.allowed_emails;
create policy "members read the allowlist" on public.allowed_emails
  for select to authenticated using (public.is_member());

drop policy if exists "members use app_config" on public.app_config;
create policy "members use app_config" on public.app_config
  for all to authenticated using (public.is_member()) with check (public.is_member());

drop policy if exists "members use library" on public.library;
create policy "members use library" on public.library
  for all to authenticated using (public.is_member()) with check (public.is_member());

drop policy if exists "members use profiles" on public.profiles;
create policy "members use profiles" on public.profiles
  for all to authenticated using (public.is_member()) with check (public.is_member());

drop policy if exists "members use days" on public.days;
create policy "members use days" on public.days
  for all to authenticated using (public.is_member()) with check (public.is_member());

-- ---------------------------------------------------------------- realtime
-- So Madhu's phone updates while Aravind is logging on his.
do $$
begin
  begin alter publication supabase_realtime add table public.days;       exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table public.profiles;   exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table public.library;    exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table public.app_config; exception when duplicate_object then null; end;
end $$;

-- ---------------------------------------------------------------- seed
-- EDIT THESE TWO LINES to the real addresses before running, or run the
-- insert again afterwards. Only these addresses can read or write anything.
insert into public.allowed_emails (email, note) values
  ('madhu@example.com',   'Madhu'),
  ('aravind@example.com', 'Aravind')
on conflict (email) do nothing;

-- Check it worked: this should return true once you are signed in as one
-- of the addresses above.
--   select public.is_member();
