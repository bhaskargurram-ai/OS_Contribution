# chonkie #631 — String tokenizer resolution ignores HF_HUB_OFFLINE and blocks on the network

**Status:** branch pushed (commit `17023e5`), PR not yet opened
**Branch:** `bhaskargurram-ai/chonkie` → `fix/tokenizer-honours-hf-offline`
**Open the PR:** https://github.com/feyninc/chonkie/compare/main...bhaskargurram-ai:chonkie:fix/tokenizer-honours-hf-offline?expand=1

Title:

```
Honour HF offline mode and local cache when resolving string tokenizers
```

Body (paste as-is):

---

Fixes #631.

Building a chunker or refinery with a string tokenizer (e.g. `TokenChunker(tokenizer="gpt2")`, `OverlapRefinery(tokenizer="gpt2")`) resolves the string in `chonkie/tokenizer.py::_create_auto_tokenizer_from_string`, which calls `tokie.Tokenizer.from_pretrained(...)` (first with the mapped id, e.g. `openai-community/gpt2`, then with the raw string).

`tokie.Tokenizer.from_pretrained` (tokie 0.1.2–0.1.4, built on the `hf-hub` 0.4.3 Rust crate) only has a local fast path for the *default* cache directory (`~/.cache/huggingface/hub`): it uses `hf_hub::Cache::default()` / `ApiBuilder::new()`, not the `from_env()` variants, so `HF_HOME`, `HF_HUB_CACHE` and `HF_ENDPOINT` are ignored, and `hf-hub` has no notion of `HF_HUB_OFFLINE` / `TRANSFORMERS_OFFLINE` at all. Its `ureq` agent is built without any request timeout. So whenever the tokenizer is cached anywhere other than the default location (the usual containerised setup: `HF_HOME=/models/hf`), or is not cached at all, chonkie makes a blocking hub request to `huggingface.co` — with the offline switches set or not — and if the hub is slow or unreachable, construction blocks for as long as the TCP connection takes to die (a black-holed connection never returns).

### Change

`src/chonkie/tokenizer.py` resolves the HuggingFace cache itself before asking tokie to download anything:

