# Fork list 2 — 20 new repositories

None of these repos appear in `fork-list.md`, `fifty-targets.md` or `company-oss-targets.md`.
Each row has one vetted target issue: open, unassigned, no linked PR, and the mechanism
described precisely enough to reproduce on CPU. Vetted 2026-09-26 against the live issue pages.

● = nobody has claimed or offered a fix; start immediately.
◐ = the reporter offered a PR or a maintainer decision is pending; post a one-line "I'll take
this" comment first and wait a day before pushing.

## Ready now (14 repos)

| # | Fork | Target issue | Language |
|---|---|---|---|
| 1 | [huggingface/datatrove](https://github.com/huggingface/datatrove/fork) | [#529](https://github.com/huggingface/datatrove/issues/529) C4BadWordsFilter: uppercase word-list entries can never match ● | Python |
| 2 | [milvus-io/pymilvus](https://github.com/milvus-io/pymilvus/fork) | [#3794](https://github.com/milvus-io/pymilvus/issues/3794) `import pymilvus` runs `dictConfig()` and closes every existing logging handler ● | Python |
| 3 | [cohere-ai/cohere-python](https://github.com/cohere-ai/cohere-python/fork) | [#796](https://github.com/cohere-ai/cohere-python/issues/796) batched embeddings drop embedding types absent from the first response ● | Python |
| 4 | [google/flax](https://github.com/google/flax/fork) | [#5577](https://github.com/google/flax/issues/5577) `nnx.WeightNorm.scales` is not an `nnx.Param`, so it never trains ● | Python |
| 5 | [jax-ml/jax](https://github.com/jax-ml/jax/fork) | [#40965](https://github.com/jax-ml/jax/issues/40965) `expon.logcdf` returns -inf for small x (`log1p(-sf)` cancellation) ● | Python |
| 6 | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime/fork) | [#32802](https://github.com/microsoft/onnxruntime/issues/32802) `quant_pre_process` loses optimizer output when shape-inference stages are skipped ● | Python |
| 7 | [microsoft/Olive](https://github.com/microsoft/Olive/fork) | [#2676](https://github.com/microsoft/Olive/issues/2676) `import olive` fails: telemetry exporter imports undeclared `requests` ● | Python |
| 8 | [Lightning-AI/litserve](https://github.com/Lightning-AI/litserve/fork) | [#667](https://github.com/Lightning-AI/litserve/issues/667) Swagger UI sends an empty body to `/predict`, causing a 500 ● | Python |
| 9 | [Lightning-AI/litdata](https://github.com/Lightning-AI/litdata/fork) | [#888](https://github.com/Lightning-AI/litdata/issues/888) checkpoint uploads truncate the output prefix for stable filenames ● | Python |
| 10 | [ml-explore/mlx-lm](https://github.com/ml-explore/mlx-lm/fork) | [#1906](https://github.com/ml-explore/mlx-lm/issues/1906) MiniCPM3 batch generation ignores the left-padding mask ● | Python |
| 11 | [feyninc/chonkie](https://github.com/feyninc/chonkie/fork) | [#631](https://github.com/feyninc/chonkie/issues/631) string tokenizer resolution ignores `HF_HUB_OFFLINE` and blocks on the network ● | Python |
| 12 | [ogx-ai/ogx](https://github.com/ogx-ai/ogx/fork) | [#6581](https://github.com/ogx-ai/ogx/issues/6581) `starter` extra has no lower bound on `sentence-transformers` ● | Python |
| 13 | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/fork) | [#29451](https://github.com/ggml-org/llama.cpp/issues/29451) `usage.completion_tokens` counts one choice, undercounts by `n` ● | C++ |
| 14 | [huggingface/text-embeddings-inference](https://github.com/huggingface/text-embeddings-inference/fork) | [#880](https://github.com/huggingface/text-embeddings-inference/issues/880) `te_queue_size` metric never increases when requests are queued ● | Rust |

## Comment first, then fix (6 repos)

| # | Fork | Target issue | Language | Why ◐ |
|---|---|---|---|---|
| 15 | [safetensors/safetensors](https://github.com/safetensors/safetensors/fork) | [#861](https://github.com/safetensors/safetensors/issues/861) slicing a tensor with a zero-length dimension errors, even for `[:]` ◐ | Rust/Python | reporter offered a PR |
| 16 | [data-privacy-stack/presidio](https://github.com/data-privacy-stack/presidio/fork) | [#2256](https://github.com/data-privacy-stack/presidio/issues/2256) context enhancement is ineffective for agglutinative languages (good first issue) ◐ | Python | labelled good-first-issue; likely to attract others, so claim it |
| 17 | [onnx/onnx](https://github.com/onnx/onnx/fork) | [#8437](https://github.com/onnx/onnx/issues/8437) DynamicQuantizeLinear: spec, function body and reference disagree on `y_scale` for all-zero input ◐ | Python/C++ | reporter is waiting for a maintainer to pick which of the three is right |
| 18 | [mistralai/client-python](https://github.com/mistralai/client-python/fork) | [#626](https://github.com/mistralai/client-python/issues/626) eager dual-client instantiation and asymmetric `__exit__`/`__aexit__` leak HTTP clients ◐ | Python | SDK is Speakeasy-generated; confirm the fix belongs in the hand-written layer |
| 19 | [browser-use/browser-use](https://github.com/browser-use/browser-use/fork) | [#5817](https://github.com/browser-use/browser-use/issues/5817) user-agent shadow roots reported as `SHADOW(open)` in serialized page state ◐ | Python | reporter proposed two fixes and asked the maintainers to choose |
| 20 | [huggingface/candle](https://github.com/huggingface/candle/fork) | [#3707](https://github.com/huggingface/candle/issues/3707) CPU quantized matmul has no batch path; prefill runs token-at-a-time ◐ | Rust | unclaimed but a multi-day change; confirm the approach with maintainers first |

## Backups (if a target above gets taken)

| Repo | Issue | Note |
|---|---|---|
| ggml-org/llama.cpp | [#29458](https://github.com/ggml-org/llama.cpp/issues/29458) `/infill` accepts out-of-range token ids that `/completion` rejects | ● same reporter, same day as #29451 |
| Lightning-AI/litdata | [#402](https://github.com/Lightning-AI/litdata/issues/402) wrong `len(StreamingDataLoader)` when `drop_last=False` | ● help-wanted since 2024; maintainer removed "won't fix" |
| microsoft/Olive | [#2688](https://github.com/microsoft/Olive/issues/2688) calibration reader returns the wrong batches after `set_range` | ◐ reporter says a fix is prepared |
| pyannote/pyannote-audio | [#2042](https://github.com/pyannote/pyannote-audio/issues/2042) discrete DER reports 0.0 because frame counts saturate float16 | ◐ reporter offered a PR |
| huggingface/huggingface.js | [#2521](https://github.com/huggingface/huggingface.js/issues/2521) `checkCredentials` rejects non-`hf_` tokens on self-hosted hubs | ◐ reporter offered a PR |
| anthropics/anthropic-sdk-typescript | [#749](https://github.com/anthropics/anthropic-sdk-typescript/issues/749) surface `ping`/`error` in `RawMessageStreamEvent` | maintainers labelled it `code-change` in Apr 2026 after initially declining; design-level |

## Caveats by repo

- **flax, jax, langextract-style Google repos** need the Google CLA signed once at
  https://cla.developers.google.com before a PR can merge.
- **onnxruntime, Olive** (Microsoft) use the Microsoft CLA bot; it signs on the first PR.
- **mlx-lm** runs on Linux CPU via the `mlx` wheel; the MiniCPM3 issue includes a weight-free
  reproduction script, so no model download is needed.
- **llama.cpp** needs a CPU build (`cmake -B build && cmake --build build -j`) and a small
  GGUF (the issue uses Qwen2.5-0.5B-Instruct Q4_K_M).
- **text-embeddings-inference, safetensors, candle** are Rust; builds are slow the first time
  but the affected code is CPU-only.
- **ogx** was `meta-llama/llama-stack`; fixes may need to target the `release-1.0.x` branch as
  well as `main`.
- **chonkie** moved from `chonkie-inc/chonkie` to `feyninc/chonkie`; the fork link above is the
  new location.

## Repos scanned and rejected this round

Every candidate in these repos was already claimed, fixed on main, had a linked PR, or needed
GPU hardware: adk-python, anthropic-sdk-typescript (#1116), candle (#3878), deepeval, DeepSpeed,
executorch, faster-whisper, FlagEmbedding, Guardrails (3 issues, all taken), huggingface.js
(#2545), instructor, kernels, langchainjs (3 issues, all taken), langextract (3 issues, all
reporter-fixed), langgraph, lerobot, litellm, llm-compressor, MCP python-sdk (3 issues, all
claimed), MCP typescript-sdk (2 claimed), NeMo, ollama-python, openai-agents-js, openai-node,
optax, optimum-onnx, pgvector-python, pytorch-image-models, qdrant-client, ragas, ray, scikit-learn
(#34883, #34942 both claimed), spaCy, speechbrain, stable-baselines3, tiktoken, torchtitan,
torchtune, torchvision, trl, vercel/ai, web-llm.
