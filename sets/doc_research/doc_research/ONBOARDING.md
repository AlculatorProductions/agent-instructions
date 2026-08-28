# ONBOARDING

One-time setup, the first time this notebook is added to a repository. An agent can do all of it.
Each step is safe to re-run.

- [ ] **Ask about documentation effort.** Ask, in these words or close to them:

      > When you ask me for something, how should I split the time between doing it and writing
      > it down?
      >   thorough — I document fully: every step transcribed, the calculation independently
      >     checked, everything cross-linked. Slower.
      >   light — I do the work, write a short entry and a figure caption, and stop there.
      >     Documenting stays a small part of each request.

      Write the answer into `TASTE.md` as the first rule, dated, e.g.
      `- 2026-08-28 — documentation effort: light.` Say it can be changed any time by saying so.

- [ ] **Ask where the code lives.** This notebook does not create a code directory — it documents
      the code already in the repository. Record the path(s) in `TASTE.md`, e.g.
      `- 2026-08-28 — code lives in analysis/ and scripts/sim/.`

- [ ] **Ask how plots are made.** Which library, which style, whether there is an existing helper
      already in use. Record it in `TASTE.md`. Never impose a plotting style on someone's code.

- [ ] **Explain `FEEDBACK.md`.** One or two sentences: when something goes wrong or is confusing,
      you write it down there; it stays on this machine; it can be sent back to whoever set the
      notebook up, and the instructions get fixed.

- [ ] **Explain `TASTE.md`.** You change how the agent behaves by saying so in the chat.

- [ ] **Environment (optional).** `cd doc_research && pixi install`, if pixi is available. The
      scripts also run with plain `python3`, so this is convenience, not a requirement.

- [ ] **LaTeX.** `latexmk` and `biber` must exist for the PDFs to build (MacTeX on macOS:
      `brew install --cask mactex`). Check with `cd doc_research && latexmk -pdf labbook.tex`. If
      TeX is missing, say so and carry on — the `.tex` record is still being written.

- [ ] **Gate.** `python3 doc_research/scripts/check.py` passes.

- [ ] **Finish.** Delete this file and commit.
