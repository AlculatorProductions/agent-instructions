# figures/

Every plot, with an explanation of what it shows.

Figures are produced by Erin's own plotting code, in her own style — no plotting library, palette
or house style is imposed by this notebook.

## The rule

Every figure file has a sibling `<name>.md`, from `_template.md`. `pixi run check` fails if one is
missing.

```
figures/spectrum-vs-cutoff.pdf
figures/spectrum-vs-cutoff.md
```

The caption file is written for someone who is tired and has twenty seconds. In particular the
**Axes** section explains both axes in words, with units, including the ones that look obvious —
that is the section that stops a plot from becoming unreadable three months later.

## New kinds of plot

Before making a kind of plot Erin has not seen before — a convergence check, a sweep against a
cutoff, a residual plot, anything diagnostic rather than physical — the agent says in at most
three sentences what it shows and why that kind of plot is the right one. Then it makes it.

An unexplained diagnostic plot is worse than no plot.
