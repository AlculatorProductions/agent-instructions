"""Local consistency gate for the notebook.

Checks that the record hangs together: sources are registered and hashed, cited
citekeys exist, runs are documented, links resolve, and the lab book's shard
structure is intact. With ``--write`` it also regenerates the tables in
INDEX.md from frontmatter and shard headers.

    pixi run check            # verify
    pixi run check --write    # verify and refresh INDEX.md

Stdlib only, on purpose: the gate must run in any checkout without installing
anything. Exits 1 on any error; warnings do not fail the build.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHARD_MAX_LINES = 280
LARGE_FILE_BYTES = 5 * 1024 * 1024

RUN_REQUIRED_SECTIONS = [
    "Hypothesis",
    "Command",
    "Environment",
    "Result",
    "Interpretation",
    "Uncertainty",
    "Gates",
    "Next steps",
]

SHARD_HEADER_KEYS = ["SHARD-ID", "SHARD-TITLE", "SHARD-SUMMARY", "SHARD-KEYWORDS"]

SKIP_DIRS = {".git", ".pixi", "__pycache__", ".pytest_cache", ".ruff_cache"}


@dataclass
class Report:
    """Collected problems. Errors fail the run; warnings only inform."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #


def read_frontmatter(path: Path) -> dict[str, object]:
    """Parse the YAML subset we actually use: scalars and flat lists."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        value = raw.split("  #")[0].strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
            data[key.strip()] = [v for v in items if v]
        else:
            data[key.strip()] = value
    return data


def markdown_title(path: Path) -> str:
    """Frontmatter title if present, else the first ``# `` heading, else stem."""
    fm = read_frontmatter(path)
    title = fm.get("title")
    if isinstance(title, str) and title:
        return title
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def is_scratch(path: Path) -> bool:
    """Templates and other underscore-prefixed paths are not real entries."""
    return any(part.startswith("_") for part in path.relative_to(ROOT).parts)


def entry_files(directory: Path) -> list[Path]:
    """Dated Markdown entries in a notebook directory."""
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.glob("*.md")
        if p.name != "README.md" and not p.name.startswith("_")
    )


def markdown_files() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)
    )


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #


def bib_citekeys(rep: Report) -> set[str]:
    bib = ROOT / "literature" / "references.bib"
    if not bib.exists():
        rep.error("literature/references.bib is missing")
        return set()
    return set(re.findall(r"^@\w+\{([^,\s]+)\s*,", bib.read_text(encoding="utf-8"), re.MULTILINE))


def sources_rows(rep: Report) -> dict[str, dict[str, str]]:
    """Parse the registered-source table in literature/SOURCES.md."""
    manifest = ROOT / "literature" / "SOURCES.md"
    if not manifest.exists():
        rep.error("literature/SOURCES.md is missing")
        return {}
    rows: dict[str, dict[str, str]] = {}
    in_table = False
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Registered sources"):
            in_table = True
            continue
        if not in_table or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Citekey", ""} or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].startswith("_"):
            continue
        rows[cells[0]] = {"citation": cells[1], "path": cells[5], "sha256": cells[6]}
    return rows


def check_sources(rep: Report, keys: set[str]) -> dict[str, dict[str, str]]:
    rows = sources_rows(rep)

    for citekey, row in rows.items():
        if citekey not in keys:
            rep.error(f"SOURCES.md registers {citekey!r} with no entry in references.bib")
        local = row["path"]
        if local in {"missing-local", "", "—", "-"}:
            continue
        target = ROOT / local if local.startswith("literature/") else ROOT / "literature" / local
        if not target.exists():
            rep.error(f"SOURCES.md: {citekey} points at missing file {local}")
            continue
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if row["sha256"].lower() not in {digest, "—", "-", ""}:
            rep.error(f"SOURCES.md: SHA256 mismatch for {citekey} ({local})")

    pdfs = ROOT / "literature" / "pdfs"
    for pdf in sorted(pdfs.glob("*")) if pdfs.is_dir() else []:
        if pdf.name.startswith("."):
            continue
        if pdf.stem not in rows:
            rep.error(f"literature/pdfs/{pdf.name} has no row in literature/SOURCES.md")
    return rows


def check_citekeys(rep: Report, keys: set[str]) -> None:
    for path in markdown_files():
        if is_scratch(path):
            continue
        cited = read_frontmatter(path).get("sources", [])
        if not isinstance(cited, list):
            continue
        for key in cited:
            if key not in keys:
                rel = path.relative_to(ROOT)
                rep.error(f"{rel}: frontmatter cites {key!r}, not in literature/references.bib")


