# flax #5577 — The scales field of the NNX WeightNorm module isn't learnable

**Status:** branch pushed (commit `210178f`), PR not yet opened
**Branch:** `bhaskargurram-ai/flax` → `fix/nnx-weightnorm-trainable-scales`
**Open the PR:** https://github.com/google/flax/compare/main...bhaskargurram-ai:flax:fix/nnx-weightnorm-trainable-scales?expand=1

Title:

```
Make nnx.WeightNorm scales trainable nnx.Param variables
```

Body (paste as-is):

---

# What does this PR do?

Fixes #5577.

`nnx.WeightNorm.__init__` built `self.scales` as a dict of plain `jax.Array`s
(wrapped in `nnx.data(...)`) rather than `nnx.Variable`s. Because they were not
Variables, the scales were not part of the module's state: `nnx.state(model, nnx.Param)`
did not list them, `nnx.grad` / `nnx.value_and_grad` returned no gradient for them, and
`nnx.Optimizer(model, tx, wrt=nnx.Param)` never updated them. The scale `g` in weight
normalization (Salimans & Kingma, 2016, https://arxiv.org/abs/1602.07868) is a learned
parameter, and the Linen `WeightNorm` already creates it via `self.param(...)`, so the
NNX version silently trained a different model.

Reproduction on `main` with `nnx.WeightNorm(nnx.Linear(2, 3, rngs=rngs), rngs=rngs)`:

| | `main` | this branch |
|---|---|---|
| `type(model.scales[('kernel',)])` | `ArrayImpl` | `Param` |
| `nnx.state(model, nnx.Param)` paths | `layer_instance/bias`, `layer_instance/kernel` | + `scales/('kernel',)` |
| `nnx.grad` paths | `layer_instance/bias`, `layer_instance/kernel` | + `scales/('kernel',)` |
| scales after one `nnx.Optimizer(sgd(0.1), wrt=nnx.Param)` step | `[1. 1. 1.]` (unchanged) | `[0.9915 -0.5994 0.9783]` |

### Change

- `flax/nnx/nn/normalization.py`: each scale is now created as
  `nnx.Param(scale_init(rngs['params'], scale_shape, self.param_dtype))`. The scale is
  also initialized with `param_dtype` (previously the argument was documented but not
  applied to the scales), matching Linen. `_weightnorm_inplace` reads the scale value
  with `self.scales[path][...]`. The `scales` container is still a dict keyed by the
  param path, so `variable_filter`, `feature_axes` and `use_scale=False` (`scales is None`)
  behave as before. The class docstring now describes the `scales` attribute and the
  example shows the scale appearing in the `nnx.Param` state.

### Tests

- `tests/nnx/nn/normalization_test.py`: new `TestWeightNorm` class:
  - `test_scales_are_trainable_params` (parameterized over `param_dtype` float32/float16
    and `feature_axes=-1` / `(0, 1)`): asserts the scale is an `nnx.Param` with the
    expected dtype/shape, is present in `nnx.state(model, nnx.Param)`, receives a
    non-zero gradient from `nnx.grad`, and changes after one `nnx.Optimizer` step.
  - `test_variable_filter_selects_scaled_params`: `variable_filter=nnx.PathContains('bias')`
    produces exactly one `Param` scale for `('bias',)`.
  - `test_no_scales_without_use_scale`: `use_scale=False` keeps `scales is None` and no
    `scales` entry in the Param state.

  On `main` the first two tests fail (`AssertionError: Array([1., 1., 1.], dtype=float32)
  is not an instance of <class 'flax.nnx.variablelib.Param'>`; 5 failed, 1 passed); on
  this branch all pass. The existing `test_nnx_linen_weightnorm_equivalence` cases
  (including `param_dtype=float16`) still pass.

Commands run (CPU, Python 3.12, jax 0.11.2):

- `pytest tests/nnx/nn/normalization_test.py` → 114 passed
- `pytest --doctest-modules flax/nnx/nn/normalization.py` → 7 passed (includes the updated `WeightNorm` docstring example)
- `ruff check flax/nnx/nn/normalization.py tests/nnx/nn/normalization_test.py` → All checks passed

## Checklist
- [x] This PR fixes a minor issue (e.g.: typo or small bug) or improves the docs (you can dismiss the other checks if that's the case).
- [x] This change is discussed in a Github issue/[discussion](https://github.com/google/flax/discussions): #5577
- [x] The documentation and docstrings adhere to the [documentation guidelines](https://github.com/google/flax/blob/main/docs/README.md#how-to-write-code-documentation).
- [x] This change includes necessary high-coverage tests. (No quality testing = no merge!)

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced the bug on `main` with a script (`nnx.WeightNorm(nnx.Linear(2, 3, rngs=rngs), rngs=rngs)`):
  `scales` entries were `ArrayImpl`, absent from `nnx.state(model, nnx.Param)` and from `nnx.grad` output,
  and unchanged (`[1. 1. 1.]`) after an `nnx.Optimizer(optax.sgd(0.1), wrt=nnx.Param)` step. After the fix the
  entries are `Param`, appear in both, and change to `[0.99153876 -0.5994141 0.97826606]`.
- Confirmed NNX handles a dict of `nnx.Param` with tuple keys through `nnx.state`, `nnx.split`/`merge`, `nnx.jit`
  and `nnx.grad` (paths come out as `('scales', ('kernel',))`).
- New tests: fail on `main` (5 failed / 1 passed — the `use_scale=False` guard test passes on both), pass on the branch (6 passed).
- Full file `pytest tests/nnx/nn/normalization_test.py`: 114 passed. Doctests for `flax/nnx/nn/normalization.py`: 7 passed.
- `ruff check` on both changed files: clean. `ruff format --diff` reports only pre-existing formatting differences
  (repo has `ruff-format` and `pyink` disabled in `.pre-commit-config.yaml`; count went 187 → 185 lines, none on the added code).
- `param_dtype` note for reviewers: the scale is now initialized with `param_dtype` (Linen does the same via
  `self.param(..., self.param_dtype)`). Previously it was always float32 regardless of `param_dtype`. The existing
  Linen-equivalence test with `param_dtype=float16` still passes.
- CHANGELOG.md: has a `vNext` section, but `CONTRIBUTING.md` does not ask contributors to add entries and the file has not
  been maintained since 0.8.2 (current version 0.12.10), so no entry was added.
- Google CLA applies to `google/flax`; nothing to do locally.
- Environment: outbound `api.github.com` blocked, so the issue text was taken from the task description rather than fetched.
