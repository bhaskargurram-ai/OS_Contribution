# client-python #626 — Eager dual-client instantiation and asymmetric `__exit__`/`__aexit__` leaks unclosed HTTP clients

**Status:** branch pushed (commit `ebeeda5`), PR not yet opened
**Branch:** `bhaskargurram-ai/client-python` → `fix/lazy-http-clients-and-symmetric-close`
**Open the PR:** https://github.com/mistralai/client-python/compare/main...bhaskargurram-ai:client-python:fix/lazy-http-clients-and-symmetric-close?expand=1

Title:

```
Create HTTP clients lazily and close both on context-manager exit
```

Body (paste as-is):

---

Fixes #626.

`Mistral.__init__` eagerly created both an `httpx.Client` and an `httpx.AsyncClient` whenever the caller did not inject one, although any given caller only ever uses one of them. `__exit__` then closed only the sync client and `__aexit__` only the async client, so `with Mistral(...)` leaked the never-used `AsyncClient` and `async with Mistral(...)` leaked the never-used `Client`.

The leaked client was left to the `weakref.finalize(close_clients, ...)` fallback, which calls `asyncio.run(async_client.aclose())` during garbage collection to close an async client the sync user never touched. That is the mechanism behind #509 (event loops/socketpairs created at GC time, `Too many open files` at interpreter exit) and it also misbehaves when a loop is already running (FastAPI, Jupyter).

Reproduction on `main` (no network needed; spies on the `httpx` constructors):

| Scenario | `main` | this branch |
|---|---|---|
| `with Mistral(...)`: `httpx.AsyncClient` constructed | 1 (left open after exit) | 0 |
| `async with Mistral(...)`: `httpx.Client` constructed | 1 (left open after exit) | 0 |
| GC of a sync-only `Mistral`: `asyncio.run()` calls in finalizer | 3 | 0 |

### Change

Only `src/mistralai/client/sdk.py` is touched (no change to `basesdk.py`, `sdkconfiguration.py` or `httpclient.py`):

- New `_LazyClientSDKConfiguration(SDKConfiguration)`: `client` / `async_client` are properties that instantiate the SDK-owned `httpx.Client` / `httpx.AsyncClient` on first read (double-checked locking, so concurrent first use creates a single instance). Injected clients are stored and returned unchanged; `client_supplied` / `async_client_supplied` keep their meaning. `release_owned_clients()` detaches both attributes, stops any further lazy creation and returns only the clients the SDK created.
- `Mistral.__init__` no longer constructs any `httpx` client. The `issubclass(..., HttpClient)` assertions still run for injected clients.
- `__exit__` and `__aexit__` are now symmetric: each closes every SDK-owned client that was actually created and never an injected one. An async client that was created inside a sync `with` block (sync + async usage on the same instance) is closed with the existing best-effort `close_clients` helper, since a sync exit cannot `await`.
- The GC finalizer closes whatever exists at collection time, so a sync-only SDK no longer spins up an event loop when collected.
- SDK init hooks still receive a sync client when any are registered (reading the attribute creates it); none are registered today, so nothing is created for them.

Behaviour note: after `with Mistral(...) as c:` exits, `c.sdk_configuration.async_client` is now `None` as well (previously the leaked, still-open async client was reachable there). Using the SDK after exiting its context manager was never supported.

### Tests

New `tests/test_http_client_lifecycle.py` (14 tests, no network) covering: no `httpx` client is created at construction; sync use never constructs an `AsyncClient`; async use never constructs a `Client`; concurrent first access from 8 threads yields one instance; `with` / `async with` close every owned client that was created (including the mixed sync+async case); `__exit__` is idempotent; injected clients are never closed by either context manager or by the finalizer; GC of a sync-only SDK closes the sync client without calling `asyncio.run()`.

On `main`, 9 of the 14 tests fail; on this branch all 14 pass.

Commands run:

