# runs/

One directory per recorded execution: `runs/<YYYY-MM-DD>-<slug>/`. A computation without a run
directory is not citable — the `[C:...]` tag points here.

```
runs/2026-07-29-expansion-convergence/
├── README.md          hypothesis, command, environment, result, interpretation, uncertainty
├── params.toml        the exact parameters used (copied by run.py)
├── provenance.json    code SHA, pixi.lock hash, command (written by run.py)
├── data/              small text summaries — committed; bulk arrays — not
└── figures/           vector figures used in notes or the lab book
```

Start from [`_template/README.md`](_template/README.md). `pixi run check` fails if a run directory
has no README or is missing a required section, and warns when the "Why these parameters" section
is absent — `params.toml` records what, not why.

## What gets committed

Committed: the README, `params.toml`, `provenance.json`, summary CSV/JSON under ~1 MB, vector
figures (PDF/SVG) that appear in notes or the lab book.

Not committed: bulk arrays (`*.npy`, `*.h5`, …) and anything over 5 MB. These get a stub in the
README — path, size, SHA256, producing command — so their absence is auditable and regeneration is
mechanical. See the artefact policy in [`../AGENTS.md`](../AGENTS.md).

## Runs that failed

A run that crashed, diverged, or produced nonsense is still recorded, with what went wrong. It is
the cheapest possible warning to the next session. If the *approach* failed rather than the
execution, write it up in [`../attic/`](../attic/) too and link both ways.

## Uncertainty

Every headline number carries its uncertainty, and the README says what the uncertainty is *of*:
statistical scatter, solver tolerance, discretisation error from a convergence study, or a plain
order-of-magnitude estimate. Physics the model omits belongs next to the number, not in a footnote.

A number with no stated uncertainty is treated as unverified.
