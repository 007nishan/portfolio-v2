#!/usr/bin/env node
/*
 * katex_render.js — build-time math batch renderer (BCS v1.1 §B.2).
 *
 * Reads a JSON array of {tex, display} objects from stdin and writes a JSON
 * array of rendered KaTeX HTML strings to stdout, in the same order. ALL
 * equations for a book render in ONE Node process (fixes the per-equation
 * subprocess latency residual risk). throwOnError:true so a bad formula aborts
 * the whole build loudly — no silent .katex-error nodes ever reach the HTML.
 *
 * This runs ONLY at build time (book_generator.py). The shipped page and the
 * WeasyPrint PDF contain zero JS: they consume the static HTML this emits.
 */
const path = require("path");
const katex = require(path.join(__dirname, "node_modules", "katex"));

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  let items;
  try {
    items = JSON.parse(raw);
  } catch (e) {
    process.stderr.write("katex_render: invalid JSON on stdin: " + e.message + "\n");
    process.exit(2);
  }
  const out = [];
  for (let i = 0; i < items.length; i++) {
    const { tex, display } = items[i];
    try {
      out.push(
        katex.renderToString(tex, {
          displayMode: !!display,
          throwOnError: true,
          strict: "warn",
          output: "html",
        })
      );
    } catch (e) {
      process.stderr.write(
        "katex_render: TeX error in item " + i + ": " + e.message + "\n  TeX=" + JSON.stringify(tex) + "\n"
      );
      process.exit(3);
    }
  }
  process.stdout.write(JSON.stringify(out));
});
