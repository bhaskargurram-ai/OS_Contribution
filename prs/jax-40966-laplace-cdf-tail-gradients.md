# jax #40966 — jax.scipy.stats.laplace.cdf gives NaN gradients in the tails

**Status:** branch pushed (commit `be0ae59c9`), PR not yet opened
**Branch:** `bhaskargurram-ai/jax` → `fix/laplace-cdf-tail-gradients`
**Open the PR:** https://github.com/jax-ml/jax/compare/main...bhaskargurram-ai:jax:fix/laplace-cdf-tail-gradients?expand=1

Title:

```
Fix NaN gradients of laplace.cdf in the tails
```

Body (paste as-is):

---

Fixes #40966.

`jax.scipy.stats.laplace.cdf` selected between `0.5 * exp(z)` and `1 - 0.5 * exp(-z)` with `z = (x - loc) / scale`, evaluating both branches unconditionally. Once `|z|` exceeds the `exp` overflow threshold (about 88 in float32, 709 in float64) the branch that is not selected is `inf`. The forward value is still correct, but the transpose of the select multiplies that `inf` by a zero cotangent, so the derivatives with respect to `x`, `loc` and `scale` were `NaN` instead of `0`. In JAX's default float32 mode this happens for parameters as ordinary as `x=0, loc=10, scale=0.1` (`|z| = 100`).

| input | before (`main`) | after | reference |
|---|---|---|---|
| `grad(cdf)(float32(1000.))` | `nan` | `0.0` | `scipy.stats.laplace.pdf(1000.) = 0.0` |
| `grad(cdf)(float32(-1000.))` | `nan` | `0.0` | `0.0` |
| `grad(cdf)(float64(±1000.))` | `nan` | `0.0` | `0.0` |
| `grad(cdf, argnums=(0,1,2))(0., 10., 0.1)` (float32) | `(nan, nan, nan)` | `(0.0, -0.0, 0.0)` | pdf is `~1.9e-43`, i.e. `0` in float32 |
| `cdf(float64(50.))`, `grad` | `1.0`, `9.64e-23` | unchanged | `1.0`, `9.64e-23` |
| `grad(cdf)(0.)` | `0.5` | `0.5` (unchanged) | `0.5` |

### Change

`cdf` now evaluates `exp` once, on `select(z <= 0, z, -z)` (i.e. `-|z|`), and uses that value in both branches: `select(z <= 0, t, 1 - t)` with `t = 0.5 * exp(-|z|)`. The argument of `exp` is never positive, so nothing overflows and the gradients stay finite; the forward values are bit-identical to the previous implementation (each branch computes exactly what it computed before). A `select` rather than `lax.abs` is used for `-|z|` so that the derivative at `z == 0` follows the left branch and equals the pdf (`0.5 / scale`) as before; `abs` would give a derivative of `0` there.

`logpdf` and `pdf` were not affected (they already use `|x - loc|`), and `laplace` has no `logcdf`/`sf`/`logsf` in JAX.

### Tests

Added `testLaplaceCdfTailGradients` to `tests/scipy_stats_test.py` (parametrized over `jtu.dtypes.floating`, so float32 always and float64 with `JAX_ENABLE_X64=1`). For `x in [-1e3, -50, -1, 0, 1, 50, 1e3]`, with and without `loc=0.5, scale=2`, it checks that `cdf` matches `scipy.stats.laplace.cdf` and that `jax.grad(cdf)` is finite and matches `scipy.stats.laplace.pdf`; it also checks that the gradients with respect to `x`, `loc` and `scale` at the issue's example (`x=0, loc=10, scale=0.1`) are finite. On `main` the test fails for both dtypes (`np.isfinite(grad)` assertion); on this branch it passes.

Commands run (CPU, pip `jaxlib==0.11.2`, Python 3.12, this branch's `jax/` on `PYTHONPATH`):

- `pytest tests/scipy_stats_test.py -k LaplaceCdfTailGradients` — 1 passed (float32); 1 failed on `main`
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k LaplaceCdfTailGradients` — 2 passed (float32, float64); 2 failed on `main`
- `pytest tests/scipy_stats_test.py -k Laplace` — 21 passed
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k Laplace` — 22 passed
- `ruff check jax/_src/scipy/stats/laplace.py tests/scipy_stats_test.py` — all checks passed

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main` with a script (float32 default and `JAX_ENABLE_X64=1`): `jax.grad(laplace.cdf)(x)` is `nan` for `x = ±1000` in float32 and float64, while `cdf` itself is `0.0`/`1.0` (correct) and scipy's pdf is `0.0`; the issue's `jax.grad(lambda x: laplace.cdf(x, 10.0, 0.1))(0.0)` is `nan` in float32 (in float64 it is `1.86e-43`, since `exp(100)` does not overflow there); grads wrt `x`, `loc`, `scale` are all `nan` in float32. Values for `x in {-50, -1, 0, 1, 50}` and their grads already matched scipy's cdf/pdf.
- After the fix the same script gives `0.0` for the tail gradients in both dtypes, `(0.0, -0.0, 0.0)` for the issue's `(x, loc, scale)` gradient, and every forward value is unchanged (bit-identical: each branch is the same expression as before). `grad` at `x = 0` is still `0.5`. `jit(grad(cdf))` works; `nan` input propagates to `nan`; `cdf(±inf)` is `1.0`/`0.0` with gradient `0.0`; `jax.hessian(cdf)` at `0, 1, -1, 1000` is `0.5, -0.184, 0.184, 0.0` (finite); `vmap` works.
- Why a `select` for `-|z|` rather than `lax.abs`: `lax.abs` has derivative `sign(0) = 0` at zero, which would change `grad(cdf)(loc)` from `0.5/scale` to `0`. `lax.min(z, 0)` would give `0.25/scale` (balanced tie gradient). The `select` reproduces the previous `z <= 0` branch derivative exactly.
- New test fails on `main` (1 failed float32-only, 2 failed with x64) and passes on the branch; the full `-k Laplace` subset (21 / 22 tests) passes with and without x64.
- `ruff check` clean. `pre-commit` is not installed in this environment and its hook cache (pyrefly needs a pre-release jaxlib download) was not present, so only ruff was run; the change uses only `lax` ops already imported in the file, so pyrefly should be unaffected.
- No CHANGELOG entry, following the precedent of previous `jax.scipy.stats` bug fixes (e.g. #36757), whose unreleased "Bug fixes" section lists only core `jax.numpy`/`jax.lax` items. Suggested text if a reviewer asks: "Fixed {func}`jax.scipy.stats.laplace.cdf` returning NaN gradients far in the tails ({jax-issue}`#40966`)."
- Maintainer context: jakevdp's only comment on the issue is a pointer to the meta-issue #38651 ("edge cases of `special`, `stats`, and other functions"), which says the team will prioritize other work over such reports. The issue is open and unassigned with no linked PR, so a PR is still appropriate, but review may be slow; the PR body above keeps the change minimal (two lines of logic, forward values unchanged) to make review cheap.
- Environment note: the clone requires jaxlib >= 0.11.2, which only ships wheels for Python 3.12+; used a Python 3.12 venv with pip `jaxlib==0.11.2` and the branch's pure-Python `jax/` on `PYTHONPATH`. No jaxlib build.
