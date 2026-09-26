# browser-use #5817 — user-agent shadow roots are reported as SHADOW(open) in the serialized page state

**Status:** branch pushed (commit `0647ff7`), PR not yet opened
**Branch:** `bhaskargurram-ai/browser-use` → `fix/dom-user-agent-shadow-roots`
**Open the PR:** https://github.com/browser-use/browser-use/compare/main...bhaskargurram-ai:browser-use:fix/dom-user-agent-shadow-roots?expand=1

Title:

```
Do not label user-agent shadow roots as SHADOW(open) in DOM state
```

Body (paste as-is):

---

Fixes #5817.

`DOM.getDocument` with `pierce: true` returns the internal user-agent shadow root of every built-in control (`<input>`, `<textarea>`, `<select>`, `<details>`, `<video>`, `<audio>`, ...) with `shadowRootType: "user-agent"`, next to page-authored roots (`"open"` / `"closed"`). `DOMTreeSerializer.serialize_tree()` only tested for `"closed"` and mapped everything else to `|SHADOW(open)|`, so every native form control in the page state was presented to the model as an open author shadow host. `AgentMessagePrompt._extract_page_statistics()` used the same check, so those controls were also counted in the `N shadow(open)` figure in `<page_stats>`.

The user-agent fragment itself is never serialized (its children have no layout data and the empty fragment is pruned in `_optimize_tree`), so only the prefix and the count were wrong; but a page with a login form reads as a wall of `|SHADOW(open)|` hosts, which invites the agent to look for shadow content that does not exist and adds noise to every step's prompt.

The issue offered two fixes: drop the marker for user-agent roots, or emit a distinct `|SHADOW(user-agent)|`. This PR drops it. `system_prompt.md` documents `|SHADOW(open)|` / `|SHADOW(closed)|` as "shadow DOM elements", which is exactly what remains after the change, and a third token would grow the prompt for information the agent cannot act on. If a `user-agent` marker is preferred instead, it is a one-line change in the new `author_shadow_root_type` property.

### Change

- `browser_use/dom/views.py`: add `SimplifiedNode.author_shadow_root_type`, which reads the host's `shadow_roots` from the CDP data and returns `'open'` / `'closed'` for page-authored roots and `None` for user-agent roots.
- `browser_use/dom/serializer/serializer.py`: replace the two duplicated `has_closed_shadow = any(...)` blocks (SVG branch and element branch) with `_shadow_host_prefix(node)`, which emits `|SHADOW(open)|` / `|SHADOW(closed)|` only for author shadow hosts.
- `browser_use/agent/prompts.py`: the page statistics use the same property, so `shadow(open)` / `shadow(closed)` count only author shadow hosts.

Author shadow roots are unchanged: hosts still get `|SHADOW(open)|` / `|SHADOW(closed)|`, and the `Open Shadow` / `Closed Shadow` / `Shadow End` fragment lines are untouched. Traversal is not changed either: user-agent shadow roots are still walked when the tree is built (`DomService`) and simplified, and are pruned as before because their content has no snapshot data.

| Element on the test page | before | after |
| --- | --- | --- |
| `<input id=name type=text>` | `\|SHADOW(open)\|[4]<input id=name ... />` | `[4]<input id=name ... />` |
| `<select id=choice>` | `\|SHADOW(open)\|*[7]<select id=choice ... />` | `*[7]<select id=choice ... />` |
| `<details id=more>` | `\|SHADOW(open)\|*[35]<details id=more ... />` | `*[35]<details id=more ... />` |
| `<div id=open-host>` + `attachShadow({mode:'open'})` | `\|SHADOW(open)\|[51]<div id=open-host ... />` | unchanged |
| `<div id=closed-host>` + `attachShadow({mode:'closed'})` | `\|SHADOW(closed)\|[55]<div id=closed-host ... />` | unchanged |
| `<page_stats>` shadow counts | 7 shadow(open), 1 shadow(closed) | 1 shadow(open), 1 shadow(closed) |

### Tests

