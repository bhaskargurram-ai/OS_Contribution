# 20+ more targets — AI company open source

Scanned 2026-09-25, second pass. This round deliberately covers **company-backed** AI
repos the first scan missed: Apple, Meta, Microsoft, NVIDIA, OpenAI, Anthropic, AI2,
Ollama, Replicate, Modal, LangChain, EleutherAI, Hugging Face's less-travelled repos.

Same filter as before — `is:issue is:open no:assignee -linked:pr`, then narrowed to
concrete reproducible defects. Confidence graded; ● marks the ones whose mechanism is
stated precisely enough to be near-certain.

---

## Tier A ● — precise mechanism, high confidence

| # | Company | Repo | Issue | The defect |
|---|---|---|---|---|
| 1 | NVIDIA | TransformerEngine | [#3202](https://github.com/NVIDIA/TransformerEngine/issues/3202) | FusedAdam: **out-of-bounds metadata writes** when a zero-numel tensor lands in the last slot — silent data corruption |
| 2 | Hugging Face | datasets | [#8637](https://github.com/huggingface/datasets/issues/8637) | `FileLock` wrapper **discards every kwarg except `lock_file`** — `timeout` silently ignored |
| 3 | Hugging Face | tokenizers | [#2334](https://github.com/huggingface/tokenizers/issues/2334) | `Precompiled` normalizer **silently drops codepoints** in multi-codepoint graphemes; diverges from SentencePiece |
| 4 | Meta | faiss | [#5567](https://github.com/facebookresearch/faiss/issues/5567) | `IndexEDEN` with 1-bit EDEN returns **negative `METRIC_L2` distances** |
| 5 | Apple | mlx | [#4538](https://github.com/ml-explore/mlx/issues/4538) | `mlx.sort` returns **incorrect results on GPU** for large uint8 arrays |
| 6 | LangChain | langsmith-sdk | [#3569](https://github.com/langchain-ai/langsmith-sdk/issues/3569) | `raise_for_status_with_text` drops `.response`, losing status codes and retry headers |
| 7 | NVIDIA | garak | [#2226](https://github.com/NVIDIA/garak/issues/2226) | `hf_args` keys **silently dropped** on transformers 5.x — `torch_dtype` has no effect |
| 8 | Microsoft | markitdown | [#2468](https://github.com/microsoft/markitdown/issues/2468) | RSS/Atom link resolution **collapses repeated slashes**, corrupting URL paths |
| 9 | Modal | modal-client | [#4130](https://github.com/modal-labs/modal-client/issues/4130) | `modal volume get` treats a missing destination as a file, **corrupting directory downloads** |
| 10 | Hugging Face | datasets | [#8681](https://github.com/huggingface/datasets/issues/8681) | `ClassLabel.cast_storage` only handles `pa.StringArray`, so `from_pandas` breaks on pandas 3 |
| 11 | Ollama | ollama | [#18595](https://github.com/ollama/ollama/issues/18595) | **No GC for orphaned blobs** — a live 21GB orphan found by manifest audit |

## Tier B — solid, verify the repro first

| # | Company | Repo | Issue | The defect |
|---|---|---|---|---|
| 12 | Apple | mlx | [#4560](https://github.com/ml-explore/mlx/issues/4560) | `__setitem__` with a bare ellipsis fails to broadcast leading singleton dims |
| 13 | NVIDIA | TransformerEngine | [#3294](https://github.com/NVIDIA/TransformerEngine/issues/3294) | `QuantizedTensor` on CPU causes `RecursionError` |
| 14 | Hugging Face | huggingface_hub | [#4987](https://github.com/huggingface/huggingface_hub/issues/4987) | Unexpected 401s when listing with generated JWTs |
| 15 | Hugging Face | tokenizers | [#2447](https://github.com/huggingface/tokenizers/issues/2447) | 1.0.0rc2 regression: byte atom not found in vocabulary |
| 16 | OpenAI | openai-python | [#2699](https://github.com/openai/openai-python/issues/2699) | Rate-limit errors handled inconsistently between Responses and Chat Completions |
| 17 | Keras | keras-hub | [#1191](https://github.com/keras-team/keras-hub/issues/1191) | No integration test asserting `generate()` stability across backends |
| 18 | Replicate | cog | [#1323](https://github.com/replicate/cog/issues/1323) | Push fails with `--separate-weights` |
| 19 | Modal | modal-client | [#4126](https://github.com/modal-labs/modal-client/issues/4126) | "Deployment skipped" detection inconsistent across deploys from one commit |
| 20 | EleutherAI | gpt-neox | [#1340](https://github.com/EleutherAI/gpt-neox/issues/1340) | AssertionError in position embedding, likely a missing `clear_cache` between batches |
| 21 | Microsoft | markitdown | [#2382](https://github.com/microsoft/markitdown/issues/2382) | DOCX OCR text matched to images by position instead of identity |

## Tier C — needs hardware, or not fixable in the repo

| Company | Repo | Issue | Caveat |
|---|---|---|---|
| Meta | xformers | [#1392](https://github.com/facebookresearch/xformers/issues/1392) | NaNs from CUTLASS GQA op — needs an Ampere/Ada GPU, nondeterministic |
| Anthropic | anthropic-sdk-python | [#1926](https://github.com/anthropics/anthropic-sdk-python/issues/1926) | Unicode double-escaping in strict tool calls — may be model behaviour, not an SDK bug |
| AI2 | olmocr | [#463](https://github.com/allenai/olmocr/issues/463) | One specific PDF fails to parse — needs the file to reproduce |
| Hugging Face | optimum | [#2487](https://github.com/huggingface/optimum/issues/2487) | `iostream error` on export — environment-specific |
| W&B | wandb | [#12943](https://github.com/wandb/wandb/issues/12943) | **Not contributable** — `[Bug-App]` issues are the hosted web app, not the OSS client |
| Gradio | gradio | [#13833](https://github.com/gradio-app/gradio/issues/13833) | Missing MCP button — feature gap rather than defect |

---

## Zero unclaimed issues

`meta-llama/llama-stack`, `microsoft/presidio`, `streamlit/streamlit`,
`huggingface/safetensors` — all returned nothing. Added to the growing ruled-out list in
`fifty-targets.md`.

## What this round changes

The first scan leaned toward frameworks. This one reaches **infrastructure and SDKs**, and
the defects are sharper for it: out-of-bounds writes, dropped kwargs, silently deleted
codepoints, negative distances, wrong GPU sort results. Those are easier to reproduce,
easier to test, and harder for a maintainer to argue with than a framework-level
behaviour question.

Targets 1–3 are the strongest on either list. Each is a contained bug in a widely-depended-on
library, with the mechanism already named in the issue.
