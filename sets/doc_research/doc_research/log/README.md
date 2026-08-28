# log/

The work log — what happened, week by week. Built into `worklog.pdf` by `cd doc_research && latexmk -pdf worklog.tex`.

Separate from the lab book on purpose. The lab book answers "how does this work"; the work log
answers "what did I do, and what is still open". Nothing in the lab book depends on it.

| | |
|---|---|
| `../worklog.tex` | master file. |
| `weeks.tex` | generated include list. Never edit by hand. |
| `weekly/` | one `.tex` per ISO week, `YYYY-Www.tex`. |

## Writing a week

`python3 doc_research/scripts/weekly.py` builds the skeleton for the current week from git history — commits, entries
touched, figures produced, calculations added, code still unchecked — with `TODO` markers where
prose is needed. The agent fills those in, then runs `python3 doc_research/scripts/build_entries.py` and commits.

Sections, in order:

1. **What you worked on** — plain language, five bullets at most. No jargon that has to be looked up.
2. **Results** — only claims with a figure, a run or a calculation behind them. Anything unverified says so.
3. **Code** — what changed and why, not a commit list.
4. **New figures** — each with its one-line meaning, linked to its caption file.
5. **Still unchecked** — agent-written code awaiting the researcher's read.
6. **Open questions** — things to take to ChatGPT or to a colleague.
7. **To paste elsewhere** — three or four lines that can be pasted into a chat message. The only
   export from this repository, and it is done by hand.

## Fridays

On any Friday, an agent offers this once at the start of the session, before anything else. On
other days it does not bring it up. If the answer is no, that is the end of it until next week.
