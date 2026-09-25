# 50 repositories, one PR target each

Scanned 2026-09-25. Every issue is **open, unassigned, and has no linked PR**
(`is:issue is:open no:assignee -linked:pr`).

**What the vetting means.** Each was chosen because its title states a concrete,
reproducible defect with a determinate fix — not a feature request, support question or
roadmap item. That filter threw out most of what the counts contain. It is **not** the same
as having reproduced each one; reproduction is step one of the work. Confidence is graded
below, and the ones marked ● are the ones whose mechanism is stated precisely enough to be
near-certain.

**Before starting any of them**, check `docs/ai-contribution-policies.md`. Two repos here
auto-close PRs that skip an approval gate.

---

## Tier A — mechanism stated precisely, high confidence ●

| # | Repo | Issue | The defect |
|---|---|---|---|
| 1 | huggingface/accelerate | [#4253](https://github.com/huggingface/accelerate/issues/4253) | `compile_regions` runs the **uncompiled** model when the root module has a hook — silent, no error ✅ *fixed* |
| 2 | UKGovernmentBEIS/inspect_ai | [#5525](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5525) | Blank target scores every sample CORRECT ✅ *fixed, gated* |
| 3 | stanfordnlp/dspy | [#10497](https://github.com/stanfordnlp/dspy/issues/10497) | Method-named fields hold two different values at once ✅ *fixed* |
| 4 | deepset-ai/haystack | [#12939](https://github.com/deepset-ai/haystack/issues/12939) | `Sockets.__getattribute__` references `_sockets`; the real attribute is `_sockets_dict` |
| 5 | huggingface/transformers.js | [#1767](https://github.com/huggingface/transformers.js/issues/1767) | `createInferenceSession()` memoises a **rejected** promise, breaking every later session |
| 6 | weaviate/weaviate | [#12959](https://github.com/weaviate/weaviate/issues/12959) | `[HNSW] AddMulti` panics on nil multivector input |
| 7 | openvinotoolkit/openvino | [#38246](https://github.com/openvinotoolkit/openvino/issues/38246) | ROI tensor keeps owner's strides after `set_shape()`; `copy_to()` reads out of bounds (SIGSEGV) |
| 8 | evidentlyai/evidently | [#1930](https://github.com/evidentlyai/evidently/issues/1930) | `TestSummaryInfo.has_all` checks `any_column` instead of `all_column` |
| 9 | chroma-core/chroma | [#7688](https://github.com/chroma-core/chroma/issues/7688) | hnswlib persists **uninitialized heap memory** into `length.bin` |
| 10 | mem0ai/mem0 | [#7454](https://github.com/mem0ai/mem0/issues/7454) | Qdrant entity-store silently truncates after 10k rows |
| 11 | huggingface/sentence-transformers | [#4060](https://github.com/huggingface/sentence-transformers/issues/4060) | Inputs silently truncated at `max_seq_length` with no way to detect it |
| 12 | mlflow/mlflow | [#26144](https://github.com/mlflow/mlflow/issues/26144) | `min_relative_change` accepts worse models when the baseline metric is negative |
| 13 | comet-ml/opik | [#8454](https://github.com/comet-ml/opik/issues/8454) | Dotted-key metadata filter silently returns 0 rows |
| 14 | agno-agi/agno | [#10594](https://github.com/agno-agi/agno/issues/10594) | Tools silently replace an explicit `max_results=0` with the default |
| 15 | microsoft/graphrag | [#2573](https://github.com/microsoft/graphrag/issues/2573) | `community_level` does not select a level — broken since v2.0.0 |
| 16 | promptfoo/promptfoo | [#11056](https://github.com/promptfoo/promptfoo/issues/11056) | Provider IDs truncate model names containing a colon |
| 17 | huggingface/smolagents | [#2746](https://github.com/huggingface/smolagents/issues/2746) | `LocalPythonExecutor` silently drops the `else` clause of `for`/`while` |
| 18 | dottxt-ai/outlines | [#1971](https://github.com/dottxt-ai/outlines/issues/1971) | `Optional[T]` emits Python `None` instead of JSON `null` in DSL containers |
| 19 | microsoft/autogen | [#8282](https://github.com/microsoft/autogen/issues/8282) | `TextMentionTermination(sources=…)` drops `sources` on dump/load |
| 20 | Arize-ai/phoenix | [#16519](https://github.com/Arize-ai/phoenix/issues/16519) | `executeSql` JSON path returns NULL on PostgreSQL, works on SQLite |

## Tier B — solid defects, verify the repro first

| # | Repo | Issue | The defect |
|---|---|---|---|
| 21 | stanfordnlp/dspy | [#10498](https://github.com/stanfordnlp/dspy/issues/10498) | Fallback re-calls the LM on validation errors ✅ *fixed* |
| 22 | EleutherAI/lm-evaluation-harness | [#4230](https://github.com/EleutherAI/lm-evaluation-harness/issues/4230) | Regex filter matches "Note: All" as answer A — no word boundary |
| 23 | UKGovernmentBEIS/inspect_ai | [#5544](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5544) | Grok refusals not swallowed as `content_filter` — **`accepted, qualified`** |
| 24 | milvus-io/milvus | [#53508](https://github.com/milvus-io/milvus/issues/53508) | Cancelling one search fails every request merged into the same group |
| 25 | docling-project/docling | [#4357](https://github.com/docling-project/docling/issues/4357) | Threaded parser drops most of a scanned PDF's OCR text layer |
| 26 | qdrant/qdrant | [#10757](https://github.com/qdrant/qdrant/issues/10757) | Range-to-OR filters cause up to 10.2× search latency regression |
| 27 | langchain-ai/langchain | [#40809](https://github.com/langchain-ai/langchain/issues/40809) | Bedrock Converse drops redacted reasoning from `content_blocks` |
| 28 | pydantic/pydantic-ai | [#8767](https://github.com/pydantic/pydantic-ai/issues/8767) | Breaking out of `stream_text()` logs an async-generator error |
| 29 | Lightning-AI/pytorch-lightning | [#21431](https://github.com/Lightning-AI/pytorch-lightning/issues/21431) | `save_checkpoint()` occasionally writes a corrupt checkpoint |
| 30 | huggingface/peft | [#3813](https://github.com/huggingface/peft/issues/3813) | BOFT Conv2d ignores dilation, 2D stride/padding, `padding_mode` ⚠️ gated |
| 31 | langfuse/langfuse | [#17949](https://github.com/langfuse/langfuse/issues/17949) | Non-ASCII prompt variables extracted but never compiled |
| 32 | voxel51/fiftyone | [#8351](https://github.com/voxel51/fiftyone/issues/8351) | Representativeness `norm` parameter hard-coded to `local` |
| 33 | datalab-to/marker | [#1110](https://github.com/datalab-to/marker/issues/1110) | `--disable_multiprocessing` only sets `pdftext_workers=1` |
| 34 | huggingface/lighteval | [#1299](https://github.com/huggingface/lighteval/issues/1299) | `wikitext:103:document_level` task does not work |
| 35 | Unstructured-IO/unstructured | [#4434](https://github.com/Unstructured-IO/unstructured/issues/4434) | Fallback encoding detection skipped for file-like objects |
| 36 | huggingface/transformers | [#33946](https://github.com/huggingface/transformers/issues/33946) | `DataCollatorWithFlattening` incompatible with non-list input ids |
| 37 | argilla-io/distilabel | [#1157](https://github.com/argilla-io/distilabel/issues/1157) | The guide's own example fails to load `magpie_generator_0` |
| 38 | neuml/txtai | [#1239](https://github.com/neuml/txtai/issues/1239) | Transformers breaking change broke the text-to-audio pipeline |
| 39 | vllm-project/vllm | [#31624](https://github.com/vllm-project/vllm/issues/31624) | ModelOpt Llama-4 checkpoints take 5+ minutes to load |
| 40 | sgl-project/sglang | [#8174](https://github.com/sgl-project/sglang/issues/8174) | Mllama ambiguous multi-image behaviour |

## Tier C — real but larger, riskier, or needing a judgement call

| # | Repo | Issue | Note |
|---|---|---|---|
| 41 | camel-ai/camel | [#4351](https://github.com/camel-ai/camel/issues/4351) | MCP servers created with no authentication (CVSS 9.8). Security — coordinate with maintainers first |
| 42 | microsoft/semantic-kernel | [#14072](https://github.com/microsoft/semantic-kernel/issues/14072) | No runtime access control in auto function invocation. Design-level |
| 43 | huggingface/diffusers | [#9508](https://github.com/huggingface/diffusers/issues/9508) | AnimateDiff SparseCtrl RGB doesn't match the reference implementation |
| 44 | pytorch/pytorch | [#89197](https://github.com/pytorch/pytorch/issues/89197) | Collective ops fail with `BoolTensor` on gloo. Old, but well-specified |
| 45 | axolotl-ai-cloud/axolotl | [#3152](https://github.com/axolotl-ai-cloud/axolotl/issues/3152) | `total_num_steps` wrong with `sample_packing_eff_est`. Marked *waiting for reporter* |
| 46 | unslothai/unsloth | [#11952](https://github.com/unslothai/unsloth/issues/11952) | Device mismatch training Gemma 4 31b. Needs a GPU to reproduce |
| 47 | ultralytics/ultralytics | [#26139](https://github.com/ultralytics/ultralytics/issues/26139) | Models truncate long OCR text. 44 comments — read the thread first |
| 48 | crewAIInc/crewAI | [#7629](https://github.com/crewAIInc/crewAI/issues/7629) | Sanitized tool-name collisions. No repro given — confirm it bites |
| 49 | guidance-ai/guidance | [#1396](https://github.com/guidance-ai/guidance/issues/1396) | Grammar constraints leak unexpected tokens. Could be user error |
| 50 | InternLM/lmdeploy | [#4558](https://github.com/InternLM/lmdeploy/issues/4558) | AWQ OOM with TurboMind on V100. Hardware-specific |

---

## Forks needed

Already forked: `dspy`, `peft`, `diffusers`, `accelerate`, `transformers`, `vllm`,
`sglang`, `inspect_ai`, `lm-evaluation-harness`, `pytorch`, `langchain`, `autogen`.

Still to fork, in Tier A order: `haystack`, `transformers.js`, `weaviate`, `openvino`,
`evidently`, `chroma`, `mem0`, `sentence-transformers`, `mlflow`, `opik`, `agno`,
`graphrag`, `promptfoo`, `smolagents`, `outlines`, `phoenix` — then Tier B's
`milvus`, `docling`, `qdrant`, `pytorch-lightning`, `langfuse`, `fiftyone`, `marker`,
`lighteval`, `unstructured`, `distilabel`, `txtai`.

## Repos ruled out — zero unclaimed issues

`google/jax`, `NVIDIA/NeMo`, `NVIDIA/TensorRT-LLM`, `NVIDIA/warp`, `NVIDIA/NeMo-Guardrails`,
`langchain-ai/langgraph`, `Browser-use/browser-use`, `All-Hands-AI/OpenHands`,
`huggingface/trl`, `BerriAI/litellm`, `ray-project/ray`, `run-llama/llama_index`,
`modelcontextprotocol/python-sdk`, `explodinggradients/ragas`, `duckdb/duckdb`,
`pytorch/torchtune`, `microsoft/DeepSpeed`, `hiyouga/LLaMA-Factory`, `infiniflow/ragflow`,
`Giskard-AI/giskard`, `microsoft/onnxruntime`, `openai/whisper`.

Scanned but yielded no concrete defects: `confident-ai/deepeval`, `guardrails-ai/guardrails`,
`huggingface/pytorch-image-models`, `mlfoundations/open_clip`, `keras-team/keras`.

Google and NVIDIA repos auto-assign their issues, so there is no entry path through an
existing issue at all.

## Where to start

Targets 4, 5, 6, 8 and 15 are the cheapest real wins: each is a stated, local defect in a
pure-Python or well-isolated file, in a repo with no approval gate.
