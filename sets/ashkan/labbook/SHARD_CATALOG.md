# Shard catalog

Stable labels, summaries and search keywords for the lab book rooted at
[`../labbook.tex`](../labbook.tex). This is the lookup table: scan it to find which shard covers a
topic, then open that shard.

The same metadata lives in the `% SHARD-*` header of each file. `pixi run check` verifies that the
two agree and that every shard is included exactly once.

## `NB-00-FRONTMATTER`

- Source: `sections/00_frontmatter_status.tex`
- Title: Scope, Status, and Evidence Rules
- Summary: Declares what this lab book is, what counts as an established result, and how evidence tags and gates are used in the text.
- Keywords: scope, status, evidence, gates, claim policy

## `NB-01-PROGRAMME-MAP`

- Source: `sections/01_programme_map.tex`
- Title: Programme Map
- Summary: Lists the research axes the notebook covers and the order in which their foundations must be laid.
- Summary: Asserts no connections between axes that have not been established.
- Keywords: programme, research axes, scope, roadmap

## `NB-02-LAB-LOG`

- Source: `sections/02_lab_log.tex`
- Title: Lab Log
- Summary: Append-only chronological record of what was established, when, on what evidence, and with which gates.
- Summary: The primary entry point for reconstructing how a result came about.
- Keywords: lab log, chronology, session record, handoff, provenance

## `NB-03-REPRO-MAP`

- Source: `sections/03_reproducibility_map.tex`
- Title: Reproducibility Map
- Summary: Maps each simulation to the runs it produced and each run to the claims and figures that depend on it.
- Summary: States the rules that make a number in this lab book regenerable from a recorded command.
- Keywords: reproducibility, runs, simulations, figures, artefacts, provenance

## `NB-04-OPEN-QUESTIONS`

- Source: `sections/04_open_questions.tex`
- Title: Source Queue and Open Questions
- Summary: Collects what is not yet known: sources to acquire, claims marked unverified, and questions the notebook is trying to answer.
- Keywords: open questions, source queue, unverified, backlog, next steps
