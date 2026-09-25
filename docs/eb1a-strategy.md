# Open-source contributions as EB-1A evidence — an honest read

*Not legal advice. I am not an immigration attorney; confirm all of this with one.*

## The blunt version

The plan "find every unclaimed issue in the top AI repos and contribute to all of them"
optimises for the wrong variable. Under `8 CFR 204.5(h)(3)(v)` the criterion is
**original contributions of major significance in the field** — not *number of accepted
patches*. Since *Kazarian v. USCIS* (9th Cir. 2010), adjudication is two-step: you first
satisfy three criteria, then face a **final merits determination** on whether the record
as a whole shows sustained acclaim. A long list of small merged PRs passes neither step
well. It reads as competent contributor, not as extraordinary ability, and the second
step is where that framing gets denied.

What an adjudicator can actually act on is evidence *outside your own control*: someone
else saying your work mattered.

## What the evidence has to look like

| Criterion | What counts | What doesn't |
|---|---|---|
| (v) Original contributions of major significance | A feature/algorithm you authored that others demonstrably depend on: release notes naming you, downstream adoption, citations, independent expert letters | Merged PRs, counted |
| (viii) Leading or critical role for a distinguished organization | Listed in `MAINTAINERS`/`CODEOWNERS`, commit rights, org membership, a named subsystem you own | Being a frequent contributor |
| (iv) Judging the work of others | Designated reviewer on a major project, conference PC member, journal reviewer | Commenting on issues |
| (vi) Authorship of scholarly articles | A paper on the work; arXiv plus a venue | A blog post |

Notice that three of the four are *status*, not *output*. That is the actual target.

## The strategy that follows

**Depth in one or two projects, not breadth across twenty.**

1. **Pick one project and become a maintainer of one subsystem.** From the scan,
   `huggingface/peft` and `huggingface/diffusers` are the realistic candidates: small
   enough to become visible in, important enough to be "distinguished", and with
   maintainers who actively promote contributors. PyTorch and vLLM are more prestigious
   and much slower to gain standing in.

2. **Own a seam, not a ticket.** The scan surfaced one: **FSDP2 + LoRA/QLoRA
   correctness**, spanning `peft#3800`, `peft#3802`, `peft#3803` and `accelerate#3874`.
   Fixing that cluster as a coherent body of work, with tests and a design note, is a
   story ("made FSDP2 fine-tuning correct in the HF stack"). Four unrelated patches are
   not a story.

3. **Ship one *named* thing.** A model/pipeline integration in `diffusers`
   (`#12257` Wan 2.2 S2V, `#7219` SUPIR, `#10043` F5-TTS) appears in release notes with
   your name, is documented, and is independently citable. That is the most legible
   single artifact available on this list.

4. **Produce a quantified performance win.** `vllm#31624` (checkpoints taking 5+ minutes
   to load) yields a number — "reduced Llama-4 checkpoint load time by N×" — and numbers
   survive translation to a non-technical adjudicator better than anything else.

5. **Convert contribution into status.** After several substantive merges, ask to be
   added as a reviewer/maintainer for that subsystem. This is a normal request in these
   projects and it is what actually produces criterion (viii) and (iv) evidence.

6. **Write it up.** An arXiv paper on the technique, citing your own implementation, is
   criterion (vi) and reinforces (v).

## Sequencing

- **Months 0–2:** land 3–5 substantive merges in one project. Build the relationship.
- **Months 2–5:** own the seam (the FSDP2 cluster) and ship the named integration.
- **Months 5–8:** request reviewer/maintainer status; start reviewing others' PRs.
- **Months 6–12:** paper; solicit letters from maintainers you have worked with directly.

Maintainer letters are the highest-leverage artifact in the whole plan, and you only get
a good one from someone who has merged your work repeatedly. That is the real reason
depth beats breadth.

## What to stop doing

Filing many small PRs across many repos produces a GitHub profile that looks busy and a
petition that looks thin. If the goal is the petition, the contribution graph is not the
deliverable — the maintainer's letter is.
