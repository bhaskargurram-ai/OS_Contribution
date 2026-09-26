# dspy #10498 — ChatAdapter falls back on validation errors

**Status:** branch pushed (commit `8eb2a57`), PR not yet opened
**Branch:** `bhaskargurram-ai/dspy` → `fix/chat-adapter-validation-fallback`
**Open the PR:** https://github.com/stanfordnlp/dspy/compare/main...bhaskargurram-ai:dspy:fix/chat-adapter-validation-fallback?expand=1

Title:

```
Don't fall back to JSONAdapter when a value fails validation
```

Body (paste as-is):

---

Fixes #10498.

`ChatAdapter` raises `AdapterParseError` for two unrelated situations:

1. the response does not conform to the chat wire format (field markers missing or garbled), and
2. the response is well-formed but a value fails validation against its field annotation.

The `JSONAdapter` fallback currently treats both as format failures. For the second case
that costs a second LM call which cannot succeed — the LM is asked again and returns the
same out-of-domain value — and the specific validation error is replaced by a generic
serialization error from `JSONAdapter`, so the actual cause is lost.

This also contradicts the documented intent of `use_json_adapter_fallback`, whose
docstring already says only invalid *format* should trigger the extra call.

### Change

`AdapterParseError` gains an `is_format_error` flag. It is set to `False` where
`parse_value` rejects a value that was successfully extracted — reaching that point means
the markers were found, so the format was fine. `ChatAdapter.__call__`/`acall` fall back
only when the failure is a genuine format error.

The flag defaults to `True`, so any caller that does not classify its failure keeps the
previous behaviour.

`XMLAdapter` subclasses `ChatAdapter` and had the same split between "XML did not parse"
and "field value failed validation", so it is classified the same way.

### Behaviour

```python
class Color(dspy.Signature):
    question: str = dspy.InputField()
    color: Literal["red", "blue"] = dspy.OutputField()
```

With the LM returning a well-formed response carrying `green`:

| | before | after |
|---|---|---|
| LM calls | 2 | 1 |
| error surfaced | generic JSON serialization error | the `Literal` validation error, naming the field |

A response with no field markers at all still falls back exactly as before.

### Tests

Four tests in `tests/adapters/test_chat_adapter.py` covering the sync path, the async
path, the preserved fallback for malformed responses, and the default value of the flag.
All three behavioural tests fail on `main` and pass here.

`tests/adapters` (373 tests) and `tests/predict` pass. Two failures in `tests/clients`
(`test_native_anthropic_top_k_stays_native`, `test_plan_reads_no_stored_login`) reproduce
identically on an unmodified checkout of `main` and are unrelated to this change.

---

## Verification performed

| Check | Result |
|---|---|
| New tests pass with the fix | 4/4 |
| New tests fail without the fix | 3/3 behavioural tests fail (4th asserts the new attribute exists) |
| `tests/adapters` | 373 passed |
| `tests/predict` + `tests/adapters` | 881 passed, 145 skipped |
| Two `tests/clients` failures | reproduce on clean `main` — pre-existing |
| `ruff check` | passes |
| `ruff format --check` | repo is not format-clean upstream; my lines add nothing new |

Diff is 113 insertions across 4 files.

## Round 2 — pushed `f8331b7` (2026-09-26)

Greptile P2 on https://github.com/stanfordnlp/dspy/pull/10499: `Literal[...] | None` was
classified as open-ended because only the top-level origin was checked. Fixed by unwrapping
unions (closed-set when every non-None member is). New test
`test_chat_adapter_does_not_fall_back_for_an_optional_literal_member_violation` fails on
the previous head, passes now. `pytest tests/adapters tests/predict` — 884 passed, 145
skipped. ruff clean.

Reply to post on the PR thread (discussion_r4109162525):

---
Good catch — `Literal[...] | None` has a `Union` origin, so the top-level check treated it
as open-ended. `f8331b7` unwraps unions: an annotation is closed-set when every member
other than `None` is. Added a test for the optional Literal case; it fails on the previous
head. `pytest tests/adapters tests/predict` — 884 passed, 145 skipped.
---
