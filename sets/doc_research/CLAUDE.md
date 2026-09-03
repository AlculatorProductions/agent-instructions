# CLAUDE.md

This repository keeps a written research record alongside the code — Scirce — in
[doc_research/](doc_research/). Everything belonging to it lives in that one folder.

**Read [doc_research/CLAUDE.md](doc_research/CLAUDE.md) at the start of every session, then
[doc_research/TASTE.md](doc_research/TASTE.md).** Those are the rules; this file only points at
them.

The short version, so that nothing is missed even if the file above is not loaded:

- Code you write gets a `# [claude YYYY-MM-DD] unchecked` marker on the line above it.
- Work that produces mathematics, code or a figure gets an entry in the lab book.
- Every figure needs a plain-language caption file next to it.
- On a Friday, offer the week's summary once.
- Preferences stated in the chat go into `doc_research/TASTE.md` and override these rules;
  things that do not work go into `doc_research/FEEDBACK.md`.

Before committing, run `python3 doc_research/scripts/check.py`. That is for you, the agent —
the researcher works through the chat and never needs to run anything.
