I have a fix ready for this and would like to put it up, but PRs are gated on the issue
carrying `accepted` — could a maintainer take a look?

Evidence, confirmed against current `main`:

```python
from inspect_ai.scorer._match import includes, match
from inspect_ai.scorer._target import Target

# with a completion of "some answer"
includes()(state, Target([""]))   # -> CORRECT
match()(state, Target([""]))      # -> CORRECT
includes()(state, Target([" "]))  # -> CORRECT
```

`includes()` finds `""` inside any string and `match()` finds that any string ends with
`""`, so a dataset with no target column — or a `FieldSpec` naming a column that does not
exist — scores every sample CORRECT. The log is indistinguishable from a genuine pass.

The comment already in `str_match_scorer` describes this shape of failure, but the earlier
change only tagged the `reason` for blank *completions*; the score itself stays CORRECT.

The fix I have skips blank targets — the same `if target.strip():` guard
`_classification.py` already uses — and warns when a sample has nothing left to match
against, so the misconfiguration is reported rather than scored silently. A blank entry
alongside real targets no longer short-circuits them.

Five tests, all failing on `main` and passing with the fix. `pytest tests/scorer/` gives
the same 112 pre-existing failures as a clean `main` checkout (they need model
credentials), plus 5 passes.

Branch is ready — I'll open the PR as soon as this is accepted.
