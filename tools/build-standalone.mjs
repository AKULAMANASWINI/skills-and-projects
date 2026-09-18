/**
 * Wraps the artifact page into a standalone HTML document for ordinary hosting.
 *
 * The published artifact omits <!doctype>, <html>, <head> and <body> — the
 * claude.ai runtime supplies them, along with a small reset. Anywhere else
 * (GitHub Pages, a local file) the page needs that shell itself, so this
 * script builds it: everything before `<div class="app">` is head material,
 * everything from there is the body.
 *
 *   node tools/build-standalone.mjs
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = resolve(root, "plate-and-barbell/index.html");
const OUT = resolve(root, "docs/index.html");

const src = readFileSync(SRC, "utf8");
const split = src.indexOf('<div class="app">');
if (split === -1) throw new Error('could not find `<div class="app">` in ' + SRC);
const head = src.slice(0, split).trim();
const body = src.slice(split).trim();

const FAVICON =
  "data:image/svg+xml," +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">` +
      `<rect width="32" height="32" fill="#F4F1E8"/>` +
      `<circle cx="11" cy="16" r="8.4" fill="none" stroke="#4B6B4F" stroke-width="2.2"/>` +
      `<circle cx="11" cy="16" r="2.6" fill="#C97155"/>` +
      `<rect x="19.4" y="14.6" width="3" height="2.8" fill="#33472F"/>` +
      `<rect x="23.8" y="11.2" width="4.4" height="9.6" fill="#33472F"/></svg>`,
  );

/* The reset the artifact runtime would otherwise provide. */
const RESET = `
:root{color-scheme:light dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}`;

const out = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Madhu and Aravind's food and training log — macros against targets, the Mon/Wed/Fri/Sun split, PRs, trends and CSV export.">
<meta name="theme-color" content="#F4F1E8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161B15" media="(prefers-color-scheme: dark)">
<link rel="icon" href="${FAVICON}">
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
console.log(`built ${OUT} — ${(out.length / 1024).toFixed(1)} KB`);
