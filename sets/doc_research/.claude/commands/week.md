---
description: Write this week's summary into the work log
---

Write the weekly summary for $ARGUMENTS (default: this week).

1. Run `python3 scripts/doc_research/weekly.py` — with `--week YYYY-Www` if a week was named.
   It builds the skeleton from git history, so the commits, entries, figures and unchecked-code
   counts in it are already real. Do not invent any of them.
2. Fill in every `TODO`:
   - **What you worked on** — plain language, at most five bullets, no jargon that has to be
     looked up. This is the part Erin actually reads.
   - **Results** — only claims with a figure, calculation or run behind them; name the evidence.
     Anything unverified says so in the sentence itself.
   - **Code** — what changed and why, not a restatement of the commit list.
   - **Open questions** — including anything you flagged in her calculations that she has not
     decided on yet, and anything worth taking to ChatGPT or a colleague.
   - **To paste elsewhere** — three or four plain lines for a chat message. She sends it herself.
3. If `FEEDBACK.md` gained entries this week, add one line saying how many, and that she can send
   the file to Gabriel.
4. Run `python3 scripts/doc_research/build_entries.py`, then `python3 scripts/doc_research/check.py`.
5. Commit.

Read the sources before writing prose — the lab book entries of the week, the figure caption
files, the calculation folders. A summary assembled only from commit subjects is not worth having.
