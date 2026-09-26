# presidio #2256 — IT_FISCAL_CODE unreachable on the default `en` image (docs part)

**Status:** branch pushed (commit `9a0e271`), PR not yet opened
**Branch:** `bhaskargurram-ai/presidio` → `docs/recognizer-registry-conf-override`
**Open the PR:** https://github.com/data-privacy-stack/presidio/compare/main...bhaskargurram-ai:presidio:docs/recognizer-registry-conf-override?expand=1

Note: the issue is labelled good-first-issue and zelihaguven's docs PR #2271 was closed by its
author on Sep 24 ("may revisit later"). Post a claim comment on #2256 before opening the PR.

Title:

```
Document enabling country-specific recognizers via registry override
```

Body (paste as-is):

---

## Change Description

Refs #2256 (docs part). Completes the documentation follow-up that was left open when #2271 was
closed by its author; the code part of the issue landed in #2259.

Several country-specific pattern recognizers (`ItFiscalCodeRecognizer`, `EsNifRecognizer`,
`PlPeselRecognizer`, ...) are registered in `default_recognizers.yaml` for their native language
only. The published `presidio-analyzer` image ships with `supported_languages: [en]`, so on that
image `IT_FISCAL_CODE` is never served: requesting it alone fails with
`No matching recognizers were found to serve the request.`, and requesting it together with a
supported entity returns `200` with the fiscal code silently missing (since #2259 the registry
also logs a deprecation warning for the ignored entity). The recognizers themselves are pattern-
and checksum-based and do not need an Italian NLP model, but there was no documentation of how
to enable them on the default image without rebuilding it, and the maintainers prefer an
explicit override over registering country recognizers for `en` by default (false positives).

### Change

- `docs/analyzer/recognizer_registry_provider.md`: new section "Enabling country-specific
  recognizers on the default English image" — why the recognizers are inactive for `en`, the
  warn-and-preserve behaviour for partially unsupported entity lists (#2259), and a three-step
  `RECOGNIZER_REGISTRY_CONF_FILE` how-to: copy `default_recognizers.yaml` and set the recognizer's
  `supported_languages` to `en` (YAML sample), mount it into the container with `-v`/`-e`, and
  verify with `GET /supportedentities?language=en` and `POST /analyze`. States that the file
  replaces (does not merge with) the default registry, that adding `it` to the registry alone
  makes startup fail with the "supported languages have to be consistent" error, and notes the
  omocodic / invalid-check-character score difference. Wording follows the verification the issue
  author posted on #2271 against `presidio-analyzer:2.2.364`.
- Cross-links to that section from `docs/supported_entities.md` (Italy table),
  `docs/installation.md` (analyzer container env vars), `docs/analyzer/languages.md`,
  `docs/analyzer/filtering_by_country.md` (country filter vs request language) and
  `docs/analyzer/analyzer_engine_provider.md`.

No code or default-registry changes; `CHANGELOG.md` untouched per CONTRIBUTING.md.

### Tests

Docs-only change, no unit tests added.

- `mkdocs build --strict` (mkdocs 1.6.1, mkdocs-material, mkdocstrings-python, mkdocs-jupyter,
  presidio packages installed editable): 23 warnings on this branch, byte-identical to the 23
  warnings on `main` at `4ef07bd` (pre-existing `ahds_integration.md`/`samples/fabric` link
  warnings and griffe/autorefs docstring warnings in `api/analyzer_python.md`); none in the six
  edited pages, so `--strict` exits non-zero on `main` and here for the same pre-existing reasons.
- Rendered site check: the new anchor
  `#enabling-country-specific-recognizers-on-the-default-english-image` exists in the built
  `analyzer/recognizer_registry_provider/index.html`, and all five cross-linking pages resolve
  to it.

## Issue reference

Refs #2256 (documentation part; the warning behaviour was addressed in #2259).

## Checklist

- [x] I have reviewed the [contribution guidelines](https://github.com/data-privacy-stack/presidio/blob/main/CONTRIBUTING.md)
- [x] I agree to follow this project's [Code of Conduct](https://github.com/data-privacy-stack/presidio/blob/main/CODE_OF_CONDUCT.md)
- [x] I confirm that I have the right to submit this contribution and that it does not knowingly contain proprietary or confidential code.
- [ ] My code includes unit tests (docs-only change)
- [x] All unit tests and lint checks pass locally (docs build checked; no code changed)
- [x] My PR contains documentation updates / additions if required

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Read #2256, #2259 (merged as `33586b8` on main), #2271 (closed; used its author-verified
  wording about `en`/`it`, the "replaces, not merges" note and the omocodia / check-character
  score observations) via github.com HTML (api.github.com is blocked).
- Confirmed against the code: `presidio-analyzer/app.py` reads `ANALYZER_CONF_FILE`,
  `NLP_CONF_FILE`, `RECOGNIZER_REGISTRY_CONF_FILE`; `default_recognizers.yaml` registers
  `ItFiscalCodeRecognizer` with `supported_languages: [it]`, `country_code: it`; the warning text
  quoted in the docs matches `recognizer_registry.py` after `33586b8`; `/supportedentities` and
  `/analyze` routes exist in `app.py`.
- `mkdocs build --strict` run on the branch and on a detached worktree of `main`; warning sets
  diffed and found identical (23 each, none in touched files). Anchors verified in built HTML.
- `docs/installation.md` uses CRLF line endings; the edit preserves them (diff is +7 lines).
- Commit `9a0e271`, author Bhaskar Gurram <gurrambhaskar.ai@gmail.com>, 6 files, +130/-0.
- Not done: I could not run the Docker image or the zensical build (`scripts/zensical_build.py`,
  the repo's actual docs pipeline) — the mkdocs build with the same nav/plugins was used instead.
- The commit subject drops the word "config" from the requested wording to stay within 72 chars.
