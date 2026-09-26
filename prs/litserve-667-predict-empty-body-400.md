# litserve #667 — Swagger UI does not expose request parameters for /predict, causing 500 error when invoked

**Status:** branch pushed (commit `e18cca4`), PR not yet opened
**Branch:** `bhaskargurram-ai/litserve` → `fix/predict-empty-body-400`
**Open the PR:** https://github.com/Lightning-AI/litserve/compare/main...bhaskargurram-ai:litserve:fix/predict-empty-body-400?expand=1

Title:

```
Return 400 for empty/malformed JSON body and declare it in OpenAPI
```

Body (paste as-is):

---

## What does this PR do?

Fixes #667.

As a user opening `/docs` for a freshly started LitServe app, I want to try `/predict` from Swagger UI and get a
usable input box and a clear error when I send nothing, instead of an empty form and a 500 Internal Server Error.

When `decode_request` takes a raw `fastapi.Request` (the default when it is unannotated, and what every quickstart
example uses), `/predict` reads the body itself via `request.json()` in `BaseRequestHandler._prepare_request`. An
empty or non-JSON body raises `json.JSONDecodeError` inside the handler; the generic `except Exception` in
`RegularRequestHandler.handle_request` converts that into `HTTPException(500, "Internal server error")` and logs a
full traceback, even though the fault is on the client side.

The same route is registered with `add_api_route` without any request body declaration, so FastAPI's OpenAPI schema
for `/predict` has no `requestBody`. Swagger UI therefore renders no input field and "Execute" sends exactly the empty
body that triggers the 500. Reproduced with `TestClient` against a minimal `LitAPI`:

| Request (`POST /predict`) | before | after |
| --- | --- | --- |
| no body | `500 {"detail":"Internal server error"}` + traceback in log | `400 {"detail":"Request body is empty. Send a JSON payload in the request body."}` |
| `Content-Type: application/json`, empty body | 500 | 400 (same message) |
| body `not json` | 500 | `400 {"detail":"Request body is not valid JSON: Expecting value: line 1 column 1 (char 0)"}` |
| `{"input": 4.0}` | `200 {"output":16.0}` | `200 {"output":16.0}` |
| `/openapi.json` → `paths./predict.post.requestBody` | absent | `{"required": true, "content": {"application/json": {"schema": {"type": "object", "additionalProperties": true}}}}` |

### Change

- `src/litserve/server.py`
  - `BaseRequestHandler._parse_json_body`: wraps `request.json()`; on `ValueError` (`JSONDecodeError` /
    `UnicodeDecodeError`) it raises `HTTPException(400)` with a detail that says whether the body was empty or not
    valid JSON. `_prepare_request` calls it for the `Request` path; form/multipart handling is untouched.
  - `StreamingRequestHandler.handle_request`: re-raise `HTTPException` as-is (as `RegularRequestHandler` already did)
    so the 400 is not downgraded to a 500 for streaming APIs.
  - `LitServer._openapi_request_body`: when `decode_request` is annotated with (or defaults to) `Request`, the route is
    registered with `openapi_extra` declaring a required `application/json` object body. Swagger UI now shows an
    editable JSON body for `/predict`. A Pydantic-annotated `decode_request` is unchanged and keeps its model schema
    (FastAPI already validates that path and returns 422 on an empty body).

The OpenAPI declaration is a generic free-form object because, with a raw `Request`, the server cannot know the
payload's shape. Users who want a typed input box can annotate `decode_request(self, request: MyModel)`, which
already worked and is now covered by a test.

### Tests

- `tests/unit/test_simple.py`
  - `test_predict_empty_or_malformed_body_returns_400` (4 cases: no body, empty JSON body, whitespace body, malformed
    JSON) — asserts 400 with a JSON-related detail, then that a valid request still succeeds.
  - `test_predict_empty_body_returns_400_streaming` — same for a streaming `LitAPI`.
  - `test_openapi_declares_request_body_for_raw_request` — asserts the `requestBody` declaration in `/openapi.json`.
- `tests/unit/test_request_handlers.py`
  - `test_prepare_request_rejects_invalid_json_with_400` (empty / malformed) — unit test of the handler; `MockRequest`
    gained a `raw_body` option and a `body()` coroutine to mirror Starlette.
- `tests/unit/test_pydantic.py`
  - `test_pydantic_openapi_request_body` — guards that a Pydantic-annotated `decode_request` keeps its
    `$ref` schema and still returns 422 on an empty body.

All 8 new non-Pydantic tests fail on `main` (500 instead of 400 / missing `requestBody`) and pass on this branch; the
Pydantic test passes on both.

Commands run:

- `pytest tests/unit/test_request_handlers.py tests/unit/test_pydantic.py tests/unit/test_simple.py tests/unit/test_form.py`
  → 34 passed (one run had `test_workers_health_custom_path[False]` fail on its 3 s sleep-based health check;
  it passed on re-run and is unrelated to this change).
- `pytest tests/unit/test_specs.py tests/unit/test_multiple_endpoints.py tests/unit/test_auth.py tests/unit/test_middlewares.py tests/unit/test_compression.py tests/unit/test_callbacks.py tests/unit/test_loops.py`
  → 89 passed.
- `ruff check src tests` → All checks passed; `ruff format --check src tests` → 100 files already formatted;
  `docformatter --check` and `codespell` on the changed files → clean.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced the bug with a `TestClient` script (`wrap_litserve_start` + minimal `LitAPI`): `POST /predict` with no
  body, with an empty `application/json` body, and with `not json` all returned
  `500 {"detail":"Internal server error"}` with `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
  logged from `server.py:_prepare_request -> request.json()`; `/openapi.json` had no `requestBody` for `/predict`.
- After the fix the same script returns 400 with the messages in the table above, the valid request still returns
  `{"output": 16.0}`, and `/openapi.json` declares the request body.
- New tests: 8 fail on `main` (verified by stashing `src/litserve/server.py`), all 9 pass on the branch.
- `tests/unit/test_lit_server.py` (the file named in the task) imports `torch` at module level; the CPU torch wheel
  index (`download.pytorch.org`) is blocked by the sandbox proxy and the PyPI CUDA wheel exceeds the disk budget, so
  that file and `tests/unit/test_batch.py` could not be run here. The tests added live in `test_simple.py`,
  `test_request_handlers.py` and `test_pydantic.py`, which exercise the same server/handler code paths through
  `TestClient`; CI (`uv sync --all-extras --dev`) will run `test_lit_server.py`.
- Full pre-commit was not run (pre-commit hook downloads go to GitHub, which is blocked); instead `ruff` (check +
  format), `docformatter==1.7.7` (the pinned hook version) and `codespell` were run directly on the changed files.
- Reviewer questions to expect: 400 vs 422 — 400 was chosen because a body that is not JSON at all is a syntax
  error rather than a validation error; the Pydantic-annotated path keeps FastAPI's 422. The OpenAPI body is
  declared only when `request_type is Request`, so custom/Pydantic annotations and spec endpoints (OpenAI, MCP)
  are unaffected.
- PR template (`.github/PULL_REQUEST_TEMPLATE.md`) sections "What does this PR do?" and the user-impact sentence are
  mirrored in the body; the template does not forbid AI-assisted PRs.
