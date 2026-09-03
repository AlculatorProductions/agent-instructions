"""Start this week's summary.

Builds the skeleton of a weekly summary from git history — commits, lab book
entries written, figures produced, calculations added, code still unchecked —
and leaves TODO markers where prose is needed. The agent fills those in; the
facts are already there so it cannot invent them.

    python3 doc_research/scripts/weekly.py                  # the current ISO week
    python3 doc_research/scripts/weekly.py --week 2026-W35
    python3 doc_research/scripts/weekly.py --force          # overwrite an existing one

The result is LaTeX, and belongs to worklog.pdf — a separate document from the
lab book. Run build_entries.py afterwards so it is included.

TEMPLATE FILE — replaced on update. Stdlib only.
"""

from __future__ import annotations

import sys

# macOS ships Python 3.9; this file must keep working there and on anything
# newer. If it ever does not, say so in one line instead of a traceback — and
# name the escape hatch, since the notebook's own pixi environment always has a
# recent Python.
if sys.version_info < (3, 9):  # pragma: no cover
    raise SystemExit(
        "Scirce needs Python 3.9 or newer; this is "
        f"{sys.version_info.major}.{sys.version_info.minor}. "
        "Either use a newer python3, or run it through the notebook's own "
        "environment: cd doc_research && pixi run check"
    )


import argparse
import datetime as dt
import re
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_entries as be  # noqa: E402
import check  # noqa: E402

ROOT = be.ROOT
TODO = r"\textcolor{red}{TODO}"

LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex(text: str) -> str:
    return "".join(LATEX_ESCAPES.get(char, char) for char in text)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=False
    )
    return result.stdout


def parse_week(value: str | None) -> tuple[int, int]:
    if value is None:
        year, week, _ = dt.date.today().isocalendar()
        return year, week
    match = re.fullmatch(r"(\d{4})-W(\d{1,2})", value)
    if not match:
        raise SystemExit(f"not a week: {value} (expected e.g. 2026-W35)")
    return int(match.group(1)), int(match.group(2))


def commits(monday: dt.date, sunday: dt.date) -> list[tuple[str, str, list[str]]]:
    """(short sha, subject, files) for each commit in the week, oldest first."""
    raw = git(
        "log",
        "--reverse",
        "--no-merges",
        f"--since={monday} 00:00:00",
        f"--until={sunday} 23:59:59",
        "--pretty=format:%x00%h%x1f%s",
        "--name-only",
    )
    found = []
    for block in raw.split("\x00"):
        block = block.strip("\n")
        if not block:
            continue
        head, _, rest = block.partition("\n")
        sha, _, subject = head.partition("\x1f")
        files = [line for line in rest.splitlines() if line.strip()]
        if files and all(f.startswith(".instructions") for f in files):
            continue
        found.append((sha, subject, files))
    return found


