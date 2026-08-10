---
id: YYYY-MM-DD-slug
title: "What this run tested"
status: seed
confidence: low
tags: []
sources: []
derivations: []
runs: []
shard:
updated: YYYY-MM-DD
---

# Run YYYY-MM-DD-slug

The eight `##` sections from Hypothesis to Next steps are required — `pixi run check` fails
without them; it warns when "Why these parameters" is missing.

## Hypothesis

What this run was meant to test, and what outcome would count as confirming or refuting it. Written
*before* looking at the output.

## Command

The simulation, its commit, and the exact invocation.

- Simulation: `sims/<slug>/run.py`
- Git SHA: `...` (from `provenance.json`)
- Parameters: `params.toml` (in this directory)

```bash
pixi run python sims/<slug>/run.py --params params.toml --out runs/YYYY-MM-DD-slug/
```

## Why these parameters

`params.toml` records *what*; this section records *why* — why this grid, this box, this duration,
this tolerance. Judgement is `[I]`. The test: a reader could change a value sensibly without
re-deriving your reasoning.

## Environment

- `pixi.lock` SHA256 (first 16): `...` (from `provenance.json`)
- Machine / accelerator, if it matters for the numbers.

## Result

The headline numbers, each with its uncertainty. Figures referenced by path.

| Quantity | Value | Uncertainty | Source of the uncertainty |
|---|---|---|---|
| | | | |

Artefacts too large to commit, with their stubs:

| Path | Size | SHA256 | Regenerate with |
|---|---|---|---|
| | | | |

## Interpretation

What the numbers mean for the hypothesis. Tag it: `[C:this-run]` for what the run shows, `[I]` for
what we conclude from it. These are not the same sentence.

## Uncertainty

Convergence (grid, timestep, box size), solver tolerances, statistical error, and — importantly —
the physics the model leaves out that could change the answer. Be specific about which of these
dominates.

## Gates

Which gates actually ran, and how. E.g.: **C** — reproduces a known analytic limit to 0.3%
(named, and independent of the equation being tested); **D** — conventions checked against
`CONVENTIONS.md`; **B** — `pixi run test` passes.

Do not list a gate you did not run.

## Next steps

What this run makes worth doing next, and what it closed off. If it refuted something, say what and
update that idea's status.
