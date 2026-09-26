# llama.cpp #29457 — large `enum` in a json_schema makes grammar construction superlinear (small request pins a core for tens of seconds)

**Status:** branch pushed (commit `f376cf7`), PR not yet opened
**Branch:** `bhaskargurram-ai/llama.cpp` → `fix/grammar-enum-linear-time`
**Open the PR:** https://github.com/ggml-org/llama.cpp/compare/master...bhaskargurram-ai:llama.cpp:fix/grammar-enum-linear-time?expand=1

Title:

```
grammar : make large enum alternations scale linearly
```

Body (paste as-is):

---

## Overview

Fixes #29457.

An `enum` with n values is converted to a flat alternation `"a" | "b" | ...`. `json_schema_to_grammar` itself is linear and cheap (15 ms for 20k values); the cost is in what that shape does to the grammar engine, all of it on the serving slot:

1. `llama_grammar_init_impl` expands the alternation into one parser stack per value and deduplicates each new stack with `std::find` over the stack vector: O(n²). `llama_grammar_accept_token` merges surviving stacks the same way, also O(n²) while many stacks are alive.
2. Every sampled token runs the reject-candidates chain once per live stack, O(n × vocab). With n = 10k and a 150k vocabulary that is one to two billion character matches for the first token, which is the "tens of seconds" in the report (`n_predict: 1` measures exactly one such step).

Measured with a standalone program (no model; a synthetic 150k-token vocab for the sampling step; enum values `"v0"…`), master vs. this branch:

| enum size | `json_schema_to_grammar` | `llama_grammar_init_impl` master → branch | live stacks master → branch | first sampling step (reject chain) master → branch | accept one char master → branch |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 0.8 → 1.0 ms | 2.1 → 0.1 ms | 1,000 → 1 | 1.38 s → 9 ms | 2.5 → 0 ms |
| 5,000 | 3.7 → 5.4 ms | 61 → 0.5 ms | 5,000 → 1 | 6.8 s → 11 ms | 49 → 0 ms |
| 10,000 | 8.0 → 10.7 ms | 193 → 0.9 ms | 10,000 → 1 | 13.3 s → 13 ms | 193 → 0 ms |
| 20,000 | 15 → 32 ms | 788 → 1.9 ms | 20,000 → 1 | 27.2 s → 34 ms | 795 → 0 ms |
| 50,000 | 36 → 58 ms | 5,053 → 4.9 ms | 50,000 → 1 | 96.4 s → 29 ms | 4,977 → 0 ms |
| 100,000 | – → 125 ms | – → 14 ms | – → 1 | – → 42 ms | – → 0 ms |

The parser-side fix on its own (a hand-written flat `root ::= ("\"v0\"" | ...)` on this branch) makes init/accept linear: 0.3 / 1.9 / 4.2 / 9.8 ms init for 1k / 5k / 10k / 20k, accept 0.2 / 1.2 / 2.8 / 5.3 ms. It does not change the per-token O(n × vocab) cost (1.5 s / 7 s / 13 s / 27 s), which is why the converter change is needed as well.

### Change

- `common/json-schema-to-grammar.cpp`: enum values (and the `allOf` enum intersection) are emitted as a prefix tree built with the existing `common_trie` (`_literal_alternatives`), so the number of live stacks is the branching factor of the values, not their count. Chains of single-child nodes are merged into one literal; a node where a value ends and longer values continue becomes `(...)?`. The accepted language is unchanged. Examples: `["red","amber","green",null,42,["foo"]]` → `("\"" ("amber\"" | "green\"" | "red\"") | "42" | "[\"foo\"]" | "null")`; `["a","ab",1,12]` → `("\"a" ("\"" | "b\"") | "1" ("2")?)`.
- `src/llama-grammar.cpp`: `llama_grammar_advance_stack` takes a `seen` set (`std::set<llama_grammar_stack>`, the same pointer-wise ordering the local set already used) that is shared by every caller advancing into the same stack vector: `llama_grammar_init_impl` (both overloads), `llama_grammar_accept`, `llama_grammar_accept_token`, `llama_grammar_reject_candidates_for_stack`. The two `std::find` calls in `advance_stack` and the one in `accept_token` are gone. This makes construction linear for hand-written grammars with many alternatives too.

Not done: no size cap on `enum`, since after the change a 100k-value enum builds in ~150 ms and samples in ~40 ms per token, so a cap did not seem necessary. `anyOf` of many `const` schemas still produces a flat alternation of rule references; its init is now linear but its per-token cost is still one stack per branch.

