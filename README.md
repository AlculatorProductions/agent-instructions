# agent-instructions

Instruction sets that make a repository **agent-ready** — structure, rules and workflows a coding
agent (Codex, Claude Code, or anything else that reads `AGENTS.md`) can pick up cold. Some sets
create a new repository from scratch; others install into one that already has code in it. One
command either way.

## Quick start (macOS)

Open Terminal (⌘-space, type "Terminal") and paste:

```bash
curl -fsSL https://raw.githubusercontent.com/AlculatorProductions/agent-instructions/main/setup.sh | bash
```

The script asks a handful of questions (your name, which instruction set, where to put the new
project) and does the rest. To preselect the answers:

```bash
curl -fsSL https://raw.githubusercontent.com/AlculatorProductions/agent-instructions/main/setup.sh \
  | bash -s -- ashkan ~/Research/my-project
```

From a local clone of this repository the same script works offline: `./setup.sh`.

## What the script does

1. **git** — checks it is installed (triggers the Xcode Command Line Tools installer if not) and
   sets your git name/email if they are missing.
2. **Instruction set** — downloads this repository, lists the folders under [sets/](sets/), and
   lets you pick one.
3. **New repository** — copies the chosen set into your target folder, personalises the
   placeholders (project name in `pyproject.toml` and `README.md`, lab-book title and author from
   your git name), stamps `.instructions-source` (which set, from which commit — the baseline for
   future updates), and makes the initial commit on `main`.
