# candle #3707 — CPU quantized matmul has no batch path: prefill runs at token-at-a-time speed

**Status:** branch pushed (commit `SHA7_PLACEHOLDER`), PR not yet opened
**Branch:** `bhaskargurram-ai/candle` → `fix/cpu-quantized-matmul-batched-prefill`
**Open the PR:** https://github.com/huggingface/candle/compare/main...bhaskargurram-ai:candle:fix/cpu-quantized-matmul-batched-prefill?expand=1

Title:

```
Tile lhs rows in the generic CPU quantized matmul for prefill
```

Body (paste as-is):

---

Fixes #3707.

`k_quants::matmul` (the generic CPU quantized matmul that `QTensor::fwd` falls back to whenever no
repacked kernel applies) walks the input rows in an outer loop and, for each row, dispatches the
weight column quads to the thread pool. With `m` prefill rows every weight block is therefore
re-read from memory `m` times and the pool is dispatched `m` times, so throughput per row stays at
the `m = 1` decode level: for a 8184 x 8192 Q4K weight (38 MB, larger than the LLC) the machine
below does 581 rows/s at `m = 1` and 587 rows/s at `m = 128`.

Since #3697/#4000 the repacked kernels already give x86 (Q4K/Q6K/Q8_0 with `n % 16 == 0`,
`k % 256 == 0`) and aarch64 (Q4_0/Q4K/Q5K/Q6K/Q8_0) a real GEMM tile, so this change only targets
what is left on the generic path: the remaining GGML types (Q4_0/Q4_1/Q5_0/Q5_1/Q8_1/Q2K/Q3K/Q5K
on x86, Q4_1/Q5_0/Q5_1/Q8_1/Q2K/Q3K everywhere), shapes the packers reject (`n` not a multiple of
the tile, `k` not a multiple of 256), and other targets (wasm simd128, plain scalar).

### Change

`candle-core/src/quantized/k_quants.rs`, `matmul`:

- The `m == 1` decode path is unchanged: one pool dispatch over the column quads (still
  `execute_static` for Q6K on x86_64, `execute_chunked` otherwise), then the `n % 4` tail.
- For `m > 1` the work items are now `(row tile, column quad)` pairs, row-tile major, in a single
  `execute_chunked` dispatch. A worker walking its range keeps one tile of 16 quantized lhs rows
  hot in cache and streams each weight quad once per tile instead of once per row. 16 is the
  src1 row block that `ggml_compute_forward_mul_mat` uses; 8/16/32 measured within a few percent
  of each other, 16 was marginally the best. The `n % 4` tail columns get a second small dispatch
  over the rows.
- Every output element is still produced by the same `vec_dot_4` / `vec_dot_2` / `vec_dot`
  call on the same inputs, only the loop order changes, so the results are bit-identical to the
  previous code and to running the rows one at a time.

The repacked paths and `matmul_f16` are untouched.

### Measurements

`cargo test -p candle-core --release --test quantized_tests -- --ignored --nocapture bench_qmatmul_prefill_cpu`
on a 4-core Intel Xeon @ 2.8 GHz (AVX512-VNNI, 33 MB L3), rows/s of `QMatMul::forward` for a
random `(m, k)` f32 input against a random `(n, k)` weight, median of the runs I did:

| weight (generic path) | m=1 before → after | m=32 before → after | m=128 before → after | m=512 before → after |
|---|---|---|---|---|
| Q4K 8184x8192 (38 MB, > L3) | 581 → 541 | 587 → 848 (1.44x) | 587 → 833 (1.42x) | – |
| Q8_0 8184x8192 (71 MB, > L3) | 255 → 257 | 277 → 398 (1.44x) | 273 → 396 (1.45x) | – |
| Q4K 2040x2048 (2.3 MB) | 10262 → 7931 | 10991 → 12147 (1.11x) | 10559 → 13076 (1.24x) | 11004 → 12294 (1.12x) |
| Q2K 2048x2048 (1.4 MB) | 12438 → 10978 | 13441 → 13843 | 12700 → 15514 (1.22x) | 13007 → 15461 (1.19x) |
| Q5K 2048x2048 (2.9 MB) | 11017 → 7742 | 11127 → 10973 | 11597 → 11639 | 10891 → 12019 (1.10x) |
| Q4_0 2048x2048 (2.4 MB) | 5665 → 4791 | 5633 → 5342 | 5927 → 5856 | 5446 → 5534 |

