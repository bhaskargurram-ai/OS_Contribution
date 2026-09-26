# jax #40968 — jax.scipy.special.zeta: the custom_jvp rule returns a different primal value than the function (nan vs finite for s < 1)

**Status:** branch pushed (commit `d23df33`), PR not yet opened
**Branch:** `bhaskargurram-ai/jax` → `fix/zeta-jvp-primal`
**Open the PR:** https://github.com/jax-ml/jax/compare/main...bhaskargurram-ai:jax:fix/zeta-jvp-primal?expand=1

Title:

```
Make zeta's JVP rule return the function's own primal value
```

Body (paste as-is):

---

Fixes #40968.

`jax.scipy.special.zeta` is a `custom_jvp` function whose rule was `partial(jax.jvp, _zeta_series_expansion)`, so under differentiation both the primal and the tangent came from the Euler-Maclaurin series used to compute the derivative. That series is an analytic continuation of the Hurwitz zeta function: it returns finite values for `x < 1`, where `lax.zeta` (and `scipy.special.zeta`, which is defined for `x > 1`) return `nan`. The same expression therefore gave different values depending on whether it was differentiated:

| expression (`x64`) | before (`main`) | after |
|---|---|---|
| `zeta(0.5, 1.0)` | `nan` | `nan` |
| `jax.jvp(zeta, (0.5, 1.0), (0.0, 1.0))[0]` | `-1.4603545088095866` | `nan` |
| `jax.value_and_grad(lambda q: zeta(0.5, q))(1.0)` | `(-1.4603545, -0.8061877)` | `(nan, nan)` |
| `jax.jvp(zeta, (2.0, 1.0), (0.0, 1.0))` | `(1.6449340668, -2.4041138063)` | `(1.6449340668, -2.4041138063)` (unchanged) |
| `jax.grad(lambda s: zeta(s, 1.0))(2.0)` | `-0.9375482543` | `-0.9375482543` (unchanged; finite difference `-0.9375482540`) |

### Change

The JVP rule is now an explicit `_zeta_jvp` that evaluates the primal with `zeta` itself (`lax.zeta`) and takes only the tangent from `jax.jvp(_zeta_series_expansion, ...)`. Where the primal is `nan` (outside the function's domain) the tangent is set to `nan` as well, using a multiplicative mask (`tangent * where(isnan(primal), nan, 1)`) rather than `jnp.where`, so that the rule stays linear in the tangent and reverse mode (`grad`, `value_and_grad`) yields `nan` too instead of silently returning `0`. Values and derivatives inside the domain (`x > 1`) are unchanged. `_zeta_series_expansion` no longer needs the `q is None` check, since `zeta` already raises before the rule can run.

### Tests

Added `testZetaJvpPrimalMatchesFunction` to `tests/lax_scipy_special_functions_test.py` (parametrized over `jtu.dtypes.floating`). For `x in [-0.5, 0.5, 1.5, 2.0, 3.0]` it asserts that the primal from `jax.jvp` is exactly equal to `zeta(x, q)` (NaN positions included), that the tangent is `nan` for `x < 1` and matches `d/dq zeta(x, q) = -x zeta(x + 1, q)` (from scipy) for `x > 1`, that `value_and_grad` agrees with the forward-mode results, and that the report's `value_and_grad(zeta)(0.5, 1.0)` is `(nan, nan)`. On `main` the test fails for both dtypes (`nan location mismatch`); on this branch it passes. The existing `testScipySpecialFun` gradient test for `zeta` (`check_grads` with `rand_positive`, i.e. `x in [1, 3)`) still passes.

Commands run (CPU, pip `jaxlib==0.11.2`, this branch's `jax/`):

- `pytest tests/lax_scipy_special_functions_test.py -k ZetaJvpPrimal` — 1 passed (float32); 1 failed on `main`
- `JAX_ENABLE_X64=1 pytest tests/lax_scipy_special_functions_test.py -k ZetaJvpPrimal` — 2 passed; 2 failed on `main`
- `pytest tests/lax_scipy_special_functions_test.py -k "zeta or Zeta"` — 11 passed
- `JAX_ENABLE_X64=1 pytest tests/lax_scipy_special_functions_test.py -k "zeta or Zeta"` — 12 passed
- `ruff check jax/_src/scipy/special.py tests/lax_scipy_special_functions_test.py` — all checks passed
- `pre-commit run --files jax/_src/scipy/special.py tests/lax_scipy_special_functions_test.py` — all hooks passed (including pyrefly type checking)

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` (float32 and float64): `zeta(0.5, 1.0)` and `zeta(-0.5, 1.0)` are `nan` (scipy: `nan`) while `jax.jvp(zeta, ...)[0]` gives `-1.4603545` and `-0.2078862`, with finite tangents; for `x in {1.5, 2, 3}` the jvp primal differed from the function only by float32 rounding (e.g. `2.6123753` vs `2.6123755`), since the series and `lax.zeta` are different algorithms.
- After the fix, `np.array_equal(zeta(x, q), jvp(zeta, ...)[0], equal_nan=True)` holds for all probed inputs in both dtypes; `jit(grad(...))`, `vmap` through `jvp`, `hessian` (`1.98928023` vs finite-difference `1.98928019` at `x = 2`), Python-scalar inputs and broadcasting (`x` scalar, `q` vector) all work.
- Derivatives inside the domain are unchanged: `grad_q zeta(2, 1) = -2.4041138063` = `-2 zeta(3, 1)`; `grad_q zeta(3.5, 0.7) = -17.8007024046` = `-3.5 zeta(4.5, 0.7)`; `grad_s zeta(2, 1) = -0.93754825` vs finite difference `-0.93754825`.
- Other edge inputs behave as before: the pole `x = 1` gives primal `inf` and tangent `-inf`/`nan`; `q <= 0` gives `inf`/`nan` primals with `nan` tangents (the series expansion does not handle `q <= 0`; pre-existing, out of scope).
- Design note for the reviewer: masking the tangent to `nan` outside the domain goes slightly beyond the literal request (primal equality). Returning the series' finite "derivative" next to a `nan` value would be inconsistent, and in reverse mode a `jnp.where` mask would transpose to `0` (the `nan` constant is not linear in the tangent), which is why a multiplicative mask is used. If maintainers prefer to keep the analytically-continued tangent, dropping the two mask lines and the `tangent[:2]`/`grad[:2]` NaN assertions restores that behaviour while keeping the primal fix.
- No CHANGELOG entry (previous `jax.scipy.special` fixes such as `#3777` for `zeta` did not add one in recent sections). Suggested text if asked: "{func}`jax.scipy.special.zeta` now returns the same primal value under {func}`jax.jvp`/{func}`jax.grad` as when called directly ({jax-issue}`#40968`)."
- Environment: Python 3.12 venv with pip `jaxlib==0.11.2` and the branch's pure-Python `jax/` on `PYTHONPATH`; no jaxlib build.
