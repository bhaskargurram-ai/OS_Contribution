# llama.cpp #29456 — llama-server does not cap logprobs / top_logprobs (n_probs)

**Status:** branch pushed (commit `44249e0`), PR not yet opened
**Branch:** `bhaskargurram-ai/llama.cpp` → `fix/server-cap-n-probs`
**Open the PR:** https://github.com/ggml-org/llama.cpp/compare/master...bhaskargurram-ai:llama.cpp:fix/server-cap-n-probs?expand=1

Title:

```
server : cap the number of token probabilities per request
```

Body (paste as-is):

---

## Overview

Fixes #29456.

`n_probs` (and the `logprobs` alias of `/completion` / `/v1/completions`, and `top_logprobs` of `/v1/chat/completions`, which `oaicompat_chat_params_parse` maps to `n_probs`) is parsed by the `n_probs` field of the completion schema (`server-schema.cpp`) without any limit. `populate_token_probs` then sorts the whole vocabulary and copies `min(n_probs, n_vocab)` entries per generated token, and `server-task.cpp` serializes them all. One request of a few hundred bytes can therefore make the server produce `n_vocab` entries per token: on a 32k-vocabulary model, `n_probs: 100000` with 8 generated tokens returns a 22 MB response (the report measures 115 MB for a 150k vocabulary, growing linearly with `max_tokens`). The OpenAI API rejects `top_logprobs > 20`, and vLLM has `--max-logprobs` (default 20).

### Change

- `common/common.h`, `common/arg.cpp`: new server option `--n-probs-max N` (env `LLAMA_ARG_N_PROBS_MAX`), default `20`, `-1` = no limit.
- `tools/server/server-schema.cpp`: the `n_probs` field gets `set_hard_limits(0, n_probs_max)` (or `INT32_MAX` for `-1`), so any request whose value exceeds the cap is rejected with `400` — this covers `n_probs`, the `logprobs` alias and the OAI `top_logprobs` mapping in one place. In the schema post-processing, `n_probs` above the vocabulary size is rejected with `400` too (it used to be silently clamped), which only matters when the cap is disabled.
- `tools/server/server-common.cpp`, `server-common.h`, `server-context.cpp`: `server_chat_params` carries `n_probs_max`, so the chat endpoint reports the error in terms of `top_logprobs` (`top_logprobs must not exceed 20 (see --n-probs-max), but got 21`) and derives its `top_logprobs` default (previously a fixed `20`) from the cap, so `logprobs: true` without `top_logprobs` keeps working when the cap is lowered.
- `tools/server/README.md`: document the cap under `n_probs`, under `/v1/chat/completions` (`logprobs` / `top_logprobs`) and add the `--n-probs-max` row to the argument table (same format as `llama-gen-docs` output).
- `tools/server/tests/utils.py`: `ServerProcess.n_probs_max` to start the test server with the option.

| Request (8 generated tokens, 32k vocabulary) | before | after |
|---|---|---|
| `/completion` `n_probs: 20` | `200`, 16 KB, 20 probs/token | unchanged |
| `/completion` `n_probs: 21` | `200`, 21 probs/token | `400 Field 'n_probs': Value must be between 0 <= value <= 20, but got 21` |
| `/completion` `n_probs: 100000` | `200`, 22 MB, 32003 probs/token | `400` |
| `/v1/chat/completions` `logprobs: true, top_logprobs: 100000` | `200`, 22 MB | `400 top_logprobs must not exceed 20 (see --n-probs-max), but got 100000` |
| `--n-probs-max 5`, `n_probs: 5` / `6` | `200` / `200` | `200` / `400` |
| `--n-probs-max -1`, `n_probs: 100` / `n_vocab + 1` | `200` / `200` (clamped to `n_vocab`) | `200` / `400 ... must not exceed the vocabulary size` |

Choice of default: `20` is applied to every endpoint, including the native `/completion`, so that one knob covers all routes that reach `n_probs`. This is a behaviour change for native clients that asked for more than 20 probabilities per token; they can restore the old behaviour with `--n-probs-max -1` (or a higher value). The alternative of capping only the OAI endpoints would leave the amplification reachable through `/completion`, which needs no special client either. If maintainers prefer a higher default for the native endpoint, only the default in `common.h` needs to change.

### Tests

