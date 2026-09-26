# PR follow-ups — checked 2026-09-26 (evening)

Scanned every open PR by bhaskargurram-ai (22 real PRs; the four "awesome-list" PRs are
not part of this campaign). No human maintainer has reviewed any of them yet. Everything
below is either a bot finding, a CLA gate, or a template gate. Items marked **you** need
the GitHub account (this session cannot post to upstream repos); items marked **done**
were handled by pushing to the fork branch, which updates the PR automatically.

## Needs you (5 minutes total)

### 1. Sign the Google CLA (blocks jax #41009 and flax #5600)
Go to https://cla.developers.google.com/ and sign as an individual with the email on the
commits (`gurrambhaskar.ai@gmail.com`). The `google-cla` check re-runs automatically; if it
does not, comment `@googlebot I signed it!` on each PR.

### 2. llama.cpp #29496 — bot converted it to draft ("PR template not respected")
Edit the PR description so it has exactly the template's three sections, then click
"Ready for review". The repo forbids AI-written PR text, so use this as a starting point
and put it in your own words:

```
## Overview

Fixes #29451.

With n > 1, llama-server merges every choice into the first result's `choices` but leaves
that result's `usage` alone, so `completion_tokens`/`total_tokens` report one choice only.
In streaming mode each choice emitted its own usage chunk. This PR adds a small usage
aggregator (sums `n_decoded` over all choices, counts the prompt once per input), uses it
for the non-streaming response, and in streaming emits a single aggregated usage on the
last chunk. n = 1 is untouched. Two server tests cover chat and completions, streaming and
non-streaming; both fail on master and pass here.

## Additional information

Related: #29451. Verified on a CPU build with `-np 4`; `n=3, max_tokens=16` now reports
`completion_tokens: 48` instead of 16.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES - an AI assistant helped locate the merge point in
  server-context.cpp and draft the tests; I reviewed and ran everything myself.
```

### 3. ogx #6669 — description has the empty template headers appended
Edit the description: move the explanation under `# What does this PR do?` and put this
under `## Test Plan`:

```
## Test Plan

uv run pytest tests/unit/providers/inference/test_sentence_transformers_registry_deps.py
  -> 2 failed on main, 2 passed on this branch
uv run pytest tests/unit/test_update_registry_deps.py tests/unit/distribution/test_list_deps_output.py tests/unit/cli/test_stack_utils.py tests/unit/providers/test_configs.py
  -> 37 passed
uv lock --check -> lockfile unchanged
```

### 4. onnxruntime #32830 — Copilot review, one high-severity finding
Fix pushed to the branch (see "Done" below). Reply on the Copilot thread with the text in
the "Round 2" section of `prs/onnxruntime-32802-quant-pre-process-skip-shape-inference.md`,
then resolve the thread.

### 5. pymilvus #3814 — nothing to do
Your `queue` comment was rejected by Mergify (needs write permission). The approver bot will
act once a maintainer reviews; ignore it.

## No action needed (waiting on maintainers)

datatrove #532 (Cursor Bugbot: no findings) · cohere-python #815 (Bugbot: "Low risk", no
findings) · Olive #2693 (Copilot: no findings, one note that the guard test cannot run when
`requests` is absent because conftest imports olive first; harmless) · LitServe #761 ·
text-embeddings-inference #936 · mlx-lm #1925 · flax #5600 (after CLA) · jax #41009 (after
CLA) · datasets #8687 / #8688 · langsmith-sdk #3597 · tokenizers #2459 · transformers.js
#1780 · accelerate #4337 · haystack #12966 (CLA signed, reviewer re-assigned) · weaviate
#13285 (Copilot + SonarQube findings already addressed in the previous push) · dspy #10499 /
#10501 (Greptile findings already addressed; the remaining #10501 note is marked
non-blocking).

## Not yet opened by you

safetensors #861, presidio #2256, onnx #8437, mistral client-python #626, browser-use
#5817, chonkie #631, candle #3707 — links and pre-open comments in
`prs/prefilled-links-2.md`.

## Closed

inspect_ai #5563 / #5568 — auto-closed by the contribution-policy bot (needs the `accepted`
label on the issue first). Do not reopen.