- `uv run pytest tests/test_http_client_lifecycle.py` — 14 passed (main: 9 failed, 5 passed)
- `uv run pytest tests/ --ignore=tests/test_gcp_v2_parity.py` — 182 passed, 46 skipped (`test_gcp_v2_parity.py` fails to import `google.auth` in my environment on `main` too; unrelated)
- `uv run pytest src/mistralai/extra/tests` — 338 passed
- `uv run ruff check src/mistralai/client/sdk.py tests/test_http_client_lifecycle.py` — only the pre-existing `E731` on the generated `security = lambda: ...` line, which is unchanged and present on `main`
- `uv run ruff format --check` on both files — clean
- `uv run mypy` on both files — clean
- `uv run pyright` on both files — 0 errors
- `uv run pylint --rcfile=pylintrc` on both files — 10.00/10

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced the bug on `main` with a scratch script that spies on `httpx.Client` / `httpx.AsyncClient` construction and on `asyncio.run` during GC: `with` constructs and leaks an `AsyncClient`, `async with` constructs and leaks a `Client`, and GC of a sync-only instance calls `asyncio.run()` 3 times. Same script on the branch: 0 / 0 / 0 and the used client is closed on exit.
- `tests/test_http_client_lifecycle.py`: 14 passed on the branch; 9 failed / 5 passed with the same test file on `main` (via `git stash`).
- `uv run pytest tests/ --ignore=tests/test_gcp_v2_parity.py`: 182 passed, 46 skipped. `test_gcp_v2_parity.py` errors at collection with `ModuleNotFoundError: No module named 'google.auth'` because the `gcp` extra is not installed in the frozen dev environment; identical on `main`, unrelated to this change.
- `uv run pytest src/mistralai/extra/tests`: 338 passed (the OTel tracing hook reads `config.client` / `config.async_client`; still works with the lazy properties).
- ruff check: only pre-existing `E731` (generated lambda, unchanged). ruff format: clean. mypy: clean. pyright: 0 errors (the two `# type: ignore[override]` comments on the property setters are needed by both mypy and pyright because a property replaces a dataclass field of the base class). pylint (`pylintrc`): 10.00/10.
- `uv.lock` was rewritten locally by `uv sync` (the repo's `exclude-newer = "2 days"` is unparseable by current uv); reverted with `git checkout -- uv.lock`, not committed. All verification used `uv run --frozen`.
- Reviewer questions to expect:
  - Why the `hooks.sdk_init_hooks` guard: `sdk_init` hooks take a concrete `HttpClient`, so when any are registered the sync client is created eagerly for them (same as before); with none registered (the current state of `_hooks/registration.py`) nothing is created.
  - Why `close_clients(...)` is reused in `__exit__`: it is the generated best-effort helper for closing an async client from sync code; it is only reached when both sync and async methods were used on the same instance inside a sync `with` block.
  - The tracing hook (`_hooks/tracing.py`) wraps `config.client` and `config.async_client` when OpenTelemetry tracing is active, which will lazily create the other client in that case; it is then closed by the symmetric exit, so no leak, just no laziness while tracing.
  - Public `close()` / `aclose()` methods (issue suggestion 3) were deliberately left out to keep the change minimal; easy follow-up.

## Caveat

- `CONTRIBUTING.md` states the repository is generated code and that direct PRs are not accepted; `CLAUDE.md`/`AGENTS.md` say to be skeptical of edits to files with the `Code generated by Speakeasy ... DO NOT EDIT` header. **`src/mistralai/client/sdk.py` carries that header and is not listed in `.genignore`**, so the maintainers may prefer to route this through Speakeasy's Python generator templates (the same eager-creation / asymmetric-exit pattern comes from the generator). **Ask the maintainers before opening the PR** (e.g. a comment on #626 offering this branch as a reference implementation) rather than opening it cold.
- Generated files changed by this branch: exactly one, `src/mistralai/client/sdk.py`. No changes to `basesdk.py`, `sdkconfiguration.py`, `httpclient.py`, `_hooks/`, or `docs/`. The new test file `tests/test_http_client_lifecycle.py` is hand-written and lives next to the other hand-written tests that CI runs (`uv run pytest tests/`).
- There is no hand-maintained override point for `Mistral.__init__`/`__exit__`/`__aexit__`: custom code regions (`# region sdk-class-body`) can only add members, no `sdk_init` hooks are registered, and `src/mistralai/extra/` cannot host the change because the same bug exists in `packages/azure` and `packages/gcp`, which do not depend on the core package.
- `packages/azure/src/mistralai/azure/client/sdk.py` and `packages/gcp/src/mistralai/gcp/client/sdk.py` **are** hand-owned (listed in their package `.genignore`) and contain the identical eager-creation / asymmetric-exit code. They were intentionally left untouched to keep this PR minimal; the same `_LazyClientSDKConfiguration` pattern applies verbatim there and would be an uncontroversial follow-up (or could be added to this PR if the maintainers ask).
- The commit and PR text contain the "AI assistance" section as instructed; `CONTRIBUTING.md` does not mention AI-assisted contributions.
