#!/usr/bin/env bash
#
# update.sh — pull newer instructions from the upstream set without touching
# any of Erin's work.
#
#   pixi run update
#   bash scripts/doc_research/update.sh [--commit <sha>] [--dry-run]
#
# Ownership comes from .instructions/manifest; the three-way merge base is the
# pristine copy in .instructions/baseline/. See UPDATING.md.
#
# TEMPLATE FILE — replaced on update (by itself, on the next run).

set -euo pipefail

REPO_OWNER="AlculatorProductions"
REPO_NAME="agent-instructions"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}"
SET_DEFAULT="doc_research"

step() { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

REF="main"
DRY_RUN=0
FROM=""
while [ $# -gt 0 ]; do
  case "$1" in
    --commit) REF="${2:-}"; shift 2 ;;
    --from) FROM="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

[ -d .git ] || die "not a git repository: $ROOT"
[ -f .instructions/manifest ] || die "no .instructions/manifest — this notebook was not installed by install.sh"
[ -d .instructions/baseline ] || die "no .instructions/baseline — cannot merge without the version you started from"

if [ -n "$(git status --porcelain)" ]; then
  die "you have uncommitted changes. Commit or stash them first — an update should be reviewable on its own."
fi

# --- what we have now --------------------------------------------------------

SET_NAME="$SET_DEFAULT"
OLD_COMMIT="unknown"
# How pixi was wired up at install time. Repositories installed before this field
# existed got a pixi.toml, so that is the default.
PIXI_MODE="toml"
if [ -f .instructions-source ]; then
  SET_NAME="$(grep -m1 '^set=' .instructions-source | cut -d= -f2- || echo "$SET_DEFAULT")"
  OLD_COMMIT="$(grep -m1 '^commit=' .instructions-source | cut -d= -f2- || echo unknown)"
  PIXI_MODE="$(grep -m1 '^pixi=' .instructions-source | cut -d= -f2- || true)"
  [ -n "$PIXI_MODE" ] || PIXI_MODE="toml"
fi

# --- fetch the new set -------------------------------------------------------

if [ -n "$FROM" ]; then
  # Offline: a local checkout of the set, for testing or a private clone.
  SRC="$(cd "$FROM" && pwd)"
  [ -f "$SRC/.instructions/manifest" ] || die "$FROM does not look like an instruction set"
  NEW_COMMIT="$(git -C "$SRC" rev-parse HEAD 2>/dev/null || echo local)"
  step "Using the local set in $SRC"
else
step "Fetching ${SET_NAME} from ${REPO_URL} (${REF})"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "${REPO_URL}/archive/${REF}.tar.gz" | tar -xz -C "$TMP" \
  || die "download failed — check the network, or pass --commit <sha>"
SRC="$(find "$TMP" -maxdepth 1 -mindepth 1 -type d | head -1)/sets/${SET_NAME}"
[ -d "$SRC" ] || die "the archive has no sets/${SET_NAME}"

NEW_COMMIT="$(curl -fsSL "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${REF}" 2>/dev/null \
              | grep -m1 '"sha"' | cut -d'"' -f4 || true)"
[ -n "$NEW_COMMIT" ] || NEW_COMMIT="$REF"
fi

if [ "$NEW_COMMIT" = "$OLD_COMMIT" ]; then
  echo "already at ${OLD_COMMIT:0:7} — nothing to do"
  exit 0
fi
echo "from ${OLD_COMMIT:0:7} to ${NEW_COMMIT:0:7}"

# --- classify ----------------------------------------------------------------

# Last matching line in the manifest wins. In a `case` pattern `*` also matches
# `/`, which is why the manifest needs no `**`.
classify() {
  local rel="$1" cls="" line kind pat
  while IFS= read -r line; do
    line="${line%%#*}"
    line="$(printf '%s' "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [ -n "$line" ] || continue
    kind="${line%% *}"
    pat="$(printf '%s' "${line#* }" | sed 's/^[[:space:]]*//')"
    case "$rel" in $pat) cls="$kind" ;; esac
  done < "$ROOT/.instructions/manifest"
  printf '%s' "$cls"
}

REPLACED=(); MERGED=(); CONFLICTS=(); ADDED=(); SKIPPED=(); ORPHANED=()

merge_one() {
  local rel="$1" mine="$ROOT/$1" base="$ROOT/.instructions/baseline/$1" new="$SRC/$1"
  if [ ! -f "$mine" ]; then cp "$new" "$mine"; ADDED+=("$rel"); return; fi
  if [ ! -f "$base" ]; then SKIPPED+=("$rel (no baseline — left alone)"); return; fi
  if cmp -s "$mine" "$base"; then cp "$new" "$mine"; REPLACED+=("$rel"); return; fi
  if git merge-file -L "yours" -L "template (installed)" -L "template (new)" \
       "$mine" "$base" "$new" >/dev/null 2>&1; then
    MERGED+=("$rel")
  else
    CONFLICTS+=("$rel")
  fi
}