- `tools/server/tests/unit/test_completion.py`
  - `test_n_probs_max_default[n_probs|logprobs]`: `20` is accepted (20 entries per token), `21` is rejected with `400` naming the field.
  - `test_n_probs_max_custom`: `--n-probs-max 5` accepts `5` / rejects `6`; `--n-probs-max 0` rejects `1`; `--n-probs-max -1` accepts `100`.
  - `test_n_probs_exceeds_vocab`: with the cap disabled, `n_vocab + 1` is rejected with `400` mentioning the vocabulary.
- `tools/server/tests/unit/test_chat_completion.py::test_logprobs_top_logprobs_max`: `top_logprobs: 20` returns 20 entries per token, `21` returns `400` mentioning `top_logprobs`.

Against the unmodified server binary: `8 failed, 1 passed` (the `top_logprobs: 20` case passes either way); with this change: `9 passed`.

Commands run (CPU build, `cmake -B build -DGGML_NATIVE=OFF && cmake --build build --target llama-server`):

```
cd tools/server/tests
python3 -m pytest -n 2 unit/test_completion.py unit/test_chat_completion.py -k "n_probs_max or exceeds_vocab or top_logprobs_max"
# unmodified binary: 8 failed, 1 passed; this branch: 9 passed
python3 -m pytest -n 2 unit/test_completion.py unit/test_chat_completion.py -m "not slow" \
  -k "usage or multiple_choices or timings_per_token or token_count or verbose_debug or stream_vs_non_stream or n_probs or invalid_chat_completion_req or logprobs or invalid_grammar"
# 29 passed
```

## Additional information

The existing `n_probs` tests (`n_probs: 10`) and the OAI `test_logprobs` (`top_logprobs: 10`) are below the default cap and are unchanged.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES — see below

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Worktree of the fork at `origin/master` (`2145525`), branch `fix/server-cap-n-probs`, commit `44249e0` authored by Bhaskar Gurram; no AI trailers in the commit. 10 files changed.
- `huggingface.co` is blocked by the sandbox egress policy, so the CI model (`ggml-org/test-model-stories260K`) could not be downloaded. Reproduction and tests used a random-weight llama GGUF (2 layers, n_embd 64, tokenizer from `models/ggml-vocab-llama-spm.gguf`, n_vocab 32003) generated with gguf-py. All new assertions are status codes, error messages and array lengths, independent of the weights. `test_n_probs_max_custom[-1-100-200]` needs `n_vocab >= 100`, which holds for the CI model (512) too.
- `ServerPreset.tinyllama2()` was temporarily pointed at that file and `ServerPreset.load_all()` short-circuited; those `utils.py` edits were reverted before committing (the committed `utils.py` diff is only the `n_probs_max` field and the `--n-probs-max` argument).
- Manual reproduction script (`/completion` with `n_probs` 5/20/21/1000/100000 and `/v1/chat/completions` with `top_logprobs` 5/20/21/100000, 8 tokens): before, all `200`, with 100000 giving 22.4 MB responses (32003 entries per token); after, values above 20 return `400` with the messages in the table.
- New tests against the unmodified binary (via `LLAMA_SERVER_BIN_PATH`): `8 failed, 1 passed` (the custom-cap tests fail there at startup because the option does not exist, the default-cap and chat tests fail with `200 != 400`); with the change: `9 passed`. Regression subset of 29 model-agnostic tests in `test_completion.py` / `test_chat_completion.py`: `29 passed`.
- `--help` output shows the new option with its env var. `clang-format-diff` only proposes reflowing the new `add_opt` block into a style the neighbouring options do not use, so the surrounding style was kept; no other C++ change is touched by it. flake8 on the test files reports only pre-existing findings on untouched lines.
- Things a reviewer may ask about:
  - Whether the cap should apply to the native `/completion` endpoint (see "Choice of default" above). Changing only the default in `common.h` is enough if a higher native default is preferred.
  - `n_probs` values below `0` are now rejected (`set_hard_limits(0, ...)`), previously they were accepted and behaved like `0`.
  - The README argument table is normally regenerated with `llama-gen-docs`; the row was added by hand in the same format because the examples were not built in this environment. Re-running `llama-gen-docs` should produce the identical row.
  - The build dir was deleted after the run.

## Caveat

`AGENTS.md` / `CONTRIBUTING.md` of this repo require an AI-usage disclosure and restrict AI-generated content, including PR descriptions. Before opening the PR, rewrite the body above in your own words (keep the facts and the "AI usage disclosure: YES" line) and make sure you can personally defend every changed line, in particular the choice of the default cap.
