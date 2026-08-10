---
id: Citekey
title: "Paper title"
status: seed          # seed | active | parked | refuted | promoted
confidence: low       # our confidence in our reading, not in the paper
tags: []
sources: [Citekey]    # this paper, plus any other registered source cited below
derivations: []
runs: []
shard:                # set once something from this paper reaches the lab book
updated: YYYY-MM-DD
---

# Citekey — Short title

Full citation. Local PDF: `../pdfs/Citekey.pdf`. Manifest row: [SOURCES.md](../SOURCES.md).

## Why we are reading it

One or two sentences: what question sent us here, and which idea or derivation it feeds.

## What the paper says

Claims with locations. Everything here is `[S:...]` — if you cannot point at a section, equation,
figure or table, it does not belong in this section.

- ... `[S:Citekey §2.1 eq.4]`
- ... `[S:Citekey Fig.3]`

## Assumptions and regime of validity

Approximations, limits, and the parameter regime the results are claimed for. Also: the conventions
the paper uses (units, signs, normalisations). If we adopt or translate any of them, record the
translation in [CONVENTIONS.md](../../CONVENTIONS.md) and link it here.

## Numbers worth having

Values we may reuse, each with its location and its uncertainty as the paper states it. Numbers
read from a figure are estimates and are marked as such.

| Quantity | Value | Location | Notes |
|---|---|---|---|
| | | | |

## What we make of it

Our reading, our extrapolations, our doubts. Everything here is `[I]` or `[?]` — this section is
explicitly *not* what the paper says.

- `[I]` ...
- `[?]` ...

## Follow-ups

- References worth acquiring (add to the source queue in the lab book).
- Results worth reproducing, and what a reproduction would need.
- Links to the ideas and derivations this feeds: `../../ideas/YYYY-MM-DD-slug.md`.
