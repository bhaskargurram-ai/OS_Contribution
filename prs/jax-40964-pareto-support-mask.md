# jax #40964 — jax.scipy.stats.pareto returns -inf/inf/nan at the support boundary when scale is small relative to loc

**Status:** branch pushed (commit `bcd307e01`), PR not yet opened
**Branch:** `bhaskargurram-ai/jax` → `fix/pareto-support-mask`
**Open the PR:** https://github.com/jax-ml/jax/compare/main...bhaskargurram-ai:jax:fix/pareto-support-mask?expand=1

Title:

```
Fix pareto support test when scale is below the resolution of loc
```

Body (paste as-is):

---

Fixes #40964.

`jax.scipy.stats.pareto.logpdf`, `cdf`, `logcdf` and `logsf` (and `pdf`/`sf`, which exponentiate them) decided whether `x` is in the support with `x < loc + scale`, evaluated in the input dtype, while computing the value from the standardized `z = (x - loc) / scale`. When `scale` is below the floating-point resolution of `loc`, `loc + scale` rounds to `loc`, so `x == loc` passes the support test although `z == 0` is outside the support. The functions then returned `log(0)`-derived values instead of the below-support constants. In JAX's default float32 mode this happens for ordinary parameters such as the issue's `x=1000, b=1, loc=1000, scale=1e-5`; in float64 it happens once `scale < ~2e-16 * loc` (e.g. `loc=1000, scale=1e-14`).

| `(x, b, loc, scale)` | function | before (`main`) | after | `scipy.stats.pareto` |
|---|---|---|---|---|
| `(1000, 1, 1000, 1e-5)` float32 | `pdf`, `logpdf` | `inf`, `inf` | `0.0`, `-inf` | `0.0`, `-inf` |
| | `cdf`, `logcdf` | `-inf`, `nan` | `0.0`, `-inf` | `0.0`, `-inf` |
| | `sf`, `logsf` | `inf`, `inf` | `1.0`, `0.0` | `1.0`, `0.0` |
| `(1e8, 2, 1e8, 1e-2)` float32 | all six | same `inf/-inf/nan` pattern | scipy's values | `0, -inf, 0, -inf, 1, 0` |
| `(1000, 2, 1000, 1e-14)` float64 | all six | same `inf/-inf/nan` pattern | scipy's values | `0, -inf, 0, -inf, 1, 0` |
| `(1e8 + 0.1, 2, 1e8, 1e-2)` float64 (inside support) | `pdf`, `cdf` | `0.2000000358`, `0.9899999988` | unchanged | `0.2000000358`, `0.9899999988` |

### Change

The four functions now test the support on the standardized value, `z < 1`, which each of them already computes. This is also how `scipy.stats.pareto` evaluates its support (`(x - loc) / scale >= 1`), so the value and the mask agree by construction, and points strictly inside the support are unaffected. `logcdf` and `logsf` gain a `one = _lax_const(x, 1)` constant that `logpdf` and `cdf` already had. `ppf` has no support mask on `x` and is unchanged.

### Tests

Added `testParetoSupportBoundary` to `tests/scipy_stats_test.py`, parametrized over `jtu.dtypes.floating` and `loc in {1e3, 1e8}`. With `scale = ulp(loc) / 8` (so that `loc + scale == loc` in the input dtype, asserted in the test) it evaluates all six functions at `z in {-8, 0, 8, 16, 800}` and, with `scale = 4 * ulp(loc)`, at `z in {0.75, 1, 1.25, 2}` (just below, at and above the boundary), comparing against `scipy.stats.pareto` evaluated on `z` in float64 (with the `1/scale` pdf normalization applied by hand, because `x - loc` is not representable in float64 when `loc` is float32). `x` is built as `loc + z * scale` with a power-of-two `scale`, so `x`, `x - loc` and `z` are exact in the input dtype. It also asserts the issue's example gives `cdf = 0`, `sf = 1`, `pdf = 0`, `logcdf = -inf`. On `main` the `scale = ulp/8` subtests fail for every function in both dtypes (values are `inf`/`-inf`/`nan`) and the float32 issue-example assertion fails; on this branch everything passes.

Commands run (CPU, pip `jaxlib==0.11.2`, Python 3.12, this branch's `jax/` on `PYTHONPATH`):

- `pytest tests/scipy_stats_test.py -k ParetoSupportBoundary` — 2 passed, 24 subtests passed (float32); 14 failed on `main`
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k ParetoSupportBoundary` — 4 passed, 48 subtests passed (float32, float64); 26 failed on `main` (24 subtests + 2 float32 parent tests; the float64 parent tests fail only through their subtests because the issue's `1000 + 1e-5` is representable in float64)
- `pytest tests/scipy_stats_test.py -k Pareto` — 72 passed
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k Pareto` — 74 passed
- `ruff check jax/_src/scipy/stats/pareto.py tests/scipy_stats_test.py` — all checks passed

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` with a script comparing `pdf, logpdf, cdf, logcdf, sf, logsf` against scipy: in float32 (default), `(x, b, loc, scale) = (1000, 1, 1000, 1e-5)`, `(1e8, 2, 1e8, 1e-2)` with `x = loc`, `x = loc + 1e-2` and `x = loc + 0.1` (all round to `loc` in float32) give `[inf, inf, -inf, nan, inf, inf]` vs scipy's `[0, -inf, 0, -inf, 1, 0]`. In float64 the issue's parameters are fine on `main` (`1e-5` is above the resolution of `1000` in float64) but `(1000, 2, 1000, 1e-14)` and `(1e8, 2, 1e8, 1e-9)` give the same `[inf, inf, -inf, nan, inf, inf]`. Inside the support (`x = 1e8 + 0.1`, float64) `main` already matched scipy to ~1e-15.
- After the fix all of the above match scipy exactly; inside-support values are unchanged (the only edit is the mask expression).
- Gradients: `jax.grad(pareto.cdf)` at the issue's float32 point is `nan` after the fix (it was `inf` before). This is the separate, pre-existing "unselected `where` branch" problem (`log(0)`/`0 ** -b` in the masked-out branch) that affects every `x < loc + scale` point on `main` too, not only the boundary; it is out of scope for this issue and was left alone to keep the change minimal. Worth mentioning if a reviewer asks.
- `nan` in `x` still propagates to `nan` (the `z < 1` comparison is false, as `x < loc + scale` was).
- New test fails on `main` and passes on the branch in both dtypes (see counts above); full `-k Pareto` subset (72 / 74 tests) passes with and without x64.
- `ruff check` clean. `pre-commit` is not installed in this environment and its hook cache (pyrefly needs a pre-release jaxlib download) was not present, so only ruff was run; the change uses only names already imported in the file.
- No CHANGELOG entry, following the precedent of previous `jax.scipy.stats` bug fixes (e.g. #36757). Suggested text if a reviewer asks: "Fixed {mod}`jax.scipy.stats.pareto` returning `inf`/`nan` for `x == loc` when `scale` is below the floating-point resolution of `loc` ({jax-issue}`#40964`)."
- Maintainer context: jakevdp's only comment on the issue is a pointer to the meta-issue #38651 ("edge cases of `special`, `stats`, and other functions"), which says the team will prioritize other work over such reports. The issue is open and unassigned with no linked PR, so a PR is still appropriate, but review may be slow.
- Environment note: the clone requires jaxlib >= 0.11.2, which only ships wheels for Python 3.12+; used a Python 3.12 venv with pip `jaxlib==0.11.2` and the branch's pure-Python `jax/` on `PYTHONPATH`. No jaxlib build.
