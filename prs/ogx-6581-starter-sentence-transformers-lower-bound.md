# ogx #6581 — starter extra has no lower bound on `sentence-transformers`, so v1.0.3 installs 0.2.3 and embeddings raise TypeError

**Status:** branch pushed (commit `b5e1d1d`), PR not yet opened
**Branch:** `bhaskargurram-ai/ogx` → `fix/starter-sentence-transformers-lower-bound`
**Open the PR:** https://github.com/ogx-ai/ogx/compare/main...bhaskargurram-ai:ogx:fix/starter-sentence-transformers-lower-bound?expand=1

Title:

```
fix(deps): add sentence-transformers floor to inline provider pip_packages
```

Body (paste as-is):

---

# What does this PR do?

Fixes #6581.

The inline `sentence-transformers` provider spec in `src/ogx/providers/registry/inference.py` (and the `BUILTIN_DEPS` list next to it) declared `"sentence-transformers"` with no version constraint. That list is what `ogx stack build`, `ogx stack list-deps`, `print_pip_install_help()` and the "missing dependencies" hint printed by `ogx stack lets-go` hand to pip/uv. With no floor, the resolver is free to satisfy the requirement with any release, and under some resolver inputs (the reporter hit it on v1.0.3) it picks `sentence-transformers==0.2.3` (2019).

