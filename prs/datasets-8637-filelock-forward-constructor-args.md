# datasets #8637 — `FileLock` wrapper drops every constructor argument

**Status:** branch pushed (`c9717a0`), PR not yet opened
**Branch:** `bhaskargurram-ai/datasets` → `fix/filelock-forward-constructor-args`
**Open the PR:** https://github.com/huggingface/datasets/compare/main...bhaskargurram-ai:datasets:fix/filelock-forward-constructor-args?expand=1

No AI-disclosure requirement in this repo (no `AGENTS.md`, nothing in `CONTRIBUTING.md`).
`make style` (ruff check + ruff format) is the quality gate; both pass.

Title:

```
Forward constructor arguments through the FileLock wrapper
```

Body (paste as-is):

---

Fixes #8637.

`datasets.utils._filelock.FileLock` took `*args, **kwargs` in `__init__`. `filelock`
decides which constructor arguments to forward by inspecting the signature of
`cls.__init__` for parameter *names*, so `timeout`, `thread_local`, `blocking`,
`is_singleton`, `poll_interval` and `lifetime` were all dropped before reaching the parent:

```python
FileLock(path, timeout=5).timeout   # -1
```

`is_singleton=True` was also broken. The wrapper injected a umask-derived `mode` into
kwargs, but `filelock` compares the arguments the *caller* passed against the cached
instance — before `__init__` runs — so the second construction saw `mode=-1` against an
instance holding the umask mode and raised
`ValueError: Singleton lock instances cannot be initialized with differing arguments`.

### Why an `__init__` fix can't work

Both checks live in `filelock`'s metaclass, ahead of `__init__`. Anything done inside
`__init__` is invisible to the signature inspection and too late for the singleton
comparison.

### Change

Move the umask and long-path handling into a metaclass `__call__`. `FileLock` no longer
overrides `__init__`, so `filelock` sees the parent's real signature and forwards every
parameter — and the injected `mode` is part of what the singleton comparison receives on
every call, so both calls agree.

### Versions

`datasets` pins `filelock` with no version bound, so users land on either major.

| | filelock 3.25.2 (reporter's) | filelock 4.0.3 |
|---|---|---|
| `timeout=5` before | **-1** | 5 |
| singleton before | **ValueError** | works |
| `timeout=5` after | 5 | 5 |
| singleton after | same instance | same instance |
| umask `mode` after | 0o644 | 0o644 |

4.x honours `**kwargs` in its inspection, which is why the bug is invisible there. The fix
behaves identically on both.

### Tests

Three added to `tests/test_filelock.py`: arguments reach `filelock`, singletons return the
cached instance, and the umask `mode` is still applied. On filelock 3.25.2 the first two
**fail on `main`** and pass here; the umask and long-path tests were never broken and pass
both ways. All four pass on 4.0.3.

`ruff check` and `ruff format --check` pass on both files.

### AI assistance

This change was produced with AI assistance. I reviewed every line, ran the tests on both
filelock versions, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on filelock 3.25.2 | `timeout=-1`, singleton `ValueError` |
| Confirmed absent on 4.0.3 | works there; 4.x honours `**kwargs` |
| New tests fail on `main` (3.25.2) | 2 of 4 fail (the two bug tests) |
| New tests pass with fix | 4/4 on 3.25.2, 4/4 on 4.0.3 |
| umask mode preserved | 0o644 on both |
| `ruff check` / `ruff format` | pass |

Diff is 47 insertions, 9 deletions across 2 files.
