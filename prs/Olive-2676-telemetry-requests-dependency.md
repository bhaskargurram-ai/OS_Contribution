# Olive #2676 — `import olive` fails on 0.13.0: telemetry exporter imports undeclared `requests`

**Status:** branch pushed (commit `8c99b37`), PR not yet opened
**Branch:** `bhaskargurram-ai/Olive` → `fix/telemetry-requests-dependency`
**Open the PR:** https://github.com/microsoft/Olive/compare/main...bhaskargurram-ai:Olive:fix/telemetry-requests-dependency?expand=1

Title:

```
Declare requests as an install dependency for telemetry
```

Body (paste as-is):

---

Fixes #2676.

## Describe your changes

`import olive` imports `olive.telemetry` (via `olive.cli.api` → `olive.cli.benchmark` → `from olive.telemetry import action`), and the OneCollector exporter in `olive/telemetry/library/` imports `requests` unconditionally at module level (`exporter.py`, `options.py`, `transport.py`). `requests` is not listed in `requirements.txt`, which is what `setup.py` uses for `install_requires`, and it is not in any extra either.

It went unnoticed because `requests` used to be pulled in transitively by `transformers`/`huggingface_hub`. Recent releases of those packages dropped `requests` in favour of `httpx`, so a fresh `pip install olive-ai` (no extras) now fails on `import olive`:

```
  File ".../olive/telemetry/library/__init__.py", line 43, in <module>
    from olive.telemetry.library.exporter import OneCollectorLogExporter
  File ".../olive/telemetry/library/exporter.py", line 14, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

Telemetry is a core, always-on component: `Telemetry()` is created in the CLI launcher, the `@action` decorator is used by the engine and every CLI command, its other dependency `opentelemetry-sdk` is already a hard requirement, and the exporter's public API (`OneCollectorTransportOptions.http_client_factory`) is typed around `requests.Session`. So the correct fix is to declare the dependency rather than make the import optional and silently disable telemetry.

### Change

- `requirements.txt`: add `requests` (already sorted the way the `requirements-txt-fixer` pre-commit hook expects).
- `test/telemetry/test_dependencies.py` (new): `test_telemetry_imports_are_declared_in_requirements` statically parses every module under `olive/telemetry`, collects the unconditional module-level third-party imports (imports inside `try`/`if TYPE_CHECKING`/functions are ignored), maps them to distribution names with `importlib.metadata.packages_distributions()` and asserts each one is declared in `requirements.txt`. This prevents a future telemetry dependency from breaking `import olive` again.

| | `main` | this branch |
|---|---|---|
| `pip install -e .` in a fresh venv, then `pip show requests` | not installed | installed (2.34.2) |
| `python -c "import olive"` in that venv | `ModuleNotFoundError: No module named 'requests'` | OK |
| `pytest test/telemetry` | 1 failed (`requests` undeclared, reported in `exporter.py`, `options.py`, `transport.py`) | 1 passed |

### Tests

- `pytest test/telemetry -q` — fails on `main` (`AssertionError: ... {'requests': ['olive/telemetry/library/exporter.py', 'olive/telemetry/library/options.py', 'olive/telemetry/library/transport.py']}`), passes here (1 passed).
- Reproduced the original failure in a fresh `uv venv` (Python 3.11) with `pip install -e .` and no extras: `import olive` raised the `ModuleNotFoundError` above; after this change the same install pulls `requests` and `import olive` succeeds.
- `ruff check --config=pyproject.toml test/telemetry` — all checks passed; `ruff format --check` — already formatted; `pylint --rcfile=pyproject.toml test/telemetry` — 10.00/10 (ruff 0.15.11, pylint 3.3.6 as pinned in `requirements-dev.txt`).
- pre-commit hooks `requirements-txt-fixer`, `end-of-file-fixer`, `trailing-whitespace` on the changed files — no changes.

## Checklist before requesting a review
- [x] Add unit tests for this change.
- [x] Make sure all tests can pass.
- [ ] Update documents if necessary. (Not needed: no document lists the core dependencies.)
- [x] Lint and apply fixes to your code by running `lintrunner -a` (ran the underlying ruff/ruff-format/pylint with the pinned versions).
- [x] Is this a user-facing change? Yes: `requests` becomes a declared install dependency of `olive-ai`, so `pip install olive-ai` works out of the box again.

## (Optional) Issue link
#2676

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Fresh `uv venv` (Python 3.11.15), `uv pip install -e .` on `main` with no extras: `uv pip show requests` → "Package(s) not found"; `python -c "import olive"` → `ModuleNotFoundError: No module named 'requests'` at `olive/telemetry/library/exporter.py:14` (full traceback goes `olive/__init__.py` → `olive/cli/api.py` → `olive/cli/benchmark.py` → `olive/telemetry/__init__.py` → `olive/telemetry/telemetry.py` → `olive/telemetry/library/__init__.py` → `exporter.py`). Installed transformers 5.17.0 / httpx 0.28.1 confirm `requests` is no longer transitively present.
- New test before fix: `1 failed` with the assertion naming `requests` in `exporter.py`, `options.py`, `transport.py`. After adding `requests` to `requirements.txt`: `1 passed`.
- Uninstalled `requests`, re-ran `uv pip install -e .` on the branch: `requests 2.34.2` installed, `import olive` OK (version `0.13.0.dev0`).
- Lint: `ruff check` / `ruff format --check` / `pylint` (pinned versions) on `test/telemetry` clean; `requirements-txt-fixer` (pre-commit-hooks 4.5.0) leaves `requirements.txt` unchanged.
- Note: `test/` has no pre-existing telemetry tests (only the `disable_telemetry` autouse fixture in `test/conftest.py`), so `test/telemetry/` is a new directory; it mirrors the layout of the other `test/<area>/` packages with a copyright-header `__init__.py`. Running any test needs `peft`, `datasets` and `onnxruntime` because of the session-scoped fixtures in `test/conftest.py`.
- Why not a lazy/optional import: `Telemetry` is instantiated unconditionally by the CLI and by the `@action` decorator on the engine and every command; the library types its options around `requests.Session`. Making `requests` optional would silently disable telemetry for users of a plain install, which contradicts docs/Privacy.md ("Telemetry is turned ON by default"). Reviewers may still prefer (or additionally want) a lazy import in `exporter.py`; that would be a small follow-up on top of this.
- Microsoft CLA bot will request signature on the PR; nothing to do locally.
- Upstream `microsoft/Olive` was not reachable from this session (api.github.com blocked), so I could not confirm whether an upstream fix already landed after the fork point (`43eb077`). Check for a duplicate before opening.
