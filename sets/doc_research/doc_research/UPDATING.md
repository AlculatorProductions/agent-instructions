# UPDATING

The instructions, scripts and slash commands in this notebook come from Scirce, upstream. They can
be updated without touching a single line of your own work.

    bash doc_research/scripts/update.sh

## What it does

`.instructions/manifest` puts every shipped file in one of three classes:

| class | on update |
|---|---|
| `template` | replaced outright. Never edit these. |
| `merge` | three-way merged against the version originally installed. |
| `seed` | written once at install, never touched again. |

Everything not listed — `labbook/entries/`, `calculations/`, `figures/`, `log/weekly/`, and all of
the repository's own code — is invisible to the updater by construction. It cannot be modified.

`.instructions-source` also records how pixi was wired up at install time
(`pixi=toml` / `pyproject` / `none`). When it is not `toml`, the updater never writes a
`pixi.toml` — pixi prefers that file over `pyproject.toml`, so dropping one in would silently
shadow the repository's own manifest.

`.instructions/baseline/` holds a pristine copy of the set as it was installed. That is what makes
the three-way merge possible, and it is also how `python3 doc_research/scripts/check.py` can tell you when a `template`
file has been hand-edited.

The updater refuses to run on a dirty worktree, and commits the result itself — including any
conflict markers — so `git revert` undoes the whole update in one step.

## If it reports conflicts

A conflict means a `merge`-class file was changed both upstream and locally. The file contains
standard markers:

    <<<<<<< yours
    ...
    ||||||| template (installed)
    ...
    =======
    ...
    >>>>>>> template (new)

Resolve them, keeping the local content and taking the upstream change around it, then:

    python3 doc_research/scripts/check.py
    git add -A && git commit -m "Resolve instruction update conflicts"

Ask about anything where the two sides genuinely disagree. Do not guess.

## If a template file was hand-edited

`python3 doc_research/scripts/check.py` warns about this. The edit will be lost at the next update. Either the change
belongs in `TASTE.md` (a preference) or in `FEEDBACK.md` (a rule that is wrong here) — move it
to whichever fits and restore the template file from `.instructions/baseline/`.
