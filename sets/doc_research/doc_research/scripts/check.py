"""The gate: does the record still hang together?

Checks that lab book entries are well formed and in order, that every figure has
a caption file a tired person could read, that the generated include lists are
current, and that nothing shipped as a template has been quietly hand-edited.
It also reports which agent-written code has not been checked yet.

    python3 doc_research/scripts/check.py            # verify
    python3 doc_research/scripts/check.py --write    # also refresh INDEX.md

TEMPLATE FILE — replaced on update. Stdlib only, on purpose: this must run in
any checkout without installing anything. Exits 1 on an error; warnings and
notes never fail the run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_entries as be  # noqa: E402

# ROOT is the notebook folder (doc_research/). REPO is the repository around it —
# The repository's own code lives there, outside the notebook, and that is where
# provenance markers and the vendored baseline are.
ROOT = be.ROOT
REPO = be.REPO

FIGURE_DIR = ROOT / "figures"
FIGURE_SUFFIXES = {".pdf", ".png", ".svg", ".jpg", ".jpeg", ".eps"}
CAPTION_REQUIRED = [
    "What you're looking at",
    "Axes",
    "Why this plot exists",
    "Made by",
]
CAPTION_ADVISED = ["What would change if", "Checked"]

CODE_SUFFIXES = {".py", ".jl", ".m", ".c", ".cc", ".cpp", ".h", ".hpp", ".f90", ".r", ".jl"}
MARK_UNCHECKED = re.compile(r"\[claude\s+(\d{4}-\d{2}-\d{2})\]")
MARK_CHECKED = re.compile(r"\[checked\s+([^\]\s]+)\s+(\d{4}-\d{2}-\d{2})\]")

SKIP_DIRS = {
    ".git",
    ".pixi",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "node_modules",
    ".instructions",
}

MANIFEST = REPO / ".instructions" / "manifest"
BASELINE = REPO / ".instructions" / "baseline"

LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")

STALE_DAYS = 180


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def walk(base: Path):
    """Every file under base, skipping build and vendor directories."""
    if not base.is_dir():
        return
    for path in sorted(base.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(base).parts):
            continue
        if path.is_file():
            yield path


def rel(path: Path) -> str:
    """Path as written in INDEX.md and in messages: relative to the notebook when
    it is inside it, otherwise relative to the repository."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return "../" + path.relative_to(REPO).as_posix()


# --------------------------------------------------------------------------- #
# Lab book
# --------------------------------------------------------------------------- #


def check_entries(report: Report) -> list[be.Entry]:
    entries = be.entries()

    if be.ENTRY_DIR.is_dir():
        for path in sorted(be.ENTRY_DIR.glob("*.tex")):
            if not be.ENTRY_NAME.match(path.name):
                report.error(
                    f"{rel(path)}: entry filenames must be YYYY-MM-DD-slug.tex "
                    "(lowercase slug) — the lab book is ordered by filename"
                )

    for entry in entries:
        missing = [k for k in be.HEADER_KEYS if k not in entry.header]
        if missing:
            report.error(f"{entry.rel}: header is missing {', '.join(missing)}")
        stamped = entry.header.get("ENTRY-DATE", "")
        from_name = entry.path.name[:10]
        if stamped and stamped != from_name:
            report.error(
                f"{entry.rel}: ENTRY-DATE is {stamped} but the filename says {from_name}"
            )

    stale = be.up_to_date()
    for name in stale:
        report.error(f"{name} is out of date — run doc_research/scripts/build_entries.py")

    return entries


def check_week_files(report: Report) -> list[be.Entry]:
    weeks = be.weeks()
    if be.WEEK_DIR.is_dir():
        for path in sorted(be.WEEK_DIR.glob("*.tex")):
            if not be.WEEK_NAME.match(path.name):
                report.error(f"{rel(path)}: weekly summaries must be named YYYY-Www.tex")
    for week in weeks:
        missing = [k for k in be.WEEK_HEADER_KEYS if k not in week.header]
        if missing:
            report.warn(f"{week.rel}: header is missing {', '.join(missing)}")

    today = dt.date.today()
    last_week = today - dt.timedelta(days=7)
    wanted = "%04d-W%02d.tex" % last_week.isocalendar()[:2]
    if be.WEEK_DIR.is_dir() and not (be.WEEK_DIR / wanted).exists():
        report.note(f"no summary for last week ({wanted[:-4]}) — weekly.py starts one")
    return weeks


