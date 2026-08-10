#!/usr/bin/env bash
#
# setup.sh — create a new agent-ready research repository from an instruction
# set in https://github.com/AlculatorProductions/agent-instructions
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/AlculatorProductions/agent-instructions/main/setup.sh | bash
#   curl -fsSL .../setup.sh | bash -s -- <set> <target-dir>   # preselect answers
#   ./setup.sh [<set>] [<target-dir>]                         # from a local clone (offline)
#
# macOS-oriented. Needs only tools that ship with macOS (curl, tar, git via the
# Xcode Command Line Tools, perl). Offers to install pixi; never installs
# anything without asking.

set -euo pipefail

REPO_OWNER="AlculatorProductions"
REPO_NAME="agent-instructions"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}"
BRANCH="main"

step() { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

case "${1:-}" in
  -h|--help) sed -n '2,14p' "$0" 2>/dev/null || true; exit 0 ;;
esac

# Interactive input must come from the terminal, not from the pipe feeding
# this script to bash. Without a terminal, defaults are used silently.
if { : </dev/tty; } >/dev/null 2>&1; then HAVE_TTY=1; else HAVE_TTY=0; fi

prompt() { # prompt <question> [default] -> stdout
  local q="$1" def="${2:-}" reply=""
  if [ "$HAVE_TTY" = 1 ]; then
    if [ -n "$def" ]; then printf '%s [%s] ' "$q" "$def" > /dev/tty
    else printf '%s ' "$q" > /dev/tty; fi
    IFS= read -r reply < /dev/tty || true
  fi
  if [ -n "$reply" ]; then printf '%s' "$reply"; else printf '%s' "$def"; fi
}

SET_ARG="${1:-}"
TARGET_ARG="${2:-}"

# --- git and identity --------------------------------------------------------

step "Checking git"
if ! git --version >/dev/null 2>&1; then
  warn "git is not installed. macOS will now offer the Command Line Tools installer."
  xcode-select --install || true
  die "finish that installation, then run this script again"
fi

if [ -z "$(git config --global user.name 2>/dev/null || true)" ]; then
  name="$(prompt 'Your full name (for git commits and the lab book):')"
  [ -n "$name" ] || die "git identity is not set and no terminal to ask — run: git config --global user.name \"Your Name\""
  git config --global user.name "$name"
fi
if [ -z "$(git config --global user.email 2>/dev/null || true)" ]; then
  email="$(prompt 'Your email (for git commits):')"
  [ -n "$email" ] || die "git email is not set and no terminal to ask — run: git config --global user.email you@example.com"
  git config --global user.email "$email"
fi
GIT_NAME="$(git config --global user.name)"
echo "git ok — committing as ${GIT_NAME}"

# --- locate the instruction sets: local clone if possible, else download -----

