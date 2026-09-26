# pymilvus #3794 — `import pymilvus` closes pre-existing logging handlers

**Status:** branch pushed (commit `07a9c94`), PR not yet opened
**Branch:** `bhaskargurram-ai/pymilvus` → `fix/import-keeps-logging-handlers`
**Open the PR:** https://github.com/milvus-io/pymilvus/compare/master...bhaskargurram-ai:pymilvus:fix/import-keeps-logging-handlers?expand=1

Title:

```
Stop closing application logging handlers on import
```

Body (paste as-is):

---

Fixes #3794.

`pymilvus/settings.py` runs `init_log("WARNING")` at import time, and `init_log` used `logging.config.dictConfig()` to set up the `pymilvus*` loggers. In its default (non-incremental) mode `dictConfig` first calls `_clearExistingHandlers()`, which runs `logging.shutdown()` over **every** handler registered in the process and empties the handler registry (`logging._handlers`). `disable_existing_loggers: False` only prevents loggers from being disabled; it does nothing about handlers.

So any logging an application configured before `import pymilvus` was silently broken: a `FileHandler`'s stream was closed, a `MemoryHandler` lost its target (buffered records dropped), every application handler disappeared from the registry so it is no longer flushed at interpreter exit, and a handler the application attached to the `pymilvus` logger itself was removed.

Reproduction on `master` (root logger with a `FileHandler`, a `MemoryHandler` and a handler on `logging.getLogger("pymilvus")`, then `import pymilvus`):

| | before `import pymilvus` | after (master) | after (this PR) |
|---|---|---|---|
| registered handler names | `app-file, app-memory, app-sdk-handler, app-stream` | `no_color_console` | `app-file, app-memory, app-sdk-handler, app-stream, pymilvus_console` |
| `FileHandler.stream.closed` | `False` | `True` | `False` |
| `MemoryHandler.target` | `<StreamHandler>` | `None` | `<StreamHandler>` |
| handlers on `pymilvus` logger | `app-sdk-handler` | `no_color_console` | `app-sdk-handler, pymilvus_console` |

### Change

`init_log()` now configures only the `pymilvus`, `pymilvus.milvus_client` and `pymilvus.bulk_writer` loggers directly through the `logging` API instead of `dictConfig`:

- same format string, same levels (`pymilvus` at the given level, the two sub-loggers at `INFO`) and `propagate = False` as before;
- one shared `StreamHandler` named `pymilvus_console`, looked up by name on the pymilvus loggers so calling `init_log()` again (e.g. `importlib.reload`) does not stack duplicate handlers;
- nothing outside the `pymilvus` logger tree is touched, and handlers an application attached to the `pymilvus` logger are kept.

The unused `colorful_console` handler definition (it was declared in the dict but never attached to any logger) is dropped; the `ColorfulFormatter` class is unchanged.

### Tests

New `tests/unit/test_settings_logging.py` (4 tests, all fail on `master`, all pass here):

- `test_init_log_keeps_application_handlers_open` – root `StreamHandler`/`FileHandler`/`MemoryHandler` survive `init_log()` and still receive records.
- `test_init_log_keeps_handler_attached_to_pymilvus_logger` – a handler the app put on `logging.getLogger("pymilvus")` is kept.
- `test_init_log_is_idempotent` – calling `init_log()` twice leaves exactly one pymilvus handler per logger, with the expected levels, formatter and `propagate=False`.
- `test_import_pymilvus_keeps_preconfigured_file_handler` – end-to-end in a fresh interpreter: a `FileHandler` configured before `import pymilvus` is still open afterwards.

Commands run:

- `PYTHONPATH=. uv run --group dev pytest tests/unit/test_settings_logging.py` → 4 passed (on `master`: 4 failed)
- `PYTHONPATH=. uv run --group dev pytest tests/unit` → 5258 passed, 3 skipped, 1 failed (`tests/unit/test_check.py::TestGetCommit::test_get_commit`, fails identically on `master` in a shallow clone; unrelated)
- `make lint` (`black pymilvus tests --check --diff` → 200 files unchanged; `ruff check pymilvus tests` → all checks passed)

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced the bug with a standalone script on `master`: after `import pymilvus`, the app's `FileHandler` stream is closed, the `MemoryHandler.target` is `None`, `logging._handlers` contains only `no_color_console`, and the handler attached to the `pymilvus` logger is gone. Same script on the branch: all four app handlers intact plus `pymilvus_console`.
- `tests/unit/test_settings_logging.py`: 4 failed with the old `settings.py` (stashed), 4 passed with the fix.
- Full unit suite: 5258 passed, 3 skipped; the single failure `test_check.py::TestGetCommit::test_get_commit` also fails on unmodified `master` (it expects specific git history / tags that a `--depth 200` clone lacks).
- `black --check` and `ruff check` clean on `pymilvus` and `tests`.
- Commit is DCO signed (`Signed-off-by: Bhaskar Gurram <gurrambhaskar.ai@gmail.com>`); the repo enforces DCO via mergify.
- Behaviour notes a reviewer may ask about:
  - `MILVUS_LOG_LEVEL`-style env handling: none exists in the repo; `init_log("WARNING")` is hard-coded as before and left as is.
  - Previously `dictConfig` also *removed* any handler an application had attached to the `pymilvus` logger before import; now such handlers are kept alongside pymilvus's own console handler. This is the behaviour the issue asks for.
  - `logging.config` is no longer imported in `settings.py`.
