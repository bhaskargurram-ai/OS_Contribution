# llama.cpp #29462 — json-schema/GBNF grammar builder does not bound the repetition count (contradictory `min*` OOM-kills the server)

**Status:** branch pushed (commit `9342769`), PR not yet opened
**Branch:** `bhaskargurram-ai/llama.cpp` → `fix/grammar-bound-repetition`
**Open the PR:** https://github.com/ggml-org/llama.cpp/compare/master...bhaskargurram-ai:llama.cpp:fix/grammar-bound-repetition?expand=1

Title:

```
grammar : reject repetition bounds with max < min
```

Body (paste as-is):

---

## Overview

Fixes #29462.

`llama_grammar_parser::parse_sequence` expands a `{m,n}` quantifier by generating `n - m` optional rules. `n_opt = max_times - min_times` is computed in `uint64_t`, so a quantifier whose upper bound is below its lower bound (`"a"{10,2}`) wraps around to ~2^64 and the loop keeps generating rules until the allocation fails. On a server without a memory limit that is an OOM kill; with `ulimit -v` it shows up as `std::bad_alloc` after several seconds. Nothing in the parser checked `max_times >= min_times`; the existing `MAX_REPETITION_THRESHOLD` check only looks at `max_times` (or `min_times` when there is no max) and passes for `{10,2}`.

The json-schema converter emits exactly that shape of quantifier for a contradictory schema: `minItems: 10, maxItems: 2` becomes `item ("," space item){9,1}` and `minLength: 10, maxLength: 2` becomes `char{10,2}`. The huge-lower-bound case from the issue (`minItems: 100000000`) was already rejected by the parser's `MAX_REPETITION_THRESHOLD` (2000) check before any allocation, so it only needed re-verification, not a change.

Measured with a small program that feeds the grammar to `llama_grammar_init_impl` (no model needed):

| input | master | this branch |
| --- | --- | --- |
| GBNF `root ::= "a"{10,2}` | ~5 GB RSS then `std::bad_alloc` under a 6 GB `ulimit -v` (~8 s); OOM-kill with no limit | parse error in <10 ms, 0 extra allocation |
| array `minItems: 10, maxItems: 2` | converter emits `{9,1}` → same blow-up in the parser | `JSON schema error at #: minItems must not be greater than maxItems` |
| string `minLength: 10, maxLength: 2` | converter emits `{10,2}` → same blow-up | `JSON schema error at #: minLength must not be greater than maxLength` |
| array `minItems: 100000000` | parse error "number of repetitions exceeds sane defaults" (already bounded) | unchanged |

### Change

- `src/llama-grammar.cpp`: `handle_repetitions` throws a parse error when a `{m,n}` quantifier has `n < m`, before any rule is generated. This covers hand-written GBNF too.
- `common/json-schema.cpp`: the schema document builder rejects `minItems > maxItems`, `minLength > maxLength` and `minimum > maximum` with the usual `JSON schema error at <path>: ...` message. The integer case did not allocate, but it silently produced a wrong grammar (`minimum: 10, maximum: 2` accepted `2` and `10..19`), so it is validated in the same place.

Both errors propagate the way existing schema/grammar errors do: `json_schema_to_grammar` wraps the `runtime_error` into `std::invalid_argument`, the server's request parser catches it and returns HTTP 400; a direct GBNF grammar fails in `common_sampler_init` and the slot returns 400 "Failed to initialize samplers".

### Tests

- `tests/test-grammar-parser.cpp`: `verify_failure` for `root ::= "a"{10,2}`. On master this test does not fail cleanly, it allocates until the machine or the test runner runs out of memory.
- `tests/test-json-schema-to-grammar.cpp`: `FAILURE` cases "minItems > maxItems", "minLength > maxLength", "minimum > maximum". On master the first two produce grammars with an inverted quantifier and the third produces a wrong grammar; all three now fail conversion as expected.

Commands (build with `-DLLAMA_BUILD_TESTS=ON`, no model):

```
cmake --build build --target test-json-schema-to-grammar test-grammar-parser test-grammar-integration -j2
./build/bin/test-grammar-parser            # exit 0
./build/bin/test-json-schema-to-grammar    # exit 0 (all cases incl. the 3 new FAILURE cases)
./build/bin/test-grammar-integration       # exit 0
```

## Additional information

The `at <pos>` suffix of the new parser message follows the other `handle_repetitions` errors; for a quantifier at the end of the rule the position text is empty, same as for the existing "expecting preceding item" error.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES - see below

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Reproduced on `master` (2145525) with a standalone program linking `libllama-common`/`libllama` (scratch file `repro_rep.cpp`, not committed): `root ::= "a"{10,2}` reached 4.99 GB RSS under a 6 GB `ulimit -v` and died with `parse: error parsing grammar: std::bad_alloc` after ~8 s; under 2 GB the same in ~8 s. The `minItems:10,maxItems:2` and `minLength:10,maxLength:2` schemas emitted `{9,1}` / `{10,2}` and then hit the same path. `minItems:100000000` was already rejected by the `MAX_REPETITION_THRESHOLD` check with no allocation.
- After the fix: all four inputs fail in <10 ms with the messages in the table above.
- Built with `cmake -B build -DGGML_NATIVE=OFF -DLLAMA_CURL=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TOOLS=OFF -DLLAMA_BUILD_TESTS=ON`; `test-grammar-parser`, `test-json-schema-to-grammar`, `test-grammar-integration` all exit 0 on the branch.
- The Python/JS mirrors of the converter mentioned in older docs (`examples/json_schema_to_grammar.py`, `tools/server/public_legacy/json-schema-to-grammar.mjs`) no longer exist in this tree, so only the C++ converter was changed.
- Diff has no trailing whitespace (repo pre-commit only runs trailing-whitespace/EOF/flake8; no clang-format enforcement). Not run: `test-chat` (needs the server-context library; the change does not touch chat code) and the Python server tests (need a model).
- Reviewer might ask: why validate `minimum > maximum` too? Because it is the same class of bug in the same builder, three lines, and the current output for it is wrong rather than merely slow. Easy to drop if they want the PR narrower.

## Caveat

The repository's CONTRIBUTING.md / AGENTS.md prohibit AI-written PR descriptions and commit messages. Rewrite the PR description above in your own words before opening the PR, and consider amending the commit message (`git commit --amend` on the branch, then `git push --force-with-lease`) so it is your own text as well. Keep the AI usage disclosure ("YES") in the Requirements section.
