# TIMELINE

The notebook's commit line and fork graph. This is the map for **branching off**: when a line of
work goes bad — context poisoned by hallucinations, a convention wrong upstream — or the topic
changes, work continues on a fresh branch from a known-good commit, and this file records where and
why. The workflow is in [AGENTS.md](AGENTS.md), section *Fork the timeline*.

Maintained by the agent, **append-only**: a milestone row is added with every milestone commit, a
graph is appended at every fork. Never rewrite history here — an abandoned line, marked `✗`, is a
result about the work; deleting it invites re-walking it.

## How to branch off

Tell the agent which commit to restart from (`C<n>` or a SHA) — or ask it to show this table and
help you choose. The agent then creates `fork/<YYYY-MM-DD>-<slug>` at that commit, appends the new
graph below with the abandoned tip marked `✗` and a one-line reason, commits, and continues there.

## Commit line

One row per milestone commit, newest last. The phrase says what the commit established, in the
same terms as its `log/` entry.

| ID | SHA | Branch | What happened |
|---|---|---|---|

_none yet_

## Fork graph

Appended at every fork; the newest graph is the current state. Example of the format:

```
C1 ── C2 ── C3 ✗                    main — abandoned at C3 (poisoned context)
        └── C4 ── C5                fork/2026-08-11-fresh-start   ← current
```

_no forks yet — everything on `main`_
