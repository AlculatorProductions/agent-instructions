# PROVENANCE

What counts as evidence in this repository, and how it is recorded. See [AGENTS.md](AGENTS.md) for
the workflows that apply this policy.

## Claim policy

Every physical, numerical or bibliographic claim must be traceable to one of:

- a source registered in [literature/SOURCES.md](literature/SOURCES.md);
- a checked derivation under [derivations/](derivations/);
- a recorded run under [runs/](runs/).

Conversation context, model memory, web snippets, and subagent reports are **not** ground truth.
They are leads. A lead becomes evidence when the artefact is local and registered.

Anything that is our own reasoning rather than a cited result is marked `[I]`. Anything still
unsupported is marked `[?]`. These are not blemishes — an accurate `[I]` is better work than a
confident unmarked assertion.

## Evidence tags

| Markdown | LaTeX | Meaning |
|---|---|---|
| `[S:Key §3.2 eq.14]` | `\evS{Key}{§3.2 eq.14}` | stated by a registered source, at that location |
| `[D:2026-07-29-slug]` | `\evD{2026-07-29-slug}` | our derivation, checked |
| `[C:2026-07-29-slug]` | `\evC{2026-07-29-slug}` | our computation, run recorded |
| `[I]` | `\evI{}` | our inference or interpretation — not yet checked |
| `[?]` | `\evQ{}` | needs a source or a check |

`[S:...]` requires that someone opened the local source at that location. Inferring what a paper
"must" say from its abstract, its title, or another paper's summary of it is `[I]`.

## Source policy

For each source record, in `literature/SOURCES.md`: citekey, full citation, its role in our work,
DOI/arXiv ID and URL, retrieval date, access route, local path, and SHA256.

Prefer lawful routes: arXiv, publisher, author page, institutional access. Store PDFs under
`literature/pdfs/` (untracked). Do not paste long copyrighted excerpts into repo files — cite the
location, paraphrase, quote only briefly.

Citations point at **local paths plus location** (page, section, equation, figure, table). A bare
URL is acquisition metadata, not a citation.

## Uncertainty

Where a number carries uncertainty, record it with the number: statistical error, tolerance,
convergence level, or the fact that it is an order-of-magnitude estimate. Where a model omits
physics that matters (finite temperature, interactions, environmental noise, neglected degrees of
freedom, …), say so next to the result rather than in a caveats section nobody reads.

Idea and derivation notes carry a `confidence:` field — `low`, `medium` or `high`. It describes our
belief in the claim, not the quality of the writing, and it must move when the evidence moves.

## Generated artefacts

Every generated dataset or figure records the script, its git commit SHA, the parameters, the exact
command, and the environment (`pixi.lock` hash) that produced it — in the run README.

Artefacts too large to commit (see the policy in `AGENTS.md`) are represented by a stub in the run
README giving path, size, SHA256 and producing command, so their absence is auditable and their
regeneration is mechanical.

## Superseded and refuted claims

Claims are corrected in place and the correction is recorded; they are not silently deleted. A
refuted idea gets `status: refuted`, a note saying what refuted it, and — if the attempt taught
something — an entry in [attic/](attic/). Session-log entries (`log/`) are not rewritten once
their session is over; a later entry supersedes an earlier one and says which.

## Subagent and tool reports

Reports from subagents, search tools and text extraction from PDFs are review artefacts. Use them
to decide where to look; then cite the local file you actually read. OCR and PDF-to-text output in
`literature/text/` is convenience, not authority — equations and numbers taken from it must be
confirmed against the PDF.
