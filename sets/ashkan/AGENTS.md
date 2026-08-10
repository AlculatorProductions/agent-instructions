# AGENTS.md — canonical guidance for agents working in this repository

This repository is a **research notebook**: a place where ideas in theoretical and computational
physics are grown from first sketch to a citable result. It is not a software product. The
artefact being built is a *record* — one that a physicist can audit line by line a year from now.

The central failure mode to avoid is **a plausible statement with no traceable source**. A
confident sentence about a scaling law, an experimental parameter, or what a paper "shows" is worth
nothing here unless it points at a local file. Fluent recall is exactly what this repo is designed
to distrust.

Read this file at the start of every session and again after any context compression.

## Entry point

Before writing anything substantive, read in this order:

1. `AGENTS.md` (this file)
2. `INDEX.md` — what already exists: ideas, sources, derivations, runs, lab-book shards
3. `PROVENANCE.md` — the claim policy
4. `CONVENTIONS.md` — units, signs, normalisations already fixed
5. `GLOSSARY.md` — terms already defined
6. `literature/SOURCES.md` — the registered sources
7. The specific idea, note, derivation, run, or shard your task touches

Then the handoff: read the newest `log/` entry, and the `ideas/` entry it points at. Those two plus
`INDEX.md` are the whole handoff — state that is missing from the files is a defect to fix (and
worth saying so), not something to ask the user to re-explain.

**Bootstrap exception.** In an empty repo an agent may create scaffolding (templates, indices,
directory READMEs, check scripts) without a source. Substantive claims wait for the source layer.

**First session in a fresh copy?** If [ONBOARDING.md](ONBOARDING.md) still exists, work through it
first.

## The three laws

**Law 1 — Ground truth before claims.** No physical statement, formula, numerical value,
experimental parameter, literature summary, or modelling assumption may come from memory. It must
cite a registered local source, a checked local derivation, or a recorded run. If the source is not
local yet, acquire and register it first, or write the gap into the note as `[?]` and stop there.

**Law 2 — Conventions before derivations.** Every technical term goes into `GLOSSARY.md`. Every
unit, sign, phase, normalisation, coordinate, or notation choice goes into `CONVENTIONS.md`
*before* a derivation or a line of code depends on it. Most silent errors in this field are sign
and factor-of-2 errors; the convention file is the defence.

**Law 3 — Literate code and literate runs.** Simulation code is part of the record. Every script
states its physical purpose, cites the source/convention/derivation it implements, and exposes the
invariant it checks. A run without a `README.md` recording hypothesis, command, environment, result
and interpretation did not happen.

If a faster path conflicts with a law, follow the law.

## Working style

- **Plan first for anything non-trivial.** Three or more steps, a new simulation, a new lab-book
  section, or anything that fixes a convention: plan, then execute. If a derivation or a run goes
  sideways, stop and re-plan rather than pushing on.
- **Search finds; reading knows.** Subagents and web search are welcome for finding which paper or
  note covers something — but never cite the subagent or the search snippet; open the paper, note
  or run it points at and cite that. A summary is a lead, and its recollections are no more
  reliable than yours. The claim counts only once the source is local, registered, and read at the
  cited location.
- **Say how you checked it.** Before calling anything done, name the gates that ran and be
  concrete about each: which section of which paper, which limiting case, which run and what it
  agreed with, to what accuracy. "Should be right" is not a check, and neither is "the code runs".
- **Be concrete about physics.** Units, signs and factors of two are where this work actually goes
  wrong — check them against `CONVENTIONS.md` rather than assuming. Never invent an experimental
  parameter: cite it or mark it unknown. Numerical results are worth nothing until they reproduce
  something known.
- **Write down why you picked a number** — a grid size, a box extent, a tolerance — in the same
  edit that introduces it. The reason is cheap now and unrecoverable in a week; anything decided
  but not justifiable from a file is `[I]`.
- **After a context compression, re-read the files** rather than trusting the summary — and
  distrust your own earlier statements in the conversation as much as anyone else's. Long chat
  context is not evidence.

## Two layers: working memory and lab book

This is the structure of the whole repo. Keep the two layers distinct.

| Layer | Where | Role |
|---|---|---|
| **Working memory** | `ideas/`, `derivations/`, `runs/`, `attic/`, `log/`, `literature/notes/` | Fast, dated, revisable, cheap to grep. Where thinking happens. **Nothing here is settled.** |
| **Lab book** | `labbook.tex` + `labbook/sections/*.tex` | The durable, citable record. A result appears here only after it has passed its gates. |

