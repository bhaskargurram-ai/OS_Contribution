# Benchmarks that credit task contributors as named authors (verified 2026-09-26)

Scope: benchmarks, datasets and evaluation suites that are **currently accepting contributed tasks/problems** (GitHub PR or form) **and** state on a live page (or in the paper's author/acknowledgement policy) that contributors get **named credit as paper co-authors or listed authors**. Already known and excluded from the ranked list: Terminal-Bench (harbor-framework/terminal-bench) and Terminal-Bench-Science (harbor-framework/terminal-bench-science, 1 merged task = 1 co-authorship point, PR window to Oct 5, 2026 - policy re-verified today at https://www.terminal-bench-science.ai/contribute: "Each merged task earns one co-authorship point ... One point qualifies you for co-authorship").

Every quote below was read on the live page on 2026-09-26. Effort estimates assume a strong software engineer working alone; "fit" refers to this user's strengths (Python/Rust/C++ numerics, ML library internals, serving, quantization, evaluation correctness; ~40 recent PRs in jax, llama.cpp, onnxruntime, pymilvus, flax).

## Ranked list

| # | Venue | Credit policy (verbatim) | Threshold | Deadline / cadence | Effort per unit | Fit |
|---|-------|--------------------------|-----------|--------------------|-----------------|-----|
| 1 | RSI Bench (Scale Labs) | "Co-authorship on the RSI Bench research paper" + "$2,000 per accepted task" | 1 accepted task | Task submission deadline **Oct 2, 2026**; final 50 tasks Nov 1; "evolving benchmark" | 20-40 h | Excellent (Infra & Systems, Harness Optimization, Evals categories) |
| 2 | OpenRSI-Index (OpenRSI Foundation, UW/TAMU/UCSC) | "Contributors receive authorship" / "all contributors will be included as paper authors" | 1 accepted task + run trajectory | Preview v0.1 released Sep 23, 2026; rolling cycles | 10-40 h (+GPU time unless harness-optimization task) | Excellent (LLM pre/post-training, inference, harness optimization) |
| 3 | SkillsBench (BenchFlow) | "Contributors who merge 1 high-quality task earn co-authorship consideration on the SkillsBench paper and dataset" | 1 merged task | Rolling; current release 1.2, expanding 87 -> 100+ tasks | 10-25 h | Very good (terminal tasks, Docker, pytest verifier; software-engineering domain) |
| 4 | Humanity's Last Exam (CAIS + Scale) | "you will be invited as an author of the paper corresponding to this dataset" | 1 accepted question | Open; "still accepting new questions" | 3-10 h per question (acceptance rate low) | Good (numerics / quantization / ML-internals questions) |
| 5 | CocoaBench (cocoabench/cocoa-agent) | "Contributors with 3 accepted tasks are eligible for co-authorship on the CocoaBench paper" | 3 accepted tasks | Rolling (`cocoabench-head/` continuously merged); COLM cutoff Mar 15, 2026 passed, later tasks go to future releases | 5-15 h per task | Good (GUI + coding tasks with deterministic answers) |
| 6 | ContextEcho (Accenture) | ">= 6 points: Co-authorship on the next dataset release" | 6 points (provider adapter = 4, session = 2-5, annotation = 1) | Rolling "rolling re-authorship" per versioned release | 10-20 h | Good (build a provider adapter for llama.cpp/vLLM/ONNX-served endpoints) |
| 7 | adopt-bench (FirstBatch) | "we offer co-authorship on the methodology paper for contributors who meet any one of these thresholds: accepted task family / accepted suite addition / three or more accepted adapter versions" | 1 task family, or 1 suite addition, or 3 adapter versions | Rolling; "evaluated at paper submission time"; suite refreshes quarterly | 20-40 h | Good (agent adapter + longitudinal coding eval; systems engineering) |
| 8 | HydroTuring (Flood-Lab) | "One merged probe earns co-authorship on the HydroTuring paper. So do five accepted model proposals." | 1 merged probe or 5 accepted model proposals | Rolling; ROADMAP lists unclaimed probes | 15-40 h | Medium (conservation-law numerics; domain reading required) |
| 9 | Every Eval Ever (EvalEval Coalition / HF / EleutherAI) | "for substantive contributions to a release, through co-authorship on the associated release paper ... subsequent releases will follow the same pattern" | Substantive contribution (adapter/converter or data) to next release | Shared-task deadline May 1, 2026 passed; repo active (Aug 2026), next release open | 10-30 h | Good (write a converter/adapter, e.g. llama.cpp perplexity/KL logs -> schema) |
| 10 | Multi-SWE-RL / Multi-SWE-bench (ByteDance Seed) | "Tier 2: New authors of technical reports ... Submit and merge 200 data entries and more than 5 repositories ... Included in our subsequent updated technical report as new author" | 200 merged entries across >5 repos (Tier 1 = acknowledgement only) | Rolling | 60-150 h (pipeline is semi-automated) | Good (C++/Rust repos welcome) but high threshold |
| 11 | AOBench (HPC agent benchmark, MSKazemi) | "Substantial corpus or methodological contributions may warrant co-authorship on a paper that depends on them" | Discretionary ("may") | Rolling; good-first-issues | 10-30 h | Good (HPC/systems tasks) but credit is conditional |
| 12 | Terminal-Bench 3.0 (already known family) | "contributors with even one accepted task will be acknowledged in the final release ... ordered by the number of tasks accepted" | 1 accepted task | Blog says merge window "through the end of May"; CONTRIBUTING.md still says "first-come-first-serve" | 15-40 h | Excellent, but TB3 page promises acknowledgement/ordering, not explicit co-authorship |

## Details per venue

### 1. RSI Bench (Scale Labs)

- Site: https://labs.scale.com/rsi-benchmark/contribute (register: https://labs.scale.com/rsi-benchmark/contribute/interest); repo: https://github.com/scaleapi/rsi-benchmark (CONTRIBUTING.md: https://github.com/scaleapi/rsi-benchmark/blob/main/CONTRIBUTING.md).
- What a contribution is: one Harbor-format task = instructions + strong baseline + container environment + verifier (`val.sh` visible, `test.sh` hidden), continuous reward, fixed compute budget. Ten categories: Architecture, Infra & Systems, Pre-training, Post-training, Multimodal, Data, Evals, Alignment, Harness Optimization, Applied.
- Credit (live page): "What you get. Co-authorship on the RSI Bench research paper. The author position reflects the scope and difficulty of what you contribute. $2,000 per accepted task (for the initial cohort of 50 tasks). Modal compute credits ... Everyone named on a selected task will be included as a co-author on the paper."
- Deadline: "Sep 4 Priority proposal deadline | Sep 18 Target feedback | Oct 2 Task submission deadline | Nov 1 Final 50 tasks selected." FAQ: "There's no cap on how many proposals you can submit." The priority proposal deadline has passed but proposals are still accepted; implementation is "invitation-based. Begin implementation after receiving an email confirmation that your proposal was selected." (CONTRIBUTING.md).
- Review: "Every submitted task goes through review, by the community and the Scale team, before being accepted into the benchmark."
- Effort: 20-40 h after approval (baseline + evaluators + agent run + write-up). Modal credits cover GPU.
- Suggested contribution (Infra & Systems / Harness Optimization): "Speed up llama.cpp or ONNX Runtime decode throughput on a fixed model under an accuracy constraint" - baseline = current kernel/graph, reward = tokens/s subject to KL-divergence-to-fp16 < threshold measured by a hidden evaluator; or an Evals task: "fix a subtly wrong perplexity/accuracy harness so that scores match a reference implementation across quantization formats."

### 2. OpenRSI-Index (OpenRSI Foundation)

- Site: https://index.openrsi.foundation/ ; contribute: https://index.openrsi.foundation/contribute.html ; repo: https://github.com/OpenRSI-Foundation/OpenRSI-Index (CONTRIBUTING.md, task ideas discussions: https://github.com/OpenRSI-Foundation/OpenRSI-Index/discussions/categories/task-ideas). Announcement: https://x.com/OpenRSI/status/2102831770458890626 (Sep 23, 2026).
- What a contribution is: an "RSI task" = a real foundation-model research workflow turned into a Harbor autoresearch environment via the "RSI-Anything" agent pipeline (proposal -> automatic review -> automatic build -> you run the frontier agent on your GPUs and upload the trajectory). Existing tasks include `minference-sparse-prefill`, pre-training optimizer geometry, Qwen-122B RL merge, IsaacLab reward search.
- Credit (live page): "Contributors receive authorship. Open research community will have the benchmark of our own. Every task here is sourced from academic open-source work, and the credit belongs back with our community." X post: "We invite task contributors and compute partners to build this open benchmark with us - all contributors will be included as paper authors." Co-lead's post: "Substantial contributions qualify for co-authorship."
- Cadence: v0.1 preview released 2026-09-23; "This cycle asks for the trajectory as well as the task"; "A proposal-only window may open next cycle."
- Review: automatic review agent (accept / revise / reject) on the GitHub Discussion, then "We review every task for scientific soundness, rigor, and novelty, and independently reproduce it."
- Effort: ~1 h to produce the proposal with the agent, then 10-40 h to validate and run; GPU needed for most tasks but "Tasks that need no GPU are welcome too. Harness optimization is one example."; "No GPUs? ... we will run the trajectory for you on our own compute" if high priority.
- Suggested contribution: an inference-side RSI task in the mould of `minference-sparse-prefill`: e.g. "improve llama.cpp/ggml KV-cache quantization or a JAX/Flax attention kernel on a fixed model under a latency budget", scored by throughput at equal accuracy - a harness-optimization or serving task needs little GPU.

### 3. SkillsBench (BenchFlow)

- Repo: https://github.com/benchflow-ai/skillsbench ; CONTRIBUTING: https://github.com/benchflow-ai/skillsbench/blob/main/CONTRIBUTING.md ; site: https://www.skillsbench.ai/ ; paper: https://arxiv.org/abs/2602.12670.
- What a contribution is: a native BenchFlow `task.md` package: `task.md` (YAML metadata + prompt), `environment/Dockerfile` + bundled inputs, `environment/skills/<skill>/SKILL.md`, `oracle/solve.sh` (human-written reference solution), `verifier/test.sh` + `test_outputs.py` (4-10 pytest checks, reward to `/logs/verifier/reward.txt`). Must run without paid APIs.
- Credit (CONTRIBUTING.md, "Authorship Policy"): "Contributors who merge 1 high-quality task earn co-authorship consideration on the SkillsBench paper and dataset. Quality beats quantity: one excellent task is worth more than many mediocre ones." (Independent review: https://evaluatingevals.substack.com/p/skillsbench-review - "Contributors who get one task merged earn co-authorship on the paper.")
- Cadence: rolling; "The current release is SkillsBench 1.2 ... expanding the 87-task runnable roster toward 100+". Leaderboard recomputed 2026-07-16.
- Review: validate idea in `#task-ideas` on Discord or GitHub Discussions first; PR must pass `bench tasks check`, oracle run with reward 1.0, at least one agent tested with and without skills; PR reviewed against the task-review skill rubric (authenticity, skill quality, verification, instructions, environment).
- Effort: 10-25 h.
- Suggested contribution: a software-engineering task where the skill is real domain procedure, e.g. "quantize a small GGUF model to a mixed-precision scheme meeting a perplexity target using llama.cpp's quantize tooling" (skill = llama.cpp quantization workflow reference), or "diagnose an ONNX Runtime graph-optimization regression from a profile JSON" with a deterministic verifier. Existing repo already has `debug-trl-grpo`, showing ML-internals tasks are welcome.

### 4. Humanity's Last Exam (CAIS + Scale AI)

- Submission form: https://lastexam.ai/submit (renders at https://agi.safe.ai/submit); dashboard: https://agi.safe.ai/dashboard ; repo: https://github.com/centerforaisafety/hle ; paper: Nature 2026 https://www.nature.com/articles/s41586-025-09962-4.
- What a contribution is: one original, closed-ended, expert-level question (exact-match or multiple-choice) + rationale; frontier models are run on it during submission to filter easy questions.
- Credit (live form): "If you submit a challenging question that passes review, your name will be associated with the question and you will be invited as an author of the paper corresponding to this dataset ... People who write more accepted questions will appear earlier in the author list of the paper ... Coauthorship on the paper is optional." The published paper PDF also states "HUMANITY'S LAST EXAM is still accepting new questions. New questions can be submitted at lastexam.ai/submit for co-authorship".
- Deadline: none stated; open now (form live with GPT-6 / Claude Fable 5.1 / Gemini 3.1 Pro as the difficulty filter).
- Review: "AIs Assess Question Difficulty" -> author writes rationale -> "Peer Review ... another round of manual review"; per the Nature paper a two-stage graduate-level reviewer + organizer approval process.
- Effort: 3-10 h per question; many are rejected as too easy or ambiguous.
- Suggested contribution: questions whose answer requires actually reasoning about numerics/ML internals, e.g. exact rounding behaviour of a specific block-quantization format under a stated input, the exact value produced by a named library's fused kernel on an edge case (verifiable, single integer/decimal answer), or a subtle IEEE-754 / Kahan-summation result.

### 5. CocoaBench (CocoaAgent)

- Repo: https://github.com/cocoabench/cocoa-agent ; contribution guide: https://github.com/cocoabench/cocoa-agent/blob/main/contrib/CONTRIBUTING.md ; site: https://cocoabench.github.io/.
- What a contribution is: a task directory (`instruction.md`, `evaluation.md`, `solution.md`, `metadata.json`) created with `contrib/create_task.py`, validated, difficulty-tested with an agent ("At least one agent should fail"), then **encrypted** (`encrypt_tasks.py`) before the PR. Tasks must combine GUI interaction with coding and have an exact-match deterministic answer; no paid APIs.
- Credit: "Contributors with 3 accepted tasks are eligible for co-authorship on the CocoaBench paper, which we plan to submit to a top-tier ML conference ... Particularly interesting or creative tasks may count for more at the discretion of project leads."
- Deadline: "We will consider all tasks submitted by March 15, 2026 for inclusion in our paper submission to COLM 2026. We also warmly welcome additional task contributions after that date ... hope to include new tasks in future releases." `cocoabench-head/` is "community contributions, continuously merged".
- Review: validator script, agent difficulty evidence in `evaluation.md`, PR review with "iterative refinement".
- Effort: 5-15 h per task; 3 tasks for authorship.
- Suggested contribution: tasks such as "open a model card / leaderboard page in the browser, gather quantization configs, then write code to compute the exact memory footprint / KL for a given GGUF layout"; "from the ONNX Runtime release notes UI, identify the commit that changed an op's numerics and reproduce the delta in code".

### 6. ContextEcho (Accenture)

- Repo: https://github.com/Accenture/ContextEcho ; CONTRIBUTING: https://github.com/Accenture/ContextEcho/blob/main/CONTRIBUTING.md ; paper arXiv:2605.24279.
- What a contribution is: a "living benchmark" for persona drift in long agentic-coding sessions. Contribution types with points: donate a qualifying session (2-5), build a provider adapter (4, "Wire a new chat-completions API target into the harness, with a parity check"), annotate a session (1), engineering/analysis (1-4, "Counts toward authorship only with meaningful effort (~15+ hours)").
- Credit: "Total points >= 6: Co-authorship on the next dataset release (e.g. the v2 / living-benchmark paper). Author order is set by point total plus intangible contributions." "rolling re-authorship model: each versioned release (v2, v3, ...) invites the contributors who cleared the threshold for that release as authors."
- Cadence: rolling; credit applies to the next release, never a paper under review.
- Review: "Points are awarded only after your contribution is reviewed and merged."
- Effort: adapter (4 pts) ~10 h + one donated session (2 pts) = threshold in ~10-20 h.
- Suggested contribution: a provider adapter for a llama.cpp `llama-server` / vLLM / ONNX-Runtime-GenAI OpenAI-compatible endpoint with the required parity check, plus a donated session.

### 7. adopt-bench (FirstBatch)

- Repo: https://github.com/firstbatchxyz/adopt-bench ; CONTRIBUTING ("Author-incentive policy"): https://github.com/firstbatchxyz/adopt-bench/blob/main/CONTRIBUTING.md ; task-family guide: https://github.com/firstbatchxyz/adopt-bench/blob/main/docs/contributing-tasks.md.
- What a contribution is: longitudinal evaluation of coding agents inside a simulated team. Three authorship routes: (1) a new task family (plugin exposing `load_instance(schedule_id, variant_id)` with an evaluator + at least one fitted schedule), (2) a suite addition (new repo mirrored into a published suite bundle), (3) three or more accepted adapter versions (agent adapters pinned to a leaderboard suite).
- Credit: "we offer co-authorship on the methodology paper for contributors who meet any one of these thresholds ... Threshold is evaluated at paper submission time. Maintainers retain the right to decline if the scientific contribution doesn't meet venue standards."
- Cadence: rolling; v1.0.0 OSS-readiness milestone shipped; suite refreshes quarterly. Apache-2.0, DCO sign-off required.
- Review: PR review, canary linter, tests, one logical change per PR.
- Effort: 20-40 h for a task family or suite addition.
- Suggested contribution: a suite addition using a numerics-heavy OSS repo the user knows (e.g. a pymilvus or onnxruntime sub-project), or a task family that scores "does the agent reuse the codebase's existing numerics helpers instead of re-implementing them" (an "organicity" axis).

### 8. HydroTuring (Flood-Lab)

- Repo: https://github.com/Flood-Lab/HydroTuring ; CONTRIBUTING (Credit section): https://github.com/Flood-Lab/HydroTuring/blob/main/CONTRIBUTING.md#credit ; ROADMAP of wanted probes: https://github.com/Flood-Lab/HydroTuring/blob/main/ROADMAP.md ; site: https://flood-lab.github.io/HydroTuring/.
- What a contribution is: a "probe" = a conservation-law test (mass/energy/momentum closure, invariance, counterfactual) applied to AI hydrologic models, packaged with `probe.yaml` (authors, affiliation, ORCID), passing the acceptance gate; or a model proposal via issue form.
- Credit: "One merged probe earns co-authorship on the HydroTuring paper. So do five accepted model proposals." "Author order will be settled before submission and circulated to every contributor for agreement." Doc fixes/harness work "do not by themselves earn authorship".
- Cadence: rolling; unclaimed probes on ROADMAP today: `mass/routing-network-closure` (standard), `energy/snowpack-cold-content` (hard).
- Review: acceptance gate + CI (`tests/test_docs_in_sync.py` checks author metadata).
- Effort: 15-40 h; requires reading the physics, but the code is numerical-invariance testing.
- Suggested contribution: claim `mass/routing-network-closure` (network-level mass conservation of routed flow), which is essentially a numerical closure/telescoping-sum test - well within reach for someone who writes numerics test suites.

### 9. Every Eval Ever (EvalEval Coalition)

- Repo: https://github.com/evaleval/every_eval_ever ; shared-task page: https://evalevalai.com/events/shared-task-every-eval-ever/ ; paper: https://arxiv.org/abs/2606.14516 (48 authors incl. shared-task contributors); datastore: https://huggingface.co/datasets/evaleval/EEE_datastore.
- What a contribution is: converters/adapters from eval harness logs or leaderboards into the EEE JSON schema, or converted result data (Track 1 public data, Track 2 proprietary data).
- Credit: paper App. E.5 (Governance Card): "Contributors are acknowledged in three ways: through git commit history, through the contributor list maintained in the repository, and, for substantive contributions to a release, through co-authorship on the associated release paper. The first such instance is the present submission, organized as a shared task; subsequent releases will follow the same pattern with criteria documented in the contributor guide." Shared-task page: "Qualifying contributors will be invited to join the paper write-up as co-authors."
- Deadline: the ACL 2026 shared task closed May 1, 2026 (workshop July 7, 2026); the repo is active (adapter PRs merged Aug 2026) and the governance card commits to the same pattern for subsequent releases, but the current CONTRIBUTING.md does not yet spell out the next release's criteria - confirm with the organizers (join@evalevalai.com) before investing.
- Review: schema validation runs automatically on every submission via HF Jobs; PR review by maintainers.
- Effort: 10-30 h for an adapter.
- Suggested contribution: an adapter for llama.cpp `llama-perplexity` / KL-divergence outputs and for ONNX Runtime GenAI accuracy logs, so quantized-model evaluations enter the datastore with generation settings recorded.

### 10. Multi-SWE-RL / Multi-SWE-bench (ByteDance Seed)

- Repo: https://github.com/multi-swe-bench/multi-swe-bench ; incentive plan: https://github.com/multi-swe-bench/multi-swe-bench/blob/main/docs/contribution-incentive-plan.md ; demo: https://github.com/multi-swe-bench/multi-swe-bench/blob/main/docs/contribution-demo.md ; HF org: https://huggingface.co/Multi-SWE-RL.
- What a contribution is: validated SWE task instances (issue + PR + Dockerised test environment) for repos in C/C++/Rust/Go/Java/TS/JS etc., uploaded to the dated data folder for the language.
- Credit: "Tier 1: Community Contributor ... Your name(Name you provided/Github Username) will also be mentioned in the acknowledgements of our subsequent updated technical report. Tier 2: New authors of technical reports - Requirement: Submit and merge 200 data entries and more than 5 repositories - Reward: Included in our subsequent updated technical report as new author." "Authors are listed alphabetically, with core maintainers noted separately."
- Cadence: rolling; contributions tracked per GitHub/HF account on a public dashboard.
- Review: "All contributions undergo peer review by community moderators."
- Effort: high (200 merged entries); the build pipeline is scripted, so a batch from 5-6 repos the user knows (llama.cpp, onnxruntime, milvus, ggml, etc.) is feasible in 60-150 h.
- Suggested contribution: C++/Rust instances from llama.cpp, onnxruntime, milvus and related repos the user already tracks.

### 11. AOBench (agents operating HPC systems)

- Repo: https://github.com/MSKazemi/aobench ; CONTRIBUTING: https://github.com/MSKazemi/aobench/blob/main/CONTRIBUTING.md ; recognition policy: https://github.com/MSKazemi/aobench/blob/main/AUTHORS.md#recognition-policy ; docs: https://mskazemi.com/aobench/.
- What a contribution is: task JSON specs in `benchmark/tasks/specs/` referencing an environment bundle with a verified gold answer; environments; corpus.
- Credit: "Substantial corpus or methodological contributions may warrant co-authorship on a paper that depends on them. If you believe that applies to your work, say so." Every merged contribution is listed in AUTHORS.md and release notes.
- Cadence: rolling; Zenodo DOI releases; good-first-issues.
- Effort: 10-30 h. Credit is discretionary, so agree scope with the maintainer first.
- Suggested contribution: an environment + task set around GPU-node diagnostics (NCCL/CUDA/quantized-inference serving on Slurm) - squarely in the user's systems experience.

### 12. Terminal-Bench 3.0 (family already known)

- Call: https://www.tbench.ai/news/tb3-contribution-call ; CONTRIBUTING: https://github.com/harbor-framework/terminal-bench/blob/main/CONTRIBUTING.md.
- Credit (live): "contributors with even one accepted task will be acknowledged in the final release. Task contributors - organizations and individuals - will be ordered by the number of tasks accepted into the dataset." CONTRIBUTING.md: "We will acknowledge all contributors whose tasks make it into a release by adding them to the contributors page on the website and readme." Note: this is acknowledgement/ordering language, not an explicit co-authorship promise like TB-Science; the TB 2.0 paper did credit task contributors as authors, so ask maintainers in `#tb-3`.
- Deadline: blog says the merge window is "open now through the end of May"; CONTRIBUTING.md still processes tasks "first-come-first-serve" - confirm on Discord whether TB3 is still merging.

## Checked and NOT qualifying (one line each)

- SciCode (github.com/scicode-bench/SciCode): no contribution path; fixed author list.
- SciCode-Verified: repo README not reachable / no call.
- LAB-Bench / BixBench (FutureHouse): questions written by authors and contracted experts; no open submission.
- CritPt (critpt.com, github.com/CritPt-Benchmark/CritPt): closed set of 71 challenges by 50+ physicists; contact-only.
- FrontierMath / Open Problems / Erdos (epoch.ai/frontiermath): problems commissioned from paid mathematicians; no open submission page; no authorship statement.
- Soohak (arXiv 2605.09063): contributors could choose authorship or pay, but the submission system is closed ("full collection ... open-sourced in late 2026").
- Humanity's Last Exam "round 2": no separate round exists; the original HLE form is simply still open (qualifies above).
- ARC-AGI-3 (arcprize.org/arc-agi/3): environment developers are named only in the paper acknowledgements; no open game-contribution path (competition is for agents).
- SWE-bench Multimodal / SWE-bench Pro / SWE-Gym / SWE-rebench / SWE-bench-Live: accept code PRs (SWE-bench-Live "welcome[s] external collaborators to help us create more SWE tasks each month") but no credit policy stated.
- LiveCodeBench, BigCodeBench, Aider polyglot, CodeContests, HumanEval-V, HumanEval-XL, Omni-MATH, MMLU-Pro, WildBench, Arena-Hard, AgentBench, ChatBench, BBEH: closed datasets; only model results / leaderboard submissions accepted.
- tau2-bench: welcomes domains but Recognition = "Added to the project's contributor list; Mentioned in release notes".
- TheAgentCompany, MLE-bench, PaperBench/frontier-evals (OpenAI), RE-Bench (METR/ai-rd-tasks), METR public-tasks, GAIA2/ARE (Meta), BrowseComp, SimpleQA (simple-evals), HealthBench, GPQA, Vending-Bench, OSWorld/OSWorld-Verified, WebArena, AppWorld, ScienceAgentBench, DiscoveryBench, CORE-Bench, ResearchCodeBench, SciReplicate, Paper2Code, CVE-bench, Cybench, BountyBench, AgentDojo, InjecAgent: no task-contribution call with credit (code PRs or results only).
- HELM / MedHELM (medhelm.org, github.com/PacificAI/medhelm): scenario contributions welcome via PR, but no authorship policy on site or CONTRIBUTING.md.
- BFCL (gorilla/berkeley-function-call-leaderboard): CONTRIBUTING.md is about adding models; no task-credit policy.
- LiveBench: docs/CONTRIBUTING.md covers bugs, code and model submissions only.
- EleutherAI lm-evaluation-harness: new tasks accepted via PR (docs/new_task_guide.md) but no authorship policy.
- Inspect Evals (UK AISI): "only accept PRs from pre-approved contributors"; new evals go through the Register / Generality Labs template with GitHub-handle credit only.
- Open LLM Leaderboard: retired; HF "community benchmarks": no such program with authorship found.
- MTEB / MMTEB: adding tasks via PR is documented (docs.mteb.org/contributing/adding_a_dataset/) but the MMTEB co-authorship points round is over; no current authorship statement.
- Reasoning Gym, TextArena, BALROG, MCPMark, Toolathlon, AlgoTune ("Adding New Tasks"), GSO, KernelBench, BackendBench, GPU MODE reference-kernels ("Contributing New Problems"), MLGym, AstaBench, HAL, OpenAI evals: accept new tasks/problems by PR but state no authorship credit.
- Kaggle AIMO (Progress Prize 3 / Proof Pilot): problems are written by a commissioned "international team of problem composers"; no open call.
- PutnamBench, miniF2F successors: closed formalization sets; PutnamBench asks people not to submit proofs.
- Lean mathlib: author credit is the collective "The mathlib Community"; Formal Conjectures (google-deepmind/formal-conjectures): open PRs welcome, but the paper has 11 fixed authors and the repo cites "The Formal Conjectures Authors" collectively; Equational Theories Project: contributors were authors but the project is finished (paper WIP).
- BIG-bench, Inverse Scaling Prize, BIG-Bench Extra Hard: closed (2022/2025).
- FrontisAI/OpenRSI (different project from OpenRSI-Index): welcomes issues/PRs; no authorship statement.
- SEACrowd SEA-VL Phase 2: offered co-authorship but is Southeast-Asian vision-language data collection, outside this user's scope.

## Method note

Live pages were fetched on 2026-09-26 via Firecrawl (non-GitHub sites) and raw.githubusercontent.com (README/CONTRIBUTING files), plus GitHub code search for "co-authorship"/"merged task"/"accepted tasks" in CONTRIBUTING.md and README.md files. Quotes are verbatim from those fetches. Repositories whose credit policy is only in a paper appendix (Every Eval Ever) or a social post (OpenRSI) are flagged as such above.
