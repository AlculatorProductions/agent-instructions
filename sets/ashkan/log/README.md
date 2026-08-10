# log/

Session worklogs and handoffs: `log/<YYYY-MM-DD>-<slug>.md`, one per working session.

This is short-term memory. It answers "what was I doing, and what did I leave half-done" — the
question that costs the most time when a session resumes cold. Durable results do not live here;
they are promoted into the lab book. If everything in a log entry matters in six months, it should
have been a lab-log entry.

## What an entry says

```markdown
---
id: YYYY-MM-DD-slug
title: "Session focus"
status: active
confidence: medium
tags: []
sources: []
derivations: []
runs: []
updated: YYYY-MM-DD
---

# YYYY-MM-DD — Session focus

## Did
What actually happened, with links to the files touched.

## Established
Results, each with the gates that ran. Nothing here without a gate.

## Left open
Deliberately unfinished, with enough context to resume. Mark anything unverified `[?]`.

## Next
The first thing the next session should do — one concrete action, not a wish list.
```

## Discipline

Write the entry at the end of the session, before committing. An entry written the next day is a
reconstruction, and reconstructions quietly invent tidy narratives that the files do not support.

Say what did not work, and say what you skipped. A log that only records successes is the most
expensive kind of log, because the next session repeats the failures.

## Relation to the lab log

`log/` is per-session and revisable; the lab log in `labbook/sections/02_lab_log.tex` is
append-only and holds only what was established. Most sessions produce a `log/` entry and no lab-log
entry — that is normal, and it is the point of having both.