SRC=""
COMMIT="unknown"
SCRIPT_PATH="${BASH_SOURCE[0]:-}"
if [ -n "$SCRIPT_PATH" ] && [ -f "$SCRIPT_PATH" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
  if [ -d "$SCRIPT_DIR/sets" ]; then
    SRC="$SCRIPT_DIR"
    COMMIT="$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
    echo "using local instruction sets in $SRC/sets"
  fi
fi
if [ -z "$SRC" ]; then
  step "Downloading instruction sets from ${REPO_URL}"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL "${REPO_URL}/archive/refs/heads/${BRANCH}.tar.gz" | tar -xz -C "$TMP" \
    || die "download failed — the repository must be public and reachable. If it is private, clone it and run ./setup.sh from the clone."
  SRC="$TMP/${REPO_NAME}-${BRANCH}"
  COMMIT="$(curl -fsSL "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${BRANCH}" 2>/dev/null \
            | grep -m1 '"sha"' | cut -d'"' -f4 || true)"
  [ -n "$COMMIT" ] || COMMIT="unknown"
fi

# --- choose the set ----------------------------------------------------------

step "Choosing an instruction set"
SETS=()
for d in "$SRC/sets"/*/; do
  [ -d "$d" ] || continue
  SETS+=("$(basename "$d")")
done
[ "${#SETS[@]}" -gt 0 ] || die "no instruction sets found under sets/"

if [ -z "$SET_ARG" ]; then
  if [ "${#SETS[@]}" -eq 1 ]; then
    SET_ARG="${SETS[0]}"
    echo "only one set available: ${SET_ARG}"
  else
    i=1
    for s in "${SETS[@]}"; do echo "  $i) $s"; i=$((i+1)); done
    n="$(prompt 'Which set? (number)' '1')"
    case "$n" in (''|*[!0-9]*) die "not a number: $n" ;; esac
    [ "$n" -ge 1 ] && [ "$n" -le "${#SETS[@]}" ] || die "invalid selection: $n"
    SET_ARG="${SETS[$((n-1))]}"
  fi
fi
[ -d "$SRC/sets/$SET_ARG" ] || die "no such set: $SET_ARG (available: ${SETS[*]})"
echo "set: ${SET_ARG}"

# --- create the repository ---------------------------------------------------

step "Creating the new repository"
if [ -z "$TARGET_ARG" ]; then
  project="$(prompt 'Name of the new project folder:' 'my-research')"
  parent="$(prompt 'Create it inside:' "$HOME")"
  TARGET_ARG="${parent}/${project}"
fi
TARGET="${TARGET_ARG/#\~/$HOME}"
PROJECT_NAME="$(basename "$TARGET")"

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  die "$TARGET already exists and is not empty — choose another location"
fi
mkdir -p "$TARGET"
cp -R "$SRC/sets/$SET_ARG/." "$TARGET/"

# Provenance stamp: which instructions this repository started from, so a
# later update (or migration to a template tool) knows the baseline.
{
  echo "# Where this repository's agent instructions came from."
  echo "repo=$REPO_URL"
  echo "set=$SET_ARG"
  echo "commit=$COMMIT"
  echo "date=$(date +%Y-%m-%d)"
} > "$TARGET/.instructions-source"

# Personalise the placeholders the sets carry (only where present).
slug="$(printf '%s' "$PROJECT_NAME" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9._-')"
if [ -f "$TARGET/pyproject.toml" ]; then
  PN="$slug" perl -pi -e 's/^name = "research-notebook"$/name = "$ENV{PN}"/' "$TARGET/pyproject.toml"
fi
if [ -f "$TARGET/labbook.tex" ]; then
  PN="$PROJECT_NAME" perl -pi -e 's/\\title\{Research Notebook --- Lab Book\}/\\title{$ENV{PN} --- Lab Book}/' "$TARGET/labbook.tex"
  AU="$GIT_NAME" perl -pi -e 's/\\author\{\}/\\author{$ENV{AU}}/' "$TARGET/labbook.tex"
fi
if [ -f "$TARGET/README.md" ]; then
  PN="$PROJECT_NAME" perl -pi -e '$. == 1 and s/^# .*/# $ENV{PN}/' "$TARGET/README.md"
fi
echo "created $TARGET (project: $PROJECT_NAME)"

step "Initialising git"
git init -q -b main "$TARGET" 2>/dev/null || { git init -q "$TARGET"; git -C "$TARGET" symbolic-ref HEAD refs/heads/main; }
git -C "$TARGET" add -A
git -C "$TARGET" commit -q -m "Initial commit: '${SET_ARG}' instruction set from ${REPO_NAME}@${COMMIT:0:7}"
echo "initial commit made on branch main"

# --- environment -------------------------------------------------------------

step "Python environment (pixi)"
if ! command -v pixi >/dev/null 2>&1 && [ -x "$HOME/.pixi/bin/pixi" ]; then
  export PATH="$HOME/.pixi/bin:$PATH"
fi
if ! command -v pixi >/dev/null 2>&1; then
  if [ "$HAVE_TTY" = 1 ]; then
    ans="$(prompt 'pixi is not installed. Install it now? (Y/n)' 'Y')"
  else
    ans="n"
  fi
  case "$ans" in
    [Yy]*)
      curl -fsSL https://pixi.sh/install.sh | sh
      export PATH="$HOME/.pixi/bin:$PATH"
      ;;
    *)
      warn "skipped — install later with: curl -fsSL https://pixi.sh/install.sh | sh"
      ;;
  esac
fi
if command -v pixi >/dev/null 2>&1 && [ -f "$TARGET/pyproject.toml" ]; then
  echo "solving the environment (first run downloads packages)..."
  (cd "$TARGET" && pixi install)
  if [ -f "$TARGET/pixi.lock" ]; then
    git -C "$TARGET" add pixi.lock
    git -C "$TARGET" commit -q -m "Add pixi.lock (onboarding)" || true
  fi
  (cd "$TARGET" && pixi run check) || warn "the consistency gate reported problems — ask your agent to fix them"
else
  warn "pixi not available — the environment, pixi.lock and the consistency gate are left for ONBOARDING.md"
fi

step "LaTeX (for the lab-book PDF)"
if command -v latexmk >/dev/null 2>&1 && command -v biber >/dev/null 2>&1; then
  echo "latexmk + biber found"
else
  warn "no full LaTeX toolchain (latexmk + biber). The lab book cannot compile until you install MacTeX:"
  echo "    brew install --cask mactex     (large download; open a new terminal afterwards)"
fi
if ! command -v pdftotext >/dev/null 2>&1; then
  echo "optional: 'brew install poppler' lets agents read and extract PDFs"
fi

# --- next steps --------------------------------------------------------------

step "Done — $TARGET"
cat <<EOF

Next steps:

  1. Open the folder in VS Code:  code "$TARGET"
     (or VS Code -> File -> Open Folder)

  2. Install the extension "Codex - OpenAI's coding agent" from the VS Code
     marketplace and sign in with your ChatGPT account. Codex reads AGENTS.md
     automatically - no further configuration.

  3. First message to the agent:

        Work through ONBOARDING.md and finish any unchecked steps.

  4. Bring your context over from ChatGPT. Paste into a normal ChatGPT chat:

        Summarize everything relevant about my physics research from our chats
        and your memory into a markdown project brief: background, current
        projects, notation and conventions, tools, open questions.

     Then paste its answer to the agent in VS Code, with:

        Seed ideas/ and the programme map from this brief. It is unverified
        context: tag recollections [?] and our reasoning [I], per AGENTS.md.

EOF
if command -v code >/dev/null 2>&1 && [ "$HAVE_TTY" = 1 ]; then
  ans="$(prompt 'Open it in VS Code now? (Y/n)' 'Y')"
  case "$ans" in [Yy]*) code "$TARGET" ;; esac
fi
