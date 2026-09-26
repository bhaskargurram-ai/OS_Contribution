# modal-client #4130 — `modal volume get` corrupts a directory download to a new path

**Status:** branch pushed (`abbd56b`), PR not yet opened
**Branch:** `bhaskargurram-ai/modal-client` → `fix/volume-get-new-directory-destination`
**Open the PR:** https://github.com/modal-labs/modal-client/compare/main...bhaskargurram-ai:modal-client:fix/volume-get-new-directory-destination?expand=1

`AGENTS.md` requires a `CHANGELOG_DEV.md` entry for fixes with significant user impact —
included. No AI-disclosure requirement found. Comments must not reference backend internals
(they don't).

Title:

```
Create the destination directory when volume get targets a new path
```

Body (paste as-is):

---

Fixes #4130.

`_volume_download` decided whether the local destination was a directory with
`Path.is_dir()`. A destination that does not exist yet is not a directory by that test, so
when the remote path named a directory, **every entry received the destination path itself
as its output path**. The concurrent downloads then wrote the same file — leaving partial or
nondeterministic contents, failing with `Output path ... already exists`, or raising
`IsADirectoryError` — instead of producing the requested tree.

### Change

Decide from the *remote* instead, before any local state is consulted: the first entry
shows whether the remote is a directory. When it is and the destination does not exist,
create the destination and map the directory's contents directly beneath it — as `cp -r`
does for a new target, and consistent with the existing single-file behaviour where a new
path *becomes* the file. An existing directory destination keeps its current behaviour, and
a remote file downloaded to a new path is still written to that path. The entry for the
remote directory itself is skipped, since the destination now represents it.

| command | before | after |
|---|---|---|
| `volume get vol dir NEW/` (NEW absent) | one corrupt file, or an error | `NEW/a.txt`, `NEW/b.txt` |
| `volume get vol file NEW.txt` (absent) | `NEW.txt` is the file | unchanged |
| `volume get vol dir EXISTING/` | `EXISTING/dir/...` | unchanged |

### Tests

Two unit tests in `test/cli_test.py` exercise `_volume_download` directly against a fake
volume, so no transfer leaves the process. The directory case **fails on `main`** with
`IsADirectoryError` (the directory entry creates the path, then a file entry opens it for
writing) and passes here — deterministically, no race needed. The single-file case passes
both ways and guards the unchanged behaviour.

### Environment note

The existing CLI tests `test_volume_get` and `test_volume_rm` fail in my environment
**identically with and without this change** — the blob transfer makes an HTTP request to
the mock server on `127.0.0.1`, which an egress policy here blocks
(`403 request blocked: no rule allows host "127.0.0.1"`). That is why the regression test
is written against a fake volume rather than through the CLI. They should pass in CI.

`ruff check` and `ruff format --check` pass on both files.

### AI assistance

This change was produced with AI assistance. I reviewed every line, reproduced the failure,
ran the tests, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on `main` | `already exists` error from the write race |
| Directory unit test fails on `main` | `IsADirectoryError` — deterministic |
| Both unit tests pass with fix | 2/2 |
| `test_volume_get` / `test_volume_rm` | fail identically with and without fix — loopback policy block |
| `ruff check` / `ruff format` | pass |
| `inv protoc` needed first | yes — generated bindings are not checked in |

Diff is 85 insertions, 1 deletion across 3 files (incl. changelog).
