# transformers.js #1767 — one rejected session breaks every later web-path session

**Status:** branch pushed (`207b2b3`), PR not yet opened
**Branch:** `bhaskargurram-ai/transformers.js` → `fix/serial-chain-rejection-poisons-later-sessions`
**Open the PR:** https://github.com/huggingface/transformers.js/compare/main...bhaskargurram-ai:transformers.js:fix/serial-chain-rejection-poisons-later-sessions?expand=1

**Policy (`.ai/AGENTS.md`):** "Coordinate on the issue first — if an issue exists, comment on
it before drafting a PR." **Comment on #1767 before opening.** It also requires the full
`pnpm test` to pass; see the environment note in the body.

Title:

```
Stop a rejected session from failing every later web-path session
```

Body (paste as-is):

---

Fixes #1767.

The issue quotes `wasmInitPromise ??= sessionPromise`; that code has since been refactored,
but the defect it describes is still present. On the web path `createInferenceSession`
serializes work through a module-level chain:

```js
webInitChain = webInitChain.then(load)
```

Storing that result back makes the chain itself reject the moment one `load` fails.
`.then(load)` on a rejected promise **skips `load` entirely** and forwards the old
rejection — so a single failed session creation (a missing execution provider, say) broke
every session created after it in the process, and none of them even attempted to load.
`runInferenceSession` chains through `webInferenceChain` the same way, so one failed run
poisoned every later run too.

### Change

Advance the chain on *settlement* instead of success, via a small `serializeOn` helper used
at both sites. Each call returns its own result, so a caller still receives its own
rejection, but the stored chain is `result.catch(() => {})`: it settles when this call
settles and never rejects, so the next call always runs. Call order is unchanged.

### Tests

New `tests/backends/onnx.test.js`. It injects a fake ONNX runtime through
`globalThis[Symbol.for('onnxruntime')]` (which `onnx.js` checks first), so no native
binary is needed, and mocks `env.js` to select the web path since `apis` is frozen.

| test | `main` | this PR |
|---|---|---|
| a failed creation does not fail later creations | ✕ | ✓ |
| creations stay serialized in call order | ✕ | ✓ |
| a failed inference run does not fail later runs | ✕ | ✓ |

The second test fails on `main` because the first test's rejection leaks into module
state — which is the bug itself; its purpose is to guard the serialization invariant the
fix must keep.

`prettier --check` passes on both files. `docs-generate` produces no changes.

### Environment note on the full suite

`onnxruntime-node`'s postinstall downloads a native binary that this environment cannot
fetch, and the model-loading tests download from the Hugging Face Hub, which is also
blocked here. Running the non-model suites (`tests/utils`, `exports`, `types`, `configs`)
gives **89 failed / 288 passed on a clean `main` checkout** and **89 failed / 291 passed
with this change** — the identical 89 failures, all
`ModelFileNotFoundError: Forbidden access to https://huggingface.co/...`, plus my three
new passes. I could not run the model tests; happy to re-run anything if CI shows a
difference.

### AI assistance

This change was produced with AI assistance. I reviewed every line, reproduced the
chain-poisoning behaviour, ran the tests, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Located the live defect (issue's code was refactored) | `webInitChain.then(load)` + `webInferenceChain.then(run)` |
| History checked for a prior fix | none in 200 commits |
| New tests fail on `main` | 3/3 |
| New tests pass with fix | 3/3 |
| Non-model suites vs clean `main` | identical 89 env failures; +3 passes |
| `prettier --check` | pass |
| `docs-generate` | no diff |

Diff is 25 insertions, 2 deletions in `onnx.js`, plus the new test file.
