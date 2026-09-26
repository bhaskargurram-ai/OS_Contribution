# cohere-python #796 — Batched embeddings drop types absent from the first response

**Status:** branch pushed (commit `463e9d9`), PR not yet opened
**Branch:** `bhaskargurram-ai/cohere-python` → `fix/merge-embed-responses-all-types`
**Open the PR:** https://github.com/cohere-ai/cohere-python/compare/main...bhaskargurram-ai:cohere-python:fix/merge-embed-responses-all-types?expand=1

Title:

```
Merge embedding types present in any batched embed response
```

Body (paste as-is):

---

Fixes #796.

`Client.embed()` splits large `texts` inputs into batches and combines the per-batch results with `merge_embed_responses()` in `src/cohere/utils.py`. For `embeddings_by_type` responses, that function decided *which* embedding fields to merge by inspecting only `responses[0].embeddings` and keeping the fields that were non-`None` there.

If a later batch contained an embedding type that the first batch did not (for example the first batch only has `float` while a second batch also has `int8`), the extra type was never added to the field list, so its values were silently dropped from the merged `EmbedByTypeResponseEmbeddings`. No error was raised, the merged response simply had `int8=None`.

Reproduction (no network, two hand-built responses):

```python
from cohere import EmbeddingsByTypeEmbedResponse, EmbedByTypeResponseEmbeddings
from cohere.utils import merge_embed_responses

first = EmbeddingsByTypeEmbedResponse(response_type="embeddings_by_type", id="1",
    embeddings=EmbedByTypeResponseEmbeddings(float_=[[0.1, 0.2]]))
second = EmbeddingsByTypeEmbedResponse(response_type="embeddings_by_type", id="2",
    embeddings=EmbedByTypeResponseEmbeddings(float_=[[0.3, 0.4]], int8=[[3, 4]]))

merged = merge_embed_responses([first, second])
print(merged.embeddings.int8)
```

| | `merged.embeddings.float_` | `merged.embeddings.int8` |
|---|---|---|
| before | `[[0.1, 0.2], [0.3, 0.4]]` | `None` (dropped) |
| after | `[[0.1, 0.2], [0.3, 0.4]]` | `[[3, 4]]` |

### Change

`src/cohere/utils.py` (listed in `.fernignore`, so it is hand-maintained and survives regeneration): the field list is now the union of `EmbedByTypeResponseEmbeddings` fields that are non-`None` on *any* of the responses, iterated in the model's declared field order so the result is deterministic and order-preserving.

Behaviour for a type that is present in some batches but not others: the batches where it is `None` contribute nothing and the values from the other batches are concatenated. This is the behaviour the existing `test_merge_embeddings_by_type_with_none_field_in_later_response` already pins down (float present in batch 1, `None` in batch 2, result is batch 1's values), so raising instead would have been a behaviour change for that case. A type that is `None` in every response stays `None` in the merged result.

`get_fields()` is now called with the model class rather than the first instance; it already accepts a class elsewhere (`overrides.allow_access_to_aliases`), and this avoids pydantic 2.11's deprecation warning for instance-level `model_fields` access.

### Tests

Added `test_merge_embeddings_by_type_includes_types_absent_from_first_response` in `tests/test_embed_utils.py`: three batches where the first has only `float`, the second has `float`/`int8`/`ubinary`, and the third has only `int8`; asserts the merged result has all three types with the values concatenated in batch order and that `uint8`/`binary`/`base64` remain `None`. It fails on `main` (`int8=None, ubinary=None` in the result) and passes with this change.

Commands run:

- `pytest tests/test_embed_utils.py` — 7 passed (6 existing + 1 new)
- `pytest tests/test_embed_utils.py tests/test_embed_streaming.py tests/test_overrides.py` — 17 passed
- `mypy src/cohere/utils.py tests/test_embed_utils.py` — Success: no issues found
- `ruff check` / `ruff format --check` on both files — the only findings (I001 on the import blocks, and "would reformat") are pre-existing on `main` and untouched by this change; I did not reformat the files to keep the diff minimal.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Cloned `bhaskargurram-ai/cohere-python` (default branch `main`, HEAD `953f5a1` "SDK regeneration (#803)"); created `fix/merge-embed-responses-all-types` from it.
- Confirmed `src/cohere/utils.py` and `tests` are listed in `.fernignore` (safe to hand-edit; CONTRIBUTING.md says Fern-generated files are overwritten otherwise).
- Reproduced the bug with the script above on unmodified code: `merged.embeddings.int8 = None`, `AssertionError: BUG: int8 from second batch was dropped`. After the fix: `int8 = [[3, 4]]`.
- New regression test run against `main`'s `utils.py`: 1 failed (`AssertionError: ... int8=None ... != ... int8=[[5, 6], [9, 10]] ...`). With the fix: passes.
- `pytest tests/test_embed_utils.py -q` — 7 passed.
- `pytest tests/test_embed_utils.py tests/test_embed_streaming.py tests/test_overrides.py -q` — 17 passed.
- `mypy src/cohere/utils.py tests/test_embed_utils.py` (mypy 1.13.0, as pinned in pyproject) — no issues.
- `ruff check` (0.11.5) and `ruff format --check` on the two files: 2 I001 findings and 2 "would reformat" — verified identical on `main` via `git stash`; not introduced by this change.
- Full `pytest` was not run: most other test files call the live Cohere API and need `CO_API_KEY`.
- No CHANGELOG file exists in the repo; no entry added.
- Commit author `Bhaskar Gurram <gurrambhaskar.ai@gmail.com>`; no AI trailers. Pushed with `git push -u origin fix/merge-embed-responses-all-types`; `origin/main` unchanged at `953f5a1`, so no rebase was needed.
