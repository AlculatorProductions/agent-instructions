"""Template simulation entry point.

Physics: <what is modelled>, solving <equation>, cited to [S:Key eq.4] or
[D:YYYY-MM-DD-slug] — give the repo-relative path too (e.g.
derivations/YYYY-MM-DD-slug.md) so the reference is click-to-open in an
editor. Conventions: SI throughout, see CONVENTIONS.md.

Copy this directory to ``sims/<slug>/`` and replace ``simulate`` with the real
computation. Everything else here is the provenance machinery that makes a run
citable: it records the code version, the parameters and the environment next to
the output, so the numbers can be regenerated.

Usage:
    pixi run python sims/<slug>/run.py --params params.toml --out runs/2026-07-29-<slug>/
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def git_sha() -> str:
    """Commit the code is running at; ``unknown`` outside a git checkout."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    dirty = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    return out.stdout.strip() + ("-dirty" if dirty else "")


def lock_hash() -> str:
    """Identify the environment by hashing pixi.lock."""
    import hashlib

    lock = REPO_ROOT / "pixi.lock"
    if not lock.exists():
        return "no-lock"
    return hashlib.sha256(lock.read_bytes()).hexdigest()[:16]


def simulate(params: dict[str, Any]) -> dict[str, Any]:
    """Run the computation and return the summary results.

    Replace this. Assert your preconditions here — grid resolution against the
    relevant length scale, timestep against the fastest phase, normalisation
    after propagation. A loud failure beats a silent NaN.
    """
    raise NotImplementedError("replace simulate() with the actual computation")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--params", type=Path, required=True, help="TOML parameter file")
    parser.add_argument("--out", type=Path, required=True, help="run directory to write into")
    args = parser.parse_args(argv)

    params = tomllib.loads(args.params.read_text())

    out = args.out
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)

    # The parameters travel with the output: a run is code SHA + params + env.
    (out / "params.toml").write_text(args.params.read_text())

    results = simulate(params)

    provenance = {
        "date": date.today().isoformat(),
        "simulation": str(Path(__file__).relative_to(REPO_ROOT)),
        "git_sha": git_sha(),
        "pixi_lock_sha256": lock_hash(),
        "command": " ".join([sys.executable, *sys.argv]),
        "results": results,
    }
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")

    print(f"wrote {out}/provenance.json — now fill in {out}/README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
