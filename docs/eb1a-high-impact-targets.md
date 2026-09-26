# High-impact targets: repos and research where contributions become evidence

Written 2026-09-26. This is the "where to go deep" companion to `contribution-strategy.md`.
It is not legal advice; it lists the kinds of artifacts attorneys typically ask for
(merged features in widely used software with usage numbers, authorship, reviewing others'
work, a named role) and where each is realistically obtainable within 6–12 months.

## What the evidence has to look like

| Evidence type | What produces it | Weak form | Strong form |
|---|---|---|---|
| Original contribution of major significance | A merged change many people run | a bug fix | a named feature/spec change in release notes, with download or dependents numbers, or a benchmark fix that changes published results |
| Authorship of scholarly articles | Papers, journal-reviewed software | blog post | JOSS paper as lead author; ReScience C replication; workshop paper citing your implementation |
| Judging the work of others | Peer review, code review with authority | ad-hoc PR comments | JOSS / pyOpenSci reviewer record (public, DOI-linked); CODEOWNERS or reviewer status in a repo; working-group reviewer |
| Leading or critical role | A role others can attest to | many commits | maintainer of a subsystem; working-group contributor named in a spec or benchmark release; program organiser |
| Recognition | Letters from people who depended on the work | thanks in a thread | a maintainer who merged 5+ substantive PRs; a lab whose paper used your fix |

The recurring theme: one coherent body of work in one place beats many scattered patches.
The 41 PRs so far are the entry ticket; the next phase is depth.

## Tier 1 — foundational repos where a merged feature is a durable credential

Each row names a *seam*: a cluster of related open problems that one person can own and
that reads as a single story afterwards. Several were surfaced by this week's scans.