**Promotion path** — the main workflow of this repo:

```
idea  →  derivation and/or simulation run  →  gates S,D,M,C pass
      →  new or extended shard in labbook/sections/
      →  registered in labbook/SHARD_CATALOG.md + labbook/README.md order table
      →  dated entry appended to labbook/sections/02_lab_log.tex
      →  back-link written into the source idea/run (`shard:` frontmatter field)
```

The Lab Log (`02_lab_log.tex`) is **append-only**. Entries are never rewritten or deleted; a later
entry supersedes an earlier one and says so. That is what makes it a lab book rather than a draft.

Do not promote a result because it looks right. Promote it because the gates ran.

**The lab book carries the physics behind its results.** Every derivation or equation a recorded
result uses — or that is needed to understand it — is written into the lab book alongside the
result, with its tags, not left in working memory. And a session that edited the lab book ends
with a successful `pixi run labbook`: the compiled PDF is part of the deliverable.

## Evidence tags — cited fact versus our inference

Every factual sentence in a note or a lab-book shard carries a tag. **Untagged means unverified.**

| Markdown | LaTeX | Meaning |
|---|---|---|
| `[S:Key §3.2 eq.14]` | `\evS{Key}{§3.2 eq.14}` | stated by a source registered in `literature/SOURCES.md` |
| `[D:2026-07-29-slug]` | `\evD{2026-07-29-slug}` | our derivation, checked, in `derivations/` |
| `[C:2026-07-29-slug]` | `\evC{2026-07-29-slug}` | our computation, run recorded in `runs/` |
| `[I]` | `\evI{}` | **our inference or interpretation** — plausible, not yet checked |
| `[?]` | `\evQ{}` | needs a source or a check |

The two that matter most are `[I]` and `[?]`. An agent that hedges by leaving statements untagged
defeats the whole scheme; an agent that marks its own reasoning `[I]` is doing the job. Never
upgrade `[I]` to `[S:...]` without opening the source and reading the passage.

Standing queries:

```bash
grep -rn '\[?\]' --include='*.md' --include='*.tex' .   # the open-verification queue
grep -rn '\[I\]' --include='*.md' --include='*.tex' .   # our unchecked reasoning
```

## Validation gates

Name the gates you actually ran — in the run README, in the `log/` entry, and in the Lab Log entry.
Claiming a gate you did not run is the one unrecoverable error in this repo.

| Gate | Meaning |
|---|---|
| **S** — Source | the source is registered locally, hash recorded, citation points at a local path |
| **D** — Definition | terms are in `GLOSSARY.md`, conventions in `CONVENTIONS.md` |
| **M** — Math | a derivation or a cited theorem supports the statement |
| **C** — Computation | a run or test checks an invariant, a known limit, or a published number |
| **R** — Review | independently reviewed, or explicitly reviewed by the repository owner |
| **B** — Build | `pixi run check`, `pixi run test`, `pixi run labbook` pass |

"It runs without errors" is not gate C. A useful check tests physics: a conserved quantity, a
known analytic limit, a published number reproduced, or convergence under grid and timestep
refinement. And the check must be **independent of the statement it checks**: verifying an
equation against itself — the same equation re-derived along the same path, or the output of the
same code that implements it — is circular and does not count. Compare against a separately
trusted property.

## Layout

```
labbook.tex            master: preamble + \include order only, no prose
labbook/               shards, catalog, macros
literature/            references.bib, SOURCES.md, pdfs/ (ignored), text/, src/, notes/
ideas/                 brainstorms, hypotheses, open questions
derivations/           quick derivations, worked out and checked
sims/                  simulation code, one directory per simulation
runs/                  one directory per execution: params, data, figures, interpretation
attic/                 failed attempts worth keeping, and why they failed
log/                   session worklogs and handoffs
scripts/check.py       the local consistency gate (`pixi run check`)
INDEX.md               generated index of everything above
TIMELINE.md            the commit line and fork graph (see "Fork the timeline")
ONBOARDING.md          one-time setup steps for a fresh copy; deleted once done
```

Each directory has a `README.md` with its local rules and a `_template.md` where relevant. Read the
directory README before adding a file to it.

