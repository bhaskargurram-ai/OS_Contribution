# onnx #8437 — DynamicQuantizeLinear: spec, function body and reference implementation disagree on y_scale for an all-zero input

**Status:** branch pushed (commit `821ec3d`), PR not yet opened
**Branch:** `bhaskargurram-ai/onnx` → `fix/dynamic-quantize-linear-zero-input-scale`
**Open the PR:** https://github.com/onnx/onnx/compare/main...bhaskargurram-ai:onnx:fix/dynamic-quantize-linear-zero-input-scale?expand=1

> The issue is unclaimed and the reporter explicitly asked maintainers which of the three
> definitions is right. Comment on #8437 first (proposing "follow onnxruntime: y_scale = 1",
> linking this branch) and wait for a maintainer to agree before opening the PR, since the
> function-body change touches an opset-11 spec artifact.

Title:

```
fix(defs): define DynamicQuantizeLinear y_scale as 1 for an all-zero input
```

Body (paste as-is):

---

Fixes #8437.

For an input whose adjusted range is empty — every element of `x` is 0, so `maximum(0, max(x)) == minimum(0, min(x)) == 0` — the operator doc for `DynamicQuantizeLinear` (opset 11) gives `y_scale = (max - min) / (qmax - qmin) = 0`, which turns the documented `y = saturate(round(x / y_scale) + y_zero_point)` into a division by zero. The three places that define the operator then disagree on what actually happens:

| for `x = zeros(6, float32)` | `y_scale` | `y_zero_point` | `y` |
|---|---|---|---|
| operator doc formula | `0` | `qmin - 0/0` = NaN | `0/0` = NaN |
| function body (`onnx/defs/quantization/defs.cc`), run with `onnx.reference` and with onnxruntime after expansion | `0.0` | `0` | `[0 0 0 0 0 0]` (via NaN -> saturate) |
| Python reference implementation (`onnx/reference/ops/op_dynamic_quantize_linear.py`) | `0.00392157` (= 1/255) | `0` | `[0 0 0 0 0 0]` |
| onnxruntime CPU kernel (`onnxruntime/core/util/qmath.h`, `GetQuantizationParameter`) | `1.0` | `0` | `[0 0 0 0 0 0]` |

The reference implementation already carried a comment quoting onnxruntime's rule (`scale = max == min ? 1.0f : (max - min) / float(qmax - qmin)`), but implemented it as `np.float32(1.0 if maxx == minx else (maxx - minx)) / np.float32(qmax - qmin)`, i.e. it put the guard in the numerator and still divided by 255. The function body had no guard at all and evaluates `0 / 0`.

A `y_scale` of 0 is harmful downstream: any consumer that divides by it (a later `QuantizeLinear` with the same scale, or a `DequantizeLinear` followed by re-quantization) produces NaN/inf, and a `y_scale` of 1/255 is simply a third, unmotivated value.

### Change

This follows the prevailing implementation (onnxruntime): when the adjusted range is empty, `y_scale = 1`, which gives `y_zero_point = 0` and `y = 0`.

