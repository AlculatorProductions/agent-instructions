# Research notebook

A working notebook for theoretical and computational physics. (The project name and title are set
at onboarding — see [ONBOARDING.md](ONBOARDING.md).)

It holds papers and reading notes, brainstorms and hypotheses, quick derivations, reproducible
simulations, and a LaTeX lab book that accumulates the results that survived checking. It is built
so that both a human and an AI agent can pick it up cold and find their way — agents read
[AGENTS.md](AGENTS.md).

## The idea in one paragraph

Everything is written twice, at two different levels of commitment. **Working memory** — `ideas/`,
`derivations/`, `runs/`, `literature/notes/`, `log/` — is fast, dated and revisable; nothing there
is claimed to be true. The **lab book** — `labbook.tex` and its shards — is the durable record, and
a result gets in only after it has been checked against a source, a derivation, or a run. Every
factual sentence in either layer carries a tag saying where it came from, so a cited fact never
gets confused with our own inference.

## Layout

| Path | What lives there |
|---|---|
| [AGENTS.md](AGENTS.md) | Canonical agent guidance: laws, tags, gates, workflows |
| [INDEX.md](INDEX.md) | Generated index of ideas, sources, derivations, runs and shards |
| [PROVENANCE.md](PROVENANCE.md) | Claim policy: what counts as evidence |
| [CONVENTIONS.md](CONVENTIONS.md) | Units, signs, normalisations — fixed before code depends on them |
| [GLOSSARY.md](GLOSSARY.md) | Terms, with sources |
| [TIMELINE.md](TIMELINE.md) | Commit line and fork graph — the map for branching off |
| [labbook.tex](labbook.tex), [labbook/](labbook/) | The lab book: sharded LaTeX, incl. a dated lab log |
| [literature/](literature/) | `references.bib`, `SOURCES.md`, PDFs (untracked), extracted text, reading notes |
| [ideas/](ideas/) | Brainstorms, hypotheses, open questions |
| [derivations/](derivations/) | Quick derivations, worked out and checked |
| [sims/](sims/) | Simulation code, one directory per simulation |
| [runs/](runs/) | One directory per execution: params, data, figures, interpretation |
| [attic/](attic/) | Failed attempts worth keeping, and what they rule out |
| [log/](log/) | Session worklogs and handoffs |
| [scripts/check.py](scripts/check.py) | The consistency gate |
| [ONBOARDING.md](ONBOARDING.md) | One-time setup for a fresh copy; deleted once done |

## Quickstart

First time in a fresh copy: work through [ONBOARDING.md](ONBOARDING.md) — git identity, project
name and author, `pixi install` plus committing `pixi.lock`, and the LaTeX toolchain.

```bash
pixi install       # environment from pixi.lock
pixi run check     # verify sources, citekeys, runs, links and lab-book shards
pixi run labbook   # compile labbook.pdf (needs system LaTeX: latexmk + biber)
```

`pixi run labbook` uses the system TeX installation (MacTeX on macOS); TeX Live is deliberately
not pulled into the pixi environment.

## Recipes

**Add a paper.** Save the PDF as `literature/pdfs/<Citekey>.pdf`, add its BibTeX entry to
`literature/references.bib`, register it in [literature/SOURCES.md](literature/SOURCES.md) with
DOI, retrieval date and SHA256, then write reading notes in `literature/notes/<Citekey>.md` from
the template. PDFs stay out of git; the manifest makes them re-acquirable.

**Start an idea.** Copy `ideas/_template.md` to `ideas/<YYYY-MM-DD>-<slug>.md`. Say what the
question is, what would confirm it, and what would kill it. Tag recollections `[?]` until a source
is registered.

**Do a run.** Put the code in `sims/<slug>/`, then record the execution in
`runs/<YYYY-MM-DD>-<slug>/` with hypothesis, exact command, why these parameters, environment,
result, interpretation and uncertainty. Small summaries and vector figures are committed; bulk
arrays are not, but their producing command is.

**Promote a result.** Once it has passed its checks: add or extend a shard in `labbook/sections/`,
register it in `labbook/SHARD_CATALOG.md`, and append a dated entry to the lab log in
`labbook/sections/02_lab_log.tex`. See the promotion path in [AGENTS.md](AGENTS.md).

**Record a dead end.** Write it into [attic/](attic/) with what it rules out. Failed attempts are
results.

**Branch off.** When a line of work goes bad (poisoned context, a wrong turn) or the topic changes,
work continues on a fresh branch from a known-good commit. [TIMELINE.md](TIMELINE.md) holds the
commit line and fork graph; the workflow is in [AGENTS.md](AGENTS.md).

## Conventions in brief

- Citekeys `AuthorYYYYkeyword`; everything about one paper shares that key.
- Dated slugs `<YYYY-MM-DD>-<slug>` for ideas, derivations, runs, log and attic entries.
- Evidence tags: `[S:key]` sourced · `[D:id]` derived · `[C:run]` computed · `[I]` our inference ·
  `[?]` unverified.
- Gates: **S**ource, **D**efinition, **M**ath, **C**omputation, **R**eview, **B**uild.
