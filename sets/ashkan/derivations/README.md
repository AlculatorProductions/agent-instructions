# derivations/

Quick derivations: the pen-and-paper layer, written down so it can be checked. One file per
derivation, `<YYYY-MM-DD>-<slug>.md`, from [`_template.md`](_template.md).

Markdown with LaTeX maths (`$...$`, `$$...$$`) is the default — it is fast, greppable and diffable.
A derivation that becomes central — one that results or simulations presented in the lab book rest
on, or that is needed to understand them — is promoted into a lab-book shard, where it is rewritten
properly in LaTeX with `\evS`/`\evD` tags. Do not start in the lab book: most derivations do not
survive, and the lab book is for the ones that do.

## Rules

1. **State the starting point.** Which equation, from which source, in which convention.
   `[S:Key eq.7]`. A derivation that starts from a remembered equation starts from nothing.
2. **Fix conventions first.** If the derivation depends on a sign, a factor, a normalisation or a
   Fourier convention that is not already in [`../CONVENTIONS.md`](../CONVENTIONS.md), put it there
   before continuing.
3. **Show the steps that could be wrong.** Skip the algebra that cannot fail; write out the step
   where a sign flips, a limit is taken, or a term is dropped — and say *why* the term is dropped.
4. **Check it.** Every derivation ends with at least one check:
   - dimensional analysis;
   - a limiting case with a known answer (free particle, no interactions, short time);
   - a special case that matches a published result;
   - a numerical spot-check — which becomes a run under [`../runs/`](../runs/) and a `[C:...]` tag.
5. **Record what it does not cover.** The regime of validity is part of the result.

## Status

Same field as ideas: `seed`, `active`, `parked`, `refuted`, `promoted`. A derivation is only
`active` once it has been checked — an unchecked derivation is a draft, and `confidence: low`.

A derivation found to be wrong is corrected in place with a note saying what was wrong, or moved to
[`../attic/`](../attic/) if the whole approach failed. It is not deleted: a wrong derivation that
looked convincing is exactly what a future session needs to see.
