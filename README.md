# OS_Contribution

Working repository for a planned open-source contribution campaign across major AI
projects, and for the evidence trail that goes with it.

## Contents

| Path | What it is |
|---|---|
| `docs/target-list.md` | Verified scan of unclaimed issues across 13 top AI repos (2026-09-25) |
| `docs/eb1a-strategy.md` | Honest assessment of what actually counts as EB-1A evidence |
| `tools/scan_unclaimed.py` | Reproduces the scan; needs `GITHUB_TOKEN` |

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

Breadth is the wrong instinct here. Volume of merged PRs is weak EB-1A evidence; what
carries weight is *status* and *independent attestation* — maintainer role, release notes
naming you, letters from maintainers who have merged your work repeatedly. That argues
for going deep in one or two projects rather than wide across twenty.

See `docs/eb1a-strategy.md`. Not legal advice.

## Re-running the scan

```bash
export GITHUB_TOKEN=...          # public-repo read is enough
python tools/scan_unclaimed.py --json scan.json
```
