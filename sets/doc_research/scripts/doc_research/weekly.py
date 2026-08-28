"""Start this week's summary.

Builds the skeleton of a weekly summary from git history — commits, lab book
entries written, figures produced, calculations added, code still unchecked —
and leaves TODO markers where prose is needed. The agent fills those in; the
facts are already there so it cannot invent them.

    pixi run week                     # the current ISO week
    python3 scripts/doc_research/weekly.py --week 2026-W35
    python3 scripts/doc_research/weekly.py --force    # overwrite an existing one

The result is LaTeX, and belongs to worklog.pdf — a separate document from the
lab book. Run `pixi run entries` afterwards so it is included.

TEMPLATE FILE — replaced on update. Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
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

    return f"""% WEEK-ID: {week_id}
% WEEK-RANGE: {monday} to {sunday}
% WEEK-SUMMARY: TODO — one line, written by the agent.
%
% Skeleton generated by scripts/doc_research/weekly.py from git history.
% The facts below are real; replace every TODO with prose, then delete this
% comment block and run `pixi run entries`.

\\section{{{week_id} \\quad {monday} -- {sunday}}}
\\label{{sec:week-{week_id}}}

\\subsection*{{What you worked on}}

% Plain language. At most five bullets. No jargon that has to be looked up.
% This is the section Erin reads first; write it for a Friday afternoon.
{itemize([TODO], "Nothing committed this week.")}

\\subsection*{{Results}}

% Only claims with a figure, a calculation or a run behind them. Name the
% evidence. Anything not yet verified says so, in the sentence itself.
{itemize([TODO], "No results this week.")}

\\subsection*{{Code}}

% What changed and why — not a list of commits.
{itemize([TODO] + [f"\\texttt{{{tex(p)}}}" for p in buckets["code"]] if buckets["code"] else [], "No code changed this week.")}

\\subsection*{{Lab book entries written}}

{itemize(entry_titles, "No entries written this week.")}

\\subsection*{{New figures}}

{itemize(figure_items, "No figures produced this week.")}

\\subsection*{{Still unchecked}}

% Agent-written code Erin has not read yet. {checked_count} block(s) checked so far.
{itemize(unchecked_items, "Nothing outstanding — everything the agent wrote has been checked.")}

\\subsection*{{Open questions}}

% Things to take to ChatGPT, or to a colleague. Include anything the agent
% flagged and Erin has not decided on yet.
{itemize([TODO], "")}

\\subsection*{{Commits}}

{itemize(commit_items, "No commits this week.")}

\\subsection*{{To paste elsewhere}}

% Three or four lines, plain text, for a chat message. Erin sends it herself if
% she wants to; nothing here is shared automatically.
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
        print(f"{target.relative_to(ROOT)} already exists — edit it, or pass --force")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(year, week), encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    print("now: replace every TODO with prose, then run `pixi run entries`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
