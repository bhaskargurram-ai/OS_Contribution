# onnxruntime #32802 — quant_pre_process loses optimizer results when shape inference stages are skipped

**Status:** branch pushed (commit `0cfb994`), PR not yet opened
**Branch:** `bhaskargurram-ai/onnxruntime` → `fix/quant-pre-process-skip-shape-inference`
**Open the PR:** https://github.com/microsoft/onnxruntime/compare/main...bhaskargurram-ai:onnxruntime:fix/quant-pre-process-skip-shape-inference?expand=1

Title:

```
Keep optimized model in quant_pre_process when shape inference is skipped
```

Body (paste as-is):

---

### Description

Fixes #32802.

`quant_pre_process` (`onnxruntime/python/tools/quantization/shape_inference.py`) runs three optional stages: symbolic shape inference, ORT graph optimization, and ONNX shape inference. The optimizer writes its result to `optimized.onnx` in a temporary directory and stores that path in `input_model`, but the in-memory `model` variable was only cleared to `None` when symbolic shape inference had run (because that is where the model was written out for the optimizer), and the optimized file was only loaded back into `model` inside the ONNX shape inference stage.

With optimization enabled this produced two failure modes, depending on which shape-inference stages were skipped:

- `skip_onnx_shape=True, skip_symbolic_shape=False`: `model` was `None`, and the fallback `onnx.load(input_model)` ran after the `with tempfile.TemporaryDirectory()` block had exited, so it tried to read `.../optimized.onnx` from a directory that no longer existed and raised `FileNotFoundError`.
- `skip_symbolic_shape=True` (with either value of `skip_onnx_shape`): `model` still held the unoptimized model. Either the ONNX shape inference stage re-saved that stale `model` over `input_model` (discarding the optimized file), or the final `if model is None` fallback was never taken. Either way the saved output was the original, unoptimized graph.

Only the default combination (`skip_onnx_shape=False, skip_symbolic_shape=False`) carried the optimizer output through.

Before / after with an `Identity -> Add` model (`skip_optimization=False`; the basic ORT optimizer removes the `Identity`):

| `skip_onnx_shape` | `skip_symbolic_shape` | main | this PR |
| --- | --- | --- | --- |
| False | False | ok, `['Add']` | ok, `['Add']` |
| False | True | `['Identity', 'Add']` (optimization lost) | ok, `['Add']` |
| True | False | `FileNotFoundError: .../optimized.onnx` | ok, `['Add']` |
| True | True | `['Identity', 'Add']` (optimization lost) | ok, `['Add']` |

With `skip_optimization=True` all four combinations return `['Identity', 'Add']` before and after, as expected.

### Change

- After the optimizer session has been created successfully, set `input_model = opt_model_path` **and** `model = None`, so every later stage and the final save use the optimized file regardless of whether symbolic shape inference ran.
- Move the `if model is None: model = onnx.load(input_model)` fallback inside the `with tempfile.TemporaryDirectory()` block, so a model that lives in the temporary directory is loaded before the directory is removed.
- The `input_model = opt_model_path` assignment now only happens when optimization succeeded (it is inside the `try`). Previously, on optimizer failure, the code either pointed at a nonexistent `optimized.onnx` (raising a confusing `ValidationError`/`FileNotFoundError` later) or silently continued with the unoptimized model, depending on `skip_symbolic_shape`. Now it consistently carries the pre-optimization model forward after logging the failure, which matches the existing "Consider rerun with option `--skip_optimization`" message.

### Motivation and Context

Users who disable one of the shape-inference stages (for example `skip_symbolic_shape=True` to avoid the `sympy` dependency, or `skip_onnx_shape=True` for large models) either got a crash or silently lost the optimizer's work, which reduces the effectiveness of subsequent quantization.

### Tests

Added `TestSkipShapeInferenceKeepsOptimization` to `onnxruntime/test/python/quantization/test_quant_preprocess.py`. It builds an `Identity -> Add` model with `onnx.helper`, runs `quant_pre_process` for all 8 combinations of `skip_optimization` / `skip_onnx_shape` / `skip_symbolic_shape` (as `subTest`s), and asserts that the saved model exists, contains `Add`, and contains `Identity` iff `skip_optimization=True`.

On `main` the test fails in 3 of the 8 subtests (`FileNotFoundError` for `skip_onnx_shape=True, skip_symbolic_shape=False`; `'Identity' unexpectedly found` for the two `skip_symbolic_shape=True` combinations). With this change all 8 pass.