def bucket(files: set[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "entries": [],
        "figures": [],
        "calculations": [],
        "code": [],
    }
    for path in sorted(files):
        if path.startswith("labbook/entries/") and be.ENTRY_NAME.match(Path(path).name):
            buckets["entries"].append(path)
        elif path.startswith("figures/") and not path.endswith(".md"):
            buckets["figures"].append(path)
        elif path.startswith("calculations/"):
            buckets["calculations"].append(path)
        elif Path(path).suffix.lower() in check.CODE_SUFFIXES:
            buckets["code"].append(path)
    return buckets


def itemize(items: list[str], empty: str) -> str:
    if not items:
        return f"\\noindent\\textit{{{empty}}}\n"
    body = "\n".join(f"  \\item {item}" for item in items)
    return f"\\begin{{itemize}}\n{body}\n\\end{{itemize}}\n"


def build(year: int, week: int) -> str:
    monday = dt.date.fromisocalendar(year, week, 1)
    sunday = monday + dt.timedelta(days=6)
    week_id = f"{year}-W{week:02d}"

    log = commits(monday, sunday)
    touched: set[str] = set()
    for _, _, files in log:
        touched.update(files)
    buckets = bucket(touched)

    entry_titles = []
    for path in buckets["entries"]:
        full = ROOT / path
        header = be.read_header(full) if full.exists() else {}
        title = header.get("ENTRY-TITLE", Path(path).stem)
        summary = header.get("ENTRY-SUMMARY", "")
        entry_titles.append(
            f"\\textbf{{{tex(title)}}}"
            + (f" --- {tex(summary)}" if summary else "")
            + f" \\hfill \\texttt{{{tex(path)}}}"
        )

    figure_items = []
    for path in buckets["figures"]:
        caption = ROOT / "figures" / (Path(path).stem + ".md")
        meaning = TODO + " what it shows, in one line"
        if caption.exists():
            text = caption.read_text(encoding="utf-8", errors="replace")
            match = re.search(
                r"##\s*What you're looking at\s*\n+(.+?)\n", text, re.IGNORECASE
            )
            if match and not match.group(1).strip().startswith("One plain sentence"):
                meaning = tex(match.group(1).strip())
        figure_items.append(f"\\texttt{{{tex(path)}}} --- {meaning}")

    unchecked, checked_count = check.scan_markers(check.Report())
    unchecked_items = [
        f"\\texttt{{{tex(check.rel(m.path))}:{m.line}}} (written {m.date})"
        for m in unchecked
    ]

    commit_items = [f"\\texttt{{{sha}}} {tex(subject)}" for sha, subject, _ in log]

    # Everything the template interpolates is computed here, as a plain name.
    # An f-string expression part may not contain a backslash before Python 3.12,
    # and LaTeX is nothing but backslashes.
    code_items = (
        [TODO] + [f"\\texttt{{{tex(p)}}}" for p in buckets["code"]]
        if buckets["code"]
        else []
    )
    worked_on = itemize([TODO], "Nothing committed this week.")
    results = itemize([TODO], "No results this week.")
    code = itemize(code_items, "No code changed this week.")
    entries = itemize(entry_titles, "No entries written this week.")
    figures = itemize(figure_items, "No figures produced this week.")
    outstanding = itemize(
        unchecked_items, "Nothing outstanding — everything the agent wrote has been checked."
    )
    questions = itemize([TODO], "")
    commits_block = itemize(commit_items, "No commits this week.")
    heading = f"{week_id} \\quad {monday} -- {sunday}"

    return f"""% WEEK-ID: {week_id}
% WEEK-RANGE: {monday} to {sunday}
% WEEK-SUMMARY: TODO — one line, written by the agent.
%
% Skeleton generated by doc_research/scripts/weekly.py from git history.
%
% NOT FOR THE RESEARCHER TO EDIT. The facts below are real, taken from the
% week's commits. The agent replaces each TODO with prose, deletes this comment
% block, and runs build_entries.py.

\\section{{{heading}}}
\\label{{sec:week-{week_id}}}

\\subsection*{{What you worked on}}

% Plain language. At most five bullets. No jargon that has to be looked up.
% This is the section that gets read first; write it for a Friday afternoon.
{worked_on}

\\subsection*{{Results}}

% Only claims with a figure, a calculation or a run behind them. Name the
% evidence. Anything not yet verified says so, in the sentence itself.
{results}

\\subsection*{{Code}}

% What changed and why — not a list of commits.
{code}

\\subsection*{{Lab book entries written}}

{entries}

\\subsection*{{New figures}}

{figures}

\\subsection*{{Still unchecked}}

% Agent-written code not read yet. {checked_count} block(s) checked so far.
{outstanding}

\\subsection*{{Open questions}}

% Things to take to ChatGPT, or to a colleague. Include anything the agent
% flagged and that has not been decided on yet.
{questions}

\\subsection*{{Commits}}

{commits_block}

\\subsection*{{To paste elsewhere}}

% Three or four lines, plain text, for a chat message. It gets sent by hand if
% at all; nothing here is shared automatically.
\\begin{{quote}}
{TODO}
\\end{{quote}}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", help="ISO week, e.g. 2026-W35 (default: this week)")
    parser.add_argument("--force", action="store_true", help="overwrite an existing summary")
    args = parser.parse_args()

    year, week = parse_week(args.week)
    target = be.WEEK_DIR / f"{year}-W{week:02d}.tex"
    if target.exists() and not args.force:
        print(
            f"{target.relative_to(ROOT)} already exists — the agent edits that file "
            "directly, or pass --force to start it over"
        )
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(year, week), encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    print(
        "This is a skeleton, not a finished summary: the facts come from git, and "
        "the TODOs are for the agent to write up.\n"
        "Nothing here is for the researcher to fill in by hand.\n"
        "Agent: replace every TODO with prose, delete the header comment, then run "
        "build_entries.py."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
