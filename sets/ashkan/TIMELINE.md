# TIMELINE

The commit line and fork history of this notebook — the map for going back. When a line of work
goes bad — poisoned context, a wrong turn, or just the feeling that the notes no longer reflect
your research — work continues on a fresh branch from an earlier commit, and this file is where
that commit is found and where the fork is recorded.

**To go back, you never need git.** Telling the agent is enough — "I want to go back", "this
stopped feeling like my project" — and it follows [FORKING.md](FORKING.md): it asks what feels
wrong, shows you what the notebook looked like at candidate commits, and does all the git work.

## Reading the commit line

The table below is **generated from git history** — `pixi run check --write` refreshes it, and
the agent refreshes it before any fork. Do not edit it by hand; a commit cannot contain its own
SHA, so the table always describes the commits that exist at refresh time.

A ✓ marks a commit whose message names passed gates — a technically sound anchor. The right
commit to go back to is *not* necessarily the last ✓: when the reason for going back is drift or
taste rather than a defect, invoke the fork protocol and judge the snapshots yourself.

<!-- BEGIN:GENERATED timeline -->
_no commits yet_
<!-- END:GENERATED timeline -->

## Forks

Hand-written and **append-only**: one block per fork, newest last. Each block records the base
commit (C-number and short SHA), the abandoned tip marked ✗, and — most importantly — the reason
in the user's own words: the subjective why is the one thing git cannot store. Never rewrite an
old block; an abandoned line is a result about the work.

Format:

    ### YYYY-MM-DD — fork/YYYY-MM-DD-<slug> from C2 (91be044)
    Abandoned: main at C3 ✗ — hallucinated source claims contaminated the idea note.

    C1 ── C2 ── C3 ✗                  main
            └── C4 ── …               fork/YYYY-MM-DD-<slug>   ← current

_no forks yet — everything on `main`_
