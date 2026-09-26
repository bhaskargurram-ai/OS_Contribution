# Triage notes — issues examined and rejected

Not every unclaimed issue is a PR. Recording the ones investigated and dropped, so they
don't get picked up again.

| Issue | Verdict |
|---|---|
| [dspy #8879](https://github.com/stanfordnlp/dspy/issues/8879) — `Embedder` KeyError with custom function | **Not a bug.** The traceback is inside the reporter's own `jina_embeddings`. `Embedder` documents that a custom callable "takes a list of strings as input"; theirs treats the argument as a single string and wraps it in a list, producing a nested list the Jina API rejects. The `KeyError: 'data'` is their code reading an error response. Answer on the issue; do not open a PR. |
| [peft #3723](https://github.com/huggingface/peft/issues/3723) — opaque `TypeError` in `set_adapter` | **Claimed.** The reporter states they have a fix and regression test ready. No linked PR yet, so it passes the `-linked:pr` filter, but opening one would duplicate their work. |

## What this implies about the scan numbers

The ~600 "unclaimed" issues in `target-list.md` are not ~600 available PRs. Sampling them,
the population breaks down roughly as:

- **user error or unreproducible** — the reporter's own code, or an environment problem
- **environment-specific** — a provider outage, one Azure deployment, a network filesystem
- **feature proposals** — need design agreement before any code is worth writing
- **promotional** — vendors opening issues to advertise a product
- **claimed in comments** — someone said "working on this" without opening a PR
- **actually actionable** — a reproducible defect with a clear fix

Only the last category converts to a mergeable PR, and it is a minority of the total.
Budget effort against that fraction, not against the headline count.
| [markitdown #2468](https://github.com/microsoft/markitdown/issues/2468) — RSS/Atom link resolution collapses repeated slashes | **Deferred by maintainers.** Root cause is CPython's `urllib.parse.urljoin` (CPython #84774, upstream PR #126679 open). A workaround in markitdown would be closed as waiting-on-upstream. Do not build. |
| [markitdown #2382](https://github.com/microsoft/markitdown/issues/2382) — DOCX OCR text matched to images by position | **Reporter-owned.** The reporter laid out the full design (SHA-256 digest matching) and said they will submit the PR. Also needs new ≥12-image reversed-order fixtures. Duplicating it would get closed. |
| [evidently #1930](https://github.com/evidentlyai/evidently/issues/1930) — `has_all` checks `any_column` | **Claimed — PR exists.** [#1931](https://github.com/evidentlyai/evidently/pull/1931) is open with the one-line fix and six tests; an earlier [#1747](https://github.com/evidentlyai/evidently/pull/1747) proposed the same change. Referenced in the thread, not formally linked, so `-linked:pr` missed it. Do not build. |
| [garak #2226](https://github.com/NVIDIA/garak/issues/2226) — `hf_args` keys silently dropped on transformers 5 | **Claimed — reporter has a branch.** On Sep 24 the reporter proposed a scoped `torch_dtype`→`dtype` fix, said a branch with tests is ready, and the maintainer (`jmartin-tech`) approved the scope the same day. Issue is still `needs-triage` (not `bug-verified`), which `AGENTS.md` says to avoid anyway. No PR is linked yet, so `-linked:pr` still lists it. Do not build. |
| [faiss #5567](https://github.com/facebookresearch/faiss/issues/5567) — negative `METRIC_L2` distances from unbiased 1-bit EDEN | **Already fixed.** [#5569](https://github.com/facebookresearch/faiss/pull/5569) landed the fix; a would-be contributor withdrew for the same reason in the thread. Issue left open. Do not build. |
| [gpt-neox #1340](https://github.com/EleutherAI/gpt-neox/issues/1340) — position-embedding assertion during `generate_until` | **Unreproducible.** A maintainer trained the reporter's config and could not reproduce; the reporter lost track of which eval-harness version triggered it and never posted a repro. Needs a GPU either way. Do not build. |
| [keras-hub #1191](https://github.com/keras-team/keras-hub/issues/1191) — `generate()` stability integration tests | **Feature/infra, not a bug.** Labelled `type:feature` + `infra`; wants real preset checkpoints exercised across torch/tf/jax, which this environment cannot download or run. Do not build. |
| [cog #1323](https://github.com/replicate/cog/issues/1323) — `push --separate-weights` fails | **Registry-side.** A 2023 `404` from `r8.im/_token` when the `-weights` image does not exist yet; workarounds in the thread are deleting `.cog/` and `.dockerignore`. Needs Docker plus Replicate's registry to reproduce. Do not build. |
| [chroma #7688](https://github.com/chroma-core/chroma/issues/7688) — hnswlib persists uninitialised heap into `length.bin` | **Wrong repo, and spoken for.** The fix (`calloc` at three `malloc` sites) lives in `chroma-core/hnswlib`, which is not forked here; a commenter asked to be assigned on Sep 8. Do not build from the `chroma` fork. |
| [TransformerEngine #3202](https://github.com/NVIDIA/TransformerEngine/issues/3202) — `multi_tensor_apply` OOB metadata writes | **CUDA-only.** The bug is in a `.cuh` kernel launcher and the Python-side guard (`FusedAdam` skipping `numel()==0`) can only be exercised on a GPU. Cannot reproduce or test here. Deferred. |
| [TransformerEngine #3294](https://github.com/NVIDIA/TransformerEngine/issues/3294) — CPU `QuantizedTensor` recursion | **CUDA-only.** Building the NVFP4 tensor to move to CPU needs a GPU. Maintainers agree it should be fixed; cannot test here. Deferred. |
| [mlx #4538](https://github.com/ml-explore/mlx/issues/4538) / [#4560](https://github.com/ml-explore/mlx/issues/4560) — GPU sort / kernel bugs | **Apple-silicon / CUDA only.** No way to run the affected backends here. Deferred. |
| [huggingface_hub #4987](https://github.com/huggingface/huggingface_hub/issues/4987) — 401s on `/tree` and `/paths-info` with generated JWTs | **Server-side.** Repo-info and file reads succeed with the same token; only listing endpoints reject it, and only on private repos. That is Hub authorization logic, not SDK code. Nothing to fix in this repo. |
| [openai-python #2699](https://github.com/openai/openai-python/issues/2699) — Responses API raises rate-limit errors mid-stream, Chat raises pre-stream | **Deferred.** Needs a live rate-limited Azure endpoint to reproduce, no maintainer response in two months, and no agreed fix direction (where the error should surface is a design call). Not buildable offline with confidence. |
| [tokenizers #2334](https://github.com/huggingface/tokenizers/issues/2334) — `Precompiled` normalizer drops codepoints | **Deferred — two-repo change.** The proposed fix adds `transform_prefix()` to the separate [`spm_precompiled`](https://github.com/huggingface/spm_precompiled) crate and then rewrites `precompiled.rs` to consume it. A tokenizers-only PR cannot fix it, and the longest-prefix algorithm choice has no maintainer direction yet. High value; needs the crate change landed first. |
| [ollama #18595](https://github.com/ollama/ollama/issues/18595) — orphaned blobs never garbage-collected | **Feature request, not a defect.** Asks for auto-GC on `ollama rm` or a new `prune`/`gc` subcommand — a design decision (automatic vs on-demand, safety around in-flight pulls) with no maintainer direction. The scan mislabeled this as a bug. Not a contained fix. |
