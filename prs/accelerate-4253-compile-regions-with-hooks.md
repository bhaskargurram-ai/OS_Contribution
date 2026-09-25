# accelerate #4253 — compile_regions silently runs the uncompiled model

**Status:** branch pushed (`6b931c3`), PR not yet opened
**Branch:** `bhaskargurram-ai/accelerate` → `fix/compile-regions-with-hooks`
**Open the PR:** https://github.com/huggingface/accelerate/compare/main...bhaskargurram-ai:accelerate:fix/compile-regions-with-hooks?expand=1

Title:

```
Rebind hook-wrapped forward when copying a module in compile_regions
```

Body (paste as-is). Note: accelerate has **no** AI-disclosure requirement — no `AGENTS.md`
and nothing in `CONTRIBUTING.md` — so the disclosure paragraph is optional here, unlike
peft and dspy. It is included below; remove it if you prefer.

---

Fixes #4253.

`compile_regions` copies the parent module and rebinds its instance attributes so the copy
calls its own compiled children:

```python
for name, value in list(new_module.__dict__.items()):
    if hasattr(value, "__func__") and getattr(value, "__self__", None) is module:
        new_module.__dict__[name] = MethodType(value.__func__, new_module)
```

That recognises bound methods, which carry `__func__` and `__self__`. But
`add_hook_to_module` installs forward as:

```python
module.forward = functools.update_wrapper(functools.partial(new_forward, module), old_forward)
```

A `partial` has neither attribute, so it was left pointing at the **original** module. The
copy then ran the original's uncompiled children, and its compiled blocks were never
reached — silently, with no error raised and no speedup delivered.

### Change

Rebind partials whose arguments reference the original module, preserving the wrapper
metadata `add_hook_to_module` attached.

### Reproduction

Counting forward-hook invocations on the compiled blocks, as in the issue:

| model | before | after |
|---|---|---|
| plain | 3 | 3 |
| `add_hook_to_module` | **0** | 3 |

### Tests

`test_hook_wrapped_forward_is_rebound` added to the existing
`RegionalCompilationRebindTester` in `tests/test_compile.py`, using the same `trace`
mechanism as its neighbours. It fails on `main` and passes here.

Ran `pytest tests/test_compile.py` (3 passed, 5 skipped — the skips are GPU-gated) and
`pytest tests/test_hooks.py tests/test_utils.py tests/test_modeling_utils.py` (94 passed,
18 skipped).

`ruff check` reports one pre-existing `if-with-same-arms` finding at `other.py:454`, which
reproduces on an unmodified checkout and is untouched by this change. `ruff format --check`
is clean on both files.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced the bug first | yes — 0 compiled-block calls with a hook attached |
| New test passes with the fix | yes |
| New test fails without it | yes |
| `tests/test_compile.py` | 3 passed, 5 skipped |
| `test_hooks` + `test_utils` + `test_modeling_utils` | 94 passed, 18 skipped |
| `ruff check` | 1 finding, pre-existing and unrelated |

Diff is 37 insertions across 2 files.
