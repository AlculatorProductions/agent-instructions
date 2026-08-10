---
id: YYYY-MM-DD-slug
title: "What is being derived"
status: seed          # seed | active | parked | refuted | promoted
confidence: low
tags: []
sources: []           # citekeys the starting point comes from
derivations: []       # derivations this builds on
runs: []              # numerical checks of this derivation
shard:
updated: YYYY-MM-DD
---

# Title

## Goal

The statement to be derived, written out. What it will be used for.

## Starting point

The equations we start from, each cited: `[S:Key §2.1 eq.4]`. State the convention they are in and
confirm it matches [CONVENTIONS.md](../CONVENTIONS.md) — or record the translation.

$$ \ldots $$

## Assumptions

Every approximation, with the regime it requires. Each tagged: sourced `[S:...]`, our own `[I]`, or
unchecked `[?]`.

## Derivation

Steps. Write out the ones that can go wrong; say why each dropped term is negligible.

$$ \ldots $$

## Result

$$ \boxed{\ldots} $$

What it means in words, and where it is valid.

## Checks

At least one, with its outcome recorded:

- **Dimensions**: ...
- **Limit** (e.g. non-interacting / short time / weak coupling): reduces to ... `[S:Key eq.2]`
- **Special case**: matches ...
- **Numerics**: `[C:YYYY-MM-DD-slug]` — agreement to ...

Gates run: **M** ... **C** ...

## Does not cover

The regimes, terms and effects this derivation explicitly excludes.

## Links

- Idea: `../ideas/YYYY-MM-DD-slug.md`
- Sources: `../literature/notes/Citekey.md`
- Runs: `../runs/YYYY-MM-DD-slug/README.md`
