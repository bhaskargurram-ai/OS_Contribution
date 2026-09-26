# litdata #888 — Checkpoint uploads truncate output prefix for stable checkpoint filenames

**Status:** fix committed locally (commit `2988165` on `/home/user/litdata`, branch `fix/checkpoint-upload-keeps-prefix`), PUSH BLOCKED — the fork `bhaskargurram-ai/litdata` does not exist / is not in this session's authorized repo set (git push 403, `add_repo` "not found or no access", `list_repos` returns nothing for litdata). PR not yet opened.
**Branch:** `bhaskargurram-ai/litdata` → `fix/checkpoint-upload-keeps-prefix` (to push after forking: `cd /home/user/litdata && git push -u origin fix/checkpoint-upload-keeps-prefix`)
**Open the PR:** https://github.com/Lightning-AI/litdata/compare/main...bhaskargurram-ai:litdata:fix/checkpoint-upload-keeps-prefix?expand=1

**Note:** the issue author already opened https://github.com/Lightning-AI/litdata/pull/889 ("fix(processing): preserve checkpoint paths without UUIDs", open since Aug 18 2026, no reviews, only touches `remove_uuid_from_filename` + `tests/processing/test_utilities.py`). This branch takes the same approach (regex on the basename) and additionally covers `_upload_dest` / `_upload_fn` in `tests/processing/test_data_processor.py`. Decide whether to open a competing PR or comment on #889.

Title:

```
Keep output prefix when uploading stable checkpoint filenames
```

Body (paste as-is):

---

<details>
  <summary><b>Before submitting</b></summary>

- [x] Was this discussed/agreed via a Github issue? (no need for typos and docs improvements)
- [x] Did you read the [contributor guideline](https://github.com/Lightning-AI/lit-data/blob/main/CONTRIBUTING.md), Pull Request section?
- [x] Did you make sure to update the docs? (no docs change needed; docstring updated)
- [x] Did you write any new necessary tests?

</details>

## What does this PR do?

Fixes #888.

`BinaryWriter.save_checkpoint()` now writes stable `checkpoint-<rank>.json` files, but the upload path still went through `remove_uuid_from_filename()`, which assumed every file under `.checkpoints` ends in `-<32 hex uuid>.json` and unconditionally chopped the last 38 characters off the *whole* destination path. For a 17-character stable name that removes 21 characters of the output prefix, so checkpoints were written outside the requested directory (and, with bucket versioning, re-written there on every checkpoint):

| Local checkpoint | Output dir | Before | After |
| --- | --- | --- | --- |
| `/cache/.checkpoints/checkpoint-0.json` | `s3://bucket/output/data/train` | `s3://bucket/output/dat.json` | `s3://bucket/output/data/train/.checkpoints/checkpoint-0.json` |
| `/cache/.checkpoints/checkpoint-0.json` | `/output/data/train` (local) | `/output/dat.json` | `/output/data/train/.checkpoints/checkpoint-0.json` |
| `.checkpoints/checkpoint-0-9fe2c4e9…716c.json` | any | `…/checkpoint-0.json` | `…/checkpoint-0.json` (unchanged behaviour) |

### Change

`remove_uuid_from_filename()` in `src/litdata/processing/utilities.py` now only inspects the basename and only strips the suffix when it matches `checkpoint-<rank>-<32 hex chars>.json`; the directory part (local path or remote URL) is copied verbatim. Stable checkpoint names, `config.json`, near-miss suffixes and paths outside `.checkpoints` are returned unchanged. Legacy uuid names are still normalized, so the existing `test_remove_uuid_from_filename` keeps passing. `_upload_dest()` is untouched and picks the fix up automatically.

### Tests

- `tests/processing/test_utilities.py`: `test_remove_uuid_from_filename_keeps_paths_without_uuid` (7 parametrized cases) and `test_remove_uuid_from_filename_keeps_prefix_for_legacy_names`.
- `tests/processing/test_data_processor.py`: `test_upload_dest_keeps_prefix_for_stable_checkpoint_names` (local + s3, the exact reproduction from the issue), `test_upload_dest_normalizes_legacy_checkpoint_names`, and `test_upload_fn_checkpoint_keeps_output_prefix` (runs `_upload_fn` with a mocked fs provider and asserts the remote key).

On `main` (483b57f) the new tests fail: `9 failed, 4 passed` for `pytest tests/processing/test_utilities.py tests/processing/test_data_processor.py -k "uuid or upload_dest or upload_fn_checkpoint"`. With this change:

- `pytest tests/processing/test_utilities.py tests/processing/test_data_processor.py -k "uuid or upload_dest or upload_fn or checkpoint"` → 21 passed
- `pytest tests/processing/test_utilities.py tests/processing/test_data_processor.py` → 106 passed, 7 skipped, 1 failed (`test_adaptive_download_concurrency_env_and_jobs`, which also fails on `main` on this 4-core machine; unrelated)
- `ruff check` / `ruff format --check` on the three changed files → clean; `codespell` → clean

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced with the issue's snippet on `main` (483b57f): `_upload_dest(Dir(path="/output/data/train", url=None), "/cache/.checkpoints/checkpoint-0.json", None)` → `/output/dat.json`; s3 variant → `s3://bucket/output/dat.json`; also `.../.checkpoints/config.json` → `s3://bucket/outp.json`.
- After the fix the same script prints the full `<output>/.checkpoints/checkpoint-0.json` / `config.json` paths and the legacy uuid name still normalizes to `checkpoint-0.json`.
- New tests: 9 fail on `main`, all pass on the branch (stash-tested).
- Full `tests/processing/test_utilities.py` + `tests/processing/test_data_processor.py`: 106 passed, 7 skipped, 1 pre-existing failure (`test_adaptive_download_concurrency_env_and_jobs`, `assert 4 == 5`, depends on `os.cpu_count()`; fails identically with the fix stashed).
- Lint: `ruff check` and `ruff format --check` (ruff 0.16.9, repo config) pass on changed files; codespell clean. Other pre-commit hooks (mdformat, prettier, pyproject-fmt) do not apply to the changed files.
- No CHANGELOG file in the repo. PR template sections mirrored above.
- Env: venv with system torch 2.14 (CUDA wheels removed to stay under the disk budget), `pip install -e .`; tests run with `-p no:randomly`.

## Caveat

- Push to `bhaskargurram-ai/litdata` failed (403 from the git proxy; `add_repo` reports the repo is not found / not accessible; `list_repos` has no litdata entry). The fork most likely has not been created yet. The commit is ready on the local clone; once the fork exists (and is added to the session), run `cd /home/user/litdata && git push -u origin fix/checkpoint-upload-keeps-prefix`.
- Upstream PR #889 by the issue author already proposes an equivalent fix (see Note above).