The provider loads models with `SentenceTransformer(model, trust_remote_code=trust_remote_code)` and encodes with `encode(input_list, show_progress_bar=False)`. `trust_remote_code=` only exists on the constructor from sentence-transformers 2.3.0 onward (0.2.3's signature is `__init__(model_name_or_path=None, modules=None, device=None)`), so loading the embedding model raises `TypeError: SentenceTransformer.__init__() got an unexpected keyword argument 'trust_remote_code'` on every embeddings request.

`main` already carries `sentence-transformers>=6.0.0` in the `starter` extra of `pyproject.toml` (#6592), but the registry entry was never brought in line, and `.github/scripts/update_registry_deps.py` (run by the dependabot-constraints workflow) only rewrites entries that *already* have a `>=` floor, so the drift could not be repaired automatically.

### Change

- `src/ogx/providers/registry/inference.py`: declare `"sentence-transformers>=6.0.0"` in the `inline::sentence-transformers` `pip_packages` and in `BUILTIN_DEPS`, with a comment explaining the floor. The provider's own API needs `>=2.3.0` (`trust_remote_code=` landed in 2.3.0), but the project constrains `transformers>=5.0.0` and only sentence-transformers 6.x supports transformers 5 (5.6.0 still pins `transformers<6,>=4.41` and breaks on `HybridCache` imports with 5.x; 6.0.0 requires `transformers<6,>=5`), so the registry floor is set to match the `starter` extra rather than the bare API minimum. Keeping the two identical also means the dependabot sync script will now maintain the registry entry too.
- No `pyproject.toml` / `uv.lock` change: the extra already had the floor, `uv lock --check` passes unchanged, and `provider_codegen.py` / `distro_codegen.py` do not render `pip_packages` so no generated docs change.

| | before | after |
|---|---|---|
| `ogx stack list-deps` / `lets-go` hint for the provider | `sentence-transformers` (any version, 0.2.3 admissible) | `sentence-transformers>=6.0.0` |
| `pip install ogx[starter]` | `>=6.0.0` (already, since #6592) | unchanged |
| `SentenceTransformer(model, trust_remote_code=...)` on the resolved version | `TypeError` on 0.2.3 | supported (added in 2.3.0) |

### Tests

Added `tests/unit/providers/inference/test_sentence_transformers_registry_deps.py`:

- `test_provider_pip_packages_declare_sentence_transformers_floor` — the `inline::sentence-transformers` spec's `sentence-transformers` entry has a `>=` floor equal to the one in the `starter` extra of `pyproject.toml`.
- `test_builtin_deps_declare_sentence_transformers_floor` — same for `BUILTIN_DEPS`.

Both fail on `main` (`AssertionError: sentence-transformers must declare a >= lower bound ..., got <Requirement('sentence-transformers')>`) and pass on this branch.

## Test Plan

```
uv run pytest -q tests/unit/providers/inference/test_sentence_transformers_registry_deps.py
# main:        2 failed
# this branch: 2 passed

uv run pytest -q tests/unit/test_update_registry_deps.py tests/unit/distribution/test_list_deps_output.py \
    tests/unit/cli/test_stack_utils.py tests/unit/providers/test_configs.py
# 37 passed

ruff (v0.12.2, the pre-commit pin) check + format --check on the two changed files: clean
python scripts/provider_codegen.py && python scripts/distro_codegen.py: no diff from this change
uv lock --check: passes, lockfile unchanged
```

Reproduction of the failure mode (weight-free, since `download.pytorch.org` is not reachable from my sandbox): loaded the `SentenceTransformer` class from the `sentence-transformers==0.2.3` sdist with `torch`/`pytorch_transformers` stubbed and invoked it exactly as `_load_model()` in the provider does:

```
0.2.3 __init__ signature: (self, model_name_or_path: str = None, modules: Iterable[object] = None, device: str = None)
0.2.3 encode signature  : (self, sentences: List[str], batch_size: int = 8, show_progress_bar: bool = None) -> List[numpy.ndarray]
TypeError: SentenceTransformer.__init__() got an unexpected keyword argument 'trust_remote_code'
```

Signature check across released wheels/sdists: `trust_remote_code` is absent from `SentenceTransformer.__init__` in 0.2.3 and 2.2.2, present from 2.3.0, and present in 6.0.0 (`sentence_transformers/sentence_transformer/model.py`, alongside `encode(..., show_progress_bar=...)`).

Backport note: the reporter is on v1.0.3. On that line `pyproject.toml`'s `starter` extra also lacks the floor (it was added to `main` in #6592), so a backport to the 1.0.x release branch should carry both the registry change here and the `starter` extra floor.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Clone of `bhaskargurram-ai/ogx` (default branch `main`, HEAD `5ad585a`); branch `fix/starter-sentence-transformers-lower-bound`; commit `b5e1d1d` authored by Bhaskar Gurram; pushed after `add_repo`/`register_repo_root` (first push got the expected 403).
- Grepped every declaration of the dependency: `pyproject.toml` (`starter` extra, already `>=6.0.0` since #6592 on `main`), `src/ogx/providers/registry/inference.py` (`pip_packages` and `BUILTIN_DEPS`, both unbounded — fixed here). No `requirements*.txt`, distribution `build.yaml`, or Containerfile pins the package; `docs/docs/providers/inference/inline_sentence-transformers.mdx` does not render `pip_packages`.
- Consumers of `pip_packages` confirmed: `src/ogx/core/build.py::get_provider_dependencies`, `src/ogx/cli/stack/_list_deps.py`, `src/ogx/cli/stack/lets_go.py` (missing-deps install hint). `BUILTIN_DEPS` has no other references in the repo; updated for consistency.
- Floor determination from real package metadata/sources (`pip download --no-deps`): 0.2.3 sdist, 2.2.2 sdist, 2.3.0 wheel, 5.6.0 wheel, 6.0.0 wheel. `trust_remote_code` first appears in 2.3.0; `show_progress_bar` already exists in 0.2.3 (so the kwarg on `encode()` is not the failing one — the constructor is). 5.6.0 requires `transformers<6,>=4.41`; 6.0.0 requires `transformers<6,>=5` and `torch>=2.2`; repo constrains `transformers>=5.0.0`.
- New unit test: 2 failed on `origin/main` (run in a throwaway worktree with `PYTHONPATH` pointed at its `src`), 2 passed on the branch.
- Neighbouring tests: `tests/unit/test_update_registry_deps.py`, `tests/unit/distribution/test_list_deps_output.py`, `tests/unit/cli/test_stack_utils.py`, `tests/unit/providers/test_configs.py` — 37 passed.
- `uvx ruff@0.12.2 check` and `format --check` on both changed files: "All checks passed!", "2 files already formatted".
- `scripts/provider_codegen.py` and `scripts/distro_codegen.py` executed: only an unrelated, environment-dependent diff in `docs/docs/providers/inference/remote_bedrock.mdx` (AWS_* env vars set in the sandbox; the pre-commit hook runs the script under `env -i`), reverted and not committed.
- `uv lock --check`: "Resolved 409 packages", exit 0, `uv.lock` untouched (pyproject unchanged).
- Could not install real `torch` (`download.pytorch.org` is policy-denied by the sandbox proxy; PyPI torch pulls CUDA wheels far beyond the disk budget), so the end-to-end all-MiniLM-L6-v2 encode was not run; the failure was reproduced with the real 0.2.3 class and a stubbed torch, and the fixed floor was verified by signature inspection of the 6.0.0 wheel.
- No `release-1.0.x` (or any non-`main`) branch exists on the fork; the PR targets `main` and the body notes the 1.0.x backport needs the `pyproject.toml` floor as well.
- No CHANGELOG entry: `RELEASE_NOTES.md` is written per release, not per PR. CONTRIBUTING.md does not forbid AI-assisted PRs.
