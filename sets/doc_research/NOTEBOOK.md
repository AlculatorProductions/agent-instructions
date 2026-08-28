# Research notebook

This repository keeps a written record of your work alongside the code, so that you can look back
and find out what you did, why, and whether it was checked.

## What is here

| | |
|---|---|
| `labbook.pdf` | The technical record: your calculations, transcribed to LaTeX, and the code that came out of them. Chronological. |
| `worklog.pdf` | Week-by-week summaries: what you worked on, what came out, what is still open. |
| `figures/` | Every plot, each with a short plain-language explanation of what it shows. |
| `calculations/` | The photos of your handwritten calculations, next to their transcriptions. |
| `TASTE.md` | Your rules for how the agent behaves. |
| `FEEDBACK.md` | Things that did not work, collected for us. |

## Four things worth knowing

**Nothing is remembered outside these files.** There is no hidden memory of what you think or how
you work. Everything the agent knows about this project is a dated file you can read, change or
delete — and deleting it really does delete it.

**You change the agent by saying so.** "Shorter messages." "Stop explaining every step."
"Plot it the way I do." It writes the rule into `TASTE.md` and follows it from then on. You never
have to edit a configuration file.

**When something annoys you, it gets written down.** If you say you do not understand a plot, or
correct the same thing twice, the agent logs it in `FEEDBACK.md` — what you were doing, what went
wrong, and which of our instructions was at fault. Send that file to Gabriel whenever you like,
and we fix it for everyone. It stays on your machine until you do.

**Fridays.** On any Friday the agent offers to write the week's summary into `worklog.pdf`. Say no
if you are busy; it will ask again next week.

## Code the agent wrote

Anything the agent writes is marked:

```python
# [claude 2026-08-28] unchecked
```

Once you have read it and are happy, say so — the marker becomes `# [checked erin 2026-09-02]`.
`pixi run check` lists everything still unchecked, and the weekly summary counts it, so the parts
of the codebase you have not personally read stay visible.

## Your calculations

Paste a photo of a handwritten calculation into the chat. The agent transcribes it into the lab
book exactly as written — your notation, your steps — and writes the code from it.

Afterwards it checks the mathematics. If it thinks it has found a mistake it will show you the
step, the evidence, and a proposed fix. **It never changes your mathematics itself.** You decide,
and whichever way you decide is recorded.

## If you get stuck

Ask the agent. `CLAUDE.md` is the full rulebook if you ever want to see what it has been told.
