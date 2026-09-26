# jax #40969 — jax.scipy.stats.poisson.entropy returns NaN gradients for large mu (and small mu in float32)

**Status:** branch pushed (commit `765a98a`), PR not yet opened
**Branch:** `bhaskargurram-ai/jax` → `fix/poisson-entropy-gradients`
**Open the PR:** https://github.com/jax-ml/jax/compare/main...bhaskargurram-ai:jax:fix/poisson-entropy-gradients?expand=1

Title:

```
Fix NaN gradients of poisson.entropy for large and small mu
```

Body (paste as-is):

---

Fixes #40969.

`jax.grad(jax.scipy.stats.poisson.entropy)` returned `NaN` for `mu >= ~88` and `mu <= ~0.39` in float32 and for `mu >= ~713` in float64, although the forward value was correct. `entropy` switches between three regimes with nested `jnp.where` (direct summation for `mu < 10`, summation with wider bounds for `10 <= mu < 100`, an asymptotic formula for `mu >= 100`), so the summation branches are evaluated for every `mu`. For `k` far from `mu` the PMF underflows to exactly `0`, and the derivative of `entr(p) = -p log p`, i.e. `-log(p) - 1`, is infinite there. The chain rule then produces `inf * 0 = nan` inside the unselected branch, and since `jnp.where` only zeroes the cotangent of that branch (it does not stop the NaN from being generated), the NaN leaks into the gradient of the selected branch.

| input | before (`main`) | after | reference |
|---|---|---|---|
| `grad(entropy)(float32(150.0))` | `nan` | `0.0033370368` | `1/(2 mu) + 1/(12 mu^2)` = `0.0033370370` |
| `grad(entropy)(float32(0.1))` | `nan` | `2.3704884` | `2.3704892` (float64 sum) |
| `grad(entropy)(float32(1e-3))` | `nan` | `6.9084473` | `6.9084483` |
| `grad(entropy)(float32(1e6))` | `nan` | `5.0000006e-07` | `5.0000008e-07` |
| `grad(entropy)(float64(1000.0))` | `nan` | `0.0005000833333333334` | `0.0005000833333333334` |
| `grad(entropy)(float32(5.0))` | `0.1046673` | `0.10466743` (unchanged up to rounding) | `0.10466770` |

### Change

The two summation regimes now compute the terms `-p(k) log p(k)` from the log PMF as `-exp(lp) * lp` (new helper `_masked_entropy_terms`, which also applies the existing `k`-range mask) instead of `entr(pmf(k, mu))`. `lp = logpmf(k, mu)` is finite for every valid `k` and `mu > 0`, and the derivative `-exp(lp) * (lp + 1) * dlp/dmu` is exactly `0` once `exp(lp)` underflows, so no `inf` is ever produced. Forward values are unchanged up to rounding (the existing `testPoissonEntropy*` tests pass with their tolerances). The asymptotic regime and the `mu == 0` handling are untouched, and `entr` is no longer imported by `poisson.py`.

### Tests

Added `testPoissonEntropyGrad` to `tests/scipy_stats_test.py` (parametrized over `jtu.dtypes.floating`). For `mu in [1e-3, 0.1, 0.39, 5, 50, 88, 150, 1e3, 1e6]` it checks that `vmap(grad(entropy))` is finite and matches a float64 reference (`-sum_k p(k) (k/mu - 1) (log p(k) + 1)` evaluated with `scipy.stats.poisson.logpmf` for `mu < 100`, and the derivative of the asymptotic formula `1/(2 mu) + 1/(12 mu^2)` for `mu >= 100`), plus the scalar `grad(entropy)(150.0)` from the report. On `main` the test fails for both dtypes (`isfinite` assertion); on this branch it passes.

Commands run (CPU, pip `jaxlib==0.11.2`, this branch's `jax/`):

- `pytest tests/scipy_stats_test.py -k PoissonEntropyGrad` — 1 passed (float32); 1 failed on `main`
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k PoissonEntropyGrad` — 2 passed; 2 failed on `main`
- `pytest tests/scipy_stats_test.py -k Poisson` — 46 passed
- `JAX_ENABLE_X64=1 pytest tests/scipy_stats_test.py -k Poisson` — 52 passed
- `ruff check jax/_src/scipy/stats/poisson.py tests/scipy_stats_test.py` — all checks passed
- `pre-commit run --files jax/_src/scipy/stats/poisson.py tests/scipy_stats_test.py` — all hooks passed (including pyrefly type checking)

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Reproduced on `main`: `jax.grad(poisson.entropy)` is `nan` for float32 `mu in {1e-3, 0.1, 88, 150, 1e3, 1e6}` and float64 `mu in {713, 1e3, 1e6}`; finite for float32 `0.39`, `5.0` and float64 `1e-3`, `0.1`, `5`, `150`, `700`. Forward values match `scipy.stats.poisson(mu).entropy()` (except `mu = 1e6`, where scipy's own summation does not converge and returns `2.769`; JAX's asymptotic `8.3267` is correct).
- After the fix, gradients are finite for all of these and match the float64 reference derivative to relative error `<= 4e-5` in float32 (`1e-4` at `mu = 99.99`, just below the regime switch, where the truncated sum itself is only accurate to ~`1e-4`) and `<= 1.4e-7` in float64 (the `1.4e-7` at `mu = 5` is the tail mass beyond `k = mu + 20` dropped by the existing small-`mu` bound; exact `0` in the asymptotic regime).
- `jit(vmap(grad(entropy)))` and `jax.jacobian` on vectors work and agree with the scalar gradients.
- `mu == 0`: value is `0.0` (unchanged) and the gradient is `nan` both before and after (the asymptotic branch's `1/(12 mu)` and `logpmf(k >= 1, 0) = -inf`; mathematically `dH/dmu -> +inf` as `mu -> 0`). Not part of the issue; noted in case a reviewer asks. Negative `mu` still returns `nan`.
- Why log-space terms rather than the "safe where" (clamping `mu` per branch): clamping would need one guard per branch and would still leave `entr`'s infinite derivative reachable for a small `mu` inside the small-`mu` branch itself (`k = 34` with `mu = 1e-3` underflows in float32, which is exactly the reported small-`mu` NaN); computing from the finite log PMF removes the `inf` at its source with a single helper.
- No CHANGELOG entry: the unreleased "Bug fixes" section lists only core `jax.numpy`/`jax.lax` items and previous `jax.scipy.stats` fixes added none. Suggested text if asked: "Fixed NaN gradients of {func}`jax.scipy.stats.poisson.entropy` for large and small `mu` ({jax-issue}`#40969`)."
- Environment: Python 3.12 venv with pip `jaxlib==0.11.2` and the branch's pure-Python `jax/` on `PYTHONPATH`; no jaxlib build.
