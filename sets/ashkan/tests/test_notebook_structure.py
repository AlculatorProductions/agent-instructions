"""Gate B for the notebook itself: the record must hang together.

Runs the same checks as ``pixi run check`` so that ``pixi run test`` fails when
a source is unregistered, a citekey dangles, a run is undocumented, a link is
broken, or the lab book's shard structure has drifted.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check  # noqa: E402


def test_repository_is_consistent():
    assert check.main([]) == 0


def test_labbook_shards_are_registered():
    report = check.Report()
    shards = check.parse_shards(report)
    assert not report.errors, report.errors
    assert shards, "the lab book has no shards"
    assert shards[0]["id"] == "NB-00-FRONTMATTER", "the frontmatter shard must stay first"


def test_index_is_current():
    """INDEX.md must match the sources it is generated from. Read-only."""
    report = check.Report()
    keys = check.bib_citekeys(report)
    blocks = check.index_blocks(
        check.parse_shards(report),
        check.check_runs(report),
        check.check_sources(report, keys),
    )
    expected = check.render_index(blocks)
    actual = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    assert actual == expected, "INDEX.md is stale — run `pixi run check --write`"