- New `tests/ci/test_dom_user_agent_shadow_roots.py` serves a page with native controls (`input[type=text]`, `input[type=range]`, `textarea`, `select`, `details`, `video controls`) plus an open and a closed `attachShadow` host through `pytest_httpserver`, loads it in headless Chromium via `BrowserSession`, and asserts that no native control line contains `SHADOW(`, that the two author hosts still start with `|SHADOW(open)|` / `|SHADOW(closed)|`, that the open shadow content is still serialized, and that `_extract_page_statistics()` reports exactly one open and one closed shadow host. It fails on `main` (`<name> hosts only a user-agent shadow root: |SHADOW(open)|[4]<input id=name type=text placeholder=Your name />`) and passes on this branch.
- `uv run pytest tests/ci/test_dom_user_agent_shadow_roots.py tests/ci/test_dom_live_input_value.py tests/ci/test_dom_paint_order_serialization.py tests/ci/test_dom_visibility.py` — 12 passed
- `uv run pytest tests/ci/browser/test_dom_serializer.py tests/ci/test_action_blank_page.py` — 7 passed (existing shadow-DOM serializer and page-stats tests)
- `ruff check` / `ruff format --check` / `codespell` on the changed files — clean
- `pyright` on the changed files — 0 errors, 0 warnings

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` with a standalone script (headless Chromium 1194 from `/opt/pw-browsers`, `IN_DOCKER=true` so the sandbox is off when running as root). Raw CDP tree: `input`, `textarea`, `select`, `details`, `video`, `audio`, `option` and the media-control internals all carry `shadow_root_type == 'user-agent'`; `div#host` carries `'open'`. Serialized state on `main` showed `|SHADOW(open)|` on `<input>`, `<input type=range>`, `<input type=file>`, `<audio>`, `<details>`, `<select>`, `<textarea>`; after the fix only `div#host` (`|SHADOW(open)|`) and `div#closed-host` (`|SHADOW(closed)|`) are marked, and the `Open Shadow` / `Shadow End` lines around the author shadow content are unchanged.
- User-agent shadow children: they are built into the `EnhancedDOMTreeNode` tree and walked by `_create_simplified_tree`, but the fragments end up with zero children and are pruned by `_optimize_tree`, so they never reach the LLM string. Not changed in this PR (mentioned in the body).
- New test run before the fix: 1 failed with the assertion quoted in the body. After the fix: passes.
- `pytest tests/ci/test_dom_user_agent_shadow_roots.py tests/ci/test_dom_live_input_value.py tests/ci/test_dom_paint_order_serialization.py tests/ci/test_dom_visibility.py` — 12 passed in 78s.
- `pytest tests/ci/browser/test_dom_serializer.py tests/ci/test_action_blank_page.py` — 7 passed in 42s.
- `ruff check` and `ruff format --check` on the four changed files: clean. `codespell`: clean. `pyright` (1.1.408 from the dev group; pre-commit pins 1.1.404): 0 errors. `ty check` on the changed files: all checks passed.
- Page-stats counts measured on the test page with the pre-fix `browser_use/` checked out: 7 shadow(open) / 1 shadow(closed) (six native controls plus the open author host); with the fix: 1 / 1.
- Pre-commit hooks configured in the repo (`.pre-commit-config.yaml`): yesqa, codespell, pyupgrade (`--py311-plus`), ruff-check (`--fix`), ruff-format, pyright, and the standard pre-commit-hooks (check-ast, check-toml/yaml/json, merge-conflict, symlinks, case-conflict, shebang, mixed-line-ending, BOM, end-of-file-fixer, detect-private-key). The change adds no new dependencies and no new files other than the test.
- Tests in this environment needed `IN_DOCKER=true` (running as root, Chromium refuses to start sandboxed) and the default-extension downloads are blocked by the proxy (warnings only). Neither affects the test itself; in upstream CI the module-scoped `browser_session` fixture from `tests/ci/conftest.py` is used unchanged.
- Design note for the reviewer: the property reads `original_node.shadow_roots` rather than the simplified `children`, because the empty user-agent fragment is pruned before serialization; the old code's fallback to `open` when no fragment child was present is what produced the bug. An author root whose fragment is empty still reports `open`, as before.
- No CHANGELOG file exists in the repo, so no entry was added.

## Caveat

The reporter proposed two fixes (omit the marker for user-agent roots, or emit `|SHADOW(user-agent)|`) and asked the maintainers to choose. This branch implements the omit option; the notes above explain why. Comment on the issue with that choice before opening the PR, or switch to the `user-agent` marker (a small change in `SimplifiedNode.author_shadow_root_type` plus the test assertions) if a maintainer prefers it.