# --------------------------------------------------------------------------- #
# Figures
# --------------------------------------------------------------------------- #


@dataclass
class Figure:
    path: Path
    caption: Path | None


def check_figures(report: Report) -> list[Figure]:
    figures: list[Figure] = []
    if not FIGURE_DIR.is_dir():
        return figures

    captions = {p.stem: p for p in FIGURE_DIR.rglob("*.md") if p.name != "_template.md"}
    seen_stems = set()

    for path in sorted(FIGURE_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in FIGURE_SUFFIXES:
            continue
        seen_stems.add(path.stem)
        caption = captions.get(path.stem)
        figures.append(Figure(path, caption))
        if caption is None:
            report.error(
                f"{rel(path)}: no caption file. Every figure needs figures/{path.stem}.md "
                "(copy figures/_template.md) — without it nobody can read the plot later"
            )
            continue

        text = caption.read_text(encoding="utf-8", errors="replace")
        for heading in CAPTION_REQUIRED:
            if heading.lower() not in text.lower():
                report.error(f"{rel(caption)}: missing the '{heading}' section")
        for heading in CAPTION_ADVISED:
            if heading.lower() not in text.lower():
                report.warn(f"{rel(caption)}: missing the '{heading}' section")
        if "<path>" in text or "<the command that produced it>" in text:
            report.warn(f"{rel(caption)}: still contains template placeholders")

    for stem, caption in sorted(captions.items()):
        if stem not in seen_stems and caption.name != "README.md":
            report.warn(f"{rel(caption)}: caption for a figure that does not exist")

    return figures


# --------------------------------------------------------------------------- #
# Agent-written code
# --------------------------------------------------------------------------- #


@dataclass
class Marker:
    path: Path
    line: int
    date: str


def scan_markers(report: Report) -> tuple[list[Marker], int]:
    """A habit, automated: which agent-written code has not been read yet?"""
    unchecked: list[Marker] = []
    checked = 0
    ours = (ROOT / "scripts").resolve()

    # The whole repository: the researcher's code sits outside the notebook folder.
    for path in walk(REPO):
        if path.suffix.lower() not in CODE_SUFFIXES:
            continue
        if ours in path.resolve().parents:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if MARK_CHECKED.search(line):
                checked += 1
            elif match := MARK_UNCHECKED.search(line):
                unchecked.append(Marker(path, number, match.group(1)))

    today = dt.date.today()
    for marker in unchecked:
        try:
            age = (today - dt.date.fromisoformat(marker.date)).days
        except ValueError:
            report.warn(f"{rel(marker.path)}:{marker.line}: unparseable date in marker")
            continue
        if age > STALE_DAYS:
            report.warn(
                f"{rel(marker.path)}:{marker.line}: written {age} days ago and still "
                "unchecked — worth a look or a deliberate decision to leave it"
            )
    return unchecked, checked


# --------------------------------------------------------------------------- #
# Links, template drift
# --------------------------------------------------------------------------- #


def check_links(report: Report) -> None:
    pointer = REPO / "CLAUDE.md"
    for path in [*walk(ROOT), *([pointer] if pointer.exists() else [])]:
        if path.suffix != ".md":
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8", errors="replace")):
            if re.match(r"^[a-z]+:", target) or target.startswith("//"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                report.warn(f"{rel(path)}: link does not resolve: {target}")


def read_manifest() -> list[tuple[str, str]]:
    if not MANIFEST.exists():
        return []
    rules = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[0] in {"template", "merge", "seed"}:
            rules.append((parts[0], parts[1]))
    return rules


def classify(path_rel: str, rules: list[tuple[str, str]]) -> str | None:
    """Last matching rule wins, so a specific line can override a general one."""
    from fnmatch import fnmatchcase

    found = None
    for cls, pattern in rules:
        if fnmatchcase(path_rel, pattern):
            found = cls
    return found


def check_template_drift(report: Report) -> None:
    rules = read_manifest()
    if not rules or not BASELINE.is_dir():
        return
    # Walked directly: BASELINE lives under .instructions/, which walk() skips.
    for path in sorted(BASELINE.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        path_rel = path.relative_to(BASELINE).as_posix()
        if classify(path_rel, rules) != "template":
            continue
        local = REPO / path_rel
        if not local.exists():
            report.warn(f"{path_rel}: shipped file is missing — update.sh restores it")
        elif local.read_bytes() != path.read_bytes():
            report.warn(
                f"{path_rel}: hand-edited, but it is replaced on update. Move the change "
                "into TASTE.md (a preference) or FEEDBACK.md (a rule that is wrong)"
            )


# --------------------------------------------------------------------------- #
# INDEX.md
# --------------------------------------------------------------------------- #


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(REPO), *args],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
    except OSError:
        return ""


def table(rows: list[str], header: str) -> str:
    if not rows:
        return "_none yet_"
    return header + "\n" + "\n".join(rows)


def write_index(entries, weeks, figures, unchecked) -> bool:
    index = ROOT / "INDEX.md"
    if not index.exists():
        return False
    text = index.read_text(encoding="utf-8")

    blocks = {
        "entries": table(
            [
                f"| {e.header.get('ENTRY-DATE', e.path.name[:10])} "
                f"| {e.title()} | [{e.rel}]({e.rel}) |"
                for e in entries
            ],
            "| Date | Title | File |\n|---|---|---|",
        ),
        "calculations": table(
            [
                f"| {d.name} | [{rel(d)}]({rel(d)}) |"
                for d in sorted((ROOT / "calculations").iterdir() if (ROOT / "calculations").is_dir() else [])
                if d.is_dir() and d.name != "_template"
            ],
            "| Calculation | Folder |\n|---|---|",
        ),
        "figures": table(
            [
                f"| [{rel(f.path)}]({rel(f.path)}) "
                f"| {'[caption](' + rel(f.caption) + ')' if f.caption else '**missing**'} |"
                for f in figures
            ],
            "| Figure | Caption |\n|---|---|",
        ),
        "weeks": table(
            [f"| {w.path.stem} | [{w.rel}]({w.rel}) |" for w in weeks],
            "| Week | File |\n|---|---|",
        ),
        "unchecked": table(
            [f"| {rel(m.path)}:{m.line} | {m.date} |" for m in unchecked],
            "| Location | Written |\n|---|---|",
        ),
    }

    updated = text
    for name, body in blocks.items():
        pattern = re.compile(
            rf"(<!-- BEGIN:GENERATED {name} -->\n).*?(<!-- END:GENERATED {name} -->)",
            re.DOTALL,
        )
        updated = pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), updated)

    if updated != text:
        index.write_text(updated, encoding="utf-8")
        return True
    return False


# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="rebuild the include lists and refresh INDEX.md",
    )
    args = parser.parse_args()

    report = Report()

    if args.write:
        be.main()

    entries = check_entries(report)
    weeks = check_week_files(report)
    figures = check_figures(report)
    unchecked, checked = scan_markers(report)
    check_links(report)
    check_template_drift(report)

    if args.write and write_index(entries, weeks, figures, unchecked):
        print("INDEX.md refreshed")

    print(
        f"\n{len(entries)} lab book entries, {len(weeks)} weekly summaries, "
        f"{len(figures)} figures"
    )
    if unchecked or checked:
        print(f"agent-written code: {len(unchecked)} unchecked, {checked} checked")
        for marker in unchecked[:10]:
            print(f"  unchecked  {rel(marker.path)}:{marker.line}  (written {marker.date})")
        if len(unchecked) > 10:
            print(f"  ... and {len(unchecked) - 10} more — see INDEX.md")

    for note in report.notes:
        print(f"\nnote: {note}")
    for warning in report.warnings:
        print(f"warning: {warning}")
    for error in report.errors:
        print(f"error: {error}")

    if report.errors:
        print(f"\n{len(report.errors)} error(s). The record is inconsistent.")
        return 1
    print("\nok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