### Tests

- `tests/test-json-schema-to-grammar.cpp`: the three enum expectations updated to the prefix-tree form, plus a new "enum with shared prefixes" case (`["a","ab",1,12]`). Fail on master (expectation mismatch), pass here. The "Check the expectations parse" pass verifies every expected grammar still parses.
- `tests/test-grammar-integration.cpp`: new `test_large_enum()`: a generated 5000-value enum must produce a grammar with exactly one initial stack and accept/reject the right strings (`"v0"`, `"v4999"` vs. `"v"`, `"v01"`, `"v5000"`, `v1`), plus a prefix-overlap enum (`"a"`/`"ab"`, `1`/`12`) checked for acceptance. On master the stack-count assertion fails (5000 stacks).
- All existing grammar tests pass unchanged (`test-grammar-parser`, the acceptance cases in `test-grammar-integration`, including the three `street_type` enum schemas).

Commands (build with `-DLLAMA_BUILD_TESTS=ON`, no model):

```
cmake --build build --target test-json-schema-to-grammar test-grammar-parser test-grammar-integration -j2
./build/bin/test-grammar-parser            # exit 0
./build/bin/test-json-schema-to-grammar    # exit 0
./build/bin/test-grammar-integration       # exit 0
```

## Additional information

Trie children are iterated in codepoint order, so the alternatives in the emitted grammar are sorted rather than in schema order. Recursion depth of `_literal_alternatives` (and of the parser on the nested groups) is the number of branch points on a root-to-leaf path, which the merged chains keep far below the value length in practice; `_not_strings` already recurses the same way for property names.

## Requirements

- I have read and agree with the [contributing guidelines](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)
- AI usage disclosure: YES - see below

### AI assistance

This change was produced with AI assistance. I reviewed every changed line, ran the tests
listed above, and can defend the change.

---

## Verification performed

- Profiled on `master` (2145525) with a standalone program linking `libllama-common`/`libllama` (scratch `bench_enum.cpp`, not committed) that times `common_json::parse`, `json_schema_to_grammar`, `llama_grammar_parser::parse`, `llama_grammar_init_impl`, one reject-candidates chain over a synthetic 150k-token vocab (same chaining as the static `llama_grammar_reject_candidates`), and one `llama_grammar_accept_str("\"")`. Numbers in the table above; the converter was already linear, init/accept were ~4x per doubling (quadratic), the sampling step was linear in n with a 150k constant.
- After the fix, same program: init 0.1 → 14 ms from 1k to 100k values, 1 live stack, sampling step 9–42 ms, accept ~0 ms.
- Ran the new test binaries against the unfixed libraries (`LD_LIBRARY_PATH` to a master build): `test-grammar-integration` aborts on `grammar->stacks.size() == 1` (5000 stacks), `test-json-schema-to-grammar` fails on the 'non-string enum' expectation. Both pass on the branch.
- Checked emitted grammars for escaping and Unicode: `x"y` → `"x\\\"y\""`, `é`/`éa` → `"é" ("\"" | "a\"")`; a nested property enum gives `s ::= "\"" ("Avenue\"" | "Street\"")`.
- Built with `cmake -B build -DGGML_NATIVE=OFF -DLLAMA_CURL=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TOOLS=OFF -DLLAMA_BUILD_TESTS=ON`; the three grammar tests exit 0. Not run: `test-chat` (needs server-context; it uses enums only inside tool schemas and checks parsing, not grammar text), `test-gbnf-validator`, Python server tests (need a model). If reviewers want, `test-chat` is the one to run since it calls `llama_grammar_accept` (signature unchanged, only the static helpers changed).
- Diff has no trailing whitespace; repo pre-commit hooks are trailing-whitespace/EOF/flake8 only.
- Points a reviewer may raise: (1) the changed grammar shape for small enums (sorted, prefix-shared) breaks anyone diffing grammar text, which only the unit test did in-tree; (2) whether to gate the trie behind a size threshold to keep the old output for small enums; (3) whether an explicit `enum` size cap is still wanted as defense in depth.

## Caveat

The repository's CONTRIBUTING.md / AGENTS.md prohibit AI-written PR descriptions and commit messages. Rewrite the PR description above in your own words before opening the PR, and consider amending the commit message (`git commit --amend` on the branch, then `git push --force-with-lease`) so it is your own text as well. Keep the AI usage disclosure ("YES") in the Requirements section.
