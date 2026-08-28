---
description: Walk through agent-written code that has not been checked yet
---

Erin wants to go through code she has not read yet.

1. Run `python3 scripts/doc_research/check.py` and take the unchecked list.
2. Take them oldest first, unless $ARGUMENTS names a file.
3. For each one, show her: the code, what it computes in two sentences, which equations in the lab
   book it corresponds to, and anything about it you are not confident in. Be honest about the
   last part — this is the whole point of the exercise.
4. If she says it is fine, change the marker from `# [claude YYYY-MM-DD] unchecked` to
   `# [checked erin <today>]` and tell her which file and line you changed.
5. If she wants changes, make them, and the marker resets to `# [claude <today>] unchecked`.

Stop when she wants to stop — do not push through the whole list. Commit what was checked.