def check_runs(rep: Report) -> list[Path]:
    runs_dir = ROOT / "runs"
    found: list[Path] = []
    for run in sorted(p for p in runs_dir.iterdir() if p.is_dir()) if runs_dir.is_dir() else []:
        if run.name.startswith("_"):
            continue
        found.append(run)
        readme = run / "README.md"
        if not readme.exists():
            rep.error(f"runs/{run.name}/ has no README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        for section in RUN_REQUIRED_SECTIONS:
            if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
                rep.error(f"runs/{run.name}/README.md is missing the '## {section}' section")
    return found


def check_run_sha_containment(rep: Report, runs: list[Path]) -> None:
    """``AGENTS.md``: a run's recorded SHA must contain the run directory.

    A SHA that predates its own run is worse than a missing one -- it names a
    snapshot that would reproduce *different* numbers. A 2026-08-01 review found
    twelve of fifteen in that state; this counts them so the backlog cannot grow
    unnoticed while it is worked down.
    """
    missing = []
    for run in runs:
        shas = set()
        for artefact in sorted(run.glob("*.json")):
            text = artefact.read_text(encoding="utf-8")
            shas.update(re.findall(r'"git_sha"\s*:\s*"([0-9a-f]{7,40})"', text))
        for sha in sorted(shas):
            probe = subprocess.run(["git", "cat-file", "-e", f"{sha}:runs/{run.name}"],
                                   cwd=ROOT, capture_output=True, check=False)
            if probe.returncode != 0:
                missing.append(f"{run.name}@{sha[:8]}")
    if missing:
        rep.warn(f"runs: {len(missing)} recorded SHA(s) do not contain their run "
                 f"(AGENTS.md); oldest first: {', '.join(missing[:3])}"
                 + (" ..." if len(missing) > 3 else ""))


def entry_date(path: Path) -> str:
    """The ``YYYY-MM-DD`` prefix of a dated entry name, or ``""`` if it has none."""
    match = re.match(r"(\d{4}-\d{2}-\d{2})-", path.name)
    return match.group(1) if match else ""


def check_resumability(rep: Report, runs: list[Path]) -> None:
    """``AGENTS.md``: the notebook must be pickup-able from ``INDEX.md`` alone.

    These are warnings, not errors: none of them makes a claim wrong, and a
    session that is mid-flight will trip them legitimately. But each marks state
    that exists only in someone's head, which is the thing this repository is
    built to prevent. They were added on 2026-08-06 after a review found two
    runs promoted into the lab book with no ``ideas/`` entry behind them and no
    record of why their parameters were chosen.
    """
    logs = entry_files(ROOT / "log")
    ideas = entry_files(ROOT / "ideas")

    # 1. Work with no recorded question.
    if runs and not ideas:
        rep.warn(
            "resumability: runs exist but ideas/ is empty — no file states what question "
            "the work is answering (AGENTS.md, Keep the notebook resumable)"
        )

    # 2. A session log that does not say what to do next.
    without_next = [
        path.name for path in logs
        if not re.search(r"^##\s+Next\b", path.read_text(encoding="utf-8"), re.MULTILINE)
    ]
    if without_next:
        rep.warn(
            f"resumability: {len(without_next)} log entr(y/ies) have no '## Next' section: "
            + ", ".join(without_next[:3]) + (" ..." if len(without_next) > 3 else "")
        )

    # 3. A run that no session log covers. Compared by date, since that is all the
    #    naming convention guarantees.
    newest_run = max((entry_date(run) for run in runs), default="")
    newest_log = max((entry_date(path) for path in logs), default="")
    if newest_run and newest_run > newest_log:
        rep.warn(
            f"resumability: newest run is {newest_run} but newest log entry is "
            f"{newest_log or 'none'} — a run with no session log around it is a number "
            "nobody can place"
        )

    # 4. A run whose parameters are recorded without their reasons.
    unexplained = [
        run.name for run in runs
        if (run / "README.md").exists()
        and not re.search(
            r"^##\s+Why these parameters\b",
            (run / "README.md").read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    ]
    if unexplained:
        rep.warn(
            f"resumability: {len(unexplained)} run(s) have no '## Why these parameters' "
            "section — params.toml records what, not why: "
            + ", ".join(unexplained[:3]) + (" ..." if len(unexplained) > 3 else "")
        )


def parse_shards(rep: Report) -> list[dict[str, str]]:
    """Validate the lab book's structure and return its shards in order."""
    master = ROOT / "labbook.tex"
    catalog = ROOT / "labbook" / "SHARD_CATALOG.md"
    source_map = ROOT / "labbook" / "README.md"
    for required in (master, catalog, source_map):
        if not required.exists():
            rep.error(f"{required.relative_to(ROOT)} is missing")
            return []

    body = "\n".join(
        line for line in master.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("%")
    )
    includes = re.findall(r"\\include\{([^}]+)\}", body)
    if not includes:
        rep.error("labbook.tex has no \\include statements")
        return []

    catalog_text = catalog.read_text(encoding="utf-8")
    map_text = source_map.read_text(encoding="utf-8")

    shards: list[dict[str, str]] = []
    seen_files: set[str] = set()
    seen_ids: set[str] = set()

    for include in includes:
        if not include.startswith("labbook/sections/"):
            rep.error(f"\\include{{{include}}} must point under labbook/sections/")
            continue
        if include in seen_files:
            rep.error(f"\\include{{{include}}} appears more than once in labbook.tex")
            continue
        seen_files.add(include)

        path = ROOT / f"{include}.tex"
        if not path.exists():
            rep.error(f"\\include{{{include}}} points at missing {include}.tex")
            continue

        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > SHARD_MAX_LINES:
            rep.error(f"{include}.tex is {len(lines)} lines, over the {SHARD_MAX_LINES} cap")

        header: dict[str, str] = {}
        for line in lines[:12]:
            match = re.match(r"%\s*(SHARD-[A-Z]+):\s*(.*)", line)
            if match:
                key, value = match.group(1), match.group(2).strip()
                header[key] = f"{header[key]} {value}".strip() if key in header else value
        missing = [k for k in SHARD_HEADER_KEYS if k not in header]
        if missing:
            rep.error(f"{include}.tex header is missing {', '.join(missing)}")
            continue

        shard_id = header["SHARD-ID"]
        if shard_id in seen_ids:
            rep.error(f"duplicate SHARD-ID {shard_id}")
        seen_ids.add(shard_id)
        if f"`{shard_id}`" not in catalog_text:
            rep.error(f"{shard_id} is not listed in labbook/SHARD_CATALOG.md")
        if f"`{shard_id}`" not in map_text:
            rep.error(f"{shard_id} is not in the order table in labbook/README.md")

        shards.append({"id": shard_id, "title": header["SHARD-TITLE"], "file": f"{include}.tex"})

    for orphan in sorted((ROOT / "labbook" / "sections").glob("*.tex")):
        rel = str(orphan.relative_to(ROOT).with_suffix(""))
        if rel not in seen_files:
            rep.error(f"{orphan.relative_to(ROOT)} exists but is not included in labbook.tex")

    return shards


def check_labbook_hygiene(rep: Report) -> None:
    r"""Defects a 2026-08-01 review found by hand, so they cannot recur silently.

    Empty ``\evS{key}{}`` locations violate the source-citation rule in
    ``AGENTS.md``; a promoted shard must carry no ``\TODO``. Both are warnings
    rather than errors while the backlog is worked down -- the count is what
    matters, and it must not grow.

    The citekey must be non-empty for the tag to be a citation at all. A bare
    ``\evS{}{}`` is the notation being *named* in prose -- the frontmatter
    explains the tags, and the open-questions shard refers to them -- and is not
    a citation missing its location. Matching those too cost a permanent warning
    of three that no edit could clear, which is worse than useless: a standing
    count hides a real one appearing beside it.
    """
    empty_loc = 0
    for path in sorted((ROOT / "labbook" / "sections").glob("*.tex")):
        text = path.read_text(encoding="utf-8")
        empty_loc += len(re.findall(r"\\evS\{[^}]+\}\{\s*\}", text))
        if "\\TODO{" in text:
            rep.error(f"{path.relative_to(ROOT)}: promoted shard contains a TODO")
    if empty_loc:
        rep.warn(f"labbook: {empty_loc} \\evS tags with an empty location "
                 f"(AGENTS.md requires a section/equation/figure)")


def check_links(rep: Report) -> None:
    for path in markdown_files():
        if is_scratch(path):
            continue
        text = strip_code_blocks(path.read_text(encoding="utf-8"))
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                rep.error(f"{path.relative_to(ROOT)}: broken link -> {target}")


def check_file_sizes(rep: Report) -> None:
    for path in ROOT.rglob("*"):
        parts = set(path.relative_to(ROOT).parts)
        if not path.is_file() or parts & SKIP_DIRS or "pdfs" in parts or "src" in parts:
            continue
        size = path.stat().st_size
        if size > LARGE_FILE_BYTES:
            mb = size / 1024 / 1024
            rep.warn(f"{path.relative_to(ROOT)} is {mb:.1f} MB — see the artefact policy")


# --------------------------------------------------------------------------- #
# INDEX.md generation
# --------------------------------------------------------------------------- #


def entry_rows(directory: Path, prefix: str) -> list[str]:
    rows = []
    for path in entry_files(directory):
        fm = read_frontmatter(path)
        rows.append(
            f"| [{path.stem}]({prefix}{path.name}) | {markdown_title(path)} "
            f"| {fm.get('status', '—')} | {fm.get('confidence', '—')} | {fm.get('updated', '—')} |"
        )
    if not rows:
        return ["_none yet_"]
    return ["| Entry | Title | Status | Confidence | Updated |", "|---|---|---|---|---|", *rows]


def index_blocks(shards: list[dict[str, str]], runs: list[Path], sources: dict) -> dict:
    blocks: dict[str, list[str]] = {}
    blocks["ideas"] = entry_rows(ROOT / "ideas", "ideas/")
    blocks["derivations"] = entry_rows(ROOT / "derivations", "derivations/")
    blocks["attic"] = entry_rows(ROOT / "attic", "attic/")
    blocks["log"] = entry_rows(ROOT / "log", "log/")

    if sources:
        rows = ["| Citekey | Citation | Local |", "|---|---|---|"]
        for key, row in sorted(sources.items()):
            note = ROOT / "literature" / "notes" / f"{key}.md"
            local = f"[notes](literature/notes/{key}.md)" if note.exists() else "_no notes_"
            rows.append(f"| `{key}` | {row['citation']} | {local} |")
        blocks["sources"] = rows
    else:
        blocks["sources"] = ["_none yet_"]

    sims = [
        p for p in sorted((ROOT / "sims").iterdir())
        if p.is_dir() and not p.name.startswith("_")
    ] if (ROOT / "sims").is_dir() else []
    blocks["sims"] = (
        ["| Simulation | README |", "|---|---|"]
        + [f"| `{p.name}` | [README](sims/{p.name}/README.md) |" for p in sims]
        if sims
        else ["_none yet_"]
    )

    blocks["runs"] = (
        ["| Run | Title |", "|---|---|"]
        + [
            f"| [{p.name}](runs/{p.name}/README.md) | {markdown_title(p / 'README.md')} |"
            for p in runs
            if (p / "README.md").exists()
        ]
        if runs
        else ["_none yet_"]
    )

    blocks["shards"] = (
        ["| ID | Title | Source |", "|---|---|---|"]
        + [f"| `{s['id']}` | {s['title']} | [{s['file']}]({s['file']}) |" for s in shards]
        if shards
        else ["_none yet_"]
    )
    return blocks


def render_index(blocks: dict[str, list[str]]) -> str:
    """Return INDEX.md with the generated blocks replaced. Writes nothing."""
    text = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    for name, lines in blocks.items():
        pattern = re.compile(
            rf"(<!-- BEGIN:GENERATED {name} -->\n).*?(<!-- END:GENERATED {name} -->)",
            re.DOTALL,
        )
        body = "\n".join(lines) + "\n"
        text = pattern.sub(lambda m, body=body: m.group(1) + body + m.group(2), text)
    return text


def write_index(blocks: dict[str, list[str]]) -> bool:
    index = ROOT / "INDEX.md"
    updated = render_index(blocks)
    if updated != index.read_text(encoding="utf-8"):
        index.write_text(updated, encoding="utf-8")
        return True
    return False


# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate the INDEX.md tables")
    args = parser.parse_args(argv)

    rep = Report()
    keys = bib_citekeys(rep)
    sources = check_sources(rep, keys)
    check_citekeys(rep, keys)
    runs = check_runs(rep)
    check_run_sha_containment(rep, runs)
    check_resumability(rep, runs)
    shards = parse_shards(rep)
    check_links(rep)
    check_labbook_hygiene(rep)
    check_file_sizes(rep)

    if args.write:
        changed = write_index(index_blocks(shards, runs, sources))
        print("INDEX.md updated" if changed else "INDEX.md already current")

    for warning in rep.warnings:
        print(f"warning: {warning}")
    for error in rep.errors:
        print(f"error: {error}", file=sys.stderr)

    if rep.errors:
        print(f"\n{len(rep.errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"ok — {len(sources)} source(s), {len(runs)} run(s), {len(shards)} shard(s), "
        f"{len(rep.warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
