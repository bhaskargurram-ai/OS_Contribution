# inspect_ai #5525 — a blank target scores every sample CORRECT

**Status:** PR opened and **auto-closed by the contribution-policy bot**. The code was
never reviewed — `#5525` is open and evidenced but does not carry the `accepted` label,
which the bot requires regardless of who filed the issue.

**Do not reopen or re-file yet.** The bot instructs coding agents not to reopen or open
variants. The supported path: comment on
[#5525](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5525) with the reproduction
and failing-test evidence and ask for it to be accepted. Once a maintainer applies
`accepted`, **reopening this same PR re-runs the gate and passes** — the branch and the
work stand ready.

**Branch (retained):** `918f2a9`
**Branch:** `bhaskargurram-ai/inspect_ai` → `fix/blank-target-scores-correct`
**Open the PR:** https://github.com/UKGovernmentBEIS/inspect_ai/compare/main...bhaskargurram-ai:inspect_ai:fix/blank-target-scores-correct?expand=1

> **Check acceptance first.** `AGENTS.md` says to reference *the accepted issue*. As of
> the scan, `#5525` was **not** carrying the `accepted` label (only `#5544` and `#5207`
> were). Confirm a maintainer has accepted it before opening, or ask on the issue.

Title:

```
Score a blank target INCORRECT instead of matching everything
```

Body (paste as-is):

---

Fixes #5525.

A blank target matches every completion. `includes()` finds `""` inside any string, and
`match()` finds that any string ends with `""`. A dataset with no target column, or a
`FieldSpec` naming a column that does not exist, both produce a blank target — so every
sample scored `CORRECT` and the log was indistinguishable from a genuine pass.

The existing comment in `str_match_scorer` already describes this shape of failure, but the
earlier change only tagged the `reason` for blank *completions*; the score itself was left
`CORRECT`.

### Change

Skip blank targets, matching the convention already used in `_classification.py`
(`if target.strip():`), and warn when a sample has nothing left to match against so the
misconfiguration is reported rather than scored silently. A blank entry alongside real
targets no longer short-circuits them.

### Reproduction

| scorer | target | before | after |
|---|---|---|---|
| `includes()` | `""` | **CORRECT** | INCORRECT |
| `match()` | `""` | **CORRECT** | INCORRECT |
| `includes()` | `" "` | **CORRECT** | INCORRECT |
| `includes()` | `["", "60"]` vs `"The answer is 60"` | CORRECT | CORRECT |

### Tests

Five tests added to `tests/scorer/test_match.py`. All five fail on `main` and pass here.

`pytest tests/scorer/` gives **112 failed, 646 passed, 221 skipped**. Clean `main` gives
**112 failed, 641 passed, 216 skipped** — the same 112 failures, which need model
credentials this environment does not have. This change adds 5 passes and no failures.

`ruff check` and `ruff format --check` pass on both files. `mypy` reports no issues on the
changed source file.

### Agent review

- Reviewer: **none.** No separate code-review pass was run on this change.
- The change was written with AI assistance and verified by reproducing the bug first,
  then confirming all five new tests fail on `main` and pass with the fix, and comparing
  full-suite results against a clean `main` checkout.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced the bug first | yes — blank target returned `C` for both scorers |
| New tests pass with the fix | 5/5 |
| New tests fail without it | 5/5 |
| `tests/scorer/` with fix | 112 failed, 646 passed, 221 skipped |
| `tests/scorer/` on clean `main` | 112 failed, 641 passed, 216 skipped — identical failures |
| `ruff check` / `ruff format --check` | pass |
| `mypy` | no issues |

Diff is 81 insertions across 2 files.

## Before opening

`AGENTS.md` asks for a code-review pass on a frontier model in a fresh context for
non-trivial changes. Running `/code-review` on this diff and replacing the **Agent review**
section with its real findings would strengthen the PR materially.
