# attic/

Failed attempts, kept on purpose.

An approach that did not work is a result: it rules something out, and it cost real effort to
learn. Deleting it means the next session — human or agent — will cheerfully rebuild it. This
directory exists so that does not happen.

One entry per dead end: `attic/<YYYY-MM-DD>-<slug>.md`, or a directory of the same name when there
is code worth keeping alongside the write-up.

## What an entry must say

1. **What was tried** — concretely enough to recognise the same idea when it comes back in a
   different costume.
2. **Why it failed** — the actual reason. Distinguish sharply between:
   - *wrong* — the idea is refuted; here is the argument or the run that killed it;
   - *not viable here* — it might work, but not with our resources, tools or regime;
   - *abandoned* — it was set aside for priorities, not for evidence. Say so honestly; this one is
     a candidate for revival.
3. **What it rules out** — the useful part. Which region of the space is now known to be empty.
4. **What is worth salvaging** — a lemma, a piece of code, a numerical trick, a good failure mode.
5. **What would change the verdict** — the result, tool or measurement that would make it worth
   another try.

Tag the reasoning as everywhere else: `[C:run-id]` for a run that killed it, `[S:Key]` for a paper
that already showed it fails, `[I]` for our judgement that it is not worth continuing.

## Links

Every entry links back to the idea, derivation or run it came from, and that idea's `status` is set
to `refuted` (evidence killed it) or `parked` (we stopped for other reasons). Both directions —
finding the attic entry from the idea matters more than the reverse.

## What does not belong here

Runs that merely crashed: those are recorded in their own [`../runs/`](../runs/) directory. The
attic is for approaches, not for executions.
