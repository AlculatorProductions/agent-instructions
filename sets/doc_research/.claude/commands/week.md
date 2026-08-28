---
description: Write this week's summary into the work log
---

Write the weekly summary for $ARGUMENTS (default: this week).

1. Run `python3 doc_research/scripts/weekly.py` — with `--week YYYY-Www` if a week was named.
   It builds the skeleton from git history, so the commits, entries, figures and unchecked-code
   counts in it are already real. Do not invent any of them.
2. Fill in every `TODO`:
   - **What you worked on** — plain language, at most five bullets, no jargon that has to be
     looked up. This is the part that actually gets read.
   - **Results** — only claims with a figure, calculation or run behind them; name the evidence.
     Anything unverified says so in the sentence itself.
   - **Code** — what changed and why, not a restatement of the commit list.
   - **Open questions** — including anything you flagged in a calculation that has not been
     decided on yet, and anything worth taking to ChatGPT or a colleague.
   - **To paste elsewhere** — three or four plain lines for a chat message, sent by hand if at all.
3. If `doc_research/FEEDBACK.md` gained entries this week, add one line saying how many, and that
   the file can be sent back to whoever set the notebook up.
4. Run `python3 doc_research/scripts/build_entries.py`, then `python3 doc_research/scripts/check.py`.
5. Commit.

Read the sources before writing prose — the lab book entries of the week, the figure caption
files, the calculation folders. A summary assembled only from commit subjects is not worth having.
