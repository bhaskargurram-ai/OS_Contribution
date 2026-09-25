# dspy #10497 — method-named fields diverge between attribute and item access

**Status:** branch pushed (`7a3cf4f`), PR not yet opened
**Branch:** `bhaskargurram-ai/dspy` → `fix/example-field-name-collision`
**Open the PR:** https://github.com/stanfordnlp/dspy/compare/main...bhaskargurram-ai:dspy:fix/example-field-name-collision?expand=1

Title:

```
Keep method-named fields in sync between attribute and item access
```

Body (paste as-is; the disclosure line at the end is required by dspy's
`CONTRIBUTING.md`, which auto-closes and may ban undisclosed agent contributions):

---

Fixes #10497.

A field whose name collides with a method — `items`, `keys`, `values`, `get`, `copy` — could
hold two different values at the same time:

```python
ex = dspy.Example(items=["a"])
ex.items = ["b"]
ex["items"]   # ["a"]  — while the instance attribute held ["b"]
```

`__setattr__` routed any name appearing in `dir(type(self))` to a real instance attribute
and left `_store` untouched, so the write landed somewhere `__getitem__`, `toDict()`,
`keys()` and serialization never look.

### Change

Assignment now writes to `_store` whenever the field is already stored, so attribute and
item access cannot disagree. Names that are not fields keep their previous routing, and
private names are unaffected.

Attribute *reads* are deliberately left alone. Making `ex.items` return the stored value
would shadow the mapping API that `Example` exposes and that callers throughout DSPy
depend on — `ex.items()`, `ex.keys()`, `ex.get()` would all break. Instead the constructor
warns when a field name collides with a method, naming the field and pointing at subscript
access:

```
Example field(s) 'items' share a name with a method, so attribute access returns the
method rather than the stored value. Use subscript access such as example['items'] to
read them.
```

That resolves the divergence in the issue (one field, one value) and tells the reader
about the shadowing rather than leaving them to discover it, without a breaking change.

### Tests

Five tests in `tests/primitives/test_example.py`: the store stays in sync on assignment,
the mapping API stays callable, the constructor warns, ordinary fields are unchanged, and
private attributes still bypass the store. Two of them fail on `main` and pass here.

Ran `pytest tests/ --ignore=tests/clients` — 1198 passed, 523 skipped. The four errors in
`tests/signatures/test_adapter_image.py` reproduce on an unmodified checkout of `main` and
are unrelated (image fixture setup).

`ruff check` passes on both changed files.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| New tests pass with the fix | 5/5 |
| New tests fail without it | 2 fail (the other 3 assert unchanged behaviour) |
| `tests/primitives` + `tests/adapters` + `tests/predict` | 996 passed, 265 skipped |
| Full suite minus `tests/clients` | 1198 passed, 523 skipped |
| `test_adapter_image.py` errors | reproduce on clean `main` — pre-existing |
| `ruff check` | passes |

Diff is 72 insertions across 2 files.
