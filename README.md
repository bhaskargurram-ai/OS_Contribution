# OS_Contribution

Working repository for a planned open-source contribution campaign across major AI
projects: where to contribute, what is genuinely unclaimed, and how to prioritise.

## Contents

| Path | What it is |
|---|---|
| `docs/target-list.md` | Verified scan of unclaimed issues across 13 top AI repos (2026-09-25) |
| `docs/contribution-strategy.md` | How to prioritise: why depth beats breadth |
| `tools/scan_unclaimed.py` | Reproduces the scan; needs `GITHUB_TOKEN` |
| `docs/pr-status.md` | **Live status of every PR and what each needs next** |
| `docs/fork-list.md` | **20 repos to fork, with the target issue for each** |
| `docs/company-oss-targets.md` | 21 more targets across AI-company OSS (Apple, Meta, NVIDIA, Microsoft, OpenAI…) |
| `docs/fifty-targets.md` | **50 repos, one vetted PR target each** |
| `docs/top-20-targets.md` | The 20 best targets, ranked by actionability |
| `docs/triage-notes.md` | Issues examined and rejected, and why |
| `docs/ai-contribution-policies.md` | Per-repo rules on AI-assisted contributions |
| `docs/blockers.md` | What blocks automated contribution and how to clear it |
| `prs/` | One file per contribution: branch, compare URL, ready PR body, verification |

## What "unclaimed" means here

`is:issue is:open no:assignee -linked:pr` — open, unassigned, and with **no pull request
linked to it**. `-linked:pr` is GitHub's own qualifier, so this is real linkage state,
not inference.

It is not a guarantee. Someone can have an open PR that mentions an issue without
formally linking it. Check the thread and the repo's open PRs before starting.

## Headline result

Unclaimed issue counts, 2026-09-25:

```
huggingface/transformers   280      sgl-project/sglang            13
stanfordnlp/dspy           210      pytorch/pytorch                7
huggingface/diffusers       38      vllm-project/vllm              4
huggingface/accelerate      34      openai/openai-agents-python    1
huggingface/peft            18      litellm / ray / llama_index    0
```

Filters differ per repo (label vocabularies are not shared); see `tools/scan_unclaimed.py`.

## The short strategic answer

Breadth is the tempting instinct and the weaker one. Merge count does not compound;
standing does — maintainer role, release-note credit, downstream adoption, reviewers who
trust you. That argues for going deep in one or two projects rather than wide across
twenty.

See `docs/contribution-strategy.md`.

## Re-running the scan

```bash
export GITHUB_TOKEN=...          # public-repo read is enough
python tools/scan_unclaimed.py --json scan.json
```

## In flight