## Naming and identifiers

- **Sources**: BibTeX citekey `AuthorYYYYkeyword` (e.g. `Author2024keyword`). The same key names
  `literature/pdfs/<key>.pdf`, `literature/text/<key>.md`, `literature/notes/<key>.md`,
  `literature/src/<key>/`. One key, one paper, everywhere.
- **Ideas, derivations, runs, log and attic entries**: `<YYYY-MM-DD>-<slug>`, lowercase, hyphens.
  The date is the creation date and never changes.
- **Simulations**: `sims/<slug>/` — no date; simulations evolve, runs carry the date.
- **Lab-book shards**: `NB-NN-SLUG`, stable forever once assigned.

Cross-link with relative Markdown links (`../runs/2026-07-29-foo/README.md`), never bare filenames.
`pixi run check` verifies that every link resolves.

## Git policy

- **Work on the current branch** — normally `main`, or the active `fork/...` branch — and commit
  there. No feature branches, no merge step, no PR workflow: this is a single-author notebook and
  the overhead buys nothing. Branches exist for exactly one purpose: user-invoked forks of the
  timeline (next section).
- **Commit as you go**, at the boundaries the notebook already has — a run finished and written
  up, a source registered with its notes, a shard promoted. Do not accumulate a session's work
  into one commit.
- **Commit and push at milestones, without being asked** (push only if a remote `origin` is
  registered). Run the gates, commit with a message that says what was established and which gates
  ran, then push. An uncommitted milestone is a run whose recorded git SHA does not contain the
  run; an unpushed one exists on one machine only. Journal submission and arXiv posting are a
  different matter and stay the owner's.
- **Record each milestone commit in `TIMELINE.md`** — ID, short SHA, branch, one phrase — in the
  same commit. That is what makes the fork graph usable.
- **Never `git add -f` a PDF.** `literature/pdfs/` and `literature/src/` are gitignored on
  purpose.

## Fork the timeline (branch off)

[TIMELINE.md](TIMELINE.md) holds the commit line and the fork graph. Its purpose: when a line of
work goes bad — the context was poisoned by hallucinations, a convention turned out wrong upstream
— or the user wants to switch topic, work continues on a fresh branch from a known-good commit,
and the map of what was abandoned stays visible.

When the user asks to branch off:

1. Show them the commit line from `TIMELINE.md` and agree on the base commit (`C<n>` or SHA) and a
   short slug for the new direction.
2. `git switch -c fork/<YYYY-MM-DD>-<slug> <sha>`.
3. Append the updated graph to `TIMELINE.md`, marking the abandoned tip `✗` with a one-line
   reason, and commit that as the first commit of the fork.
4. Continue working there. Milestone commits keep landing in the commit line as usual.

```
C1 ── C2 ── C3 ✗                    main — abandoned at C3 (poisoned context)
        └── C4 ── C5                fork/2026-08-11-fresh-start   ← current
```

Never rewrite `TIMELINE.md` history — like the lab log, it is append-only. An abandoned line is a
result about the work; deleting it invites re-walking it.

## Workflows

### Explore an idea

1. `grep -ri "<keywords>" ideas/ literature/notes/ derivations/ labbook/` and scan `INDEX.md`
   before creating anything — the idea may already exist under another name.
2. If new: copy `ideas/_template.md` to `ideas/<YYYY-MM-DD>-<slug>.md`, fill the frontmatter,
   write the question, what would confirm it, and what would kill it.
3. Tag every statement. Recollections about the literature are `[?]` until a source is registered.
4. Link to related ideas, sources, derivations and runs as you find them.

### Add a source

1. Obtain the PDF through a lawful route (arXiv, publisher, author, institutional access) and save
   it as `literature/pdfs/<citekey>.pdf` (not tracked by git).
2. **Always try for the upstream source as well**, and unpack it into `literature/src/<citekey>/`.
   For arXiv this is `https://arxiv.org/e-print/<id>` — a tarball with the LaTeX, the figures and
   the authors' own `references.bib`. Other routes: journal supplementary material, the authors'
   GitHub/Zenodo, the data or code repository named in the paper. If no source is available, say so
   in the notes; do not silently skip the attempt.
