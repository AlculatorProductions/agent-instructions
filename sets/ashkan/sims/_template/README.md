# sims/&lt;slug&gt;

One line: what this simulates.

## Physics

What is modelled and what is not. The equation being solved, cited to its source or derivation:

$$ \ldots $$

`[S:Key eq.4]` or `[D:YYYY-MM-DD-slug]`.

State the regime: which terms are kept, which are dropped, and why.

## Conventions

Which entries of [`../../CONVENTIONS.md`](../../CONVENTIONS.md) this code depends on — units,
signs, normalisations, any Fourier convention. If this simulation forces a new choice, add it
there first.

## Parameters

`params.toml` holds the defaults, in SI. Copy it into a run directory and edit there; do not edit
defaults for a one-off.

| Parameter | Meaning | Default |
|---|---|---|
| | | |

## Validation targets

What this simulation is checked against. At least one must be implemented as a test.

- [ ] Analytic limit: ... reduces to ... `[S:Key eq.2]`
- [ ] Published number or figure: ... `[S:Key Fig.3]`
- [ ] Convergence: result stable under grid/timestep refinement to within ...
- [ ] Conserved quantity: ... conserved to ...

## Running

```bash
pixi run python sims/<slug>/run.py --params params.toml --out runs/YYYY-MM-DD-<slug>/
```

Then fill in the run README from [`../../runs/_template/README.md`](../../runs/_template/README.md).

## Known limitations

Physics left out, numerical regimes where it is known to break, and anything a user could
accidentally rely on that is not actually validated.