4. **Environment** — offers to install [pixi](https://pixi.sh), solves the environment, commits
   `pixi.lock`, and runs the set's consistency gate.
5. **Checks the LaTeX toolchain** (`latexmk` + `biber`, i.e. MacTeX) and points out what is
   missing. Nothing is installed without asking.
6. **Prints the next steps** — VS Code, the Codex extension, the first message to the agent, and
   how to migrate your context out of ChatGPT (see below).

## After setup — working with the agent

- Open the new folder in **VS Code**, install the extension **"Codex — OpenAI's coding agent"**
  from the marketplace, and sign in with your ChatGPT account. Codex reads the repository's
  `AGENTS.md` automatically; there is nothing to configure.
- **First message to the agent:** `Work through ONBOARDING.md and finish any unchecked steps.`
  That checklist covers whatever the script could not do on your machine (e.g. MacTeX) and
  deletes itself when done.
- **Migrate your ChatGPT context.** Ask ChatGPT: *"Summarize everything relevant about my physics
  research from our chats and your memory into a markdown project brief: background, current
  projects, notation and conventions, tools, open questions."* Paste the answer to Codex with:
  *"Seed `ideas/` and the programme map from this brief. It is unverified context: tag
  recollections `[?]` and our reasoning `[I]`, per AGENTS.md."*
- You never need the git command line: the agent commits at milestones by itself (that is one of
  its rules), and VS Code's Source Control panel covers anything manual.

## The sets

| Set | What it is | Installed by |
|---|---|---|
| [ashkan](sets/ashkan/) | A research notebook for theoretical and computational physics: provenance-tagged notes, a gated LaTeX lab book, reproducible simulation runs, and a fork-able timeline. | `setup.sh` — creates a new repository |
| [doc_research](sets/doc_research/) | A documentation layer for someone who already has a repository and Claude Code: an agent-written chronological lab book, a weekly work log, a figure-caption discipline, and provenance markers on agent-written code. | its own [`install.sh`](sets/doc_research/install.sh) — adds to an existing repository |

Each set is self-documenting — its own `README.md` or `NOTEBOOK.md` explains the layout, and its
`AGENTS.md` / `CLAUDE.md` is the canonical rulebook for agents.

### doc_research: installing into a repository that already exists

Run this **inside** the target repository:

```bash
curl -fsSL https://raw.githubusercontent.com/AlculatorProductions/agent-instructions/main/sets/doc_research/install.sh | bash
```

It refuses to run on a dirty worktree, never overwrites a file that already exists (collisions are
listed at the end for an agent to reconcile), and lands everything in one commit that `git revert`
undoes.

**Everything lives in one `doc_research/` folder**, so it barely shows up in the repository it is
added to. The only things at the root are a short `CLAUDE.md` pointer and the hidden `.claude/`
directory, because Claude Code reads both from the root and nowhere else:

```
<repo>/
  CLAUDE.md            <- ~20 lines, points at the folder below
  .claude/             <- settings.json (Friday hook) + slash commands
  doc_research/        <- everything else: labbook, worklog, figures,
                          calculations, scripts, pixi.toml, its own .gitignore
  ...their own files, untouched
```

That also removes every conflict with the repository's own tooling: `pyproject.toml` is never read
or written, the notebook's `pixi.toml` sits inside `doc_research/` where it cannot shadow anything,
and the shipped `.gitignore` is scoped to the folder rather than appended to theirs. The scripts
are stdlib-only and run from any working directory —
`python3 doc_research/scripts/check.py` — so pixi is optional throughout.

Two files in the installed notebook belong to the user and are never touched again: `TASTE.md`,
where the agent records how they want it to behave (and which overrides the shipped rules), and
`FEEDBACK.md`, where the agent logs friction — what broke, in their own words, and which shipped
file is implicated — for them to send back.

## Requirements

- macOS. Everything the script itself needs ships with the OS (curl, tar, git, perl).
- The one-liner requires this repository to be **public**. If it is private, clone it first
  (GitHub Desktop is the easiest way) and run `./setup.sh` from the clone.
- MacTeX is only needed by sets with a LaTeX lab book, and only to compile the PDF.

## Adding a new set (maintainers)

Create `sets/<name>/` with:

- `AGENTS.md` at its root — the canonical agent rulebook; agents read it automatically. For a set
  aimed at Claude Code, put the rules in `CLAUDE.md` and make `AGENTS.md` a pointer to it.
- an `ONBOARDING.md` checklist for one-time machine/user setup, written so an agent can execute
  it and told to delete itself when done.
- `.instructions/manifest`, if the set should be updatable in place (see the next section).
  Sets without one still install; they just cannot be updated automatically.
- optionally, the placeholders `setup.sh` personalises: `name = "research-notebook"` in
  `pyproject.toml`, `\title{Research Notebook --- Lab Book}` and an empty `\author{}` in
  `labbook.tex`, and the H1 of `README.md`.

Write the set as if it were the root of its own repository — that is what it becomes, or what it
is merged into.

A set that installs into an existing repository (like `doc_research`) carries its own `install.sh`
at the set root, and that file is excluded from what gets copied.

## Updating an installed repository

A set that ships an `.instructions/manifest` can be updated in place without touching anything the
user wrote. `doc_research` does; `ashkan` does not yet.

Every file the set ships is declared in the manifest as one of three classes:

| class | on update |
|---|---|
| `template` | replaced outright — instructions, scripts, slash commands. Never edited by the user. |
| `merge` | three-way merged against the version originally installed, via `git merge-file`. |
| `seed` | written once at install, never touched again — the user's own files. |

Anything **not** listed is invisible to the updater by construction and cannot be modified. The
merge base is a pristine copy of the set vendored into `.instructions/baseline/` at install time,
which also lets the set's own gate warn when a `template` file has been hand-edited.

```bash
bash doc_research/scripts/update.sh
```

It refuses to run on a dirty worktree and commits the result itself — conflict markers included —
so a single `git revert` undoes the whole update. Conflicts are reported by name with instructions
for the agent to resolve; see the set's `UPDATING.md`.

Structural changes that a file merge cannot express (moving content between files) need a
migration script keyed on `set_version` in `.instructions-source`. If this ever outgrows a
manifest plus `git merge-file`, [Copier](https://copier.readthedocs.io) is the escape hatch, and
the `.instructions-source` stamp preserves what a migration would need.