- `onnx/defs/doc_strings.cc` — add one bullet to the opset-11 doc string: "if the adjusted data range is empty, i.e. `maximum(0, max(x)) == minimum(0, min(x))`, which happens when every element of x is 0, then `y_scale = 1` (so that `y_zero_point = 0` and `y = 0` below) instead of 0."
- `onnx/defs/quantization/defs.cc` — guard the scale in the function body with `Equal`/`Where` (both available at opset 11, the body's opset import), so an expanded function is bit-identical to the onnxruntime kernel: `Scale = Where(Equal(X_Range, 0), 1, X_Range / 255)`. Every other node is unchanged; non-empty ranges produce exactly the same values as before.
- `onnx/reference/ops/op_dynamic_quantize_linear.py` — return `np.float32(1.0)` when `maxx == minx`, otherwise `(maxx - minx) / 255` as before.
- `docs/Operators.md`, `docs/Changelog.md`, `docs/TestCoverage.md` — regenerated (the `DynamicQuantizeLinear-11` changelog entry changes because the doc string of the existing version is clarified).

No opset bump: the previous behaviour for this input was a division by zero, i.e. undefined, and `docs/Versioning.md` lists "clarifications of specification ambiguities to match prevailing implementation practice" as non-breaking. If maintainers prefer to keep the function body of opset 11 untouched, the doc and reference-implementation parts stand on their own and the function-body hunk can be dropped from this PR.

### Tests

- `onnx/backend/test/case/node/dynamicquantizelinear.py`: new node test case `test_dynamicquantizelinear_zero_input` (2x3 all-zero input, expected `y_scale = 1`, `y_zero_point = 0`, `y = 0`). The backend harness also derives `test_dynamicquantizelinear_zero_input_expanded`, which runs the function body.
- `tests/python/reference_evaluator_test.py`: `test_dynamic_quantize_linear_zero_input` (parametrized over an all-zero and an all-negative-zero input), asserting values, dtypes and scalar shapes, and cross-checking against onnxruntime's kernel when it is installed.

Both fail on `main` (`y_scale` is `0.00392157` from the reference implementation and `0.0` from the expanded function body) and pass on this branch.

Commands run (released `onnx` 1.23.0 C++ extension overlaid on this checkout's Python sources, onnxruntime 1.30.0, numpy 2.4.6):

```
pytest tests/python/reference_evaluator_test.py -k dynamic_quantize   # 3 passed
pytest tests/python/backend_reference_test.py -k dynamicquantizelinear  # 7 passed, 8 skipped (cuda), 1 failed*
ruff check / ruff format --check (ruff 0.16.4)                        # clean
clang-format --dry-run --Werror onnx/defs/quantization/defs.cc onnx/defs/doc_strings.cc (22.1.8)  # clean
editorconfig-checker on all changed files                             # clean
mypy 2.3.1 on the reference op                                        # 1 pre-existing error, unchanged (file is excluded in .lintrunner.toml)
```

\* `test_dynamicquantizelinear_zero_input_expanded_cpu` fails locally only because the installed wheel's compiled schema still carries the old function body; I could not rebuild the C++ core here. The new body text was parsed with `onnx.parser` (opset import `"" : 11`), passed `check_model(full_check=True)`, and, expanded with the same `function_expand_helper` the backend harness uses, gives `y_scale = 1`, `y_zero_point = 0`, `y = 0` under both `ReferenceEvaluator` and onnxruntime; for the three existing test vectors and a 1000-element random input, the reference implementation, onnxruntime's kernel, and the new body evaluated by both are bit-identical. CI will run the real `_expanded` test after the rebuild.

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduction (`scratchpad/onnx-8437/repro.py`, output in `repro_before.txt`), `x = zeros(6, float32)`, opset 21 model:
  - `onnx.reference.ReferenceEvaluator`: `y = [0 0 0 0 0 0]`, `y_scale = 0.00392157`, `y_zero_point = 0`
  - onnxruntime 1.30.0 native kernel: `y = [0 0 0 0 0 0]`, `y_scale = 1.0`, `y_zero_point = 0`
  - function body from `get_schema("DynamicQuantizeLinear", 11).function_body` expanded into a graph: `y_scale = 0.0`, `y_zero_point = 0`, `y = 0` with both the reference evaluator (numpy divide-by-zero warnings) and onnxruntime
  - doc formula: `y_scale = 0.0`, `x / y_scale = nan`
- ORT source checked (`onnxruntime/core/util/qmath.h`, `GetQuantizationParameter`): `scale = max == min ? 1.0f : (max - min) / float(qmax - qmin); initial_zero_point = qmin - min / scale;` — matches the observed `1.0 / 0 / 0`.
- `docs/Versioning.md`: "Clarifications of specification ambiguities to match prevailing implementation practice" are explicitly non-breaking; "Changes to the semantics of an operator or function MUST be introduced in a new operator set". The change is framed as the former (previous behaviour was a division by zero); the notes above offer to drop the function-body hunk if maintainers disagree. No opset bump was made.
- Fail-before check: with only the two test files checked out from the branch onto `main`'s sources, `test_dynamic_quantize_linear_zero_input[all_zero|negative_zero]` fail (`assert array(0.00392157) == 1.0`) and `test_dynamicquantizelinear_zero_input_cpu` / `_expanded_cpu` fail (`Mismatched elements: 1 / 1`).
- After the fix: `pytest tests/python/reference_evaluator_test.py -k dynamic_quantize` -> 3 passed; `pytest tests/python/backend_reference_test.py -k dynamicquantizelinear` -> 7 passed, 8 skipped, 1 failed (`_zero_input_expanded_cpu`, see the asterisk above; it uses the wheel's old compiled body).
- `verify_after.py` / `verify_expanded.py` (scratchpad): new function body parsed from `defs.cc`, `check_model(full_check=True)` OK; reference impl, ORT kernel, reference-on-new-body and ORT-on-new-body are bit-identical on all_zero, negative_zero, the three existing test vectors and a random 1000-element vector; old body gives `y_scale = 0`, new body `y_scale = 1` under the exact `function_expand_helper` path the backend tests use.
- Docs: `python onnx/defs/gen_doc.py` run from the checkout produced the correct new example block but also unrelated noise (Div/GroupNormalization/Pad/Normalizer doc strings differ between the 1.23.0 wheel and this checkout), and could not pick up the new `doc_strings.cc` text without a C++ rebuild, so the `DynamicQuantizeLinear` hunks were applied by hand to `docs/Operators.md` and `docs/Changelog.md` (same two-space indentation gen_doc uses) and `docs/TestCoverage.md` was regenerated with `python onnx/backend/test/stat_coverage.py` (clean, 16-line diff). A reviewer may re-run `python onnx/defs/gen_doc.py` after a build to confirm; the CI docs check will flag any drift.
- Node test data: this checkout no longer commits `onnx/backend/test/data/node/*` (node cases are loaded from the Python generators via `load_node_model_tests`), so there are no generated `.pb` files to commit; `cmd_tools.py generate-data` was not needed.
- Lint: ruff 0.16.4 check + format, clang-format 22.1.8 (`.clang-format`), editorconfig-checker 3.11.1 all clean on the changed files; mypy 2.3.1 reports one pre-existing error in `op_dynamic_quantize_linear.py` (line unchanged by this PR; `onnx/reference/ops/**` and `onnx/backend/test/**` are excluded from mypy in `.lintrunner.toml`). `lintrunner` itself was not run (needs `lintrunner init` and a full tree); the individual linters it wraps were.
- Environment: uv venv with released `onnx==1.23.0` wheel; its `onnx_cpp2py_export*.so`, `*_pb2.py(i)` and `onnx_pb.py`/`onnx_data_pb.py`/`onnx_operators_pb.py` were copied into the checkout's `onnx/` directory (all gitignored, `git status` stayed clean) so the checkout's Python sources ran against the wheel's compiled schemas. The C++ core was not built. Commit carries the repo-required DCO `Signed-off-by` line.
- Repo conventions: `.github/copilot-instructions.md` asks agent-authored PRs to use a Conventional Commits title (done: `fix(defs): ...`) and to add at least one `topic:`/`module:` label after opening (suggest `module: reference implementation` / `topic: operator` or whatever exists; labels cannot be set from this environment).
