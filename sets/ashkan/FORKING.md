# FORKING — the protocol for going back

Follow this file, step by step, whenever the user asks to go back or branch off, or expresses
doubt that the notebook still reflects their research — even vaguely ("this stopped feeling like
my project"). Stop the current task first. Throughout: the user renders judgments on artefacts;
the agent does all the git work. No step asks the user to run a git command or read a raw SHA.

## 1. Name the symptom

Ask what feels wrong, and sort the answer into one mode — it decides what to search for:

| Mode | What the user says | What to find |
|---|---|---|
| Contaminated | wrong facts got in, hallucinations | the **first bad** commit; base is the one before it |
| Drifted | the research went somewhere they don't want | the **last commit that still felt right** |
| Taste | the notes no longer read like theirs | same as drifted, judged on voice and framing, not claims |
| New topic | nothing is wrong, new question | no search — base is the current tip; go to step 5 |

## 2. Show the terrain

Refresh the commit line (`pixi run check --write`) and show the table from
[TIMELINE.md](TIMELINE.md): phrases, dates, ✓ gate marks as orientation. Ask whether the user
already suspects a region ("somewhere before last week") and narrow the range to it.

## 3. Bisect by feel

`INDEX.md` is generated and committed, so `git show <sha>:INDEX.md` reconstructs a readable
snapshot of the whole notebook at any commit — every idea with its status and confidence, every
source, run and shard title as they stood then.

Probe the range: bisection when it is long, a walk backwards when it is short. At each probe show
a short digest, never raw diffs:

- the `INDEX.md` snapshot at that commit;
- one or two salient excerpts — the file the user is uneasy about as it read then, or that
  commit's `log/` entry.

Ask only: **"still yours / already wrong / unsure?"** Narrow until the boundary is found. The
base is the last "still yours".

## 4. Salvage before cutting

List what exists only *after* the chosen base — ideas, derivations, runs, shards — and ask what
to carry over.

- Worth keeping → copied as **file content** onto the new branch after step 5. Never cherry-pick
  commits: content travels, history does not.
- Ruled out → an `attic/` entry on the new branch: what the abandoned line tried and what it
  taught. Deleting a dead end silently means rebuilding it later.

## 5. Execute and record

1. `git switch -c fork/<YYYY-MM-DD>-<slug> <base-sha>`.
2. Append the fork block to [TIMELINE.md](TIMELINE.md): base (C-number + short SHA), abandoned
   tip marked ✗, and the reason **in the user's own words** — the subjective why is the one thing
   git cannot store, and the thing their future self needs.
3. Bring over the salvage and write the attic entries from step 4.
4. Write a `log/` entry for the fork session: the mode, the base, what was left behind, and the
   first next action.

## 6. Re-anchor

Run `pixi run check` (and `pixi run labbook` if the lab book is affected) on the new branch — a
taste-chosen base is not guaranteed gate-green. Fix what they report, refresh the commit line,
commit, and push if `origin` is registered. The fork's first commit is then itself a ✓ anchor.

## Limits

The probes are only as good as `INDEX.md` and `log/` were at each commit — which the
close-a-session rules exist to guarantee. If a probe shows a stale index, say so: that is a
defect of that commit, and it means leaning more on the `log/` entries around it.
