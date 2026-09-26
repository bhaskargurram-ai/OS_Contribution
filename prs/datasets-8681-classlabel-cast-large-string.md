# datasets #8681 — `ClassLabel.cast_storage` rejects `large_string` / `string_view`

**Status:** branch pushed (`f9e91ec`), PR not yet opened
**Branch:** `bhaskargurram-ai/datasets` → `fix/classlabel-cast-large-string`
**Open the PR:** https://github.com/huggingface/datasets/compare/main...bhaskargurram-ai:datasets:fix/classlabel-cast-large-string?expand=1

Second datasets PR; same repo rules as #8637 (no AI-disclosure requirement, `make style`
passes). The reporter offered to submit a PR — none exists yet; the body below says I'll
defer if theirs lands first.

Title:

```
Cast large_string and string_view storage in ClassLabel
```

Body (paste as-is):

---

Fixes #8681.

`ClassLabel.cast_storage` decided whether to map label names to ids with
`isinstance(storage, pa.StringArray)`. `pa.LargeStringArray` and `pa.StringViewArray` are
not subclasses of `pa.StringArray`, so arrays of those types fell through to
`array_cast(storage, int64)`, which tried to parse the label names as integers:

```
ArrowInvalid: Failed to parse string: 'neg' as a scalar of type int64
```

pandas 3 produces `large_string` for plain string columns, so the most ordinary input now
fails:

```python
feats = Features({"label": ClassLabel(names=["neg", "pos"])})
Dataset.from_pandas(pd.DataFrame({"label": ["neg", "pos", "neg"]}), features=feats)
```

`class_encode_column` was unaffected because it takes a different path.

### Change

Check the Arrow type instead of the array class, accepting `string`, `large_string` and
`string_view`.

### Verified on pandas 3.0.6 / pyarrow 25.0.1

| input type | before | after |
|---|---|---|
| `string` | `[1, None, 0]` | `[1, None, 0]` |
| `large_string` | **ArrowInvalid** | `[1, None, 0]` |
| `string_view` | **ArrowInvalid** | `[1, None, 0]` |
| `from_pandas` (pandas 3) | **ArrowInvalid** | `[0, 1, 0]` |

### Tests

The existing `test_classlabel_cast_storage` now also exercises `large_string` and
`string_view`, with a null. **Fails on `main`** with the `ArrowInvalid` above; passes here.
`tests/features/test_features.py` — 203 passed. `ruff check` / `ruff format --check` pass.

### Note

`Json.cast_storage` has the same `isinstance(storage, pa.StringArray)` check and would
miss `large_string` JSON columns the same way. I left it out to keep this to the reported
bug; happy to follow up separately if you'd like.

If the reporter's PR lands first I'll close this one.

### AI assistance

This change was produced with AI assistance. I reviewed every line, reproduced the bug on
pandas 3, ran the tests, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on pandas 3.0.6 | `large_string` → `ArrowInvalid` |
| Extended test fails on `main` | yes |
| Extended test passes with fix | yes; full `test_features.py` 203 passed |
| `ruff check` / `ruff format` | pass |

Diff is 16 insertions, 1 deletion across 2 files.
