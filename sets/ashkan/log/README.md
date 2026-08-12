# log/

Session worklogs and handoffs: `log/<YYYY-MM-DD>-<slug>.md`, one per working session.

This is the notebook's chronological record and its short-term memory. It answers "what was I
doing, and what did I leave half-done" — the question that costs the most time when a session
resumes cold — and, through its **Established** sections, when a result was established and on
what evidence. Durable results themselves do not live here: they are promoted into lab-book
shards, and the log entry records that it happened, with the gates.

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

Once its session is over, an entry is not rewritten. A later entry supersedes an earlier one and
says so — that is what lets `log/` serve as the notebook's chronology.

Say what did not work, and say what you skipped. A log that only records successes is the most
expensive kind of log, because the next session repeats the failures.
