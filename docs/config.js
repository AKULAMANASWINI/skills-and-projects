/* Plate & Barbell — self-hosted configuration.
 *
 * Fill these in with your Supabase project's URL and *anon* key
 * (Supabase dashboard -> Project Settings -> API).
 *
 * The anon key is meant to be public — it identifies the project, it does not
 * grant access. Access is decided by row-level security in supabase/schema.sql,
 * which only lets the two addresses in `allowed_emails` read or write anything.
 * Never put the *service_role* key here; that one does bypass every policy.
 *
 * Leave the placeholders and the app falls back to this-browser-only storage.
 */
window.PB_CONFIG = {
  supabaseUrl:     "YOUR_PROJECT_URL",   // e.g. https://abcdefgh.supabase.co
  supabaseAnonKey: "YOUR_ANON_KEY"
};