Commands run (from `onnxruntime/test/python/quantization/`, using the released `onnxruntime` 1.30.0 / `onnx` 1.23.0 wheels with the source tree's `quantization` package overlaid):

- `python -m pytest -q test_quant_preprocess.py test_quant_issues.py` → 7 passed, 8 subtests passed
- `ruff check onnxruntime/python/tools/quantization/shape_inference.py onnxruntime/test/python/quantization/test_quant_preprocess.py` → All checks passed
- `ruff format --check` on the same two files → 2 files already formatted
- `lintrunner --take RUFF,RUFF-FORMAT <both files>` → ok No lint issues

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests listed above, and can defend the change.

---

## Verification performed

- Cloned the fork (`--depth 50 --filter=blob:none`, HEAD `4c86862`, i.e. current upstream `main`), branch `fix/quant-pre-process-skip-shape-inference`.
- Did NOT build onnxruntime. Created a uv venv (python 3.11) with `onnxruntime==1.30.0`, `onnx==1.23.0`, `numpy==2.4.6`, `sympy`, `pytest`, `ruff==0.12.12`, `lintrunner==0.13.1`, `lintrunner-adapters==0.14.1`. Overlay method: moved `site-packages/onnxruntime/quantization` to `quantization.bak` and symlinked the clone's `onnxruntime/python/tools/quantization` in its place (verified `onnxruntime.quantization.shape_inference.__file__` resolves into the clone). The venv was deleted after finishing.
- Note: the released ORT 1.30.0 wheel rejects the IR version that `onnx` 1.23's `onnx.helper.make_model` assigns by default (`[ONNXRuntimeError] : 1 : FAIL : Load model ... failed: Unsupported model IR version: <n>, max supported IR version: <n-1>`), which makes the optimizer stage fail and hides the bug behind a different error. The repro and the new test therefore pin `ir_version=9`, as other tests in that directory do (`test_conv_dynamic.py`, `bench_matmul_2bits.py`). Upstream CI builds ORT from source against a matching onnx, so this does not affect the test there.
- Repro script (`Identity -> Add`, all 8 flag combinations) before the fix:
  - `(skip_opt=F, skip_onnx=F, skip_sym=F)`: ok, `['Add']`
  - `(F, F, T)`: ok but `['Identity', 'Add']` (optimization lost)
  - `(F, T, F)`: `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pre.quant.xxx/optimized.onnx'`
  - `(F, T, T)`: ok but `['Identity', 'Add']` (optimization lost)
  - all `skip_opt=T`: `['Identity', 'Add']`
- After the fix: all `skip_opt=F` combinations give `['Add']`; all `skip_opt=T` give `['Identity', 'Add']`. Also checked the same 8 combinations with a `ModelProto` passed as `input_model` instead of a path: same results.
- New test on `main` (fix stashed): `3 failed, 4 passed, 5 subtests passed`; with the fix: `7 passed, 8 subtests passed` (together with `test_quant_issues.py`).
- `test_quant_issues.py::test_qnn_preprocess_...`-style tests that need on-disk model files are skipped in this environment; the ones that ran passed.
- Lint: `ruff check`, `ruff format --check`, and `lintrunner --take RUFF,RUFF-FORMAT` on the two changed files are clean (the repo uses ruff + ruff-format via `.lintrunner.toml`; there is no black/isort config).
- The assignment named the test file `test_quant_pre_process.py`; the repo's existing file is `test_quant_preprocess.py`, so the test was added there.
- Behaviour change a reviewer may ask about: on optimizer *failure* the code now always continues with the un-optimized model instead of pointing at a nonexistent `optimized.onnx`. This was already the (silent) behaviour for `skip_symbolic_shape=True`; for `skip_symbolic_shape=False` it previously crashed later with a confusing `ValidationError: Unable to open proto file .../optimized.onnx`.
- Not touched: the unreachable `isinstance(input_model, onnx.ModelProto)` branch inside the ONNX-shape-inference stage, and the fact that `extract_raw_data_from_model` mutates a caller-supplied `ModelProto` when `skip_symbolic_shape=True` — both pre-existing and out of scope.

## Round 2

**PR:** microsoft/onnxruntime#32830 — Copilot review flagged one high-severity finding on `shape_inference.py`: when `input_model` is a `ModelProto` and optimizer session creation fails, the fallback carries forward a corrupted model because `extract_raw_data_from_model(input_model)` mutates the same object held by `model`.

**New commit:** `81eedc9` ("Keep the original ModelProto when the optimizer fails in quant_pre_process"), pushed on top of `0cfb994` to `bhaskargurram-ai/onnxruntime:fix/quant-pre-process-skip-shape-inference` (no rebase, no force-push).

### What changed

- `onnxruntime/python/tools/quantization/shape_inference.py`: in the `isinstance(input_model, onnx.ModelProto)` branch of the optimizer stage, `extract_raw_data_from_model` now runs on `copy.deepcopy(input_model)` (`session_model`), and `session_model.SerializeToString()` is what goes to `InferenceSession`. `model`/`input_model` keep the untouched proto, so the `except` fallback (and the caller's own object) are intact. Added `import copy`. Success path unchanged: the session gets the same serialized-without-raw-data bytes plus the same `add_external_initializers` OrtValues as before, and the optimized file is written to the temp dir and loaded back before the `TemporaryDirectory` exits.
- `onnxruntime/test/python/quantization/test_quant_preprocess.py`: new `TestOptimizerFailureKeepsModelProtoInput` next to `TestSkipShapeInferenceKeepsOptimization`. It builds an `Identity -> Add` ModelProto with a raw-data `bias` initializer, patches `onnxruntime.InferenceSession` to raise, calls `quant_pre_process(input_model=<ModelProto>, skip_optimization=False)` for all 4 `skip_onnx_shape` x `skip_symbolic_shape` combinations (subTests), and asserts: the caller's initializer still has `raw_data` and is not `EXTERNAL`; the saved model exists, `onnx.load`s, passes `onnx.checker.check_model`, has nodes `["Identity", "Add"]`, and its initializer is not `EXTERNAL` and equals the original values.

### Reproduction (before the fix, commit `0cfb994`)

ModelProto input, `InferenceSession` patched to raise, `skip_optimization=False`:

- `skip_symbolic_shape=False` (either `skip_onnx_shape`): ok — symbolic shape inference returns a new proto and writes it to a file, so the ModelProto branch is not taken.
- `skip_onnx_shape=False, skip_symbolic_shape=True`: `ValidationError: Data of TensorProto ( tensor name: bias) should be stored in /tmp/pre.quant.xxx/foo.bin, but it is not regular file.` raised from inside `quant_pre_process` (the ONNX shape inference stage saves and reloads the mutated proto).
- `skip_onnx_shape=True, skip_symbolic_shape=True`: call returns, but the caller's initializer has `data_location=EXTERNAL`, `raw_data` cleared, `external_data=[('location', 'foo.bin')]`; the saved output has the same, and `onnx.load(output)` raises the same `ValidationError`.

After the fix all four combinations return, the caller's proto has `data_location=DEFAULT` with `raw_data` present, and the saved model loads with the original `bias` values. Also re-checked the ModelProto *success* path (no patch) for the same 4 combinations: output is `['Add']` with the correct `bias`, `check_model` passes.

Note: this mutation predates the PR (the ModelProto branch and `extract_raw_data_from_model` are unchanged on `main`); the previous round's notes listed it as pre-existing/out of scope, but since the PR makes the fallback path the deliberate behaviour on optimizer failure, it is fair to fix it here.

### Test / lint results

Same overlay setup as round 1 (uv venv, python 3.11, `onnxruntime==1.30.0`, `onnx==1.23.0`, `numpy`, `sympy`, `pytest`, `ruff==0.12.12`, `lintrunner`, `lintrunner-adapters`; `site-packages/onnxruntime/quantization` replaced by a symlink to the clone's package). Venv deleted afterwards.

- `python -m pytest -q test_quant_preprocess.py test_quant_issues.py` (from `onnxruntime/test/python/quantization/`) → 8 passed, 12 subtests passed
- New test with the fix stashed → `2 failed, 1 passed, 2 subtests passed` (the two `skip_symbolic_shape=True` subtests fail on `initializer.HasField("raw_data")`)
- `ruff check` on both changed files → All checks passed
- `ruff format --check` on both → 2 files already formatted
- `lintrunner --take RUFF,RUFF-FORMAT` on both → ok No lint issues

### Reply draft for the Copilot thread

Good catch, thanks. `extract_raw_data_from_model` does clear `raw_data` in place and point the initializers at a placeholder `foo.bin`, so with a `ModelProto` input and `skip_symbolic_shape=True` a failed session creation left both the fallback model and the caller's proto referencing a file that does not exist. Fixed in 81eedc9 by running the extraction on a `copy.deepcopy` of the proto and serializing that copy for the session; the original is kept for the fallback path and the success path is unchanged. Added `TestOptimizerFailureKeepsModelProtoInput`, which forces `InferenceSession` to raise with a ModelProto input and checks that the caller's initializers keep their raw data and that the saved model loads, passes the checker and matches the input, for both `skip_symbolic_shape` values.
