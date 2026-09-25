# Unclaimed-Issue Scan — Top AI Repositories

**Scan date:** 2026-09-25
**Definition of "unclaimed":** `is:issue is:open no:assignee -linked:pr`
— open, nobody assigned, and **no pull request linked to it**. This is GitHub's own
`linked:pr` qualifier, so it reflects real linkage rather than a guess.

**Caveat that matters:** `-linked:pr` only excludes *formally linked* PRs. Someone can
have an open PR that mentions the issue in prose without linking it. Always re-check the
issue thread and search the repo's open PRs before starting work.

---

## Summary table

| Repository | Unclaimed (filter used) | Read |
|---|---|---|
| huggingface/transformers | **280** (Good First/Second Issue, Feature request) | Huge surface, slow review queue |
| stanfordnlp/dspy | **210** (all labels) | Fast-moving, receptive maintainers |
| huggingface/accelerate | **34** (all labels) | Deep distributed-training bugs |
| huggingface/diffusers | **38** (gfi, help wanted, contributions-welcome) | Explicit "looking for community contribution" issues |
| huggingface/peft | **18** (all labels) | Highest signal-to-noise of the set |
| sgl-project/sglang | **13** (gfi, help wanted) | Kernel/perf work, high prestige |
| pytorch/pytorch | **7** (good first issue) | Mostly ancient; hard review bar |
| vllm-project/vllm | **4** (gfi + help wanted) | Few but very high value |
| openai/openai-agents-python | **1** (gfi, help wanted, enhancement) | Thin |
| BerriAI/litellm | **0** | Maintainers self-assign everything |
| ray-project/ray | **0** | No unclaimed labelled issues |
| run-llama/llama_index | **0** | No unclaimed labelled issues |
| modelcontextprotocol/python-sdk | **0** | No unclaimed labelled issues |

---

## Tier A — best effort-to-impact ratio

### huggingface/peft
Small codebase, precise bug reports, maintainers merge quickly, and the library sits
under nearly every fine-tuning stack in production. Several of these are real
correctness bugs with clear repro paths.

| # | Title | Comments | Age |
|---|---|---|---|
| 3814 | Trainable Tokens nests tied output-head wrappers with Transformers v5 metadata | 2 | 12h |
| 3813 | BOFT Conv2d forward ignores dilation, 2D stride/padding and padding_mode | 3 | 19h |
| 3804 | Adapter loading never warns about unexpected keys, `strict=True` silently ignored | 3 | 1d |
| 3803 | LoRA on FSDP2-sharded model gets local shard shape when mesh dim isn't named `fsdp` | 2 | 1d |
| 3802 | `save_pretrained` fails on FSDP2-sharded adapters (DTensor gather only when `_tp_size` set) | 2 | 1d |
| 3800 | FSDP2 `reshard_after_forward=False`: `disable_adapter()` leaves LoRA frozen | 2 | 1d |
| 3795 | DoRA convolution dropout path ignores non-zero `padding_mode` | 1 | 2d |
| 3793 | `load_adapter` infers `cuda` even when base model is on CPU | — | — |
| 3767 | Two test-infrastructure bugs found adding LoHa/LoKr/LN Tuning coverage | 2 | 6d |
| 3742 | PiSSA / MiCA / CorDA init bypasses quantized-layer guard | — | — |
| 3628 | TP + LoRA broken on transformers 5.16 (removed `add_tensor_parallel_hooks_to_module`) | 2 | 25d |
| 3723 | `PeftModel.set_adapter` raises opaque `TypeError: unhashable type: 'list'` | 1 | 13d |

**Note:** the FSDP2 cluster (3800/3802/3803) is one coherent body of work by a single
reporter. Fixing it as a set is a materially stronger contribution than three isolated
patches — it is a "FSDP2 support is correct in PEFT" story.

### huggingface/diffusers
Maintainers open issues *explicitly asking* for community contributors, which means a
named model integration lands with your name on it in release notes.

