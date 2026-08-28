# labbook/

The technical record. Built into `labbook.pdf` by `cd doc_research && latexmk -pdf labbook.tex`.

| | |
|---|---|
| `../labbook.tex` | master file: preamble, the rules chapter, the generated include list. Yours to edit. |
| `preamble.tex` | shared preamble and macros. Template — replaced on update. |
| `00_rules.tex` | how the lab book works. Template — replaced on update. |
| `entries.tex` | generated include list. Never edit by hand. |
| `entries/` | one `.tex` per piece of work, `YYYY-MM-DD-slug.tex`. |

Entries are chronological and never reorganised. `00_rules.tex` has the full format; the short
version is a metadata header comment, an `\entryhead`, then the calculation, the code, the
figures and what came out.

After adding an entry, run `python3 doc_research/scripts/build_entries.py` to regenerate `entries.tex`.
