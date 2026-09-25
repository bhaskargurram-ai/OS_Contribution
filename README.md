# OS_Contribution

Working repository for a planned open-source contribution campaign across major AI
projects: where to contribute, what is genuinely unclaimed, and how to prioritise.

## Contents

| Path | What it is |
|---|---|
| `docs/target-list.md` | Verified scan of unclaimed issues across 13 top AI repos (2026-09-25) |
| `docs/contribution-strategy.md` | How to prioritise: why depth beats breadth |
| `tools/scan_unclaimed.py` | Reproduces the scan; needs `GITHUB_TOKEN` |
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
