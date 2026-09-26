# jax #40965 — jax.scipy.stats.expon.logcdf returns -inf for small positive x

**Status:** branch pushed (commit `7fd36442e`), PR not yet opened
**Branch:** `bhaskargurram-ai/jax` → `fix/expon-logcdf-small-x`
**Open the PR:** https://github.com/jax-ml/jax/compare/main...bhaskargurram-ai:jax:fix/expon-logcdf-small-x?expand=1

Title:

```
Fix expon.logcdf returning -inf for small positive x
```

Body (paste as-is):

---

Fixes #40965.

`jax.scipy.stats.expon.logcdf` was computed as `log1p(-sf(x))`, i.e. `log1p(-exp(-(x - loc) / scale))`. Once the standardized argument drops below about `eps / 2` (roughly `6e-8` in float32, JAX's default, and `1.1e-16` in float64), `exp(-x)` rounds to exactly `1`, so the result becomes `log(0) = -inf` and `jax.grad(logcdf)` becomes `inf`. The true value is finite (`log(x)` to leading order) and `scipy.stats.expon.logcdf` returns it.

| input | before (`main`) | after | `scipy.stats.expon.logcdf` |
|---|---|---|---|
| `logcdf(float32(1e-8))` | `-inf` | `-18.420681` | `-18.420680748952364` |
| `grad(logcdf)(float32(1e-8))` | `inf` | `1e+08` | (`1 / expm1(1e-8)` = `1e+08`) |
| `logcdf(float64(1e-17))` | `-inf` | `-39.14394658089878` | `-39.14394658089878` |
| `grad(logcdf)(float64(1e-17))` | `inf` | `1e+17` | (`1e+17`) |
| `logcdf(float64(50.0))` | `-1.9287498479639178e-22` | `-1.9287498479639178e-22` (unchanged) | `-1.9287498479639178e-22` |

`cdf` was not affected: it already computes `-expm1(-x)`, so it returns `1e-08` for the same input.

### Change

`logcdf` now standardizes its argument and evaluates `jax.nn.log1mexp((x - loc) / scale)` (already used the same way by `jax.scipy.stats.gumbel_r`), keeping the `x < loc` branch at `-inf`. `log1mexp` computes `log(1 - exp(-z))` as `log(-expm1(-z))` for `z < log(2)`, which has no cancellation, and as `log1p(-exp(-z))` otherwise, so values for larger arguments are bit-identical to the previous implementation (a plain `log(-expm1(-z))` everywhere would have lost relative accuracy near `0` for large `z`). Its custom JVP yields the finite derivative `1 / expm1(z)` for every `z > 0`. `sf`, `logsf` and `cdf` are unchanged.

### Tests

Added `testExponLogCdfSmallX` to `tests/scipy_stats_test.py` (parametrized over `jtu.dtypes.floating`, so float32 always and float64 with `JAX_ENABLE_X64=1`). For `x in [eps/8, eps/2, eps, 1e-3, 1.0, 40.0]` it checks that `logcdf` is finite and matches `scipy.stats.expon.logcdf` evaluated in float64, that `jax.grad` is finite and matches `1 / expm1(x)`, that `scale` is still applied, and that `x < loc` still returns `-inf`. On `main` the test fails for both dtypes (`-inf` for the two smallest inputs); on this branch it passes.

Commands run (CPU, pip `jaxlib==0.11.2`, the clone's `jax/`):

- `pytest tests/scipy_stats_test.py -k ExponLogCdfSmallX` — 1 passed (float32)
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k ExponLogCdfSmallX` — 2 passed (float32, float64); 2 failed on `main` with the same command
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k Expon` — 63 passed
- `pytest tests/scipy_stats_test.py -k Expon` — 62 passed
- `ruff check jax/_src/scipy/stats/expon.py tests/scipy_stats_test.py` — all checks passed
- `pre-commit run --files jax/_src/scipy/stats/expon.py tests/scipy_stats_test.py` — all hooks passed (including pyrefly type checking)

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` with a script: `expon.logcdf(jnp.float32(1e-8))` → `-inf`, `jax.grad(expon.logcdf)(jnp.float32(1e-8))` → `inf`; with x64, `expon.logcdf(jnp.float64(1e-17))` → `-inf`, grad `inf`. scipy gives `-18.420680748952364` and `-39.14394658089878`. `expon.cdf(jnp.float32(1e-8))` → `1e-08` (already fine, uses `-expm1`).
- After the fix the same script gives `-18.420681` / `1e+08` (float32) and `-39.14394658089878` / `1e+17` (float64); `logcdf(50.0)` is unchanged at `-1.9287498479639178e-22`; `logcdf(-1.0)` and `logcdf(0.5, loc=1.0)` are still `-inf`; `grad` at `x < loc` is `-0.0` (no NaN from the unselected `where` branch); `grad` at exactly `x == loc` is `inf` (mathematically the derivative of `log(x)` at 0, same as before); `jit` and `vmap(grad)` work; `nan` input propagates to `nan`; `logcdf(2.00001, loc=2.0, scale=3.0)` → `-12.610182` vs scipy `-12.61153942029799` (difference is float32 rounding of `2.00001 - 2.0`, identical before and after).
- New test fails on `main` (both dtypes, `np.all(np.isfinite(actual))` assertion) and passes on the branch; full `-k Expon` subset passes with and without x64.
- `ruff check` clean; `pre-commit run --files` on both changed files: check-ast, merge-conflict, end-of-file, debug-statements, trailing-whitespace, ruff, pyrefly, copyright all passed.
- Why `jax.nn.log1mexp` rather than the issue's suggested bare `log(-expm1(-x))`: the bare form is accurate for small `x` but, for large `x`, `log(1 - tiny)` loses all relative accuracy (e.g. returns `0` instead of `-1.9e-22` at `x = 50`, and ~3e-3 relative error at `x = 10` in float32), which would degrade the existing `testExponLogCdf` comparison; `log1mexp` switches at `log(2)` and is what `gumbel_r` already uses, so the large-`x` path is unchanged.
- No CHANGELOG entry: the previous `expon` bug fix (`10b238613`, #36757, `expon.ppf` ignoring `scale`) added none, and the unreleased "Bug fixes" section lists only core `jax.numpy`/`jax.lax` items. Easy to add under `## Unreleased` → `* Bug fixes` if a reviewer asks; suggested text: "Fixed {func}`jax.scipy.stats.expon.logcdf` returning `-inf` (with an infinite gradient) for small positive `x` ({jax-issue}`#40965`)."
- Environment note: the clone requires jaxlib >= 0.11.2, which only ships wheels for Python 3.12+; used a Python 3.12 venv with pip `jaxlib==0.11.2` and the clone's pure-Python `jax/` installed editable (`uv pip install -e . --no-deps`). No jaxlib build.