3. Add the BibTeX entry to `literature/references.bib` with DOI/arXiv ID.
4. Register it in `literature/SOURCES.md`: citekey, full citation, role, URL/DOI, retrieval date,
   local path, SHA256 (`shasum -a 256 literature/pdfs/<key>.pdf`). The citekey, local path and
   SHA256 cells are parsed literally — write them bare, with no backticks.
5. If useful, extract text to `literature/text/<citekey>.md`.
6. Write `literature/notes/<citekey>.md` from `literature/_template.md`: what the paper actually
   claims (with section/equation numbers), what it assumes, what we can use, and — separately —
   what *we* infer from it, tagged `[I]`.
7. **Update `CONVENTIONS.md` and `GLOSSARY.md` in the same session, without being asked.** This is
   part of registering a source, not a follow-up task:
   - every unit, sign, normalisation or notation the source fixes goes into `CONVENTIONS.md`, with
     the invariant that lets a reader *check* it, not merely the statement;
   - every convention that differs from ours gets a row in the **Source translations** table, with
     the conversion and the instruction to apply it on entry;
   - every technical term the source introduces goes into `GLOSSARY.md` with its location.

   A source is not finished being registered until both files are current. Do not queue this for
   the owner's approval and do not defer it to "once the axis is fixed" — an unrecorded convention
   is how a wrong result acquires a correct-looking derivation, and the cost of recording it is
   minutes. Where the right choice genuinely is not ours to make, record the options and the
   trade-off as `[?]` rather than recording nothing.
8. Do not paste long copyrighted excerpts into the repo. Cite location, paraphrase, quote briefly.

**Read the LaTeX source in preference to the rendered PDF when it exists.** The source gives exact
equations rather than glyphs recovered from a rendering, real `\label{}`s to cite, the authors'
own bibliography for follow-up sources, and it greps. A `[S:...]` tag pointing at a LaTeX label is
more auditable than one pointing at a page number. Where a paper's own equations disagree with each
other, the source is what lets you prove it — record the discrepancy as `[I]` in the notes and
resolve it in `CONVENTIONS.md` before any code depends on it.

Cite the location as the reader will find it: section and equation *number* for a published paper,
section plus LaTeX label for a preprint whose equations are auto-numbered.

**Say which version you read, in the tag.** Preprint and published versions differ — in title, in
section numbering, and sometimes in content. A location valid in one is not valid in the other. If
the local file is a preprint, every `[S:...]` from it says so, and the note says plainly at the top
that its tags are not citations to the published article. Registering a source without recording
this is how a citation silently rots.

**Record reading depth.** A note that was skimmed for one number and a note that was read end to
end look identical afterwards. State per source which sections were actually read; a later reader —
including you — needs to know which claims rest on a full reading.

### Acquisition routes that work

Publishers actively block scripted download; these were established by trial on 2026-07-29 and save
a lot of failed attempts.

| Target | Route |
|---|---|
| Any DOI → arXiv ID | Semantic Scholar: `api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,externalIds,openAccessPdf` |
| arXiv PDF and source | `arxiv.org/pdf/<id>` and `arxiv.org/e-print/<id>` — these keep working even when the arXiv **API** returns 503 |
| APS (PRL, PRA, PRResearch) | **Blocked** (HTTP 403) on both `journals.aps.org` and `link.aps.org`. Use the arXiv preprint, or ask for an institutional download |
| Science / Science Advances | **Blocked** (HTTP 403) on `science.org`. Use Europe PMC |
| Europe PMC | metadata `ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"<doi>"&format=json&resultType=core`; full text `.../<PMCID>/fullTextXML`; PDF `europepmc.org/articles/<PMCID>?pdf=render` (the REST `fullTextPDF` endpoint 404s) |
| Nature journals (open access) | `nature.com/articles/<id>.pdf` works directly |
| Bibliographic record | Crossref: `api.crossref.org/works/<doi>` |

Europe PMC full-text XML is the publisher's own text and is authoritative for prose, but **it
strips equations** — anything equation-level must come from the PDF or the LaTeX source.

Reading a PDF requires `pdftoppm` (`brew install poppler`).

### Verify a claim

1. Locate the claim's tag. If untagged, that is the finding — mark it `[?]`.
2. For `[S:...]`, open the local source at the cited location and confirm it says what we say it
   says. Check the convention (units, sign, factor conventions) matches ours in `CONVENTIONS.md`.