| Target | Branch | State |
|---|---|---|
| [dspy #10498](https://github.com/stanfordnlp/dspy/issues/10498) — ChatAdapter falls back on validation errors | `bhaskargurram-ai/dspy:fix/chat-adapter-validation-fallback` | pushed, [PR ready to open](https://github.com/stanfordnlp/dspy/compare/main...bhaskargurram-ai:dspy:fix/chat-adapter-validation-fallback?expand=1) |
| [dspy #10497](https://github.com/stanfordnlp/dspy/issues/10497) — method-named fields diverge | `bhaskargurram-ai/dspy:fix/example-field-name-collision` | pushed, [PR ready to open](https://github.com/stanfordnlp/dspy/compare/main...bhaskargurram-ai:dspy:fix/example-field-name-collision?expand=1) |

| [accelerate #4253](https://github.com/huggingface/accelerate/issues/4253) — compile_regions silently runs uncompiled model | `bhaskargurram-ai/accelerate:fix/compile-regions-with-hooks` | pushed, [PR ready to open](https://github.com/huggingface/accelerate/compare/main...bhaskargurram-ai:accelerate:fix/compile-regions-with-hooks?expand=1) |

| [inspect_ai #5525](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5525) — blank target scores every sample CORRECT | `bhaskargurram-ai/inspect_ai:fix/blank-target-scores-correct` | pushed, [PR ready to open](https://github.com/UKGovernmentBEIS/inspect_ai/compare/main...bhaskargurram-ai:inspect_ai:fix/blank-target-scores-correct?expand=1) |

| [haystack #12939](https://github.com/deepset-ai/haystack/issues/12939) — Sockets.__getattribute__ reads a non-existent attribute | `bhaskargurram-ai/haystack:fix/sockets-getattribute-attribute-name` | pushed, [PR ready to open](https://github.com/deepset-ai/haystack/compare/main...bhaskargurram-ai:haystack:fix/sockets-getattribute-attribute-name?expand=1) |

| [datasets #8637](https://github.com/huggingface/datasets/issues/8637) — FileLock wrapper drops every constructor arg | `bhaskargurram-ai/datasets:fix/filelock-forward-constructor-args` | pushed, [PR ready to open](https://github.com/huggingface/datasets/compare/main...bhaskargurram-ai:datasets:fix/filelock-forward-constructor-args?expand=1) |

| [langsmith-sdk #3569](https://github.com/langchain-ai/langsmith-sdk/issues/3569) — HTTPError drops `.response` | `bhaskargurram-ai/langsmith-sdk:fix/http-error-keeps-response` | pushed, [PR ready to open](https://github.com/langchain-ai/langsmith-sdk/compare/main...bhaskargurram-ai:langsmith-sdk:fix/http-error-keeps-response?expand=1) |

| [datasets #8681](https://github.com/huggingface/datasets/issues/8681) — ClassLabel rejects pandas-3 `large_string` | `bhaskargurram-ai/datasets:fix/classlabel-cast-large-string` | pushed, [PR ready to open](https://github.com/huggingface/datasets/compare/main...bhaskargurram-ai:datasets:fix/classlabel-cast-large-string?expand=1) |

| [transformers.js #1767](https://github.com/huggingface/transformers.js/issues/1767) — one rejected session poisons every later one | `bhaskargurram-ai/transformers.js:fix/serial-chain-rejection-poisons-later-sessions` | pushed, [PR ready to open](https://github.com/huggingface/transformers.js/compare/main...bhaskargurram-ai:transformers.js:fix/serial-chain-rejection-poisons-later-sessions?expand=1) — **comment on the issue first** (repo policy) |

| [modal-client #4130](https://github.com/modal-labs/modal-client/issues/4130) — `volume get` corrupts a directory download to a new path | `bhaskargurram-ai/modal-client:fix/volume-get-new-directory-destination` | pushed, [PR ready to open](https://github.com/modal-labs/modal-client/compare/main...bhaskargurram-ai:modal-client:fix/volume-get-new-directory-destination?expand=1) |

| [weaviate #12959](https://github.com/weaviate/weaviate/issues/12959) — HNSW `AddMulti` panics on a nil multivector | `bhaskargurram-ai/weaviate:fix/hnsw-addmulti-nil-multivector` | pushed, [PR ready to open](https://github.com/weaviate/weaviate/compare/main...bhaskargurram-ai:weaviate:fix/hnsw-addmulti-nil-multivector?expand=1) |

| [graphrag #2573](https://github.com/microsoft/graphrag/issues/2573) — `community_level` has no effect since v2.0.0 | `bhaskargurram-ai/graphrag:fix/community-level-rollup-groups-by-entity` | pushed, [PR ready to open](https://github.com/microsoft/graphrag/compare/main...bhaskargurram-ai:graphrag:fix/community-level-rollup-groups-by-entity?expand=1) — **not as a Draft** (repo policy) |

Before submitting any of these, read `docs/ai-contribution-policies.md` — dspy requires an AI-assistance
disclosure line, which is included in each prepared body.

## Commit authorship

Commits must be authored with `gurrambhaskar.ai@gmail.com`, the address verified on the
`bhaskargurram-ai` GitHub account. An earlier batch used a different address which GitHub
attributes to a separate account, so the commits and the pull request showed two different
authors. All branches have been re-authored.

```bash
git config user.name "Bhaskar Gurram"
git config user.email "gurrambhaskar.ai@gmail.com"
```