| weight (x86 repacked path, unchanged code) | m=1 | m=128 |
|---|---|---|
| Q4K 2048x2048 | 10603 → 12850 | 31280 → 31628 |
| Q8_0 2048x2048 | 12691 → 12438 | 34380 → 34987 |

The `m = 1` column goes through the unchanged decode branch; its spread (±30 % between runs of the
same binary) is the noise floor of this shared VM for a 0.1 ms call.

So the loop reorder fixes the "prefill runs at decode speed" symptom only where the issue's
premise holds, i.e. the weight does not fit in the last-level cache: there each row tile reads the
weight once instead of `m` times and throughput goes up ~1.45x. When the weight is LLC-resident
(everything up to ~30 MB on this box) the generic path is bound by the per-element `vec_dot`
kernel, and reordering loops gains 0–25 %. Closing the remaining ~3x gap to the repacked kernels
needs kernels that reuse the unpacked weight block across several lhs rows (a multi-row
`vec_dot`), which is a per-type SIMD change rather than a loop-order one.

### Tests

- `qmatmul_batched_rows_match_single_row_cpu` (new, `candle-core/tests/quantized_tests.rs`):
  for all 15 GGML types and `m` in {2, 3, 4, 7, 8, 9, 16, 17, 33, 64} against a 23 x 512 weight
  (`n = 23` keeps every architecture on the generic path), asserts with `assert_eq!` that the
  batched output equals the single-row output row by row. It passes on `main` too (the old loop
  order satisfied it), and pins down the bit-identical guarantee that the tiled order must keep.
- `bench_qmatmul_prefill_cpu` (new, `#[ignore]`): the timing harness above.
- `cargo test -p candle-core --release --test quantized_tests`: 53 passed, 1 ignored.
- `cargo test -p candle-core --test quantized_tests`: DEBUG_QT_PLACEHOLDER
- `cargo test -p candle-core --lib`: DEBUG_LIB_PLACEHOLDER
- `cargo fmt --all -- --check`: clean.
- `cargo clippy -p candle-core --all-targets -- -D warnings`: clean.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced the issue on `main` with the new `bench_qmatmul_prefill_cpu` harness: on the generic
  path rows/s at `m = 128` equals rows/s at `m = 1` (Q4K 8184x8192: 581 vs 587; Q4K 2040x2048:
  10262 vs 10559; Q5K: 11017 vs 11597), i.e. prefill runs at decode speed. On the x86 repacked
  path (Q4K/Q8_0 2048x2048) `main` already reaches ~3x that, because #3697/#4000 landed after the
  issue was filed.
- Tile-size sweep (temporary env override, removed before committing) for tiles 1/4/8/16/32:
  in-cache shapes are within noise of each other; for the 38 MB / 71 MB weights tile 1 (= old
  order) gives 560 / 279 rows/s at `m = 128`, tile 8 gives 789–801 / 366–382, tile 16 gives
  850 / 392, tile 32 gives 854–862 / 386–410. Picked 16 (ggml's `blck_1`).
- `qmatmul_batched_rows_match_single_row_cpu` passes in both release and debug with the change; it
  also passes on `main` (invariance test, not a fail-before test). The exact-equality assertion
  is what would catch any accidental change in how an element is computed.
- Full `candle-core` quantized test file in release and debug, `candle-core` lib tests, `cargo fmt
  --check`, `cargo clippy -p candle-core --all-targets -D warnings` (results listed above).
- Not run: CUDA/Metal/MKL features (CPU-only container); aarch64 (the new test keeps `n = 23` so
  it exercises the generic path there too, but only x86_64 was executed); GGUF end-to-end model
  timing (huggingface.co is blocked here, the harness constructs weights via `QTensor::quantize`).
- Reviewer question to expect: the `dst` writes go through a raw pointer shared by the workers.
  Each `(row, column)` is written by exactly one work item (row tiles partition the rows, quads
  partition the columns, the tail dispatch writes only columns `>= n_quad`), which is the same
  argument the previous code relied on for its per-row `main_ptr`.

## Caveat

This is a larger change than a one-line bug fix and its benefit is conditional (material only for
weights larger than the LLC; 0–25 % otherwise, and the real prefill gap on the generic path needs
multi-row `vec_dot` kernels). The user will confirm the approach with the maintainers (e.g. on the
issue) before opening the PR. Candle's `CONTRIBUTING`/PR template does not forbid AI-assisted PRs
(there is no PR template in the repo).
