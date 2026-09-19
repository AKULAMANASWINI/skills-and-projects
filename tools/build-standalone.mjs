/**
 * Wraps each artifact page into a standalone HTML document for ordinary hosting.
 *
 * A published artifact omits <!doctype>, <html>, <head> and <body> — the
 * claude.ai runtime supplies them, along with a small reset. Anywhere else
 * (GitHub Pages, a local file) the page needs that shell itself, so this
 * script builds it: everything before `<div class="app">` is head material,
 * everything from there is the body.
 *
 * Plate & Barbell keeps the root of the site, so the URL that has been handed
 * out stays valid; every project added since gets its own directory.
 *
 *   node tools/build-standalone.mjs
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const icon = (body) =>
  "data:image/svg+xml," +
  encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">${body}</svg>`);

const PROJECTS = [
  {
    src: "plate-and-barbell/index.html",
    out: "docs/index.html",
    description:
      "Madhu and Aravind's food and training log — macros against targets, the Mon/Wed/Fri/Sun split, PRs, trends and CSV export.",
    themeLight: "#F4F1E8",
    themeDark: "#161B15",
    favicon: icon(
      `<rect width="32" height="32" fill="#F4F1E8"/>` +
        `<circle cx="11" cy="16" r="8.4" fill="none" stroke="#4B6B4F" stroke-width="2.2"/>` +
        `<circle cx="11" cy="16" r="2.6" fill="#C97155"/>` +
        `<rect x="19.4" y="14.6" width="3" height="2.8" fill="#33472F"/>` +
        `<rect x="23.8" y="11.2" width="4.4" height="9.6" fill="#33472F"/>`,
    ),
  },
  {
    src: "hobby-ledger/index.html",
    out: "docs/hobby-ledger/index.html",
    description:
      "A ledger for the hours you actually spend on your hobbies — sessions, streaks, weekly goals, a consistency grid and CSV export.",
    themeLight: "#EBEDEE",
    themeDark: "#0F1416",
    favicon: icon(
      `<rect width="32" height="32" fill="#EBEDEE"/>` +
        `<rect x="6" y="19" width="4" height="7" fill="#2a78d6"/>` +
        `<rect x="12" y="14" width="4" height="12" fill="#1baf7a"/>` +
        `<rect x="18" y="9" width="4" height="17" fill="#eb6834"/>` +
        `<rect x="24" y="5" width="3" height="21" fill="#0E4552"/>`,
    ),
  },
];

/* The reset the artifact runtime would otherwise provide. */
const RESET = `
:root{color-scheme:light dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}`;

for (const p of PROJECTS) {
  const SRC = resolve(root, p.src);
  const OUT = resolve(root, p.out);

  const src = readFileSync(SRC, "utf8");
  const split = src.indexOf('<div class="app">');
  if (split === -1) throw new Error('could not find `<div class="app">` in ' + SRC);
  const head = src.slice(0, split).trim();
  const body = src.slice(split).trim();

  const out = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="${p.description}">
<meta name="theme-color" content="${p.themeLight}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="${p.themeDark}" media="(prefers-color-scheme: dark)">
<link rel="icon" href="${p.favicon}">
<style>${RESET}</style>
${head}
</head>
<body>
${body}
</body>
</html>
`;

  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, out);
  console.log(`built ${p.out} — ${(out.length / 1024).toFixed(1)} KB`);
}
