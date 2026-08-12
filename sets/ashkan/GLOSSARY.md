# GLOSSARY

Every technical term used in this repository is defined here before it is relied on (Law 2 in
[AGENTS.md](AGENTS.md)). One entry per term: the definition, the source, and — where it matters —
what it does *not* mean here.

Entries are alphabetical. Definitions taken from a source carry its tag; definitions that are our
own working usage carry `[I]` and say so.

## How to add an entry

```markdown
### Term (abbreviation)

Definition in one or two sentences. [S:Citekey §2.1]

Notes: how we use it, what it is often confused with, or which convention in
[CONVENTIONS.md](CONVENTIONS.md) it depends on.
```

Do not add a term you cannot define from a local source or a checked derivation. An entry with a
`[?]` tag is a request for the next session, and is better than an entry that sounds right.

## Repository terms

These are definitions of how *this repository* works, not physics.

### Evidence tag

The bracketed mark attached to a factual sentence recording where it came from: `[S:...]` sourced,
`[D:...]` derived, `[C:...]` computed, `[I]` our inference, `[?]` unverified. See
[PROVENANCE.md](PROVENANCE.md).

### Gate

One of the six checks a claim can pass — **S**ource, **D**efinition, **M**ath, **C**omputation,
**R**eview, **B**uild. Claims entering the lab book name the gates that were actually run.

### Promotion

Moving a result from working memory (`ideas/`, `derivations/`, `runs/`) into the lab book
(`labbook/sections/`) once its gates pass, recorded in the session's `log/` entry.

### Run

One recorded execution of a simulation, stored as `runs/<YYYY-MM-DD>-<slug>/` with its hypothesis,
exact command, environment, results and interpretation. A computation with no run directory is not
citable.

### Shard

One `labbook/sections/NN_*.tex` file: a self-contained section of the lab book with a stable
`SHARD-ID`, target ~200 lines, hard cap 280.

## Physics terms

_None yet — added the day the first sources are registered, per Law 2 in AGENTS.md._