| Repo | Why it counts | Seam to own | Entry points (open, unclaimed as of today) |
|---|---|---|---|
| [jax-ml/jax](https://github.com/jax-ml/jax) | Core numerical library for Google DeepMind and much of ML research; the JAX paper has thousands of citations; CLA-gated but fast to merge small numerics fixes | **`jax.scipy.stats` numerical stability**: six fresh bugs from one audit, all the same shape (cancellation / NaN gradients in tails) | [#40964](https://github.com/jax-ml/jax/issues/40964) pareto support mask, [#40966](https://github.com/jax-ml/jax/issues/40966) laplace.cdf tail gradients, [#40968](https://github.com/jax-ml/jax/issues/40968) zeta custom_jvp primal mismatch, [#40969](https://github.com/jax-ml/jax/issues/40969) poisson.entropy NaN gradients, [#41000](https://github.com/jax-ml/jax/issues/41000) sign() zero derivative for complex — plus #40965 already submitted. Owning all six, then writing a short note "numerically stable log-cdf/sf across jax.scipy.stats", is a named contribution. |
| [onnx/onnx](https://github.com/onnx/onnx) + [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | ONNX is a standard, not just a library; a merged operator-spec clarification makes you an author of the spec every runtime implements | **Quantization spec conformance**: cases where spec, function body, reference and ORT disagree | onnx [#8437](https://github.com/onnx/onnx/issues/8437) (branch ready), onnxruntime [#32719](https://github.com/microsoft/onnxruntime/issues/32719) opset-23 Quantize/DequantizeLinear dtype spec, [#32730](https://github.com/microsoft/onnxruntime/issues/32730) DequantizeLinear 1-D block_size treated per-axis, #32802 (submitted). Join the ONNX Operators SIG meetings (public calendar on onnx.ai) and present the conformance findings. |
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 130k stars, the inference engine behind Ollama, LM Studio, and most local-LLM products | **llama-server OpenAI-compat correctness and hardening**: one reporter filed five server bugs on 2026-09-26 alone | [#29458](https://github.com/ggml-org/llama.cpp/issues/29458) `/infill` accepts out-of-range token ids, [#29456](https://github.com/ggml-org/llama.cpp/issues/29456) uncapped `n_probs`, [#29462](https://github.com/ggml-org/llama.cpp/issues/29462) unbounded grammar repetition allocation (OOM), [#29457](https://github.com/ggml-org/llama.cpp/issues/29457) superlinear grammar build for large enums (DoS) — the last two are security-adjacent and get attention. #29451 submitted. |
| [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) + [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | The two evaluation frameworks whose numbers appear in papers and model cards; a scoring bug you fix changes published results, which is the cleanest "significance" argument available | **Evaluation scoring correctness** | lm-eval [#4230](https://github.com/EleutherAI/lm-evaluation-harness/issues/4230) regex matches "Note: All" as answer A, [#4159](https://github.com/EleutherAI/lm-evaluation-harness/issues/4159) group stderr, [#4084](https://github.com/EleutherAI/lm-evaluation-harness/issues/4084) cache keys omit task config; inspect_ai [#5544](https://github.com/UKGovernmentBEIS/inspect_ai/issues/5544) (labelled accepted). inspect_ai needs the `accepted` label before a PR; comment on the issue first. |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | The most rigorously reviewed ML library; a merged fix there is understood by every reviewer of your record | **Numerical stability of linear models** | [#35029](https://github.com/scikit-learn/scikit-learn/issues/35029) LogisticRegression silently wrong coefficients on off-centred data (label "Numerical Stability"), [#35016](https://github.com/scikit-learn/scikit-learn/issues/35016) Ridge solver reported as Cholesky when SVD used, [#34857](https://github.com/scikit-learn/scikit-learn/issues/34857) QuantileTransformer sparse subsampling. Claim on the issue first; sklearn contributors move fast. |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | The serving engine of record; performance numbers travel | **A quantified performance win** | [#31624](https://github.com/vllm-project/vllm/issues/31624) ModelOpt checkpoints take 5+ min to load. Needs a GPU box; the fix (lazy/parallel weight loading) is CPU-testable, the benchmark is not. |
| [huggingface/transformers](https://github.com/huggingface/transformers) / [diffusers](https://github.com/huggingface/diffusers) | Highest-visibility ML repos; model integrations are documented and credited in release notes | **One named model or pipeline integration** | diffusers [#12257](https://github.com/huggingface/diffusers/issues/12257) Wan 2.2 S2V, [#7219](https://github.com/huggingface/diffusers/issues/7219) SUPIR, [#10043](https://github.com/huggingface/diffusers/issues/10043) F5-TTS (from `contribution-strategy.md`). |
| [pytorch/pytorch](https://github.com/pytorch/pytorch) | The most prestigious credential; slowest to earn | **Distributed / gloo correctness** | [#89197](https://github.com/pytorch/pytorch/issues/89197) collectives fail with BoolTensor on gloo. One clean merge here is worth several elsewhere; do not expect a fast review. |

## Tier 2 — standards bodies and benchmark suites (working-group evidence)

These produce artifacts with your name on a specification or benchmark release, which is a
different category of evidence from a merged PR.

| Body | How to join | What to contribute | Evidence produced |
|---|---|---|---|
| [MLCommons](https://mlcommons.org/get-involved/) — free for individuals and academics | Subscription form with your email; then Discord + working-group calls | AI Safety (AILuminate), [MLPerf Inference](https://github.com/mlcommons/inference), [AlgoPerf](https://github.com/mlcommons/algorithmic-efficiency) (algorithmic efficiency benchmark), [Croissant](https://github.com/mlcommons/croissant) metadata standard | Named contributor on a benchmark or spec release; working-group minutes; co-authorship on the WG's paper |
| [ONNX](https://onnx.ai) SIGs (Operators, Converters, Model Zoo) | Public SIG meetings; LF AI & Data | Operator spec fixes (see Tier 1), converter conformance | Spec authorship; SIG contributor listing |
| [Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol) spec | Open; SEP (spec enhancement proposal) process | A SEP that gets accepted, or reference-SDK conformance work ([python-sdk](https://github.com/modelcontextprotocol/python-sdk) has many `ready for work` P2 bugs) | Named author of an accepted SEP |
| [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions) | Open SIG, weekly call | Attribute definitions for LLM/agent telemetry (what Langfuse, Phoenix, Opik all implement) | Spec authorship in a CNCF project |
| [Stanford CRFM HELM](https://github.com/stanford-crfm/helm) | Open repo, active maintainers | New scenarios/metrics; correctness of existing ones | Contributor on a benchmark whose leaderboard is cited |

## Tier 3 — research collaboration with a co-authorship path

| Programme | Status | What you get |
|---|---|---|
| [EleutherAI Summer of Open AI Research (SOAR)](https://www.eleuther.ai/soar) | Annual, 5 weeks, fully online, applications open each spring (2026 cohort applied in May/June). Between cohorts: the EleutherAI Discord research channels and the lm-eval / gpt-neox repos are the same people | "Participants … are credited on work that may result in publication" (their words). Best co-authorship path for someone without a lab. |
| [Cohere Labs Open Science Community](https://cohere.com/research/open-science/application) | Rolling application; 4,500 members; produced Aya and several papers with community co-authors | Research groups you can join (multilingual, evaluation, efficiency); published papers list community contributors |
| [ML Collective](https://mlcollective.org/community/) | Open Discord; weekly reading group; Research Jams; "the lab" requires bringing one active project | Collaborators and mentorship for an independent project; a venue to present |
| [ReScience C](http://rescience.github.io/) | Rolling; submissions are public GitHub PRs; ML domain welcome | A peer-reviewed, DOI'd **replication paper** with you as first author. Pick a well-cited paper whose code you can reproduce and stress (a natural fit: the evaluation-correctness work above). |
| [Journal of Open Source Software](https://joss.theoj.org/about) | Rolling; "you must be a major contributor to the software" | (a) **Author**: once you own a tool (e.g. a numerically-stable stats module, an eval-correctness checker, a quantization-conformance suite), a JOSS paper gives it a citable DOI. (b) **Reviewer**: [volunteer here](https://reviewers.joss.theoj.org/join); every review is a public GitHub issue with your name — this is the fastest legitimate "judging the work of others" record available. |
| [pyOpenSci](https://www.pyopensci.org/about-peer-review/) | Rolling; "review 1–2 packages per year, no prior experience needed" | Same as JOSS reviewing (packages accepted by pyOpenSci can fast-track to JOSS) |
| [AI2 / allenai](https://github.com/allenai) (OLMo, olmocr, OLMES) | Open repos, Apache, credits external contributors in releases | Fully open training/eval stacks; a substantive fix lands in a release note of a lab that publishes constantly |

## Recommended shape for the next 90 days

1. **Pick two seams, not two repos**: `jax.scipy.stats` stability (6 issues, all CPU,
   fast CI once the CLA is signed) and llama.cpp server hardening (4 issues, two
   security-adjacent). Each becomes one named body of work with a write-up.
2. **Join MLCommons (free) this week** and attend one AlgoPerf or AI Safety working-group
   call; pick one open task from their GitHub. This starts the standards-body clock.
3. **Sign up as a JOSS and pyOpenSci reviewer** now; the first review takes ~4 hours and
   creates a public, dated record.
4. **Apply to Cohere Labs Open Science** (rolling) and set a reminder for EleutherAI SOAR
   next spring.
5. **Plan one ReScience C replication** built on the evaluation-correctness work: pick a
   benchmark paper, reproduce it with lm-eval-harness, and document where scoring bugs
   changed the numbers. That paper is the bridge from "fixed bugs" to "original
   contribution of major significance".

## Explicitly not recommended

- awesome-list PRs (several are open on the account): they carry no weight and can look
  like padding.
- Repos that forbid or heavily restrict AI-assisted contributions without disclosure being
  enough (openai-agents-python is collaborator-only; chonkie's `main` is frozen): the work
  can be silently discarded.
- More breadth. The count is already high enough; reviewers now look for depth.
