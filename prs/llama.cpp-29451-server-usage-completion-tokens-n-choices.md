# llama.cpp #29451 — `usage.completion_tokens` counts only one choice when `n > 1`

**Status:** branch pushed (commit `395d48b`), PR not yet opened
**Branch:** `bhaskargurram-ai/llama.cpp` → `fix/server-usage-completion-tokens-n-choices`
**Open the PR:** https://github.com/ggml-org/llama.cpp/compare/master...bhaskargurram-ai:llama.cpp:fix/server-usage-completion-tokens-n-choices?expand=1

Title:

```
server : report usage across all choices when n > 1
```

Body (paste as-is):

---

## Overview

Fixes #29451.

With `n > 1`, `llama-server` runs one task per choice (a parent task plus `n - 1` child tasks that share the prompt). In `handle_completions_impl` the non-streaming OAI-compatible response is built by moving every result's `choices[0]` into the first result's `choices` array, but the first result's `usage` object is left untouched. `usage.completion_tokens` (and `total_tokens`) therefore reports the `n_decoded` of the first choice only, so with `n=3` and `max_tokens=16` the response says `completion_tokens: 16` instead of `48`.

In streaming mode the same happens per choice: each choice's final result emits its own usage (a trailing `choices: []` chunk for `/v1/chat/completions` with `stream_options.include_usage`, the final chunk itself for `/v1/completions`), each with a single choice's count, so a client gets `n` usage objects instead of one. `/v1/completions` with an array of prompts had the related problem of only reporting the prompt tokens of the first prompt.

### Change

- `server-task.h/.cpp`: add `server_task_result_usage`, which sums `n_decoded` over every final result and counts `n_prompt_tokens` / `cached_tokens` once per input: the `n_cmpl` results generated from the same prompt have consecutive indices starting at the parent task (`server_response_reader::post_tasks`), so the prompt is counted for `index % n_cmpl == 0` only. The existing `usage_json_oaicompat()` and the new aggregator share one formatting helper.
- `server-context.cpp`, non-streaming: after merging the choices, replace `usage` with the aggregated one.
- `server-context.cpp`, streaming: when the request has more than one task and the format is OAI chat/completions, drop the per-choice usage from every final result but the last one (moving its `timings`, if any, to the previous chunk) and put the aggregated usage on the last one. Requests with a single task (the common `n=1` case) take none of these paths and are unchanged. Anthropic/Responses formats are not touched.

| Request (`max_tokens=16`, all choices `finish_reason=length`) | before | after |
|---|---|---|
| `/v1/chat/completions`, `n=3`, non-stream: `completion_tokens` | 16 | 48 |
| `/v1/chat/completions`, `n=3`, stream + `include_usage`: usage chunks | 3 (each `completion_tokens: 16`) | 1 (`completion_tokens: 48`, last chunk, `choices: []`) |
| `/v1/completions`, `n=3`, non-stream: `completion_tokens` | 16 | 48 |
| `/v1/completions`, `n=3`, stream: chunks carrying `usage` | 3 (each 16) | 1 (48, last chunk) |
| `/v1/completions`, 2 prompts × `n=2`, `max_tokens=4`: `prompt_tokens` / `completion_tokens` | 5 / 4 | 14 (=5+9) / 16 |

### Tests

- `tools/server/tests/unit/test_chat_completion.py::test_chat_completions_multiple_choices_usage`: `n=2`, non-stream and stream + `include_usage`; asserts `completion_tokens == n * max_tokens`, `prompt_tokens` equal to the single-choice request, `total_tokens` consistent, and exactly one usage chunk (the last one) in the stream.
- `tools/server/tests/unit/test_completion.py::test_completion_multiple_choices_usage`: same for `/v1/completions`, plus the two-prompts × `n=2` case where `prompt_tokens` must be the sum of both prompts.

Both fail on `master` (`assert 8 == (2 * 8)`) and pass with this change.

Commands run (CPU build, `cmake -B build -DGGML_NATIVE=OFF && cmake --build build --target llama-server`):

```
cd tools/server/tests
python3 -m pytest -n 2 unit/test_chat_completion.py unit/test_completion.py -k multiple_choices_usage   # master: 2 failed; this branch: 2 passed
python3 -m pytest -n 2 unit/test_chat_completion.py unit/test_completion.py -m "not slow" \
  -k "usage or multiple_choices or timings_per_token or token_count or verbose_debug or stream_vs_non_stream or n_probs or invalid_chat_completion_req"
# 19 passed
```

`clang-format` was checked on the touched lines; the only differences it proposes are the file's pre-existing style (aligned declarations/parameter columns), which the surrounding code does not follow, so the existing style was kept. `flake8` with the repo's `.flake8` settings reports nothing new on the added test lines.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES — see below

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Clone of the fork at `master` (`2145525`), branch `fix/server-usage-completion-tokens-n-choices`, commit `395d48b` authored by Bhaskar Gurram; no AI trailers in commit or notes.
- `huggingface.co` is blocked by the sandbox egress policy (proxy 403), so the CI test model (`ggml-org/test-model-stories260K`) could not be fetched. Reproduction and tests were run against a locally generated random-weight llama GGUF (2 layers, n_embd 64, tokenizer copied from the repo's `models/ggml-vocab-llama-spm.gguf`, chatml template) — token accounting is exact regardless of weights, and every assertion in the new tests is model-agnostic (`finish_reason == "length"`, `n * max_tokens`, prompt tokens compared to a single-choice request).
- To run the suite locally, `ServerPreset.tinyllama2()` was temporarily pointed at that file and `ServerPreset.load_all()` short-circuited; those `utils.py` edits were reverted before committing (`git diff` of the commit touches only the 5 listed files).
- Manual reproduction script (`/v1/chat/completions` and `/v1/completions`, `n=3`, `max_tokens=16`, stream and non-stream, plus 2 prompts × `n=2`) produced the before/after numbers in the table above; per-choice `/tokenize` counts of the returned content were 17–18 tokens each (retokenization of decoded text is not exact), which is why the tests use `max_tokens` with `finish_reason == "length"` instead.
- New tests: fail on the unfixed library (rebuilt with the C++ change stashed): `2 failed`, `assert 8 == (2 * 8)`; pass with the fix: `2 passed`.
- Regression subset of 19 model-agnostic tests in `test_chat_completion.py` / `test_completion.py` (usage, multiple choices, timings-per-token stream usage, token count, verbose, stream vs non-stream, n_probs, invalid requests): `19 passed`. Tests asserting tinyllama-specific output text were not meaningful with the synthetic model and were not run; the CI runs them with the real model.
- Things a reviewer may ask about:
  - Prompt tokens are counted once per input via `index % n_cmpl == 0`; this relies on `post_tasks` assigning consecutive indices parent-then-children, which is also what `wait_for_all` relies on.
  - `cached_tokens` is taken from the parent task of each prompt (children typically report a higher cache hit since they reuse the parent's prompt); with a shared prompt, reporting it once matches `prompt_tokens` being reported once.
  - In streaming mode the aggregator lives in the `set_next` lambda captured by value with `mutable`; `server_res_spipe::set_next` stores that std::function once and invokes it in place, so the state persists across chunks.
  - For `/v1/completions` streaming, the intermediate finals lose their per-choice `usage` (OpenAI sends usage once per request); `timings` on those chunks is preserved.
- `build/` and temporary binaries were deleted after the run.