3. For `[D:...]`, re-derive independently, or check limits, dimensions and special cases.
4. For `[C:...]`, confirm the run README's command reproduces the recorded number.
5. Record the outcome. A refuted claim is *not deleted*: mark it, correct it, and note what was
   wrong. If it was load-bearing, follow its links and fix what depended on it.

### Run or extend a simulation

1. Code lives in `sims/<slug>/`; each simulation has a README stating the physics, the equations
   solved, the conventions it obeys, and its validation tests.
2. Every execution that produced something worth remembering gets `runs/<YYYY-MM-DD>-<slug>/`
   built from `runs/README.md`'s required structure: hypothesis, sim and git commit SHA, exact
   command, `params.toml`, why these parameters, environment, headline result, interpretation,
   uncertainty, gates, next steps.
3. Record uncertainty honestly: grid and timestep convergence, tolerances, statistical error,
   and which physical effects the model leaves out.
4. Commit small text summaries and vector figures; leave bulk arrays out (see artefact policy) and
   record their size, SHA256 and producing command so they can be regenerated.

### Promote a result into the lab book

Only when gates S, D, M and C have actually run:

1. Extend an existing shard, or add `labbook/sections/NN_<slug>.tex` with the four-line
   `% SHARD-*` header, and `\include` it in `labbook.tex`.
2. Register it in `labbook/SHARD_CATALOG.md` and the order table in `labbook/README.md`.
3. Append a dated entry to `labbook/sections/02_lab_log.tex` naming what was established, the run
   IDs and citekeys behind it, and the gates run.
4. Set `shard:` in the originating idea's frontmatter and set its `status: promoted`.
5. `pixi run check && pixi run labbook`.

### Record a finding

**Whenever something new is established, record it in the lab book in the same session.** Not at
the end of the week. A finding that lives only in a run README or a chat transcript is not part of
the record — and a chat transcript is discarded when the context compacts.

**"Finding" is broader than "positive result."** All of these count and must be written down:

- a derived identity or scaling law, even with no number attached;
- an analysis that answers a design question — including when the answer is *no*, or *only under
  these conditions*, or *this is two orders of magnitude short*;
- a bound, a ceiling, or a reason something cannot work;
- a retraction of something recorded earlier;
- a convention or a discrepancy between sources that changes how a number must be read.

A negative or bounding result is often the most reusable thing in the notebook, because it stops the
next session from re-deriving it. Record it with the same care as a positive one.

**Run provenance takes two commits.** `provenance.json` records `HEAD` at execution time, which is
necessarily the commit *before* the run is committed — so the recorded SHA identifies the
**generator state the run used**, which is what reproduction needs, but does not *contain* the run's
own artefacts. For a run whose result is promoted, close the loop: commit the run, re-execute it from
that commit, and commit the refreshed provenance. `pixi run check` counts the runs where this gap is
open.

**Lab-log shards are split by week, not by date.** Open a new one when the current shard nears the
280-line cap, not whenever the date changes. Name the shard for the week it opens and move nothing
that does not have to move.

1. Append a dated entry to the **newest lab-log shard** — `labbook/sections/02_lab_log.tex` or its
   continuation, whichever is current per `labbook/README.md` — naming what was found, the run and
   sources behind it, and the gates that actually ran.
2. If the finding is substantive rather than incremental, give it a shard: `NN_<slug>.tex`,
   registered in the three places listed in `labbook/README.md`.
3. **Write in the derivations and equations the finding rests on** — the lab book must be readable
   without the working-memory layer.
4. **Add a figure when a figure carries the argument** — a stationary point, a limit being
   approached, a curve whose shape is the result. Not for decoration, and not for a number that a
   sentence states better.
5. Figures are **TikZ/pgfplots reading plain-text `.dat` files** written by the simulation into its
   run directory. The committed artefact is the data, never an image: it stays greppable and
   diffable, the fonts match the document, and the figure is rebuilt from the numbers every time.
   Never hand-type figure data.
6. Say what the finding does *not* establish. That paragraph is usually the most useful one.

### Record a failure

Failed attempts are results. When an approach dies, write `attic/<YYYY-MM-DD>-<slug>.md` (or a
directory, if code is worth keeping): what was tried, why it failed, **what it rules out**, and
what is worth salvaging. Set the originating idea to `status: refuted` or `parked` and link both
ways. Deleting a dead end silently means the next agent will rebuild it.

### Close a session

