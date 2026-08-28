# figures/

Every plot, with an explanation of what it shows.

Figures are produced by the researcher's own plotting code, in their own style — no library, palette
or house style is imposed by this notebook.

## The rule

Every figure file has a sibling `<name>.md`, from `_template.md`. `python3 doc_research/scripts/check.py` fails if one is
missing.

```
figures/spectrum-vs-cutoff.pdf
figures/spectrum-vs-cutoff.md
```

The caption file is written for someone who is tired and has twenty seconds. In particular the
**Axes** section explains both axes in words, with units, including the ones that look obvious —
that is the section that stops a plot from becoming unreadable three months later.

## New kinds of plot

Before making a kind of plot the researcher has not seen before — a convergence check, a sweep against a
cutoff, a residual plot, anything diagnostic rather than physical — the agent says in at most
three sentences what it shows and why that kind of plot is the right one. Then it makes it.

An unexplained diagnostic plot is worse than no plot.
