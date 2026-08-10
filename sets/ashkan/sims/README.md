# sims/

Simulation code. One directory per simulation: `sims/<slug>/` — no date, because a simulation
evolves; the dated record of *executing* it lives in [`../runs/`](../runs/).

Start from [`_template/`](_template/):

```bash
cp -r sims/_template sims/my-simulation
```

## Structure of a simulation

| File | Purpose |
|---|---|
| `README.md` | the physics: what is modelled, which equations, which conventions, which validation targets |
| `run.py` | entry point — reads a params file, writes into a run directory |
| `params.toml` | default parameters, all in SI, each with a comment giving its meaning |
| `test_*.py` | the validation tests (`pixi run test` collects them) |

## Rules

1. **Literate code.** The module docstring states the physical purpose, cites the source or
   derivation it implements (`[S:Key eq.4]`, `[D:2026-07-29-slug]`) — alongside the tag, give the
   repo-relative path (e.g. `derivations/2026-07-29-slug.md`) so the reference is click-to-open in
   an editor — and names the conventions it obeys. A reader should recognise the derivation in the
   code.
2. **SI units everywhere**, per [`../CONVENTIONS.md`](../CONVENTIONS.md). Constants come from
   `scipy.constants`, never from a typed-in literal.
3. **Parameters live in a file, not in the source.** Anything that changes between runs is in
   `params.toml`, so a run is fully described by code SHA + params + environment.
4. **Validation before use.** Each simulation names its validation targets in its README — an
   analytic limit, a published number, a figure to reproduce, a convergence study — and has a test
   for at least one of them. Output from an unvalidated simulation is not usable in an argument.
5. **Determinism.** Seed every random generator explicitly and record the seed in the run.
6. **Write outputs into the run directory**, passed in as an argument. A simulation never writes
   into its own source directory.
7. **Fail loudly.** Assert preconditions (grid resolution against the smallest physical length
   scale, timestep against the fastest dynamics, normalisation after propagation). A silent NaN is
   worse than a crash.
8. **pixi is the environment.** Everything runs through `pixi run ...` — never a system Python or
   an ad-hoc venv. The `pixi.lock` hash is part of every run's provenance.

## Convergence

Resolution, timestep, box size and tolerance are *results*, not settings. The first run of any new
simulation is a convergence study, and its outcome is recorded in the run README and repeated in
every run that relies on it.
