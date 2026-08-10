# agent-instructions

Instruction sets that turn an empty folder into an **agent-ready research repository** — a git
repo whose structure, rules and workflows a coding agent (Codex, Claude Code, or anything else
that reads `AGENTS.md`) can pick up cold. One command sets everything up.

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

| Set | What it is |
|---|---|
| [ashkan](sets/ashkan/) | A research notebook for theoretical and computational physics: provenance-tagged notes, a gated LaTeX lab book, reproducible simulation runs, and a fork-able timeline. |

Each set is self-documenting — its own `README.md` explains the layout, its `AGENTS.md` is the
canonical rulebook for agents.

## Requirements

- macOS. Everything the script itself needs ships with the OS (curl, tar, git, perl).
- The one-liner requires this repository to be **public**. If it is private, clone it first
  (GitHub Desktop is the easiest way) and run `./setup.sh` from the clone.
- MacTeX is only needed by sets with a LaTeX lab book, and only to compile the PDF.

## Adding a new set (maintainers)

Create `sets/<name>/` with:

- `AGENTS.md` at its root — the canonical agent rulebook; agents read it automatically.
- an `ONBOARDING.md` checklist for one-time machine/user setup, written so an agent can execute
  it and told to delete itself when done.
- optionally, the placeholders `setup.sh` personalises: `name = "research-notebook"` in
  `pyproject.toml`, `\title{Research Notebook --- Lab Book}` and an empty `\author{}` in
  `labbook.tex`, and the H1 of `README.md`.

Write the set as if it were the root of its own repository — that is what it becomes.

## Updating an existing repository

Every generated repository carries `.instructions-source` (set name + source commit). For now,
updates are manual: point your agent at this repository and ask it to compare and merge what
changed since that commit. If this needs to scale, the plan is to move the sets to a
[Copier](https://copier.readthedocs.io) template so `copier update` does three-way merges — the
`.instructions-source` stamp preserves the information needed to migrate.
