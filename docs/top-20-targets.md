# The 20 best PR targets

Ranked by *actionability*, not by repo prestige. Every issue below is open, unassigned and
has no linked PR as of 2026-09-25.

**What "vetted" means here:** each was selected because its title describes a concrete,
reproducible defect with a determinate fix — not a feature proposal, a support question or
an environment report. That is a strong filter, but it is not the same as having
reproduced each one. Reproduction is the first step of the work on each.

---

> **Gate confirmed the hard way.** An inspect_ai PR referencing an open, well-evidenced
> issue was auto-closed in under a minute because *the issue itself* was not labelled
> `accepted`. Every inspect_ai target below needs that label first. See
> `docs/ai-contribution-policies.md`.

## Tier 1 — maintainer-validated (do these first)

`inspect_ai` labels issues `accepted` once a maintainer agrees the bug is real, which
removes the single biggest source of wasted effort.

| # | Issue | Why it's good |
|---|---|---|
| 1 | [inspect_ai #5544](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5544) — Grok API blocks/refusals don't get swallowed as `content_filter` and fail the eval | Labelled **`accepted, qualified`** — maintainers already confirmed it |
| 2 | [inspect_ai #5525](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5525) — a blank `Sample.target` makes every completion CORRECT | Severe silent-correctness bug; scores every eval wrong |
| 3 | [inspect_ai #5207](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5207) — model provider for Tinker checkpoints | Labelled **`accepted`** |

## Tier 2 — concrete correctness bugs, pure Python, fast tests

| # | Issue | Why it's good |
|---|---|---|
| 4 | [lm-eval-harness #4230](https://github.com/EleutherAI/lm-evaluation-harness/issues/4230) — `MultiChoiceRegexFilter` matches "Note: All" as answer A (no word boundary) | Regex bug with an exact repro; corrupts benchmark scores |
| 5 | [lm-eval-harness #4159](https://github.com/EleutherAI/lm-evaluation-harness/issues/4159) — group rows keep 0.0 stderr when every subtask is on the boundary | Statistics bug, self-contained |
| 6 | [lm-eval-harness #4084](https://github.com/EleutherAI/lm-evaluation-harness/issues/4084) — request-cache keys omit the task config | Cache-correctness; wrong results across tasks |
| 7 | [lm-eval-harness #4158](https://github.com/EleutherAI/lm-evaluation-harness/issues/4158) — GGUF backend `echo=true` broken against current llama-server | Clear contract mismatch |
| 8 | [lm-eval-harness #3252](https://github.com/EleutherAI/lm-evaluation-harness/issues/3252) — auto batch size in `generate_until` overly conservative | Measurable perf win |
| 9 | [inspect_ai #5560](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5560) — `ToolEvent.span_id` is the enclosing span, not its tool span | One-line semantics bug, easily tested |
| 10 | [inspect_ai #5535](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5535) — human approval waits counted as sample working time | Accounting bug, deterministic |
| 11 | [inspect_ai #5529](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5529) — Groq cached prompt tokens billed at full rate | Cost-accounting bug |
| 12 | [inspect_ai #5528](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5528) — Grok reasoning tokens left out of `output_tokens` | Same family as 11; could share a PR |
| 13 | [inspect_ai #5526](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5526) — Google provider retries Gemini per-day quota 429s | Retry-policy bug; wastes quota |

## Tier 3 — peft (bundle these; see the approval gate below)

peft forbids one-off PRs for small fixes and **auto-closes any PR without a maintainer
comment containing `@peft-triage approved`**. Comment on the issues first.

| # | Issue | Why it's good |
|---|---|---|
| 14 | [peft #3800](https://github.com/huggingface/peft/issues/3800) + [#3802](https://github.com/huggingface/peft/issues/3802) + [#3803](https://github.com/huggingface/peft/issues/3803) — FSDP2 + LoRA correctness | **One PR, not three.** Coherent body of work |
| 15 | [peft #3813](https://github.com/huggingface/peft/issues/3813) — BOFT Conv2d ignores dilation, 2D stride/padding, `padding_mode` | Deterministic, CPU-testable |
| 16 | [peft #3795](https://github.com/huggingface/peft/issues/3795) — DoRA conv dropout ignores non-zero `padding_mode` | Same family as 15; bundle them |
| 17 | [peft #3804](https://github.com/huggingface/peft/issues/3804) — adapter loading never warns on unexpected keys, `strict=True` ignored | Reporter already proposed the design |
| 18 | [peft #3793](https://github.com/huggingface/peft/issues/3793) — `load_adapter` infers `cuda` even when base model is on CPU | Small, testable without a GPU |

## Tier 4 — agentic frameworks

| # | Issue | Why it's good |
|---|---|---|
| 19 | [pydantic-ai #8767](https://github.com/pydantic/pydantic-ai/issues/8767) — breaking out of `stream_text()` inside `run_stream()` logs an async-generator error | Labelled `bug`, `p:3-mid` by maintainers |
| 20 | [accelerate #4253](https://github.com/huggingface/accelerate/issues/4253) — `compile_regions` runs the uncompiled model when the root module has an accelerate hook | Silent perf regression; exact repro |

---

## Repos to fork

Needed for the list above:

- `UKGovernmentBEIS/inspect_ai` — targets 1, 2, 3, 9, 10, 11, 12, 13
- `EleutherAI/lm-evaluation-harness` — targets 4, 5, 6, 7, 8
- `pydantic/pydantic-ai` — target 19

Already forked: `peft`, `accelerate`, `dspy`, `diffusers`, `transformers`, `vllm`, `sglang`.

## Repos ruled out — do not spend time here

Each returned **zero** open, unassigned, unlinked issues:

`google/jax`, `NVIDIA/NeMo`, `NVIDIA/TensorRT-LLM`, `NVIDIA/warp`, `NVIDIA/NeMo-Guardrails`,
`langchain-ai/langgraph`, `Browser-use/browser-use`, `All-Hands-AI/OpenHands`,
`huggingface/trl`, `BerriAI/litellm`, `ray-project/ray`, `run-llama/llama_index`,
`modelcontextprotocol/python-sdk`.

Google and NVIDIA repos in particular auto-assign their issues, so there is no entry path
through an existing issue — contributing there means an RFC or a bug you find yourself.

`keras-team/keras` has 9, but they are RFCs and roadmap trackers rather than defects, and
[#23601](https://github.com/keras-team/keras/issues/23601) announces a new and stricter PR
policy. Low yield.

## Revised sequencing

`lm-evaluation-harness` (targets 4–8) has no acceptance gate, so it is now the fastest
path to merged work. The inspect_ai targets are still worth doing, but each needs its
issue labelled `accepted` before any code is written — file or comment first, then build.

## Original sequencing note

Tier 1 and 2 are 13 issues across two repos with fast Python test suites. That is the
efficient path: two environments to set up, thirteen targets, and `inspect_ai`'s `accepted`
label means the maintainers have already agreed the bugs are real.