- `_find_cached_tokenizer_file(repo_id)` looks for a cached `tokenizer.json` under `HF_HUB_CACHE`, `$HF_HOME/hub` and `~/.cache/huggingface/hub` (huggingface_hub's own resolution order), following `refs/main` and falling back to any snapshot. A hit is loaded with `tokie.Tokenizer.from_json`, with zero network I/O.
- On a cache miss, `_hf_offline()` checks `HF_HUB_OFFLINE` / `TRANSFORMERS_OFFLINE` (same truthy values as huggingface_hub) and raises immediately with a clear message; the existing `InvalidTokenizerError` wraps it as before.
- Only when the cache misses and offline mode is not set does it fall through to `tokie.Tokenizer.from_pretrained`, exactly as today.

The change is confined to the string-resolution path; passing a tokenizer instance is untouched.

| Scenario (hub black-holed: TCP connect accepted, never answered) | before | after |
|---|---|---|
| `tokenizer.json` cached under `HF_HOME`, no offline flag | blocked, killed after 180 s | loads in 0.36 s |
| `tokenizer.json` cached under `HF_HOME`, `HF_HUB_OFFLINE=1` | blocked, killed after 180 s | loads in 0.34 s |
| not cached, `HF_HUB_OFFLINE=1` | blocked, killed after 180 s | `InvalidTokenizerError` in 0.36 s: `... was not found in the local HuggingFace cache and HF_HUB_OFFLINE / TRANSFORMERS_OFFLINE is set, so the hub will not be contacted.` |

One limitation remains outside chonkie: an *online* cache miss against an unreachable hub still blocks inside tokie, because its hf-hub client has no timeout and the Python binding exposes no way to set one. That needs a fix in tokie; this PR removes the hang for the cached and offline cases, which is what #631 reports.

### Tests

Added to `tests/test_tokenizer.py` (the `cached_tokenizer_repo` fixture seeds a hub-style cache in `tmp_path` with a tokenizer.json built locally by `tokenizers`, parametrised over `HF_HUB_CACHE` and `HF_HOME`; `hub_download_calls` monkeypatches `tokie.Tokenizer.from_pretrained` so any download attempt is recorded and fails — no network is needed):

- `test_string_tokenizer_loads_from_local_cache_without_network` (×6: two cache env vars × {no flag, `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`}) — cached tokenizer is used, `from_pretrained` is never called.
- `test_string_tokenizer_offline_cache_miss_fails_fast` (×2) — raises `InvalidTokenizerError` mentioning the offline switches, `from_pretrained` never called.
- `test_string_tokenizer_downloads_on_cache_miss_when_online` — guards that the online path still calls `from_pretrained` and surfaces its error.

On `main`, the first 8 fail (the cached tokenizer triggers a download attempt / offline mode is ignored); all 9 pass on this branch.

Commands run:

- `pytest tests/test_tokenizer.py -k "local_cache or cache_miss"` → 9 passed (branch); 8 failed, 1 passed (`main`)
- `pytest tests/test_tokenizer.py tests/refinery` → 132 passed, 9 failed, 18 skipped on the branch vs 123 passed, 9 failed, 18 skipped on `main`. The 9 failures are identical on both and are the tests that download `gpt2`/`p50k_base` from the hub, which is blocked in my sandbox (`Proxy failed to connect` / `403`).
- `ruff check .` → All checks passed; `ruff format --check .` → clean.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Located the resolution chain: `AutoTokenizer.__new__` → `_create_auto_tokenizer_from_string` → `tokie.Tokenizer.from_pretrained` (mapped id, then raw id). `OverlapRefinery` and all chunkers go through `AutoTokenizer`, so they are covered by the one change. tiktoken/tokenizers/transformers are only used for *instances* passed in, never for string resolution.
- Read tokie 0.1.2/0.1.3/0.1.4 `crates/tokie/src/hub.rs` (sdists from PyPI) and hf-hub 0.4.3 `src/lib.rs` / `src/api/sync.rs` (crates.io): confirmed `Cache::default()` + `ApiBuilder::new()` (no `HF_HOME`/`HF_ENDPOINT`, no offline support, no ureq timeout). `grep -a` of the installed tokie `.so` finds no `HF_*` string at all.
- huggingface.co is blocked by the sandbox proxy (CONNECT 403), so real `gpt2` could not be downloaded. Reproduction is therefore weight-free: a small BPE `tokenizer.json` built with `tokenizers` and placed in hub cache layout (`models--openai-community--gpt2/refs/main` + `snapshots/<sha>/tokenizer.json`) under a temporary `HF_HOME`, plus a local "black-hole" proxy (accepts TCP, never replies) selected via `HTTPS_PROXY` (tokie/ureq honours proxy env vars; `HF_ENDPOINT` is ignored by tokie so it cannot be used to redirect it).
- Before (main): `AutoTokenizer("gpt2")` with the cache warm under `HF_HOME` blocked until killed by `timeout 180`, with and without `HF_HUB_OFFLINE=1`; uncached + `HF_HUB_OFFLINE=1` likewise blocked. (An earlier unbounded run of the same scenario was still blocked after 224 s when I killed it.)
- After (branch): same three scenarios complete in 0.34–0.36 s (two successful loads, one immediate `InvalidTokenizerError`).
- Also checked that with the cache in the *default* location tokie's own fast path already avoids the network in 0.1.4, so the change does not regress that case (it now loads via `from_json` from the same file).
- `ruff check` / `ruff format --check` on the repo: clean. New tests pass under both `HF_HUB_CACHE` and `HF_HOME` layouts.
- Commit author: Bhaskar Gurram <gurrambhaskar.ai@gmail.com>; no AI trailers.

## Caveat

`CONTRIBUTING.md` on `main` currently says: "PRs are frozen. We're building Chonkie v2. v1.7 is the last 1.x release; fixes go into 2.0. New pull requests on `main` will be closed automatically until v2 is stable." The fork only has `main`; there is no public v2 branch to target yet. The PR may be auto-closed — consider linking the branch in a comment on #631 instead, or waiting for the v2 branch. (No AI-policy restriction was found in CONTRIBUTING.md; the AI-assistance section is kept.)