step "Applying"
while IFS= read -r -d '' path; do
  rel="${path#"$SRC"/}"
  case "$rel" in .git/*|install.sh|.gitignore|*/__pycache__/*) continue ;; esac
  # Never drop a pixi.toml into a repository whose pyproject.toml owns pixi —
  # pixi prefers pixi.toml, so it would silently shadow their manifest.
  if [ "$rel" = "pixi.toml" ] && [ "$PIXI_MODE" != "toml" ]; then
    SKIPPED+=("pixi.toml (your pyproject.toml owns pixi)"); continue
  fi

  cls="$(classify "$rel")"
  target="$ROOT/$rel"
  mkdir -p "$(dirname "$target")"

  case "$cls" in
    template)
      if [ -f "$target" ] && cmp -s "$target" "$SRC/$rel"; then :
      else cp "$SRC/$rel" "$target"; REPLACED+=("$rel"); fi
      ;;
    merge) merge_one "$rel" ;;
    seed)
      if [ -f "$target" ]; then SKIPPED+=("$rel (yours)"); else cp "$SRC/$rel" "$target"; ADDED+=("$rel"); fi
      ;;
    *)
      if [ -f "$target" ]; then SKIPPED+=("$rel (not in manifest)")
      else cp "$SRC/$rel" "$target"; ADDED+=("$rel"); fi
      ;;
  esac
done < <(find "$SRC" -type f -print0)

# Files that were shipped before and are gone upstream: only remove the ones
# that were never touched locally. Anything else is reported, not deleted.
while IFS= read -r -d '' path; do
  rel="${path#"$ROOT/.instructions/baseline"/}"
  [ -f "$SRC/$rel" ] && continue
  [ -f "$ROOT/$rel" ] || continue
  if cmp -s "$ROOT/$rel" "$path"; then rm "$ROOT/$rel"; REPLACED+=("removed $rel")
  else ORPHANED+=("$rel"); fi
done < <(find "$ROOT/.instructions/baseline" -type f -print0)

if [ "$DRY_RUN" = 1 ]; then
  step "Dry run — reverting"
  git checkout -- . && git clean -fdq
  echo "nothing was kept"
fi

# --- record and commit -------------------------------------------------------

if [ "$DRY_RUN" = 0 ]; then
  rm -rf "$ROOT/.instructions/baseline"
  mkdir -p "$ROOT/.instructions/baseline"
  cp -R "$SRC/." "$ROOT/.instructions/baseline/"
  rm -f "$ROOT/.instructions/baseline/install.sh" "$ROOT/.instructions/baseline/.gitignore"
  rm -rf "$ROOT/.instructions/baseline/.instructions/baseline"
  find "$ROOT/.instructions/baseline" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

  {
    echo "# Where this notebook's instructions came from. Written by install.sh / update.sh."
    echo "repo=$REPO_URL"
    echo "set=$SET_NAME"
    echo "commit=$NEW_COMMIT"
    grep -m1 '^set_version=' .instructions-source 2>/dev/null || echo "set_version=1"
    grep -m1 '^installed=' .instructions-source 2>/dev/null || echo "installed=$(date +%Y-%m-%d)"
    echo "updated=$(date +%Y-%m-%d)"
    echo "pixi=$PIXI_MODE"
  } > "$ROOT/.instructions-source.new"
  mv "$ROOT/.instructions-source.new" "$ROOT/.instructions-source"
fi

step "Summary"
printf '  replaced: %d\n  merged:   %d\n  added:    %d\n  kept:     %d\n' \
  "${#REPLACED[@]}" "${#MERGED[@]}" "${#ADDED[@]}" "${#SKIPPED[@]}"
for f in "${CONFLICTS[@]:-}"; do [ -n "$f" ] && printf '  \033[1;31mCONFLICT\033[0m %s\n' "$f"; done
for f in "${ORPHANED[@]:-}"; do [ -n "$f" ] && printf '  orphaned (edited locally, gone upstream): %s\n' "$f"; done

[ "$DRY_RUN" = 1 ] && exit 0

if [ -z "$(git status --porcelain)" ]; then
  echo "no changes"
  exit 0
fi

git add -A
git commit -q -m "Update instructions: ${SET_NAME}@${OLD_COMMIT:0:7} -> ${NEW_COMMIT:0:7}

Replaced ${#REPLACED[@]}, merged ${#MERGED[@]}, added ${#ADDED[@]}, conflicts ${#CONFLICTS[@]}.
Revert this single commit to undo the whole update."
echo "committed — \`git revert HEAD\` undoes the whole update"

if [ "${#CONFLICTS[@]}" -gt 0 ]; then
  warn "${#CONFLICTS[@]} file(s) have conflict markers. Ask your agent: \"resolve the instruction update conflicts\" (see UPDATING.md)."
  exit 1
fi

command -v python3 >/dev/null 2>&1 && python3 scripts/doc_research/check.py || true
