# ideas/

Brainstorms, hypotheses and open questions. This is the cheapest layer in the notebook: writing an
idea down costs nothing, and an idea that turns out to be wrong is still a record of ground covered.

One file per idea: `<YYYY-MM-DD>-<slug>.md`, from [`_template.md`](_template.md). The date is the
creation date and never changes, even when the idea evolves.

## Before you add one

`grep -ri "<keywords>" ideas/ literature/notes/ derivations/ labbook/` and scan
[`../INDEX.md`](../INDEX.md). Ideas are easy to reinvent under a different name; the cross-links are
worth more than the file.

## What makes a good entry

The question, sharply. Then, in order of importance:

- **What would confirm it** — the calculation, run or measurement that would make us believe it.
- **What would kill it** — the same, in reverse. An idea with no possible refutation is not yet a
  research idea.
- What it assumes, and which of those assumptions we have not checked.
- What it connects to: sources, other ideas, derivations, runs.

Tag everything. Recollections about the literature are `[?]` until a source is registered; our own
reasoning is `[I]`. An idea note is mostly `[I]` and `[?]` by nature — that is correct, and it is
why nothing here is quotable as a result.

## Status field

| Status | Meaning |
|---|---|
| `seed` | written down, not worked on |
| `active` | being worked on now |
| `parked` | deliberately set aside; say why and what would restart it |
| `refuted` | shown wrong; link the `attic/` entry or the run that killed it |
| `promoted` | reached the lab book; set `shard:` to the shard ID |

Keep `status` and `updated` current — [`../INDEX.md`](../INDEX.md) is generated from them.

## When an idea grows up

A derivation goes to [`../derivations/`](../derivations/), code to [`../sims/`](../sims/), results
to [`../runs/`](../runs/), and — once the gates pass — the result is promoted into the lab book. The
idea file stays where it is and accumulates links to all of them.
