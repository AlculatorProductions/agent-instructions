#!/usr/bin/env bash
#
# SessionStart hook: on a Friday, remind the agent to offer the week's summary.
#
# Prints a JSON object whose additionalContext is injected into the session.
# Silent on every other day, and silent once the week already has a summary.
#
# TEMPLATE FILE — replaced on update.

set -u

[ "$(date +%u)" = "5" ] || exit 0

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
week="$(date +%G-W%V)"
[ -f "$root/log/weekly/${week}.tex" ] && exit 0

cat <<JSON
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"It is Friday and ${week} has no summary yet (log/weekly/${week}.tex is missing). Before anything else, offer once to write this week's summary: run \`pixi run week\` (or python3 scripts/doc_research/weekly.py), fill in the TODOs from the real work of the week, run \`pixi run entries\`, and commit. If Erin says no, drop it and do not raise it again today."}}
JSON
