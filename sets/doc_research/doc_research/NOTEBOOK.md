# Scirce — your research notebook

This folder keeps a written record of your work alongside the code, so that you can look back and
find out what you did, why, and whether it was checked.

**You work the way you already do.** Talk to Claude Code in the chat as normal — ask for code,
paste a calculation, ask a question. The record gets written as a side effect. There are no
commands for you to run and no files for you to fill in.

## It starts empty, and fills up

Right now `labbook.pdf` and `worklog.pdf` are nearly empty, and `figures/` and `calculations/` have
nothing in them. **That is the correct starting state.** Nothing is missing and nothing is broken.

They fill up as you work. Ask for a piece of code and an entry appears. Paste a calculation and it
is transcribed. Make a plot and it gets an explanation written next to it. After a few weeks the
lab book is worth reading; on day one it is nearly blank, and that is fine.

You never write the `.tex` files by hand. The agent does that. If you ever open one and see `TODO`
in it, that is the agent's own scaffolding, not a task for you.

## What is here

| | |
|---|---|
| `labbook.pdf` | The technical record: your calculations, transcribed to LaTeX, and the code that came out of them. Chronological. |
| `worklog.pdf` | Week-by-week summaries: what you worked on, what came out, what is still open. |
| `figures/` | Every plot, each with a short plain-language explanation of what it shows. |
| `calculations/` | The photos of your handwritten calculations, next to their transcriptions. |
| `TASTE.md` | Your rules for how the agent behaves. |
| `FEEDBACK.md` | Things that did not work, collected to be sent back. |

## Four things worth knowing

**Nothing is remembered outside these files.** There is no hidden memory of what you think or how
you work. Everything the agent knows about this project is a dated file you can read, change or
delete — and deleting it really does delete it.

**You change the agent by saying so.** "Shorter messages." "Stop explaining every step." "Plot it
the way I do." It writes the rule into `TASTE.md` and follows it from then on. You never have to
edit a configuration file.

**When something annoys you, it gets written down.** If you say you do not understand a plot, or
correct the same thing twice, the agent logs it in `FEEDBACK.md` — what you were doing, what went
wrong, and which of the shipped instructions was at fault. Send that file back to whoever set this
up whenever you like, and it gets fixed for everyone. It stays on your machine until you do.

**Fridays.** On any Friday the agent offers to write the week's summary into `worklog.pdf`. Say no
if you are busy; it will ask again next week.

## Code the agent wrote

Anything the agent writes is marked:

```python
# [claude 2026-08-28] unchecked
```

Once you have read it and are happy, say so in the chat — the marker becomes
`# [checked <you> 2026-09-02]`. The weekly summary counts what is still unchecked, so the parts of
the codebase you have not personally read stay visible.

## Your calculations

Paste a photo of a handwritten calculation into the chat. The agent transcribes it into the lab
book exactly as written — your notation, your steps — and writes the code from it.

Afterwards it checks the mathematics. If it thinks it has found a mistake it will show you the
step, the evidence, and a proposed fix. **It never changes your mathematics itself.** You decide,
and whichever way you decide is recorded.

## If you get stuck

Ask the agent, in the chat. `CLAUDE.md` in this folder is the full rulebook if you ever want to see
what it has been told.
