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

- [ ] **Say that it starts empty.** In one or two sentences: the lab book and the work log are
      nearly blank right now, that is the normal starting state, and they fill up by themselves as
      work happens. Nothing has to be filled in by hand — the `.tex` files are written by the
      agent, and a `TODO` inside one is the agent's own scaffolding, not a task for the researcher.

- [ ] **Offer an initial read of the repository.** Ask:

      > Would you like me to read through the repository once and write a short opening entry —
      > what the code does, how it is laid out, what is already here? It is a starting point, not
      > a full audit.

      If yes: read the code, then write **one** entry,
      `labbook/entries/<today>-starting-point.tex`, of at most a page. What the project is, the
      main components and where they live, anything already documented, and what is conspicuously
      undocumented. Tag every claim you inferred rather than read — this entry is orientation, not
      established fact. Do not transcribe mathematics you have not been shown, and do not add
      `[claude ...]` markers to code you did not write.

      If no: write nothing.

      Either way, say the same closing line: from here on, the work gets documented as it
      happens — the record starts now, and this is what it starts from.

- [ ] **Environment (optional).** `cd doc_research && pixi install`, if pixi is available. The
      scripts also run with plain `python3`, so this is convenience, not a requirement.

- [ ] **LaTeX.** `latexmk` and `biber` must exist for the PDFs to build (MacTeX on macOS:
      `brew install --cask mactex`). Check with `cd doc_research && latexmk -pdf labbook.tex`. If
      TeX is missing, say so and carry on — the `.tex` record is still being written.

- [ ] **Checks pass.** `python3 doc_research/scripts/check.py` reports no problems.

- [ ] **Finish.** Delete this file and commit.
