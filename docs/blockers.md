# What blocks automated contribution, and how to clear it

This session can read any public repo but can only use the GitHub **API** — issues, forks,
pull requests — on repositories explicitly attached to it. Attaching requires **push
permission on that repository**, which nobody has on an upstream they do not maintain.

The consequences, in order of how much they cost:

## 1. Forks cannot be created from here

`fork_repository` on `huggingface/peft` is refused: forking is an API write against the
*upstream*, and the upstream cannot be attached. So work is only possible in projects
where **a fork already exists** under the account.

Forks that exist today: `dspy`, `pytorch`, `langchain`, `autogen`, `agent-zero`,
`cartography`, `hiero-sdk-python`, `openai-agents-js`, `beads`.

Forks needed for the Tier A targets in `target-list.md`: **peft, diffusers, accelerate,
vllm, sglang, transformers**. Each is one click on the upstream's *Fork* button; after
that they can be attached and worked normally.

## 2. Pull requests cannot be opened from here

Opening a PR is a write against the upstream, so it is refused for the same reason. The
workflow that does work end to end:

1. branch from `upstream/main` in the fork's clone
2. implement, test, lint
3. push the branch to the fork
4. open the PR from the compare URL — one click

Each entry under `prs/` carries its compare URL and a ready-to-paste body.

## 3. Forks go stale

The `dspy` fork was ~11 months behind upstream. Always branch from `upstream/main`, not
from the fork's default branch:

```bash
git remote add upstream https://github.com/<owner>/<repo>
git fetch --depth 1 upstream main
git checkout -b <branch> upstream/main
```

## 4. Repo-wide autoformatters

`ruff format` on a whole file in `dspy` rewrote ~1900 unrelated lines, because upstream is
not itself format-clean. Format only your own added lines, and check `git diff --stat`
before committing — a PR carrying an incidental reformat of the whole file will not be
reviewed.
