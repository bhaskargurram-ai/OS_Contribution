# mlx-lm #1906 — MiniCPM3 batch generation ignores the left-padding mask

**Status:** branch pushed (commit `06f0704`), PR not yet opened
**Branch:** `bhaskargurram-ai/mlx-lm` → `fix/minicpm3-left-padding-mask`
**Open the PR:** https://github.com/ml-explore/mlx-lm/compare/main...bhaskargurram-ai:mlx-lm:fix/minicpm3-left-padding-mask?expand=1

Title:

```
Honour the left-padding mask in MiniCPM3 and Phixtral batch generation
```

Body (paste as-is):

---

Fixes #1906.

`MiniCPM3Model.__call__` built its attention mask with
`create_attention_mask(h, cache)`, passing the whole per-layer cache list
instead of one cache object. `create_attention_mask` only delegates to the
cache when the object it receives has a `make_mask` method; a Python list does
not, so the call fell through to the plain `"causal"` string mask. The
`BatchKVCache` left padding therefore never reached the attention, and a
prompt run as the shorter, left-padded member of a batch attended to its
padding tokens. This changes the logits at the last prompt position and,
because the padded keys stay in the cache, at every decode step after it.
This is the mechanism mira687 identified in the issue thread.

`phixtral.py` had the identical call (`create_attention_mask(x, cache)`) and
the identical symptom, so it is fixed in the same way here.

### Change

- `mlx_lm/models/minicpm3.py`: fill `cache` with `[None] * len(self.layers)`
  before building the mask, then call `create_attention_mask(h, cache[0])`,
  matching `llama.py` / `qwen3.py`.
- `mlx_lm/models/phixtral.py`: same change (`create_attention_mask(x, cache[0])`
  after filling the cache list from `len(self.transformer.h)`).

No behaviour change for single-sequence generation: `cache[0]` is a `KVCache`
whose `make_mask` returns the same causal mask as before.

Weight-free check (random-init 2-layer model, prompt A alone vs A left-padded
in a batch with a longer prompt B, `max |logit diff|` at the last position):

| model    | step    | main      | this PR |
|----------|---------|-----------|---------|
| minicpm3 | prefill | 1.53e+00  | 0.0     |
| minicpm3 | decode  | 1.46e+00  | 0.0     |
| phixtral | prefill | 1.50e+00  | 0.0     |
| phixtral | decode  | 1.76e+00  | 0.0     |

### Tests

`tests/test_models.py`:

- new `left_padding_test_runner(model)` helper: runs a prompt alone with
  `make_prompt_cache`, then the same prompt left-padded inside a
  `BatchKVCache` batch, and asserts the last-position logits match for the
  prefill and for one decode step.
- new `test_minicpm3` (there was no MiniCPM3 model test) and `test_phixtral`,
  each running `model_test_runner` plus the new helper.

Both new tests fail on `main` (`AssertionError` on the prefill comparison) and
pass on this branch.

Commands run:

- `python -m pytest tests/test_models.py -k "minicpm or phixtral"` → 3 passed
- `python -m pytest tests/test_models.py` → 103 passed, 3 failed, 1 skipped
  (the 3 failures, `test_bitnet` and `test_gated_delta*`, are identical on
  `main`; they need a Metal kernel / CPU-unsupported op — I ran on the Linux
  CPU build of MLX 0.32.2)
- `black --check`, `isort --profile=black --check-only`, `ruff check` on the
  three changed files → clean

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran
the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` with a weight-free script (random-init MiniCPM3,
  `hidden_size=64`, 2 layers): prompt `[5,6,7]` alone via `make_prompt_cache`
  vs the same prompt left-padded by 3 inside a `BatchKVCache` batch with
  `[11..16]`. `max|logit diff|` 1.53 (prefill) / 1.46 (decode) on main; 0.0 on
  the branch. Same script against `phixtral`: 1.50 / 1.76 on main, 0.0 fixed.
  Scripts: `scratchpad/mlx-lm-1906/repro.py`, `repro_phixtral.py`.
- Grepped every `create_attention_mask(` / `create_ssm_mask(` call in
  `mlx_lm/models/*.py`; `minicpm3.py` and `phixtral.py` were the only two
  passing the raw cache list. All others pass `cache[i]` / a single cache.
- Confirmed the new tests fail on main by stashing only the two model files and
  re-running (`2 failed`), then restoring.
- Full `tests/test_models.py`: 103 passed / 3 failed / 1 skipped on branch vs
  101 / 3 / 1 on main (same 3 pre-existing CPU-backend failures).
- `left_padding_test_runner` casts the model to float32 first because
  `model_test_runner` leaves it in float16 and the CPU `GatherMM` used by
  Phixtral's MoE only supports float32; a reviewer on Metal would not see that
  error but the cast is harmless and keeps the tolerance meaningful.
- Formatting: black (`--target-version py311`, the installed black is newer
  than the pinned 26.5.1 mirror but produced no diff), isort, ruff all clean.
  Could not run `pre-commit` itself (pre-commit hook mirrors are not reachable
  through the proxy) so black/isort/ruff were run directly.
- Commit author: Bhaskar Gurram <gurrambhaskar.ai@gmail.com>; no AI trailers.

## Caveat

`CONTRIBUTING.md` (AI Usage Policy) says AI-generated code is allowed with
explicit disclosure, but that it is "strictly prohibited to use AI to write
your posts for you (... pull request descriptions ...)", and the PR template
has a checkbox "I understand it is strictly prohibited to use AI to write PR
description" plus an "AI usage disclosure:" line. The body above was drafted
with AI assistance: before opening the PR, rewrite the description in your own
words (the facts and table above are accurate and can be reused as notes), tick
the template checkbox, and fill the "AI usage disclosure" line honestly (e.g.
"code change and tests drafted with an AI coding assistant; reviewed and run by
me").
