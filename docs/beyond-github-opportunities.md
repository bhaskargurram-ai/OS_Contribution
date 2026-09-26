# Beyond GitHub: Documentable Contribution Opportunities for an EB-1A Evidence Record (12-month plan)

*Researched 2026-09-26. Every claim below was checked on the linked page on that date (via web scrape). Items marked "(expected)" are inferred from a verified annual cadence; the next-cycle page itself was not yet live. Items that turned out to be closed or non-recurring are listed at the end of each section so you do not waste time on them.*

Profile assumed: strong ML/AI engineer, no academic affiliation, ~10 h/week, ~40 merged/open PRs in major AI repos.

Legend for "Evidence value": how well the artifact maps to EB-1A criteria (authorship of scholarly articles; judging the work of others; original contributions of major significance; membership in associations requiring outstanding achievement; awards). "Effort" is a rough total over the year at 10 h/week.

---

## 1. Reproducibility and replication venues (authorship)

### 1.1 TMLR reproducibility paper → MLRC track at NeurIPS
- **URL:** https://reproml.org/call_for_papers (MLRC), https://jmlr.org/tmlr/ (TMLR), https://neurips.cc/Conferences/2026/CallForReproducibility
- **What you do:** Write a replication/reproducibility study of a paper published in a top ML venue (2025-present), submit it to TMLR (rolling, double-blind, ~9-week decisions, 12-page main text preferred). Ask reviewers/AE for the **Reproducibility Certification** ("papers whose primary purpose is reproduction of other published work... must contribute significant added value through additional baselines, analysis, ablations, or insights"). Then self-nominate to MLRC.
- **Artifact:** Peer-reviewed journal paper in TMLR (ISSN 2835-8856, OpenReview-hosted, DOI-less but indexed; Google Scholar picks up arXiv copy), optional TMLR certification badge, and for MLRC-selected papers a NeurIPS presentation (oral/poster) and listing in MLRC proceedings. MLRC 2026 is "an official track at NeurIPS 2026", first time in MLRC's history.
- **Who:** Anyone; no affiliation needed. TMLR reviews on technical correctness, not novelty ("Are the claims supported by evidence?" and "would some in TMLR's audience be interested?").
- **Deadline / cadence:** MLRC 2026 hard deadline for a TMLR *decision* is **Sept 30, 2026 AOE** (form: https://forms.gle/bvYxagcRjKSmYhUM7); accepted-paper announcement Oct 7, 2026; NeurIPS Dec 6-13, 2026 (Sydney). MLRC 2027 not yet announced; the 2026 eligibility window began June 20, 2025, so a TMLR paper submitted Q4 2026-Q1 2027 should fall in the next window (expected).
- **Assessment:** ~120-200 h for one solid replication. Highest evidence value in this list: a journal publication plus a conference track plus a named certification, all obtainable solo. Do this first.

### 1.2 ReScience C
- **URL:** http://rescience.github.io/ (journal), https://github.com/ReScience/submissions (submit), http://rescience.github.io/faq/
- **What you do:** Re-implement a published computational study from scratch in open-source code (Python preferred; no proprietary tools) and write a short article using the LaTeX template. Submission is a GitHub issue with PDF + YAML metadata + code URL. Open peer review happens in the issue thread. Cannot replicate your own work. You can pick targets from https://github.com/ReScience/call-for-replication.
- **Artifact:** Journal article with a **Zenodo DOI** (e.g., 10.5281/zenodo.18400484 for a Jan 2026 article), archived code, public review thread. Volume 11 (2026) is active. Platinum open access, no fees.
- **Who:** Anyone including students; explicitly "adding to one's publication record".
- **Deadline / cadence:** Rolling; no deadlines.
- **Assessment:** ~80-150 h. Lower prestige than TMLR but a DOI'd, peer-reviewed publication with essentially no gatekeeping on affiliation. Good second replication venue, or the venue for a replication that is too narrow for TMLR.

### 1.3 TMLR certifications as an author (Reproducibility, Featured, J2C)
- **URL:** https://jmlr.org/tmlr/reviewer-guide.html (certification definitions), https://jmlr.org/tmlr/faq.html
- **What you do:** Any TMLR acceptance may also receive a Reproducibility, Featured, Survey (note: TMLR stopped accepting survey papers on Sept 1, 2026), or Journal-to-Conference (J2C) certification; the last gives a presentation slot at NeurIPS/ICML/ICLR via https://neurips.cc/public/JournalToConference. "Expert Reviewer Certification" is awarded to papers authored by highly-rated TMLR reviewers, so reviewing (see 3.4) compounds here.
- **Artifact:** Named badge on the OpenReview page, plus a conference presentation for J2C.
- **Who:** Any TMLR author.
- **Cadence:** Rolling.
- **Assessment:** No extra effort beyond a strong paper; the badge is a documentable "recognition" line item.

### 1.4 NeurIPS Evaluations & Datasets track (reproducibility of evals)
- **URL:** https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets (2026 call; 2027 expected ~April-May 2027)
- **What you do:** MLRC's CFP explicitly routes "replicability and stress-testing of evaluation benchmarks" to MLRC, but "generalizable insights on evaluations" to this track. A benchmark-audit paper (e.g., contamination, label errors, harness variance across a widely used eval) fits.
- **Artifact:** NeurIPS proceedings paper (Datasets & Benchmarks/E&D track papers appear in the main proceedings).
- **Who:** Anyone; NeurIPS "welcomes submissions from all compliant institutions and individuals".
- **Cadence:** Annual; NeurIPS 2027 CFP expected spring 2027 (expected).
- **Assessment:** 200+ h and a competitive review; only pursue if a TMLR replication (1.1) surfaces a genuinely general finding.

### Not viable now (verified)
- **Papers-with-Code style reproduction bounties:** no active bounty program found; the reproducibility signal now lives in TMLR/MLRC and ReScience.
- **AISI evals bounty** (see 2.x): closed (Stage 1 deadline Dec 14, 2024; final Mar 15, 2025); not recurring per the page.

---

## 2. Benchmarks and standards with named contributors

### 2.1 Terminal-Bench (main) — continuous benchmark, named task authors
- **URL:** https://github.com/harbor-framework/terminal-bench (README "Contributing Tasks"), https://www.tbench.ai/news/writing-a-good-terminal-bench-task
- **What you do:** Propose (GitHub Discussions/Discord), then build a hard, programmatically verified CLI task in Harbor format; PR goes through automated checks, LLM judge, human review, "hacker-fixer" adversarial hardening. Task repairs to merged tasks are also accepted. Also open: submit an agent to the leaderboard (see 4.x).
- **Artifact:** Your name (and GitHub) in `task.toml` author metadata and in the README "Task Authors" table alongside ScaleAI, Snorkel, Turing; tagged dataset releases on Harbor Hub (v4.0.0, Aug 26 2026). Terminal-Bench 3.0 promised contributors with "even one accepted task will be acknowledged in the final release", ordered by number of tasks. The Terminal-Bench paper (ICLR 2026, ~90 authors) credited task contributors as co-authors.
- **Who:** Anyone; weekly open contributor meeting Thursdays 9am PT.
- **Cadence:** Continuous ("benchmarks are software"); TB 3.0 merge window closed end of May 2026, TB 4.0 released Aug 28, 2026; new tasks accepted on a rolling basis.
- **Assessment:** 15-40 h per task. Named credit on a benchmark cited in Anthropic/OpenAI model cards; very high evidence-per-hour for an engineer.

### 2.2 Terminal-Bench-Science 0.2 — co-authorship for merged tasks
- **URL:** https://www.terminal-bench-science.ai/contribute, https://github.com/harbor-framework/terminal-bench-science
- **What you do:** Propose a real scientific-computing research workflow (Airtable form), build it in Harbor format, PR through three human review rounds. After one merged task you may join the reviewer pool; strong reviewers become "senior reviewers" with elevated co-authorship.
- **Artifact:** "Each merged task earns one co-authorship point... One point qualifies you for co-authorship on the Terminal-Bench-Science paper" (targeting a high-impact journal) plus listing on the Contributors page. Points carry over between releases. Benchmark featured in the Claude Fable 5.1 and GPT-6 Astra release notes.
- **Who:** "Practicing researchers" preferred, but tasks in applied math/scientific computing/statistics/engineering are open to anyone who can build a verifiable workflow.
- **Deadline:** **PRs for 0.2 open until Oct 5, 2026**; further releases follow the continuous model. Weekly meeting Tuesdays 9am PT; office hours Tue/Wed/Thu.
- **Assessment:** 20-50 h per task. Co-authorship on a lab-cited benchmark paper plus a documentable reviewer role; second-highest priority in this list.

### 2.3 MLCommons working groups (individual membership)
- **URL:** https://mlcommons.org/get-involved/ (WG access table), https://mlcommons.org/community/subscribe/ (subscription form)
- **What you do:** Individuals can join as a free "Observer Member, Individual" (board approval; "Participate in all working groups; Working group chair opportunities") or simply subscribe to the WGs whose access requirement is **None**: Croissant, Datasets, Medical, Automotive, Tiny, Storage, AI Risk & Reliability (AILuminate), Algorithms (AlgoPerf), Chakra, DMLR, Science. MLPerf Training/Inference/Client/Power/Infra/Mobile require Members & Affiliates. Croissant (Wed 9:05am PT weekly) has open workstreams (RAI, Geo, Bio) and a public GitHub (submit your GitHub ID via the form to get commit access).
- **Artifact:** Named WG participation, commit credit in mlcommons repos, potential co-authorship on WG papers/specs (Croissant 1.1 spec, AILuminate benchmark reports), and for MLPerf a public result under your name only if you become a Member (free for individuals but board-approved) since "Affiliates are not allowed to participate in MLCommons benchmarks".
- **Who:** "We welcome academics, individuals and small startups as non-paying members."
- **Cadence:** Rolling; weekly WG calls (calendar on the page).
- **Assessment:** 2-4 h/week sustained. Standards-body membership plus named spec/benchmark contributions; moderate evidence value, high credibility. AlgoPerf: no 2026 competition round announced (last results Aug 2024); treat as WG participation only.

### 2.4 Inspect Evals (UK AISI) — build and register an eval
- **URL:** https://github.com/UKGovernmentBEIS/inspect_evals, registry: https://ukgovernmentbeis.github.io/inspect_evals/register/, guide: https://ukgovernmentbeis.github.io/inspect_evals/contributing/
- **What you do:** **Policy changed:** "We've updated our contribution policy to only accept PRs from pre-approved contributors" (APPROVED_CONTRIBUTORS.md). Two open paths remain: (a) build an eval in your own repo and "share your evaluation by adding a listing" to the registry; (b) file issues with `.eval` logs demonstrating problems in existing evals. Maintained by Generality Labs.
- **Artifact:** Registry listing under your name; issue-driven fixes credited in changelog; potential promotion to approved contributor.
- **Who:** Anyone for the registry/issues; PRs only for approved contributors.
- **Cadence:** Rolling.
- **Assessment:** 20-60 h per eval. Evidence value dropped with the policy change; still worthwhile because the registry is the AISI-branded index of community evals.

### 2.5 lm-evaluation-harness (EleutherAI) and HELM (Stanford CRFM) — new tasks/scenarios
- **URL:** https://github.com/EleutherAI/lm-evaluation-harness (new-task guide in `docs/`), https://crfm.stanford.edu/helm/ and https://crfm-helm.readthedocs.io/
- **What you do:** Contribute a new task/scenario (YAML + Python) with validation against reference numbers; HELM has domain leaderboards (MedHELM etc.) with named scenario authors.
- **Artifact:** Named task in the two most widely used eval harnesses; HELM sub-benchmark papers frequently credit scenario contributors.
- **Who:** Anyone via PR.
- **Cadence:** Rolling.
- **Assessment:** 10-30 h per task. This is closer to "ordinary PRs", so use it only as a stepping stone to a benchmark paper (e.g., an eval you later publish via 1.4 or 4.x).

### 2.6 OpenSSF AI/ML Security Working Group (Linux Foundation)
- **URL:** https://openssf.org/groups/ai-ml-security/, https://github.com/ossf/ai-ml-security
- **What you do:** Join Slack/mailing list, attend the open Zoom meeting, contribute to WG deliverables (vulnerability-disclosure guidance for AI, model-signing, secure-AI guides). Sandbox-level WG; presents quarterly to the OpenSSF TAC.
- **Artifact:** Named contributor to LF/OpenSSF guidance documents; possible WG lead roles.
- **Who:** Anyone (no OpenSSF membership required to participate in WGs).
- **Cadence:** Rolling; regular WG meetings.
- **Assessment:** 1-3 h/week. Moderate evidence value as standards-body participation; better if you author a specific deliverable.

### 2.7 IEEE SA (individual membership) and ISO/IEC JTC 1/SC 42
- **URL:** https://standards.ieee.org/participate/ ("individual or entity/corporate membership"), https://standards.ieee.org/initiatives/autonomous-intelligence-systems/ (AIS; "Individuals and teams are invited to submit proposals"), https://sagroups.ieee.org/ic16-002/related-activities/ (join P7000-series WGs). ISO SC 42: https://www.iso.org/committee/6794475.html (participation is via national bodies; e.g., Canada's SCC mirror committee page https://scc-ccn.ca/get-involved/become-member/join-mirror-committee/mcisoiec-jtc-1sc-42-artificial-intelligence).
- **What you do:** IEEE: buy an individual SA membership, join an open P-series WG (AI ethics/transparency/agentic standards), contribute text and vote. ISO: apply to your national mirror committee (US: INCITS/ANSI; not verified in this pass).
- **Artifact:** Listed WG member / contributor on a published standard; IEEE WG rosters are public.
- **Who:** IEEE SA individual membership is open to anyone (fee-based). ISO depends on national body rules.
- **Cadence:** Rolling.
- **Assessment:** Low hours per month but slow (standards take years); strongest as a "membership in association" line only if the WG requires expertise-based admission. Lower priority than 2.1-2.4.

### 2.8 NIST — AI RMF and ARIA
- **URL:** https://www.nist.gov/itl/ai-risk-management-framework, https://ai-challenges.nist.gov/aria
- **Status verified:** AI RMF 1.0 "is being revised as part of the White House AI Action Plan"; a concept note for a Critical-Infrastructure profile was released Apr 7, 2026; comments go to aiframework@nist.gov. ARIA pilot ran Dec 2024-Jan 2025; page lists no new cycle ("Participant Login: coming soon"; join the mailing list).
- **Assessment:** Public comments are documentable but weak evidence; ARIA has no open round. Low priority; subscribe and watch for the AI RMF 2.0 comment period.

### Not viable now (verified)
- **UK AISI evals/agent-scaffold bounty:** closed (2024-25 cycle only).
- **METR Task Standard:** repo is a format spec (https://github.com/METR/task-standard); no open task-submission or bounty program found. Use the format for your own evals.
- **OpenAI `openai/evals`:** repo still public, but OpenAI's eval effort moved to the API Evals product; no active community eval intake found.
- **LMArena:** open-sourced Arena-Hard-Auto and Arena-Rank code (https://github.com/lmarena); ordinary OSS contribution only, no contributor program.
- **BIG-bench successors:** no open call found.

---

## 3. Peer-review and judging roles obtainable without an institution

### 3.1 JOSS reviewer
- **URL:** https://reviewers.joss.theoj.org/join (sign-up), https://joss.readthedocs.io/en/latest/reviewer_guidelines.html
- **What you do:** Sign up with GitHub and list expertise; editors assign you research-software submissions; review is a public checklist in a GitHub issue (https://github.com/openjournals/joss-reviews), 2-4 weeks first pass, 4-6 weeks total.
- **Artifact:** Public, attributable review threads; reviewer name is recorded in the review issue and the reviewers database. JOSS papers carry DOIs (10.21105/joss.xxxxx).
- **Who:** Anyone with relevant software expertise; no degree required.
- **Cadence:** Rolling.
- **Assessment:** 4-8 h per review. Cleanest documentable "judging the work of others" evidence available to a non-academic; aim for 3-6 reviews/year.

### 3.2 pyOpenSci reviewer (and editor track)
- **URL:** https://www.pyopensci.org/about-peer-review/ (reviewer sign-up form: https://forms.gle/GHfxvmS47nQFDcBM6), editor guide: https://www.pyopensci.org/software-peer-review/how-to/editors-guide.html
- **What you do:** "Review 1-2 packages per year. No prior review experience needed"; all reviews public on GitHub (https://github.com/pyOpenSci/software-submission/issues). Editors serve 1+ year and lead 3-4 reviews; peer-review-lead role is 4-8 h/month. Accepted packages can be fast-tracked to JOSS.
- **Artifact:** Public review record; editor listed on the editorial board page.
- **Who:** Anyone with scientific-Python expertise; reviewer mentorship program exists.
- **Cadence:** Rolling.
- **Assessment:** 5-10 h per review. Editor role after a few reviews is a strong "judging" credential.

### 3.3 ReScience C reviewer
- **URL:** http://rescience.github.io/faq/ ("Become a reviewer by commenting on this issue": https://github.com/ReScience/ReScience/issues/27), board: https://rescience.github.io/board/
- **What you do:** Comment on the issue with your domains/languages; editors assign replications; reviews are public in the submission issue (you must run the code).
- **Artifact:** Named reviewer on public review threads; listed on the reviewers page.
- **Who:** Anyone.
- **Cadence:** Rolling.
- **Assessment:** 6-12 h per review (you re-run code). Good complement to 1.2.

### 3.4 TMLR reviewer (self-nomination)
- **URL:** https://jmlr.org/tmlr/faq.html (reviewer nomination form: https://docs.google.com/forms/d/17_GcSO6GlH421ZcHk6RMSPv8csLwAkUsoWtGp6fHtGk/viewform); also "Volunteer to Review" button on any TMLR submission in OpenReview.
- **What you do:** Join the pool (or ask an AE to vouch); default quota 6 papers/year, 2-week review deadline, open (anonymous) reviews. Highly rated reviewers get the Expert Reviewer Certification on their own papers.
- **Artifact:** OpenReview reviewer record; AEs rate reviews.
- **Who:** The FAQ imposes no formal degree requirement; acceptance is at the EiCs' discretion, and the "Volunteer to Review" route lets you demonstrate quality first. A TMLR publication (1.1) makes acceptance likely.
- **Cadence:** Rolling.
- **Assessment:** 6-10 h per paper. Journal reviewing in the field's main open journal; strong evidence once you have 3+ reviews.

### 3.5 ICLR 2027 reviewer self-nomination (and the reciprocal-review rule)
- **URL:** https://iclr.cc/ (banner: "ICLR 2027 Reviewer Self-Nomination Form" https://docs.google.com/forms/d/e/1FAIpQLSe50IB-kmgf9ELdinthHsCPHV4CCzK17RaS5GHzjXyBHIqupw/viewform), rules: https://iclr.cc/Conferences/2027/AuthorGuidelines
- **What you do:** Self-nominate; qualification is "at least one accepted publication" at ICLR/NeurIPS/ICML/UAI/AISTATS/JMLR/**TMLR**/ACL-family/COLM/CVPR-family/AAAI/KDD/COLT etc. (workshop papers and blog posts do not count). Reviews Nov 5-Dec 16, 2026 for ICLR 2027 (Apr 26-30, 2027, San Francisco).
- **Artifact:** OpenReview reviewer record; ICLR lists reviewers in the program.
- **Who:** Anyone meeting the publication bar. Note NeurIPS PCs reportedly require 2+ first-author top-venue papers (Reddit report, unverified) and ICML 2026 closed self-nominations; **ICLR is the realistic path**, and a TMLR acceptance unlocks it.
- **Cadence:** Annual; ICLR 2028 form expected ~Aug-Sep 2027 (expected).
- **Assessment:** ~20 h/cycle. High evidence value ("judge at a top conference") but gated on 1.1 landing first.

### 3.6 Workshop program committees (2026-27)
- **URL examples verified 2026-09-26:** LatinX in AI ICML/NeurIPS workshops recruit reviewers via open Google Forms (https://x.com/_LXAI); ALVR 2026 workshop "Call for Reviewers" (aggregated at https://scouts.yutori.com/bc343386-69f2-4683-8c16-ea693ade0883); NeurIPS 2026 position-paper track solicited area-chair self-nominations (https://blog.neurips.cc/2026/04/09/...). NeurIPS 2026 workshops (Dec 2026) recruit reviewers Sep-Oct; ICLR 2027 workshops (Apr 2027) recruit Jan-Feb 2027 (expected from cadence).
- **What you do:** Watch workshop sites for "Call for Reviewers" forms and apply; PC membership is usually listed on the workshop site.
- **Artifact:** Named PC member/reviewer on the workshop page.
- **Who:** Typically anyone with relevant expertise; many explicitly welcome industry reviewers.
- **Assessment:** 5-15 h per workshop. Modest but cumulative evidence; target 2-3 workshops in your niche (evals, agents, reproducibility).

### 3.7 Competition/hackathon judging and hosting
- **URL:** Kaggle Community Hackathons (host, "at least 3 judges", up to $10K prizes, free): https://www.kaggle.com/c/about/community-hackathons; lablab.ai regularly seats external judges ("Be the Judge of the next generation of AI innovation!": https://lablab.ai/); NeurIPS 2026 competitions publish organizer/judge lists.
- **What you do:** Host a Kaggle Community Hackathon in your specialty (you and two others are the named judges), or apply to lablab.ai/Kaggle-hosted hackathons as a judge.
- **Artifact:** Public judge listing on the competition page; host credit.
- **Who:** Anyone.
- **Cadence:** Rolling.
- **Assessment:** 10-30 h to host one. Weaker than journal reviewing but documentable "judging" with a public URL.

---

## 4. Competitions and challenges with publishable outcomes

### 4.1 NeurIPS 2026 Competition Track (16 competitions; verified list)
- **URL:** https://blog.neurips.cc/2026/07/28/neurips-2026-competitions-announced/ . Organizers may publish post-competition analyses in the Datasets & Benchmarks track or a dedicated **PMLR volume**; winners typically co-author. NeurIPS 2026 is dual-site (Sydney Dec 6-13; Paris satellite used by some competition workshops).
- Competitions and verified deadlines (three checked in detail):
  - **The Steerability Challenge** (IBM/Tara/NDIF/Cadenza/Berkeley/CUHK): https://steerability.github.io/competition/ — build a steering pipeline reducing dishonesty without capability regressions using the AISteer360 toolkit; **final submission Nov 21, 2026 AoE**; cash prizes; workshop at NeurIPS 2026 (Paris); open to "hobbyists anywhere"; select pipelines merged into the toolkit as community examples. Best fit for an engineer.
  - **Predictive AI Evaluation Competition** (Stanford AIMS): https://aimslab.stanford.edu/competition — predict AI-system correctness on held-out benchmark items; Codabench; **final codebase + technical report Oct 30, 2026 AoE**; technical reports via OpenReview (NeurIPS.cc/2026/Workshop/PAIEC); oral/poster session Dec 11, 2026 Sydney; "open to individuals regardless of affiliation".
  - **AIMO Interpretability Challenge**: https://aimo-interp.github.io/ — classify whether an AIMO-3 model solved a problem robustly vs. spuriously; **final deadline Nov 1, 2026**, technical reports Nov 1-15, peer review Nov 15-30; $12,500 prizes incl. $5,000 write-up prizes "regardless of ranking"; workshop Dec 12, 2026 Paris; leaderboard is small (22 main-track entries on Sep 26) so placing is realistic.
  - Others (see blog for links): Learn2Design 2026, Smart Buildings Challenge, Fusion Equilibrium Challenge, RealPDE, FAIR Universe Weak Lensing, SimulacraBench, AMP Challenge, Speech Accessibility Project Challenge 2, Virtual Embryo Challenge, QuantiPhy (VLM physical reasoning), RoboSynChallenge, RoCo-Spring, Agenthon 2026.
- **Assessment:** 40-100 h per competition. A top-5 finish plus technical report is a publishable, citable outcome (PMLR/NeurIPS workshop) and a documentable award. NeurIPS 2027 call for competition proposals expected ~Mar-May 2027 (2026 proposals were due May 16, 2026) if you want to *organize* one.

### 4.2 ARC Prize 2026 (Kaggle) — three tracks incl. a Paper Track
- **URL:** https://arcprize.org/competitions/2026; Kaggle: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3 , .../arc-prize-2026-arc-agi-2 , .../arc-prize-2026-paper-track
- **What you do:** Submit ARC-AGI-2 or ARC-AGI-3 solutions (entry deadline Oct 26, 2026; ARC-AGI-3 Milestone #2 Sept 30, 2026), then document your approach in the **Paper Track** (writeup ≤1,500 words or PDF + public notebook; **final deadline Nov 9, 2026**; $75K paper prizes + $375K bonus for rubric >4.5/5; judged on accuracy, universality, progress, theory, completeness, novelty). $2M total across tracks; all winning artifacts must be open-sourced.
- **Artifact:** Kaggle writeup with a formal citation ("François Chollet, Greg Kamradt, Mike Knoop, and María Cruz. ARC Prize 2026 - Paper Track... Kaggle"), prize money, and past paper-award winners are listed on arcprize.org.
- **Who:** Anyone.
- **Cadence:** Annual (March launch, Nov close); ARC Prize 2027 expected ~Mar 2027.
- **Assessment:** 60-150 h. Even a non-winning paper-track entry is a public, citable technical report; a paper award is a strong "award" criterion item.

### 4.3 ARC White-Box Estimation Challenge 2026 (Alignment Research Center, on AIcrowd)
- **URL:** https://www.aicrowd.com/challenges/arc-white-box-estimation-challenge-2026
- **What you do:** Write an executable estimator for expected activations of random ReLU MLPs under a FLOP budget (CPU-only, Python + flopscope). Phase 2 live now: **team freeze Oct 2, submissions close Oct 17, algorithmic-contribution write-up Oct 24, 2026** (23:59 UTC); winners Nov 15. $100K Phase-2 prizes incl. $20K "algorithmic contribution" judged on write-up quality; $500-5,000 community-contribution prizes.
- **Artifact:** Public leaderboard rank; PDF technical write-up; winners must open-source code (OSI license, 3 years); companion paper arXiv:2605.05179.
- **Who:** Anyone.
- **Assessment:** 40-80 h in the next three weeks. Good fit for a strong engineer; the write-up prize rewards ideas over rank.

### 4.4 AI Mathematical Olympiad (AIMO) — Progress Prize 3 closed; next round expected
- **URL:** https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3, https://aimoprize.com/
- **Status:** Progress Prize 3 ($2.2M) closed Apr 15, 2026 (entry deadline Apr 8, 2026). Cadence has been annual (Oct/Nov launch: PP2 Oct 17, 2024; PP3 launched Nov 19, 2025), so **Progress Prize 4 is expected ~Nov 2026** (expected). A "Proof Pilot" competition page also exists on Kaggle.
- **Artifact:** Kaggle leaderboard, prizes, and winning solutions are open-sourced and widely cited; AIMO-Interp (4.1) reuses AIMO-3 models.
- **Assessment:** 100+ h; extremely competitive. Consider only if math reasoning is your niche.

### 4.5 SWE-bench / Terminal-Bench leaderboards (submit an agent)
- **URL:** https://www.swebench.com/ (submissions via https://github.com/SWE-bench/experiments), https://www.tbench.ai/ (leaderboard on Harbor Hub; "Leaderboard Integrity Update" Apr 19, 2026 tightened the process; Terminal-Bench Challenges accept solutions via form https://www.tbench.ai/news/terminal-bench-challenges)
- **What you do:** Build/scaffold an agent, run the harness, submit trajectories/logs; entries list the agent and submitting org/individual.
- **Artifact:** Named leaderboard entry (public, dated); citable in a paper.
- **Who:** Anyone with API budget (SWE-bench Verified runs cost ~$0.05-1 per instance per the board).
- **Cadence:** Rolling.
- **Assessment:** 30-80 h plus API cost. A documented leaderboard placement is good supporting evidence, best paired with a write-up (blog track 7.4 or arXiv).

### 4.6 DrivenData / AIcrowd / Kaggle research competitions (general)
- **URL:** https://www.drivendata.org/competitions/ , https://www.aicrowd.com/challenges , https://www.kaggle.com/competitions
- **Status:** DrivenData's DaT Parkinson's Challenge closed Sept 16, 2026; no other open DrivenData competition on Sept 26. AIcrowd's only ongoing challenge is 4.3. Kaggle's open featured/research competitions right now are ARC (4.2); Kaggle also lists "AI4S Open Innovation" community hackathons.
- **Assessment:** Watch pages monthly; DrivenData's NIH/NASA-hosted challenges publish winners with named write-ups.

### 4.7 MLPerf submissions as an individual
- **URL:** https://mlcommons.org/get-involved/
- **Verified:** benchmark submission rights belong to Members ("Benchmark submissions and public results"); "Observer Member, Individual" is free but requires board approval; Affiliates cannot submit. Inference/Training WGs are Members & Affiliates only.
- **Assessment:** Feasible only after board-approved individual membership; hardware/cost heavy. Low priority vs. 4.1-4.3.

---

## 5. Funded or mentored research programs for independent researchers

### 5.1 EleutherAI Summer of Open AI Research (SOAR) — next cycle 2027
- **URL:** https://eleuther.ai/soar/
- **What you do:** 5-week fully online program; work on a mentor-led project (2026 list: SAE/interpretability replications, subliminal learning, agent compliance, IR encoders, astronomy FMs, SVS); "Participants... are credited on work that may result in publication". Several projects target TMLR/NeurIPS ML4PS/workshops; 2025 outputs include EMNLP Findings 2026, ICLR 2026 workshop papers; 2026 outputs already on arXiv (2609.01836, 2609.18605).
- **Who:** "Anyone may apply... A central goal of SOAR is to give people outside academia their first research experience." Explicitly welcomes "Experienced programmers interested in AI research".
- **Cadence (2026 verified):** project proposals May 15; applications May 18-**June 8**; decisions July 5; program July 13-Aug 16. 2027 cycle expected same window (expected). "Applications have closed. Please come back next year!"
- **Assessment:** 6-25 h/week for 5 weeks. Best mentored path to a co-authored paper for a non-academic; aligns perfectly with a replication for 1.1.

### 5.2 SPAR (Supervised Program for Alignment Research) — Spring 2027
- **URL:** https://sparai.org/ (interest form: https://fillout.kairos-project.org/spar-2026-interest)
- **What you do:** Part-time (5-40 h/week), remote, 3-month mentored research with 240+ mentors; Demo Day with prizes ($7,000 last year); "Most projects lead to published papers or preprints with mentee co-authors."
- **Who:** Aspiring AI safety/policy researchers; no affiliation required.
- **Cadence:** Fall 2026 closed; **Spring 2027 applications open around December 2026**.
- **Assessment:** ~10 h/week fits exactly; co-authored preprint/paper plus Demo Day recognition. Apply in December.

### 5.3 MATS (Machine Alignment Theory Scholars) — Summer 2027
- **URL:** https://www.matsprogram.org/apply (notify list: https://www.matsprogram.org/eoi)
- **What you do:** Full-time 12-week in-person/hybrid research with mentors from Anthropic/OpenAI/GDM/Redwood/ARC; $19.2k stipend + $24k compute + housing; 215+ publications produced.
- **Who:** Open; multi-stage (application, coding/reasoning assessments, mentor interviews). No degree required.
- **Cadence:** Winter 2027 closed (Stage 1 closed Sept 6, 2026; program Jan 19-Apr 10, 2027). Summer 2027 applications expected ~Mar-Apr 2027 (expected from prior cycles).
- **Assessment:** Full-time, so only if you can take 3 months off; highest-prestige mentored option.

### 5.4 OpenAI Safety Fellowship (pilot) — next cycle expected
- **URL:** https://openai.com/index/introducing-openai-safety-fellowship/
- **What you do:** External researchers/engineers do safety research with OpenAI mentors, stipend + compute, Berkeley (Constellation) or remote; "expected to produce a substantial research output... paper, benchmark, or dataset".
- **Who:** "We prioritize research ability, technical judgment, and execution over specific credentials."
- **Cadence:** 2026 cohort: applied by May 3, notified July 25, runs **Sept 14, 2026-Feb 5, 2027**. Next call expected ~Apr 2027 if the pilot recurs (expected; not confirmed).
- **Assessment:** Strong if it recurs; put the April 2027 window on your calendar.

### 5.5 Cohere Labs — Open Science Community (open now) and Scholars Program (Fall 2026)
- **URL:** https://cohere.com/research/open-science (apply: https://cohere.com/research/open-science/application), https://cohere.com/research/scholars-program
- **What you do:** Community: join (reviewed weekly), take part in community-led programs (e.g., Expedition Aya, Research Connections) that produce co-authored papers (Global MMLU, Kaleidoscope, M-RewardBench came from the community); community blog credits authors. Scholars: full-time, paid, remote-first research placement; "particularly interested in candidates with strong engineering skills... limited or no experience with published papers".
- **Cadence:** Community: rolling, "applications reviewed on a weekly basis". Scholars: "Status: Closed... Applications are expected to open in Fall 2026" (program evolving to "open calls throughout the year").
- **Assessment:** Community is zero-cost and produces co-authorships at 3-8 h/week; apply now. Scholars only if you can go full-time.

### 5.6 ML Collective (Open Collab)
- **URL:** https://mlcollective.org/community/ , events: https://mlcollective.org/events/research-jam-34/ (Research Jam #34 on Oct 2, 2026)
- **What you do:** Join Discord, present at research jams, join/lead projects; DLCT reading group weekly.
- **Artifact:** Research-jam presentations and collaborations; independent projects have reached workshops/conferences.
- **Who:** Anyone; free.
- **Cadence:** Rolling; jams roughly monthly.
- **Assessment:** Low barrier, low direct evidence; use it to find co-authors for 1.1/4.x.

### 5.7 Anthropic External Researcher Access Program / OpenAI Researcher Access Program (API credits)
- **URL:** https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program (form https://forms.gle/pZYC8f6qYqSKvRWn9); https://openai.com/form/researcher-access-program/ (SMApply https://openai.smapply.org/prog/openai_researcher_access_program/)
- **What you do:** Apply with a safety/alignment (Anthropic) or general research (OpenAI) proposal; Anthropic grants $1,000 API credits, evaluated the first Monday of each month; no nonpublic models. Anthropic also has an AI for Science program (up to $50K credits/project, any researcher eligible).
- **Artifact:** Not evidence in itself, but funds experiments for 1.1/4.x; grant letters are documentable support.
- **Cadence:** Rolling (monthly review at Anthropic).
- **Assessment:** 1-2 h to apply; do it alongside a replication project.

### 5.8 Google Summer of Code 2027 (as contributor or mentor)
- **URL:** https://developers.google.com/open-source/gsoc/timeline (2026 timeline: orgs apply Jan 19-Feb 3; orgs announced Feb 19; contributor applications Mar 16-31; projects announced Apr 30; coding May 25-Aug/Nov). 2027 dates not yet posted; expect the same months.
- **2026 AI orgs (verified via program pages/third-party index):** OpenVINO Toolkit (https://summerofcode.withgoogle.com/programs/2026/organizations/openvino-toolkit), DeepChem, Kornia, Kubeflow, ML4SCI, Metaflow, MLLAM, German Center for Open Source AI, Neuroinformatics Unit, JdeRobot, HumanAI, Julia; Google announced ~30 new AI/ML/security orgs for 2026.
- **Who:** Contributors: 18+, new/beginner to the org (not students-only since 2022). **Mentors** need no affiliation; being a listed GSoC mentor/org admin for an AI org is a documentable leadership role.
- **Assessment:** As a *mentor* for an org where you already have merged PRs (Jan-Feb 2027 org applications): ~3 h/week May-Aug; good "judging/leadership" evidence. As a contributor it is below your level.

### 5.9 Outreachy (December 2026 cohort) — as mentor
- **URL:** https://www.outreachy.org/apply/project-selection/ (Dec 2026-Mar 2027 cohort: initial applications Aug 24-31, 2026; results Oct 5; final applications Nov 2; internship Dec 7, 2026-Mar 8, 2027). Community/mentor application deadline was Sept 11, 2026 for this round; May 2027 round opens ~Feb 2027.
- **Assessment:** Same logic as GSoC: mentor an AI project in the May 2027 round (community sign-up ~Feb 2027, expected).

### 5.10 Grants for independent researchers (rolling; verified on aisafety.com/funding, updated Sept 22, 2026)
- **URL:** https://aisafety.com/funding (index), plus: Mercor AI Safety Fund grants ($5M for independent researchers; rolling), Transformative AI Fund (replaced LTFF; $10k-150k; rolling), Manifund (rolling regrants), BlueDot Rapid Grants (≤$10k; rolling), Corrigibility Research Fund (closes **Oct 31, 2026**), Foresight AI for Science & Safety Nodes (closes **Oct 31, 2026**), Leo Gao microgrants ($10k, minimal application, rolling), Iliad RFPs (rolling). OpenAI teen-development research grants close Oct 6, 2026.
- **Note on SPRIND:** no open AI challenge found in this pass; check https://www.sprind.org/ directly.
- **Assessment:** A $10-50k grant letter for a replication/eval project is documentable funding recognition; 5-10 h per application.

### Not viable now (verified)
- **HF community projects (open-r1 style):** no open call on Sept 26, 2026; HF forum "Community Calls" category is dormant. **Ai2:** expanded HF partnership (Aug 6, 2026) but no open collaboration program; contribution is via OLMo/AstaBench repos.

---

## 6. Security research with public credit

| Program | URL | Pays? | Public credit? | Scope / status (verified) |
|---|---|---|---|---|
| **Anthropic security bug bounty (HackerOne, public)** | https://hackerone.com/anthropic | Yes (third-party-fixed bugs: $100 min) | Yes: HackerOne "Top hackers" board and report disclosures | Public since May 2026 ("Now anyone can report vulnerabilities and get rewarded"); infrastructure/code scope |
| **Anthropic Model Safety Bug Bounty** | https://support.claude.com/en/articles/12119250-model-safety-bug-bounty-program (apply form on page); jailbreaks routed to https://hackerone.com/anthropic-cyber-jailbreak | Yes: up to **$35,000** per novel universal jailbreak | Limited: NDA; you may disclose that you are a selected participant | Ongoing, rolling applications; also periodic classifier-testing campaigns (e.g., up to $25K, ended May 18) |
| **OpenAI Safety Bug Bounty (Bugcrowd)** | https://bugcrowd.com/engagements/openai-safety ; announcement https://openai.com/index/safety-bug-bounty/ (Mar 25, 2026) | Yes | Bugcrowd hall of fame/CrowdStream | Agentic risks incl. prompt injection/exfiltration (≥50% reproducible), proprietary-info leaks, platform integrity; jailbreaks out of scope except periodic private bio-bounties |
| **OpenAI Security Bug Bounty (Bugcrowd)** | https://bugcrowd.com/engagements/openai | Yes | Yes | Classic security |
| **Google AI VRP** | https://bughunters.google.com/about/rules/google-friends/ai-vulnerability-reward-program-rules | Yes: base up to $20K, up to ~$30K with multipliers (flagship: Gemini apps, Search, Workspace) | Yes: Bug Hunters leaderboard/hall of fame | Launched Oct 2025; abuse and AI-specific issues |
| **Microsoft Copilot Bounty** | https://www.microsoft.com/en-us/msrc/bounty-ai | $250-$30,000 | Yes: MSRC acknowledgements | Copilot web/Edge/apps/WhatsApp/Telegram surfaces |
| **Meta Bug Bounty (LLM scope)** | https://bugbounty.meta.com/scope/ | Yes | Yes (thanks page; annual researcher conference) | "reports that demonstrate integral privacy or security issues associated with Meta's large language models" |
| **huntr (Protect AI) — AI/ML OSS** | https://huntr.com/ (FAQ https://huntr.com/new-huntr-faq; policies https://huntr.com/policies) | Yes; up to 10x multiplier when a bug allows reading/writing models or training data; current challenge worth $15,000 | Yes: **CVEs issued** ("wherever we publish a CVE for a report, it will have been reviewed and approved"), public hacktivity and profile | Model-file/format and ML-library vulns (e.g., Keras/transformers `trust_remote_code` findings) |
| **Hugging Face** | Reports via HF security policy/HackerOne (no dedicated public bounty page verified) | Unverified | Typically credited in advisories | Not verified this pass |

- **CVE credit in ML libraries:** huntr is the fastest route (they act as CNA-style publisher for listed AI/ML projects). Direct GHSA advisories in PyTorch/transformers/vLLM also credit reporters by name; that is ordinary but documentable.
- **Assessment:** 20-60 h per finding. A CVE with your name plus a paid bounty is strong, externally verifiable "original contribution" evidence, and huntr's public profile aggregates it. Prioritize huntr (public credit + CVE) and Google/Microsoft (public hall of fame) over Anthropic's model-safety program (NDA limits what you can show).

---

## 7. Writing venues that count

### 7.1 TMLR (journal)
- **URL:** https://jmlr.org/tmlr/ ; policies https://jmlr.org/tmlr/editorial-policies.html
- **Criteria:** claims supported by accurate, convincing, clear evidence; audience interest; no novelty bar; double-blind; rolling; ~9-week decisions; certifications (1.3). Surveys no longer accepted (Sept 1, 2026). Replications explicitly welcome.
- **Assessment:** The core publication venue for this plan.

### 7.2 JMLR MLOSS track
- **URL:** https://jmlr.org/mloss/mloss-info.html
- **Acceptance criteria (verified):** recognised OSI license; cover letter stating MLOSS intent, license, project URL, version under review, and "evidence of an active user community" (active developers, GitHub stars); ≤4-page description in JMLR format; public repo; review criteria: novelty/breadth/significance, openness (issue tracker, forum), comparison to prior implementations, docs (install, tutorials, non-trivial examples, full API), ease of contribution, **tests with coverage "close to 100%"**, CI on multiple platforms, runs on an open-source OS, no proprietary dependencies. Prior publication of the *method* is fine if the *software* is unpublished.
- **Artifact:** JMLR paper (top ML journal) about software you (co-)maintain.
- **Assessment:** 60-120 h if you already lead/maintain a library with real users; otherwise not reachable. If one of your 40 PR targets would list you as a core maintainer, propose an MLOSS paper to them.

### 7.3 JOSS (Journal of Open Source Software)
- **URL:** https://joss.theoj.org/ ; review criteria https://joss.readthedocs.io/en/latest/review_criteria.html
- **Acceptance criteria (verified):** open license; research-software with "obvious research application"; substantial scholarly effort (roughly ≥3 months of work); documentation, tests, CI, community guidelines; paper ≤~1,000 words with required sections (summary, statement of need, references); review is a public GitHub checklist completed in 4-6 weeks.
- **Artifact:** DOI'd, Crossref-indexed paper.
- **Assessment:** 30-60 h if you own a research tool. Pairs with 3.1 (review for JOSS too).

### 7.4 ICLR Blogposts Track
- **URL:** 2026 call https://iclr.cc/Conferences/2026/CallForBlogPosts ; 2027 page not yet posted (https://iclr.cc/Conferences/2027/CallForBlogPosts says "not yet available"); track site https://iclr-blogposts.github.io/
- **What you do:** Double-blind-reviewed post that reviews past work, gives new intuitions, discusses reproducibility, or reports negative results; Markdown/HTML in a unified template; must not advertise your own lab's work; accepted posts get a poster in the main ICLR poster session.
- **Cadence (verified 2026):** submission Dec 7, 2025; notification Feb 21, 2026; camera-ready Mar 15, 2026. **ICLR 2027 cycle expected: submission ~early Dec 2026** for the Apr 26-30, 2027 conference (expected).
- **Artifact:** Published on the ICLR blog site with OpenReview record; counts as a peer-reviewed ICLR track publication (not main-proceedings; ICLR itself says blog posts do not satisfy the reciprocal-reviewer bar).
- **Assessment:** 30-50 h. Ideal outlet for the "what we learned" side of a replication or benchmark audit; good reach.

### 7.5 arXiv + workshop papers
- Workshop CFPs for NeurIPS 2026 workshops close ~late Aug-Sept 2026 (largely passed); **ICLR 2027 workshop deadlines ~Feb 2027**, ICML 2027 workshops ~May-June 2027 (expected). Post every replication/eval report on arXiv (cs.LG) with a Software Heritage or Zenodo archive; MLRC "strongly recommends" Software Heritage archiving.
- **Assessment:** Low cost, immediate DOI-like permanence; necessary but not sufficient.

### 7.6 Distill successors
- **Status verified:** Distill "operated 2016-2021. We are now on an indefinite hiatus" (https://distill.pub/about/). Practical successors: the ICLR Blogposts Track (7.4, which explicitly positions itself relative to Distill), Transformer Circuits (Anthropic-internal, no external submissions), and self-hosted interactive posts cross-listed on arXiv.

---

## Ranked Top 10 (strong engineer, no affiliation, ~10 h/week, ~40 PRs in major AI repos)

1. **TMLR reproducibility paper with Reproducibility Certification, then MLRC/NeurIPS track (1.1, 1.3).** Submit by ~Feb 2027 to fit MLRC 2027's expected window. Unlocks 3.4 and 3.5. Start now; pick a 2025-26 paper whose code you already know from your PR work.
2. **Terminal-Bench-Science task(s) → paper co-authorship + reviewer pool (2.2).** PRs for 0.2 open until **Oct 5, 2026**; one merged task = co-authorship. Immediate and cheap relative to value.
3. **Terminal-Bench main task authorship (2.1).** Rolling; named in README/dataset metadata; your repo experience maps directly.
4. **NeurIPS 2026 competition entry with technical report: Steerability Challenge (Nov 21) or Predictive AI Evaluation (Oct 30) or AIMO-Interp (Nov 1) (4.1).** Pick one; a top-5 + report is publishable and an award.
5. **JOSS + pyOpenSci + ReScience reviewer sign-ups (3.1-3.3).** Sign up this week; 4-6 public reviews over the year is the cleanest "judging" evidence available without an institution.
6. **huntr AI/ML vulnerability research for a CVE with public credit (6).** One or two model-file/library findings = named CVE + bounty.
7. **SPAR Spring 2027 (apps open ~Dec 2026) or EleutherAI SOAR 2027 (apps ~May 18-June 8, 2027) (5.1-5.2).** Mentored co-authored paper on a 10 h/week budget.
8. **ARC Prize 2026 Paper Track (Nov 9, 2026) or ARC White-Box Challenge write-up (Oct 24, 2026) (4.2-4.3).** Citable write-ups with prize upside; pick whichever matches your skills.
9. **ICLR 2027 Blogposts Track (expected early Dec 2026) (7.4)** for the narrative/negative-results half of items 1 or 4.
10. **MLCommons individual membership + Croissant/AIRR working group (2.3)** and **ICLR 2027 reviewer self-nomination once item 1 is accepted (3.5).** Standards-body membership plus top-conference reviewing round out the record.

Calendar of hard dates (next 90 days): Sept 30 (MLRC 2026 TMLR-decision cutoff; ARC-AGI-3 milestone 2), Oct 2 (WhestBench team freeze), Oct 5 (TB-Science 0.2 PR window), Oct 17 (WhestBench close), Oct 24 (WhestBench write-up), Oct 26 (ARC entry deadline), Oct 30 (PAIEC final), Oct 31 (Corrigibility/Foresight grants), Nov 1 (AIMO-Interp), Nov 9 (ARC paper track), Nov 21 (Steerability), ~early Dec (ICLR blogposts, SPAR Spring 2027 opens), Dec 6-13 (NeurIPS 2026).
