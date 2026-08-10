# ONBOARDING

One-time steps when this notebook is instantiated as a fresh repository. An agent may perform all
of them; each is safe to re-run.

- [ ] **Git identity.** `git config user.name` and `user.email` are set, and the repository has an
      initial commit.
- [ ] **Project name.** Replace the placeholder name in `pyproject.toml` (`[project].name`),
      the `README.md` title, and `labbook.tex` (`\title{...}`).
- [ ] **Author.** Set `\author{...}` in `labbook.tex` from `git config user.name`.
- [ ] **Environment.** `pixi install`, then commit the generated `pixi.lock` — the artefact policy
      in [AGENTS.md](AGENTS.md) assumes the lock file is committed, and run provenance hashes it.
- [ ] **LaTeX.** A system TeX installation with `latexmk` and `biber` (MacTeX on macOS —
      `brew install --cask mactex`). `pixi run labbook` must produce `labbook.pdf`.
- [ ] **PDF tooling** (optional, for reading and extracting sources): `brew install poppler`.
- [ ] **Gate.** `pixi run check` and `pixi run test` pass clean.
- [ ] **Finish.** Delete this file and remove the two pointers to it (in `README.md` Quickstart
      and `AGENTS.md` Entry point), then commit.