| # | Title | Comments |
|---|---|---|
| 12257 | [Looking for community contribution] Wan 2.2 S2V audio-driven video generation | 7 |
| 7219 | Add SUPIR upscaler | 36 |
| 10043 | F5-TTS integration | 12 |
| 7380 | One-step Diffusion with Distribution Matching Distillation | 20 |
| 9329 | AnimateDiff + SparseControl + ControlNet pipeline | 17 |
| 6586 | [Tracker] micro-conditioning for SDXL trainers | 13 |
| 11216 | PixArt Sigma PEFT LoRA loader support | 16 |
| 12235 | Support fun control variants for Wan | 4 |
| 9508 | AnimateDiff SparseCtrl RGB does not match reference implementation | 9 |

A full model/pipeline integration here is the single most *legible* artifact on this
whole list: it ships in a release, it is documented under your name, and it is
independently citable.

---

## Tier B — high prestige, high bar

### vllm-project/vllm
| # | Title | Comments |
|---|---|---|
| 38175 | [RFC] Support ViT Full CUDA Graph (Tracker) | 35 |
| 33702 | [Roadmap] PD Disaggregation with `NixlConnector` | 7 |
| 40544 | Integrate fused `kMoEFinalizeARResidualRMSNorm` from FlashInfer | 7 |
| 25750 | [Feature] Tracking Whisper feature requests | 26 |
| 31624 | ModelOpt Llama-4 checkpoints take 5+ min to load | 24 |
| 31414 | Unify `vllm.utils.flashinfer` and `…quantization.utils.flashinfer_utils` | 15 |
| 23957 | Support `Phi4Flash` model in V1 | 9 |
| 9129 | CMake clean-up / refactor tasks | 21 |

`#31624` (5-minute checkpoint load) is the standout: a measurable performance win with a
number you can put in a petition. Perf wins are the easiest contributions to
*quantify* for an adjudicator.

### sgl-project/sglang
| # | Title | Comments |
|---|---|---|
| 27214 | Support new diffusion models | 9 |
| 13363 | [Roadmap] sglang auto tuner | 15 |
| 1715 | Cascade attention kernels (high priority) | 8 |
| 10585 | Integrate KVPress for KV-cache optimization heuristics | 9 |
| 1763 | 8-bit quantization of attention with SageAttention | 9 |
| 12562 | Simplify `tree_speculative_sampling_target_only` | 3 |
| 8496 | [Tracking] Improve multimodal CI coverage | 3 |
| 8174 | Mllama ambiguous multi-image behaviour | 3 |
| 2729 | Support bitsandbytes in Qwen2-VL | 4 |

### huggingface/accelerate
| # | Title | Comments |
|---|---|---|
| 2038 | [FSDP] support activation offloading with FSDP | 5 |
| 3874 | FSDP2 QLoRA | 3 |
| 2951 | `DeepSpeedEngineWrapper.backward()` does too much | 19 |
| 1239 | SLURM support | 23 |
| 4253 | `compile_regions` runs uncompiled model when root module has an accelerate hook | 1 |
| 1105 | Add backend to `InitProcessGroupKwargs` | 3 |
| 1089 | Clean exit when using `accelerate launch` | 25 |

Note the overlap with PEFT: **FSDP2 + LoRA/QLoRA correctness spans peft #3800/3802/3803
and accelerate #3874**. Owning that seam across two libraries is a coherent,
attributable body of work.

---

## Tier C — low yield, do not start here

`pytorch/pytorch` good-first-issues are mostly 2018–2022 vintage and survive because they
are awkward, not because nobody noticed. `litellm`, `ray`, `llama_index` and
`modelcontextprotocol/python-sdk` returned **zero** unclaimed labelled issues — their
maintainers self-assign. For those, the entry path is an RFC or a bug you find yourself,
not an existing issue.

---

## Re-running this scan

`tools/scan_unclaimed.py` reproduces the table. It needs a GitHub token with public-repo
read (`GITHUB_TOKEN`); run it anywhere with normal API access.
