# text-embeddings-inference #880 — te_queue_size metric does not increase when requests are appended to the queue

**Status:** branch pushed (commit `ba21e86`), PR not yet opened
**Branch:** `bhaskargurram-ai/text-embeddings-inference` → `fix/queue-size-metric-on-append`
**Open the PR:** https://github.com/huggingface/text-embeddings-inference/compare/main...bhaskargurram-ai:text-embeddings-inference:fix/queue-size-metric-on-append?expand=1

Title:

```
Keep requests in te_queue_size until their batch is dispatched
```

Body (paste as-is):

---

# What does this PR do?

Fixes #880.

`te_queue_size` is meant to report the number of requests waiting for inference, but under load it almost always reads 0. The gauge was incremented on `Queue::append` and then reset to `entries.len()` every time `next_batch` pulled a batch out of the internal `VecDeque`. The batching task (`core/src/infer.rs`) calls `next_batch` as soon as it can reserve a slot on the capacity-1 prefetch channel, and with the default batching limits (`max_batch_tokens = 16384`, no `max_batch_requests`) a whole wave of concurrent requests is moved into a single batch at once.

Those requests are still waiting for the backend, but they now live in the prefetch channel instead of the queue's `VecDeque`, so the gauge was set back to 0 microseconds after they were appended. A Prometheus scrape during sustained load therefore showed no backlog, which is the symptom reported in the issue.

### Change

- `core/src/queue.rs`: a request stays counted in `te_queue_size` from `append` until the batch it belongs to is handed over to the backend. The `NextBatch` branch no longer resets the gauge to `entries.len()`; entries discarded because the client dropped the request before it was batched decrement the gauge individually (they were already counted as `te_request_failure{err="dropped"}`). A new `pub(crate) fn record_batch_dispatched(batch_size)` decrements the gauge by the batch size and documents the metric semantics.
- `core/src/infer.rs`: `backend_task` calls `record_batch_dispatched` when it receives a batch from the prefetch channel, i.e. right before handing it to the backend.
- `core/Cargo.toml` / `Cargo.lock`: `metrics-util` (already in the lockfile as a dependency of `metrics-exporter-prometheus`) is added as a dev-dependency of `text-embeddings-core` with only the `debugging` feature, for the `DebuggingRecorder` used by the tests. The lockfile diff is three lines.

| Scenario (4 requests appended, backend busy) | `te_queue_size` before | after |
|---|---|---|
| after the 4 appends, before any batch is pulled | 4 | 4 |
| after the batching task pulled them into one prefetched batch (still waiting for the backend) | 0 | 4 |
| after the backend task takes the batch for inference | 0 | 0 |
| 1 of 2 queued requests dropped by the client, other one batched but not yet dispatched | 0 | 1 |

### Tests

Two unit tests added in `core/src/queue.rs` (`queue::tests`). They install a `metrics_util::debugging::DebuggingRecorder` as the global recorder and read the gauge from a snapshot:

- `test_queue_size_counts_batched_requests_until_dispatched`: append 4 entries, pull them into one batch, check the gauge still reports 4, dispatch, check 0.
- `test_queue_size_accounts_for_partial_batches_and_dropped_requests`: 4 entries with room for 2 per batch, one dropped by the client; checks the gauge after each batch is pulled and dispatched.

With the previous accounting (gauge reset to `entries.len()` on drain) both tests fail (`left: 0.0, right: 4.0` and `left: 0.0, right: 1.0`); with this change they pass.

Commands run (the backend crate has no model backend in its default features, so the core crate does not compile without one):

- `cargo test -p text-embeddings-core --features text-embeddings-backend/candle,hf-hub/ureq queue::` → 2 passed, 0 failed
- `cargo test -p text-embeddings-core --features text-embeddings-backend/candle,hf-hub/ureq` → 2 passed, 1 failed: the pre-existing `tokenization::tests::tokenizer` fails in my sandbox with `ProxyConnect` while downloading `BAAI/bge-m3` from the Hub (no network access), unrelated to this change
- `cargo clippy -p text-embeddings-core --features text-embeddings-backend/candle,hf-hub/ureq --all-targets` → no warnings
- `rustfmt --edition 2021 --check core/src/queue.rs core/src/infer.rs` → clean (`cargo fmt --all -- --check` needs the generated gRPC `pb` modules, i.e. `protoc`, which is not available in my sandbox)

## Before submitting

- [ ] This PR fixes a typo or improves the docs (you can dismiss the other checks if that's the case).
- [x] Did you read the [contributor guideline](https://github.com/huggingface/text-embeddings-inference/blob/main/CONTRIBUTING.md)?
- [x] Was this discussed/approved via a GitHub issue or the [forum](https://discuss.huggingface.co/)? Please add a link to it if that's the case. → #880
- [x] Did you make sure to update the documentation with your changes? The metric is not described in the docs; its semantics are documented on `record_batch_dispatched` in `core/src/queue.rs`.
- [x] Did you write any new necessary tests? If applicable, did you include or update the `insta` snapshots? No snapshot changes.

## Who can review?

@Narsil @alvarobartt

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Read the issue text via the GitHub issue page: "te_queue_size does not reliably reflect queue growth ... does not increase despite visible queueing" (TEI 1.4, Docker, looped concurrent curl calls).
- Established with `git log -S` that the `Append` branch has incremented the gauge since v0.1.0 (`metrics::increment_gauge!`, later `gauge.increment(1.0)` in #307), so "never incremented on append" is not the mechanism. The gauge always equalled `entries.len()`; the problem is that `entries` is drained into the prefetch channel immediately, so the gauge reads 0 while requests are still waiting.
- Toolchain: `rust-toolchain.toml` pins 1.92.0; installed it and used it for all commands.
- `cargo test -p text-embeddings-core` with default features does not compile on `main` either (`text-embeddings-backend` has no backend enabled: `DType::Float16` missing), and the core crate's own `tokenizer` test needs `hf-hub/ureq`. Used `--features text-embeddings-backend/candle,hf-hub/ureq` (CPU only, no CUDA/MKL). CI runs `cargo test --profile=release-debug` at the workspace level with the router's default features (`candle`), where both features are enabled.
- Before/after check: temporarily restored the old accounting (kept the helper and the tests) → both new tests fail with `left: 0.0`; restored the fix → both pass.
- `cargo clippy -p text-embeddings-core ... --all-targets`: no warnings. `rustfmt --check` on the two changed source files: clean. Trailing whitespace / end-of-file checks (pre-commit hooks) on changed files: clean.
- `Cargo.lock` diff is 3 lines (adds `metrics-util` under `text-embeddings-core` and `indexmap`/`ordered-float` under `metrics-util`; both crates were already locked). No `cargo update` was needed.
- Reviewer question to expect: this changes the semantics of `te_queue_size` from "entries not yet batched" to "requests not yet dispatched to the backend". The gauge is decrement-based now instead of reset on drain; every appended entry leaves the gauge exactly once (dropped at drain, or dispatched by `backend_task`). Entries pushed back into the queue because they do not fit the batch remain counted.
- Could not run the pre-existing `tokenization::tests::tokenizer` test (Hub download blocked by the sandbox proxy) nor `cargo fmt --all` (needs `protoc` for the generated `pb` modules).
- Deleted the 2.2 GB `target` directory after the run.
