# Lab book source map

Read this before editing the lab book.

The compiled document is rooted at [`../labbook.tex`](../labbook.tex), but that file holds **the
preamble and the include order only** — no prose. All body text lives in shards under
[`sections/`](sections/). Shared macros, including the evidence-tag macros, are in
[`macros.tex`](macros.tex).

For rapid lookup use [`SHARD_CATALOG.md`](SHARD_CATALOG.md): it gives every shard a stable label,
a short summary and search keywords. The same metadata is repeated in a comment header at the top
of each shard, so `grep` over `sections/` finds it too.

Build with `pixi run labbook` (system LaTeX: `latexmk` + `biber`). Check structure with
`pixi run check`.

## Shard order

| Order | Label | Source | Title |
|---:|---|---|---|
| 0 | `NB-00-FRONTMATTER` | `sections/00_frontmatter_status.tex` | Scope, Status, and Evidence Rules |
| 1 | `NB-01-PROGRAMME-MAP` | `sections/01_programme_map.tex` | Programme Map |
| 2 | `NB-02-LAB-LOG` | `sections/02_lab_log.tex` | Lab Log |
| 3 | `NB-03-REPRO-MAP` | `sections/03_reproducibility_map.tex` | Reproducibility Map |
| 4 | `NB-04-OPEN-QUESTIONS` | `sections/04_open_questions.tex` | Source Queue and Open Questions |

Shards 00–04 are structural and stay at the front. New material is added as `NN_<slug>.tex` with
`NN` continuing from 05.

## Rules

1. **Every shard starts with the four-line header**, exactly these keys:

   ```tex
   % SHARD-ID: NB-NN-SLUG
   % SHARD-TITLE: Human Readable Title
   % SHARD-SUMMARY: One line. Repeat the key for a second or third line.
   % SHARD-KEYWORDS: comma, separated, search, terms
   ```

   `SHARD-ID` is stable forever once assigned. Renaming a file is fine; renaming an ID is not.

2. **One `\include` per shard**, in `labbook.tex`, in the order given above. No `\input` of body
   text, no nesting.

3. **Target ~200 lines per shard, hard cap 280** (`LABBOOK_SHARD_MAX_LINES`). A shard that outgrows
   the cap gets split by topic, and both halves are registered.

4. **Register new shards in three places**: the order table above, `SHARD_CATALOG.md`, and
   `labbook.tex`. `pixi run check` fails if these disagree.

5. **Every factual sentence carries an evidence tag** — `\evS`, `\evD`, `\evC`, `\evI`, `\evQ`.
   Results state their gates with `\gates{...}`.

6. **Figures are TikZ/pgfplots reading plain-text `.dat` files from `runs/`.** The committed
   artefact is the data, not an image: it is greppable, diffable, and the figure fonts match
   the document. Generate the data with the simulation, never by hand.

7. **Citations go through the shared bibliography.** `\evS{Citekey}{§3.2}` cites
   `../literature/references.bib`, the same file the note frontmatter draws citekeys from. Do not
   create a second `.bib`.

8. **`sections/02_lab_log.tex` is append-only.** Add dated entries at the end; never edit or delete
   an old one. A later entry supersedes an earlier one and says so.

9. **`labbook.pdf` is not committed** — it is regenerable with `pixi run labbook`.

## Adding a shard

```bash
cp sections/01_programme_map.tex sections/05_my_topic.tex   # then replace the header and body
```

Then: add `\include{labbook/sections/05_my_topic}` to `labbook.tex` in the right position, add a
row to the table above and a block to `SHARD_CATALOG.md`, append a lab-log entry saying what the
shard establishes and with which gates, and run `pixi run check && pixi run labbook`.
