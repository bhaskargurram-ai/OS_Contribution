# graphrag #2573 — `community_level` has had no effect since v2.0.0

**Status:** branch pushed (`8f3da67`), PR not yet opened
**Branch:** `bhaskargurram-ai/graphrag` → `fix/community-level-rollup-groups-by-entity`
**Open the PR:** https://github.com/microsoft/graphrag/compare/main...bhaskargurram-ai:graphrag:fix/community-level-rollup-groups-by-entity?expand=1

Repo policy: **do not open as a Draft** (the template says so — drafts notify watchers).
CI requires a semversioner change file in `.semversioner/next-release/` — included. The
PR template has Description / Related Issues / Proposed Changes / Checklist / Additional
Notes sections — filled in below.

Title:

```
Fix community report roll-up to group by entity instead of community title
```

Body (paste as-is):

---

## Description

`read_indexer_reports` rolls the community hierarchy up so that each entity is represented
by the deepest community it belongs to, and `community_level` caps how deep that goes.
Since v2.0.0 the input to that roll-up is `final_communities.explode("entity_ids")`, whose
`title` column holds the *community's* title — not the entity's. Grouping by `title`
therefore kept every community at every level, so parents and children were returned
together and `community_level` no longer changed which reports were selected.

## Related Issues

Fixes #2573.

## Proposed Changes

- Group by `entity_ids` in the roll-up, which is the column that identifies the entity
  after the explode. `max()` then picks the deepest community per entity, and the level cap
  behaves as documented again.
- Add `tests/unit/query/test_indexer_adapters.py`: a two-level hierarchy where community 0
  splits into 1 and 2. With `community_level=1` (or `None`) only `{1, 2}` must survive; with
  `community_level=0` only `{0}`; and each entity must be covered by exactly one selected
  report. A further test guards that dynamic community selection still keeps every report
  under the level.
- Semversioner patch entry.

## Checklist

- [x] I have tested these changes locally.
- [x] I have reviewed the code changes.
- [x] I have updated the documentation (if necessary). — none needed
- [x] I have added appropriate unit tests (if applicable).

## Additional Notes

Without the fix, three of the five new tests fail: the level-1 and level-`None` cases
return `{0, 1, 2}` (the parent leaks through), and each entity is covered by two reports
instead of one. With the fix all five pass; the existing `tests/unit/query` suite is
unaffected (8/8). `ruff check` and `ruff format --check` pass with the project's pinned
ruff.

This change was produced with AI assistance. I reviewed every line, reproduced the
failure, ran the tests, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on `main` | level 1 returns all three communities; entities covered twice |
| New tests fail without fix | 3 of 5 fail (`{0,1,2}` instead of `{1,2}`; double coverage) |
| New tests pass with fix | 5/5 |
| `tests/unit/query` suite | 8/8 pass |
| `ruff check` / `ruff format --check` (ruff 0.16.7, project-pinned) | pass |
| `semversioner add-change -t patch` | `.semversioner/next-release/patch-20260926014029813274.json` |

Environment note: the project's default package index (`packagefeedproxy.microsoft.io`) is
blocked here, so the venv was synced from PyPI with `--default-index`; `uv.lock` was
restored afterwards and is not part of the diff.

Diff is 7 insertions, 1 deletion in `indexer_adapters.py`, plus the test file and the
semversioner entry.
