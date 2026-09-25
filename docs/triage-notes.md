# Triage notes — issues examined and rejected

Not every unclaimed issue is a PR. Recording the ones investigated and dropped, so they
don't get picked up again.

| Issue | Verdict |
|---|---|
| [dspy #8879](https://github.com/stanfordnlp/dspy/issues/8879) — `Embedder` KeyError with custom function | **Not a bug.** The traceback is inside the reporter's own `jina_embeddings`. `Embedder` documents that a custom callable "takes a list of strings as input"; theirs treats the argument as a single string and wraps it in a list, producing a nested list the Jina API rejects. The `KeyError: 'data'` is their code reading an error response. Answer on the issue; do not open a PR. |
| [peft #3723](https://github.com/huggingface/peft/issues/3723) — opaque `TypeError` in `set_adapter` | **Claimed.** The reporter states they have a fix and regression test ready. No linked PR yet, so it passes the `-linked:pr` filter, but opening one would duplicate their work. |

## What this implies about the scan numbers

The ~600 "unclaimed" issues in `target-list.md` are not ~600 available PRs. Sampling them,
the population breaks down roughly as:

- **user error or unreproducible** — the reporter's own code, or an environment problem
- **environment-specific** — a provider outage, one Azure deployment, a network filesystem
- **feature proposals** — need design agreement before any code is worth writing
- **promotional** — vendors opening issues to advertise a product
- **claimed in comments** — someone said "working on this" without opening a PR
- **actually actionable** — a reproducible defect with a clear fix

Only the last category converts to a mergeable PR, and it is a minority of the total.
Budget effort against that fraction, not against the headline count.
