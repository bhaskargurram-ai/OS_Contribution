# Fork list — 20 repositories

One click each. The targets in each row are already vetted; once a fork exists I can clone,
sync against upstream, and start work on it.

## From the AI-company scan (15 repos)

| # | Fork | Target issue(s) | Language |
|---|---|---|---|
| 1 | [NVIDIA/TransformerEngine](https://github.com/NVIDIA/TransformerEngine/fork) | [#3202](https://github.com/NVIDIA/TransformerEngine/issues/3202) OOB metadata writes ●, [#3294](https://github.com/NVIDIA/TransformerEngine/issues/3294) | Python/C++ |
| 2 | [huggingface/datasets](https://github.com/huggingface/datasets/fork) | [#8637](https://github.com/huggingface/datasets/issues/8637) FileLock drops kwargs ●, [#8681](https://github.com/huggingface/datasets/issues/8681) | Python |
| 3 | [huggingface/tokenizers](https://github.com/huggingface/tokenizers/fork) | [#2334](https://github.com/huggingface/tokenizers/issues/2334) dropped codepoints ●, [#2447](https://github.com/huggingface/tokenizers/issues/2447) | Rust |
| 4 | [facebookresearch/faiss](https://github.com/facebookresearch/faiss/fork) | [#5567](https://github.com/facebookresearch/faiss/issues/5567) negative L2 distances ● | C++/Python |
| 5 | [ml-explore/mlx](https://github.com/ml-explore/mlx/fork) | [#4538](https://github.com/ml-explore/mlx/issues/4538) wrong GPU sort ●, [#4560](https://github.com/ml-explore/mlx/issues/4560) | C++/Python |
| 6 | [langchain-ai/langsmith-sdk](https://github.com/langchain-ai/langsmith-sdk/fork) | [#3569](https://github.com/langchain-ai/langsmith-sdk/issues/3569) dropped `.response` ● | Python |
| 7 | [NVIDIA/garak](https://github.com/NVIDIA/garak/fork) | [#2226](https://github.com/NVIDIA/garak/issues/2226) hf_args silently dropped ● | Python |
| 8 | [microsoft/markitdown](https://github.com/microsoft/markitdown/fork) | [#2468](https://github.com/microsoft/markitdown/issues/2468) URL path corruption ●, [#2382](https://github.com/microsoft/markitdown/issues/2382) | Python |
| 9 | [modal-labs/modal-client](https://github.com/modal-labs/modal-client/fork) | [#4130](https://github.com/modal-labs/modal-client/issues/4130) directory corruption ●, [#4126](https://github.com/modal-labs/modal-client/issues/4126) | Python |
| 10 | [ollama/ollama](https://github.com/ollama/ollama/fork) | [#18595](https://github.com/ollama/ollama/issues/18595) orphaned blob GC ● | Go |
| 11 | [huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub/fork) | [#4987](https://github.com/huggingface/huggingface_hub/issues/4987) 401s with generated JWTs | Python |
| 12 | [openai/openai-python](https://github.com/openai/openai-python/fork) | [#2699](https://github.com/openai/openai-python/issues/2699) rate-limit inconsistency | Python |
| 13 | [keras-team/keras-hub](https://github.com/keras-team/keras-hub/fork) | [#1191](https://github.com/keras-team/keras-hub/issues/1191) generate() stability tests | Python |
| 14 | [replicate/cog](https://github.com/replicate/cog/fork) | [#1323](https://github.com/replicate/cog/issues/1323) push fails with --separate-weights | Go/Python |
| 15 | [EleutherAI/gpt-neox](https://github.com/EleutherAI/gpt-neox/fork) | [#1340](https://github.com/EleutherAI/gpt-neox/issues/1340) position embedding assertion | Python |

## Best remaining from the first scan (5 repos)

| # | Fork | Target issue | Language |
|---|---|---|---|
| 16 | [huggingface/transformers.js](https://github.com/huggingface/transformers.js/fork) | [#1767](https://github.com/huggingface/transformers.js/issues/1767) memoised rejected promise ● | JavaScript |
| 17 | [evidentlyai/evidently](https://github.com/evidentlyai/evidently/fork) | [#1930](https://github.com/evidentlyai/evidently/issues/1930) `has_all` checks the wrong column ● | Python |
| 18 | [microsoft/graphrag](https://github.com/microsoft/graphrag/fork) | [#2573](https://github.com/microsoft/graphrag/issues/2573) `community_level` broken since v2.0.0 ● | Python |
| 19 | [chroma-core/chroma](https://github.com/chroma-core/chroma/fork) | [#7688](https://github.com/chroma-core/chroma/issues/7688) uninitialized heap memory persisted ● | Rust/Python |
| 20 | [weaviate/weaviate](https://github.com/weaviate/weaviate/fork) | [#12959](https://github.com/weaviate/weaviate/issues/12959) HNSW AddMulti panics on nil ● | Go |

● = mechanism stated precisely in the issue; high confidence.

## Suggested order

If you would rather not fork all twenty at once, these five give the best return and are all
pure Python or JavaScript with fast test suites:

**datasets · langsmith-sdk · markitdown · evidently · transformers.js**

`faiss`, `mlx` and `TransformerEngine` are C++/CUDA — I can write the fix and a test, but
verifying the GPU paths is not possible in this container. `tokenizers`, `chroma` are Rust;
`ollama`, `weaviate`, `cog` are Go. All workable, just slower to set up than Python.

## Already forked — no action needed

`dspy`, `peft`, `diffusers`, `accelerate`, `transformers`, `vllm`, `sglang`, `inspect_ai`,
`lm-evaluation-harness`, `haystack`, `pydantic-ai`, `pytorch`, `langchain`, `autogen`.