1. Update the frontmatter (`status`, `updated`) of everything you touched.
2. Write `log/<YYYY-MM-DD>-<slug>.md`: what you did, what you established and with which gates,
   what you deliberately left, and what the next session should pick up first.
3. Run `pixi run check`, and `pixi run labbook` if the lab book changed — the session is not
   finished until the PDF compiles. Fix what they report.
4. `pixi run check --write` to refresh `INDEX.md`.
5. `git status`. Commit when the work is coherent, and push if `origin` is registered — see
   **Git policy**, which makes committing and pushing at milestones the default rather than
   something to ask about.

### Keep the notebook resumable

**The invariant: at every commit, someone who has never seen this work must be able to pick it up
from `INDEX.md` alone.** Not "after a handover conversation" — there is no conversation. A chat
transcript is discarded, and the next session starts cold. This is the same rule as Law 1 applied to
the work's own state rather than to its claims.

Four conditions make that true. `pixi run check` warns when they are not met.

1. **The question exists as a file.** Substantive work has an `ideas/<date>-<slug>.md` stating what
   is being asked, what would confirm it and what would kill it. Write it *before* the work if you
   can, and retroactively if you did not — a retroactive idea note that says so in its `History` is
   worth far more than none. Runs with no idea behind them are results in search of a question.
2. **Every parameter choice records its reason.** `params.toml` says a run used `T = 1.5 ms`; it
   cannot say *why* 1.5 and not 3. Put the why in the run README, marked `[I]` — it is judgement,
   not result. The test: could a reader change the value sensibly without re-deriving your
   reasoning? Grid sizes, box extents, timings and tolerances all need this.
3. **The newest `log/` entry is newer than the newest run**, and ends with a `## Next` section
   naming **one concrete action**, not a wish list. A run with no session log around it is a number
   nobody can place.
4. **Open questions are tagged where they live**, not only in the log. `[?]` and `[I]` in the file
   that carries the claim are what the standing greps find; a caveat that exists only in a session
   log is invisible to `grep -rn '\[?\]'`.

Contradicting instructions are the worst failure of this invariant, because the next agent obeys
whichever it reads first and neither is wrong. If you find two rules in conflict, fix the conflict
in the same commit as the work that exposed it.

## Artefact policy: what is committed

Commit what a reader needs in order to check a claim, and what is cheaper to store than to
regenerate. Everything else must be reconstructible from a recorded command plus `pixi.lock`.

**Committed**: Markdown, LaTeX, BibTeX, code, `pixi.lock`, `params.toml`, run READMEs, summary
CSV/JSON under ~1 MB, vector figures (PDF/SVG) that appear in the lab book.

**Not committed**: source PDFs (`literature/pdfs/`), upstream source blobs (`literature/src/`),
`.pixi/`, caches, LaTeX aux files, `labbook.pdf`, bulk arrays (`*.npy`, `*.h5`, …), anything over
5 MB.

Every ignored artefact that backs a claim gets a stub in its run README — path, size, SHA256, and
the command that produces it. Source PDFs are re-acquirable from `literature/SOURCES.md`.

If large binaries genuinely need versioning later, git-lfs is the escape hatch — but it is not
enabled, and enabling it is a decision to be discussed, not a default.

## Local policy

- **Validation is local.** Run `pixi run check`. Do not add `.github/workflows/` or propose remote
  CI unless explicitly asked.
- **Keep files shardable.** Target ~200 lines per authored Markdown, LaTeX and Python file; hard
  cap 280 lines for lab-book shards. Split growing files and index the pieces.
- **Be skeptical of everything unverified**, including previous sessions' notes, text extracted
  from PDFs, subagent reports, and your own earlier statements in this conversation. Check against
  local files.
- **Fail loudly.** Do not silently reconcile conflicting conventions, quietly drop a citation, or
  downgrade a failed check to a warning. Surface the conflict.
- **Physics conventions are non-negotiable once recorded.** If a new source uses a different
  convention, translate explicitly and record the translation in `CONVENTIONS.md`.

## Commands

```bash
pixi install            # create the environment from pixi.lock
pixi run check          # consistency gate: sources, citekeys, runs, links, lab-book shards
pixi run check --write  # the same, and regenerate INDEX.md
pixi run labbook        # compile labbook.tex -> labbook.pdf (system MacTeX)
pixi run test           # pytest
pixi run lint           # ruff
```
