#!/usr/bin/env bash
#
# install.sh — add the Scirce research notebook to an EXISTING git repository.
#
# Unlike the generic setup.sh in this repository, this does not create a new
# project. It adds a lab book, a work log, a figure-caption discipline and a set
# of Claude Code commands to a repository that already has code in it.
#
# Everything lands in a single doc_research/ folder. The only things placed at the
# repository root are a short CLAUDE.md pointer and the hidden .claude/ directory,
# because Claude Code reads both from the root and nowhere else.
#
# Usage, from inside the repository:
#   curl -fsSL https://raw.githubusercontent.com/AlculatorProductions/agent-instructions/main/sets/doc_research/install.sh | bash
#   ./install.sh [--target <dir>] [--yes]
#
# It never overwrites anything. Any file that already exists is skipped and
# listed at the end. Your pyproject.toml is not touched — the notebook brings a
# standalone pixi.toml, which pixi reads instead.
#
# macOS-oriented; needs only tools that ship with the OS.

set -euo pipefail

REPO_OWNER="AlculatorProductions"
REPO_NAME="agent-instructions"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}"
BRANCH="main"
SET_NAME="doc_research"
SET_VERSION="1"

step() { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

if { : </dev/tty; } >/dev/null 2>&1; then HAVE_TTY=1; else HAVE_TTY=0; fi
prompt() {
  local q="$1" def="${2:-}" reply=""
  if [ "$HAVE_TTY" = 1 ]; then
    printf '%s [%s] ' "$q" "$def" > /dev/tty
    IFS= read -r reply < /dev/tty || true
  fi
  printf '%s' "${reply:-$def}"
}

TARGET="$PWD"
ASSUME_YES=0
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --yes|-y) ASSUME_YES=1; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done
TARGET="$(cd "${TARGET/#\~/$HOME}" 2>/dev/null && pwd)" || die "no such directory"

# --- the repository must be ready --------------------------------------------

step "Checking the repository"
git --version >/dev/null 2>&1 || die "git is not installed"
git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1 \
  || die "$TARGET is not a git repository. Run this inside your project."
[ -z "$(git -C "$TARGET" status --porcelain)" ] \
  || die "you have uncommitted changes. Commit or stash them first, so this install is a single reviewable commit."

echo "repository ok: $TARGET"

# Nothing to negotiate about pixi any more: the notebook's pixi.toml lives inside
# doc_research/, so pixi at the repository root keeps using whatever manifest is
# already there. Nothing in pyproject.toml is read, written or shadowed.

# --- locate the set: local clone if possible, else download ------------------

SRC=""
COMMIT="unknown"
SCRIPT_PATH="${BASH_SOURCE[0]:-}"
if [ -n "$SCRIPT_PATH" ] && [ -f "$SCRIPT_PATH" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
  if [ -f "$SCRIPT_DIR/CLAUDE.md" ] && [ -f "$SCRIPT_DIR/.instructions/manifest" ]; then
    SRC="$SCRIPT_DIR"
    COMMIT="$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
    echo "using the local set in $SRC"
  fi
fi
if [ -z "$SRC" ]; then
  step "Downloading ${SET_NAME} from ${REPO_URL}"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL "${REPO_URL}/archive/refs/heads/${BRANCH}.tar.gz" | tar -xz -C "$TMP" \
    || die "download failed — the repository must be public and reachable"
  SRC="$TMP/${REPO_NAME}-${BRANCH}/sets/${SET_NAME}"
  [ -d "$SRC" ] || die "the archive has no sets/${SET_NAME}"
  COMMIT="$(curl -fsSL "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${BRANCH}" 2>/dev/null \
            | grep -m1 '"sha"' | cut -d'"' -f4 || true)"
  [ -n "$COMMIT" ] || COMMIT="unknown"
fi

# --- plan --------------------------------------------------------------------

# Files of the set that are never installed into the target repository.
skip_file() {
  case "$1" in install.sh|.gitignore|.git/*|*/.DS_Store|*/__pycache__/*) return 0 ;; esac
  return 1
}

NEW=(); COLLIDE=()
while IFS= read -r -d '' path; do
  rel="${path#"$SRC"/}"
  skip_file "$rel" && continue
  if [ -e "$TARGET/$rel" ]; then COLLIDE+=("$rel"); else NEW+=("$rel"); fi
done < <(find "$SRC" -type f -print0)

step "Plan"
echo "  ${#NEW[@]} files will be added to $TARGET"
if [ "${#COLLIDE[@]}" -gt 0 ]; then
  echo "  ${#COLLIDE[@]} already exist and will be LEFT ALONE:"
  for f in "${COLLIDE[@]}"; do echo "      $f"; done
fi
echo
echo "  Nothing existing is overwritten. Your pyproject.toml is not touched."
echo "  Everything lands in one commit, so \`git revert\` undoes all of it."

if [ "$ASSUME_YES" = 0 ] && [ "$HAVE_TTY" = 1 ]; then
  case "$(prompt 'Go ahead? (Y/n)' 'Y')" in [Yy]*) ;; *) die "cancelled" ;; esac
fi

# --- install -----------------------------------------------------------------

step "Installing"
for rel in "${NEW[@]}"; do
  mkdir -p "$TARGET/$(dirname "$rel")"
  cp "$SRC/$rel" "$TARGET/$rel"
done
chmod +x "$TARGET/doc_research/scripts/update.sh" "$TARGET/doc_research/scripts/friday.sh" 2>/dev/null || true

# The pristine copy that makes future three-way merges possible.
mkdir -p "$TARGET/.instructions/baseline"
cp -R "$SRC/." "$TARGET/.instructions/baseline/"
rm -f "$TARGET/.instructions/baseline/install.sh" "$TARGET/.instructions/baseline/.gitignore"
rm -rf "$TARGET/.instructions/baseline/.instructions/baseline"
find "$TARGET/.instructions/baseline" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

{
  echo "# Where this notebook's instructions came from. Written by install.sh / update.sh."
  echo "repo=$REPO_URL"
  echo "set=$SET_NAME"
  echo "commit=$COMMIT"
  echo "set_version=$SET_VERSION"
  echo "installed=$(date +%Y-%m-%d)"
  echo "updated=$(date +%Y-%m-%d)"
} > "$TARGET/.instructions-source"

# No .gitignore of yours is touched: the notebook ships its own inside
# doc_research/, which git applies to that folder only.

python3 "$TARGET/doc_research/scripts/build_entries.py" >/dev/null 2>&1 || true

step "Committing"
git -C "$TARGET" add -A
git -C "$TARGET" commit -q -m "Add the ${SET_NAME} notebook (${REPO_NAME}@${COMMIT:0:7})

Lab book, work log, figure captions and agent instructions. Nothing existing was
overwritten. Revert this commit to remove all of it."
echo "one commit made — \`git revert HEAD\` removes everything this added"

# --- what could not be done automatically ------------------------------------

if [ "${#COLLIDE[@]}" -gt 0 ]; then
  step "Left alone (they already existed)"
  for f in "${COLLIDE[@]}"; do echo "  $f"; done
  echo
  echo "Ask your agent to reconcile these: the shipped versions are in"
  echo ".instructions/baseline/ — for .claude/settings.json in particular, the"
  echo "SessionStart hook needs merging into your existing one for the Friday"
  echo "summary prompt to work."
fi

step "Done"
cat <<EOF

Everything Scirce owns is in doc_research/. At the repository root there is only
a short CLAUDE.md pointer and the hidden .claude/ directory, both of which Claude
Code reads from the root and nowhere else.

Claude Code is already set up, so there is nothing to install.

You do not run anything yourself. Work in the Claude Code chat the way you
already do — ask for code, paste a calculation, ask a question — and the record
gets written as a side effect. The commands and the .tex files are the agent's
job, not yours.

  1. Open this folder in VS Code and start Claude Code.

  2. First message:

        Work through ONBOARDING.md and finish any unchecked steps.

     It asks a few questions — how much documentation you want per request, where
     your code lives, how you make plots, and whether it should read the
     repository once and write a short opening entry — then writes the answers
     into TASTE.md.

The lab book and the work log are nearly empty right now. That is the normal
starting state: they fill up by themselves as you work, and after a few weeks
they are worth reading.

Two things worth knowing straight away:

  TASTE.md    You change how the agent behaves by saying so in the chat.
              "Shorter messages." "Stop explaining every equation step."
              It writes the rule down and follows it from then on.

  FEEDBACK.md When something does not work — you do not understand a plot, you
              correct the same thing twice, a command keeps failing — the agent
              writes it down here by itself, including which of our instructions
              was at fault. It stays on your machine. Send it back to whoever
              set this notebook up whenever you like, and the instructions get
              fixed for everyone. Delete anything you would rather not share.

On any Friday, the agent offers to write up the week into worklog.pdf.

EOF
