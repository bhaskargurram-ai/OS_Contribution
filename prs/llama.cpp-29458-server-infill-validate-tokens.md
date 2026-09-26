# llama.cpp #29458 — `/infill` does not validate prompt token ids, it accepts out-of-range ids that `/completion` rejects

**Status:** branch pushed (commit `9195b08`), PR not yet opened
**Branch:** `bhaskargurram-ai/llama.cpp` → `fix/server-infill-validate-tokens`
**Open the PR:** https://github.com/ggml-org/llama.cpp/compare/master...bhaskargurram-ai:llama.cpp:fix/server-infill-validate-tokens?expand=1

Title:

```
server : return the /infill validation errors to the client
```

Body (paste as-is):

---

## Overview

Fixes #29458.

`/completion` and `/v1/completions` reject a prompt that contains an out-of-range token id with `400 "Prompt contains invalid tokens"` (`server_tokens::validate()` in `launch_slot_with_task`). The report shows `/infill` answering `200` for the same `"prompt": [152936]`.

The cause is not a missing token check but a dropped error response. `post_infill` in `server-context.cpp` validates the request before building the FIM prompt:

```cpp
if (data.contains("prompt") && !data.at("prompt").is_string()) {
    res->error(format_error_response("\"prompt\" must be a string", ERROR_TYPE_INVALID_REQUEST));
}
if (!data.contains("input_prefix")) {
    res->error(format_error_response("\"input_prefix\" is required", ERROR_TYPE_INVALID_REQUEST));
}
if (!data.contains("input_suffix")) {
    res->error(format_error_response("\"input_suffix\" is required", ERROR_TYPE_INVALID_REQUEST));
}
```

None of the three branches returns, so the error written into `res` is discarded and the handler continues. A non-string `prompt` is then read with `json_value(data, "prompt", std::string())`, which logs a warning and falls back to `""`: the out-of-range id is never fed to the model, it is silently dropped and the request completes as if no `prompt` had been sent (`tokens_evaluated` is the same as for a request without `prompt`). A missing `input_prefix`/`input_suffix` goes on to `data.at(...)` and surfaces as a `500` json exception instead of the intended `400`.

Token ids passed inside `input_prefix`/`input_suffix` (which `tokenize_mixed` accepts) were already covered: they end up in the task's prompt and are rejected with the same `400 "Prompt contains invalid tokens"` at slot launch.

### Change

- `tools/server/server-context.cpp`: `return res;` after each of the three error responses in `post_infill`, so the handler rejects the request with the `400` it already produced.

| Request | before | after |
|---|---|---|
| `/infill` with `"prompt": [999999]` (or any non-string prompt) | `200`, prompt silently ignored | `400 "\"prompt\" must be a string"` |
| `/infill` without `input_prefix` / `input_suffix` | `500 [json.exception.out_of_range.403] key 'input_prefix' not found` | `400 "\"input_prefix\" is required"` |
| `/infill` with `"input_prefix": ["...", 999999]` | `400 "Prompt contains invalid tokens"` | unchanged |
| `/completion` with `"prompt": [999999]` | `400 "Prompt contains invalid tokens"` | unchanged |

### Tests

- `tools/server/tests/unit/test_infill.py`
  - `test_infill_invalid_prompt_req`: token array, negative id, mixed string/token array, number and object `prompt` are all rejected with `400` (fail on `master` with `200`).
  - `test_infill_missing_input_req`: missing `input_prefix` / `input_suffix` returns `400` (fail on `master` with `500`).
  - `test_infill_invalid_tokens_in_input`: an id equal to `n_vocab` inside `input_prefix` / `input_suffix` returns `400 "Prompt contains invalid tokens"` (already passing, added so the path stays covered).
- `tools/server/tests/unit/test_completion.py::test_completion_invalid_tokens`: `/completion` with `-1` / `999999` in the prompt returns `400 "Prompt contains invalid tokens"` (already passing, documents the behaviour `/infill` is aligned with).

Commands run (CPU build, `cmake -B build -DGGML_NATIVE=OFF && cmake --build build --target llama-server`):

```
cd tools/server/tests
python3 -m pytest -n 2 unit/test_infill.py unit/test_completion.py -k "invalid_prompt_req or missing_input_req or invalid_tokens"
# master: 8 failed, 4 passed; this branch: 12 passed
python3 -m pytest -n 2 unit/test_infill.py unit/test_completion.py -k "infill or invalid_tokens"
# this branch: 18 passed, 1 skipped (slow), 1 failed: test_infill_with_input_extra, which asserts
# model-specific output text and was run against a random-weight stand-in model (see below)
```

## Additional information

The `"prompt" must be a string` check predates this change; this PR only makes it effective. Accepting token arrays in the infill `prompt` (like `/completion` does) would be a separate feature and is not attempted here.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES — see below

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Worktree of the fork at `origin/master` (`2145525`), branch `fix/server-infill-validate-tokens`, commit `9195b08` authored by Bhaskar Gurram; no AI trailers in the commit.
- `huggingface.co` is blocked by the sandbox egress policy, so the CI models (`ggml-org/test-model-stories260K[-infill]`) could not be downloaded. A random-weight llama GGUF (2 layers, n_embd 64, tokenizer from `models/ggml-vocab-llama-spm.gguf` plus three appended `<PRE>/<SUF>/<MID>` control tokens registered as `tokenizer.ggml.fim_{pre,suf,mid}_token_id`, n_vocab 32003) was generated with gguf-py and used for reproduction and tests. All new assertions are status codes / error messages, independent of the weights.
- To run the suite, `ServerPreset.tinyllama2()` / `tinyllama_infill()` were temporarily pointed at that file and `ServerPreset.load_all()` short-circuited; those `utils.py` edits were reverted before committing (the commit touches only the 3 listed files).
- Manual reproduction (script posting to `/completion` and `/infill` with `999999` / `-1` in `prompt`, `input_prefix`, `input_suffix`, and requests missing `input_prefix`/`input_suffix`): before the change `/infill` with a token-array `prompt` returned `200` with `tokens_evaluated: 9` (identical to the request without `prompt`, i.e. the prompt was dropped), missing inputs returned `500`; after the change all return `400` with the messages in the table above. `input_prefix`/`input_suffix` arrays returned `400 "Prompt contains invalid tokens"` both before and after.
- New tests on the unfixed binary (C++ change stashed, rebuilt): `8 failed, 4 passed`; with the fix: `12 passed`.
- `clang-format-diff` on the C++ diff proposes no changes. flake8 on the two test files reports only the pre-existing patterns of these files (`global server`, star imports); nothing new on the added lines. The repo's `.flake8` excludes `tools/`.
- Things a reviewer may ask about:
  - Why reject rather than accept a token-array `prompt`: the handler already declares `prompt` must be a string and the README documents it as text "added after the FIM_MID token"; accepting arrays would also need handling of multi-prompt arrays (only `tokenized_prompts[0]` is used). Kept minimal.
  - The build dir was deleted after the run.

## Caveat

`AGENTS.md` / `CONTRIBUTING.md` of this repo require an AI-usage disclosure and restrict AI-generated content, including PR descriptions. Before opening the PR, rewrite the body above in your own words (keep the facts and the "AI usage disclosure: YES" line) and make sure you can personally defend every changed line.
