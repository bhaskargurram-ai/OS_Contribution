# presidio #2256 — NOT the agglutinative-context issue; nothing pushed

**Status:** no branch pushed, PR not opened — assignment premise does not match the issue or the code
**Branch:** `bhaskargurram-ai/presidio` → `fix/context-enhancer-agglutinative-tokens` (local only, no commits)
**Open the PR:** (none) — see findings below before choosing a target

## Findings

### 1. Issue #2256 is about unsupported entities / IT_FISCAL_CODE, not context enhancement

Actual title: "/analyze silently drops an unsupported entity when other requested entities are
supported; IT_FISCAL_CODE unreachable in the default image" (GiorgioDotcom, Sep 15 2026; labels
analyzer, PII recognizers, good first issue).

- Part 1 (silent drop) is already on `main`: commit `33586b8` "Warn about unsupported requested
  entities while preserving partial results" (PR #2259 by nikolas-sapa, merged Sep 22). Maintainer
  omri374 asked for a warning rather than a 400 for backward compatibility; that is what landed.
- Part 2 (docs: how to enable country pattern recognizers on the `en` image via
  `RECOGNIZER_REGISTRY_CONF_FILE`) was PR #2271 by zelihaguven; the issue author verified it, then
  zelihaguven closed it on Sep 24 ("may revisit later"). So a docs-only follow-up is the only
  remaining unclaimed work on #2256. Maintainer direction from the thread: document the override
  next to the Italian recognizers; do NOT register country recognizers for `en` by default.

### 2. The agglutinative-language issue is #2216, and its premise differs from the assignment

#2216 "Context enhancement is ineffective for agglutinative languages (e.g. Korean): lemma matching
cannot see inside compound words" (juno-junho, Aug 4 2026, open, unlabelled, no PR yet).

- `LemmaContextAwareEnhancer` already has `context_matching_mode="substring"` as the default
  (`presidio-analyzer/presidio_analyzer/context_aware_enhancers/lemma_context_aware_enhancer.py`,
  `_find_supportive_word_in_context`), so a keyword that is a prefix of an inflected token already
  boosts. Verified on main with a hand-built `NlpArtifacts` (spaCy blank `tr`, lemma == token):
  text `"telefonumun numarasi 5551234567"`, context `["telefon"]`, pattern score 0.3 →
  substring mode: 0.65 / supportive word `telefon`; whole_word mode: 0.3.
  Script: `<scratchpad>/presidio-2256/repro.py`.
- The real #2216 failure is Korean-specific: `ko_core_news_sm` lemmas are morpheme-joined strings
  (`급+여계+좌`, `주민등록번+호`) whose `+` boundaries cut through the keyword, so no lemma-level
  prefix or substring rule can recover it. The reporter proposes an opt-in raw-text
  `SubstringContextAwareEnhancer` (±100-char window), has a production-tested implementation on a
  branch, posted a benchmark (16/36 vs 36/36 hits), and is explicitly waiting on the maintainer's
  answers to three design questions (YAML config key? per-language matching mode? new class vs
  fallback inside the lemma enhancer?) before opening the PR. Opening a competing PR would step on
  that contributor.

### 3. Recommendation

- If the goal is #2256: only the docs part is open. It is small (a section in
  `docs/analyzer/recognizer_registry_provider.md` + cross-links; PR #2271's closed diff is a good
  reference, and the issue author's verified wording about `en`/`it` should be used). A claim
  comment on the issue first is appropriate since zelihaguven may "revisit later".
- If the goal is agglutinative context matching: the correct issue is #2216, the assignment's
  prefix-match fix is already covered by the existing `substring` mode, and the issue is
  effectively claimed by its reporter pending maintainer direction. Not recommended as a target.

## Verification performed

- Cloned `bhaskargurram-ai/presidio` (default branch `main`, HEAD `4ef07bd`), configured author,
  created local branch `fix/context-enhancer-agglutinative-tokens` (no commits).
- Installed `presidio-analyzer` editable in a scratch venv (`uv`), ran the reproduction above:
  substring mode boosts the Turkish prefix case on main; no code change needed for that scenario.
- Read #2256, #2216, PR #2271 via github.com (api.github.com is blocked; the GitHub MCP tool
  is scoped to the fork list and refused `data-privacy-stack/presidio`).
- Confirmed CONTRIBUTING.md: do not edit CHANGELOG.md in PRs; PR template requires the checklist
  (contribution guidelines, CoC, rights, unit tests, lint, docs).

## Caveat

No commit or push was made because the described change would be a no-op against current `main`
and would target the wrong issue number. The user will post a claim comment before opening any PR.
