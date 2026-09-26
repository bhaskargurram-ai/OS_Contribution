# langsmith-sdk #3569 — `raise_for_status_with_text` drops `.response`

**Status:** branch pushed (`059527c`), PR not yet opened
**Branch:** `bhaskargurram-ai/langsmith-sdk` → `fix/http-error-keeps-response`
**Open the PR:** https://github.com/langchain-ai/langsmith-sdk/compare/main...bhaskargurram-ai:langsmith-sdk:fix/http-error-keeps-response?expand=1

No AI-disclosure requirement found. `python/AGENTS.md` asks for `make format`, `make lint`,
`make tests` from `python/`; ruff check and format pass on both changed files.

**Note:** `CONTRIBUTING.md` says the SDKs are migrating to `langsmith-python-staging` and
"open new work there when you can", but merges to `main` here are mirrored hourly, so a
PR here still lands. The issue lives here, so this targets here.

Title:

```
Keep the response on HTTPError raised by raise_for_status_with_text
```

Body (paste as-is):

---

Fixes #3569.

The `requests` branch re-raised as `requests.HTTPError(str(e), response.text)`, passing the
response text positionally. `requests.HTTPError` only sets `.response` from the keyword
argument, so a positional value lands in `.args` and `.response` stays `None`:

```python
exc.response                          # None
exc.__cause__.response.status_code    # 429 — only reachable via the cause
```

The status code and headers of the failed request — `Retry-After` among them — were
unreachable from the error a caller actually catches, which breaks retry logic that reads
them. The `httpx` branch already passes `response=response`; the two were inconsistent.

### Change

Pass `response=response` as well. `.args` is unchanged, so anything reading the text
positionally still works, and `.response` now matches the `httpx` branch.

### Reproduction

A 429 with `Retry-After: 7`:

| | before | after |
|---|---|---|
| `exc.response` | `None` | the `Response` |
| `exc.response.headers["Retry-After"]` | unreachable | `"7"` |
| `exc.args[1]` | `"rate limited"` | `"rate limited"` (unchanged) |

### Tests

One test added to `tests/unit_tests/test_utils.py` asserting `.response` is the original
response, the status and header are reachable, and `.args[1]` is unchanged. **Fails on
`main`** (`assert None is <Response [429]>`), passes here.

### AI assistance

This change was produced with AI assistance. I reviewed every line, ran the test, and can
defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on `main` | `exc.response is None -> True` |
| New test fails on `main` | yes — `assert None is <Response [429]>` |
| New test passes with fix | yes |
| `ruff check` / `ruff format --check` | pass |
| `uv.lock` | rewritten by `uv sync`, reverted before commit |

Diff is 27 insertions, 1 deletion across 2 files.
