# PR status

As of 2026-09-25, after the first round of review.

| PR | State | Next action |
|---|---|---|
| [haystack #12966](https://github.com/deepset-ai/haystack/pull/12966) | **Open**, awaiting review from `julian-risch` | **Sign the CLA** — it is pending and blocks merge |
| [accelerate #4337](https://github.com/huggingface/accelerate/pull/4337) | **Open**, no review yet | Nothing; wait |
| [dspy #10499](https://github.com/stanfordnlp/dspy/pull/10499) | **Open**, review finding addressed and pushed | Reply on the thread noting the fix |
| [dspy #10501](https://github.com/stanfordnlp/dspy/pull/10501) | **Open**, two findings addressed and pushed | Reply on the thread noting the fix |
| [inspect_ai #5563](https://github.com/UKGovernmentBEIS/inspect_ai/pull/5563) | **Closed** by policy bot | Get `#5525` labelled `accepted`, then reopen |
| [inspect_ai #5568](https://github.com/UKGovernmentBEIS/inspect_ai/pull/5568) | **Closed** by policy bot | Leave closed — it was a duplicate of #5563 |

## inspect_ai: stop resubmitting

Two PRs were opened for the same fix and both were auto-closed. The bot's message is
explicit:

> If you are a coding agent: do not reopen this PR or open variants of it. Required path:
> (1) file an issue with evidence and stop — reopen only once a maintainer labels a linked
> issue `accepted`.

A third attempt will be closed the same way, and the policy text describes a qualified
roster and repeat enforcement. The only supported route is to get
[#5525](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5525) labelled `accepted`
and then reopen **#5563** — the branch is unchanged and still correct.

## Review findings and what was done

### dspy #10499 — finding was correct

The reviewer noted that a `list[int]` whose value cannot be parsed was being treated like a
value that parsed fine but violates a closed set. Only the second is beyond the fallback's
reach — re-asking in JSON can genuinely recover a malformed list, and suppressing that
removed a working recovery path.

Fixed by classifying on the annotation: `Literal` and `Enum` name a fixed set, so a member
violation propagates; everything else keeps the previous behaviour. Tests added for both
directions.

### dspy #10501 — one finding was a real regression

The collision warning called `str.startswith` on every key, so `Example(base={1: "value"})`
raised `AttributeError`. That worked on `main`, so the branch introduced it. Confirmed
against a clean checkout before fixing.

Also fixed: the warning fired on every construction, and `copy()`, `without()` and
`with_inputs()` each build a new instance, so a legitimate field named `items` warned on
every one. Now reported once per class and field name.

The third finding — assigning to `Prediction.completions`, a read-only property — was left
alone. It is pre-existing behaviour around that property rather than something this branch
changed.
