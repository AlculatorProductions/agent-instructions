---
description: Take in a pasted handwritten calculation
---

Erin has pasted a handwritten calculation (or is about to). Handle it in this order — the order
matters.

1. **Save it.** `calculations/YYYY-MM-DD-<slug>/handwriting.<ext>`, and fill in that folder's
   `README.md` from `calculations/_template/README.md`: what it computes, the symbols and their
   units, the assumptions, what it was for.
2. **Transcribe it faithfully** into a new lab book entry
   `labbook/entries/YYYY-MM-DD-<slug>.tex`, following `labbook/00_rules.tex`. Her notation, her
   ordering, her conventions. Do not tidy a step, do not re-derive, do not "improve" anything.
   Mark whatever you genuinely cannot read as `\unreadable{...}` and ask her about it.
3. **Write the code** she asked for, from the transcribed equations. Mark every function you write
   with `# [claude YYYY-MM-DD] unchecked`.
4. **Then check the mathematics.** Only now. If you find something you are reasonably confident is
   wrong, report it as: where (quote the step), what, **evidence** (dimensional analysis, a
   limiting case, a symmetry, a numeric spot-check — not "it looks wrong"), and a proposed fix
   with what it changes downstream. If you cannot produce evidence, say you are unsure and stop.

   **She decides.** Never edit her mathematics. Record the flag, the evidence and her decision in
   the entry with `\flag{...}`, whichever way she decides.
5. `python3 scripts/doc_research/build_entries.py`, then `check.py`, then commit.

$ARGUMENTS
