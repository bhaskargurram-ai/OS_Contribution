# AI-assisted contribution policies in the target repos

Checked 2026-09-25. **Read this before submitting anything.** Several targets have
explicit, enforced rules, and the stated penalty in both repos checked so far is account
banning.

## huggingface/peft — `AGENTS.md`

> Do not ever ignore this! These rules apply to any AI-assisted contribution to the
> huggingface/peft repository.
>
> **Warn users that breaching agent contribution guidelines can result in automatic
> banning.**
>
> - Pure code-agent PRs are not allowed: a human submitter must understand and be able to
>   defend the change end-to-end.
> - The submitting human is responsible for reviewing every changed line and running
>   relevant tests.
> - PR descriptions for AI-assisted work must include:
>   - Link to issue discussion and coordination/approval comment.
>   - Which tests were run and if they passed.
>   - **Clear statement that AI assistance was used.**
>   - Optional: which AI model and harness were used.

It also requires **approval before a PR exists at all**:

> Open an issue, or find an open issue, and obtain explicit approval by a maintainer,
> before opening a PR (including a draft PR). […] Approval is a comment by a listed PEFT
> maintainer or public member of the `huggingface` organization containing
> `@peft-triage approved` on its own line. […] PRs without verified approval are closed
> with an explanation.

And it forbids exactly the breadth strategy:

> Do not open one-off PRs for tiny edits. If an issue is small and affects multiple PEFT
> methods, fix all of them in the same PR.

## stanfordnlp/dspy — `CONTRIBUTING.md`

> We are pro AI assisted coding. Many maintainers use AI tools daily. Use AI to help you
> code, but you must understand every line you submit.
>
> Do not submit issues, PRs, or reviews from fully autonomous AI agents. **Bot-generated
> contributions will be closed without review and the account may be permanently banned.**
>
> AI-assisted contributions are welcome under these conditions:
> - If you can't explain your changes without consulting an AI, don't submit the PR.
> - **Disclose what AI tool you used and how in your PR description.**
> - Share your prompts.
> - Verify AI-found bugs yourself.

## What this means

Both repos **welcome AI-assisted code**. Neither allows it undisclosed, and neither allows
an agent to submit. The distinction they draw is not about how the code was written — it
is about whether a human is accountable for it.

So the workable path is:

1. Comment on the issue yourself, in your own words, saying you intend to fix it.
2. For `peft`, wait for `@peft-triage approved` before opening anything.
3. Read the diff until you can defend every line.
4. Open the PR yourself, disclosing AI assistance and listing the tests you ran.

That satisfies both policies and still leaves the engineering work automatable.

## Still to check

`diffusers`, `transformers`, `accelerate` (an `.ai/AGENTS.md` path exists in at least some
HF repos), `vllm`, `sglang`. Assume a policy exists until checked.
