# What makes an open-source contribution actually count

A note on prioritisation, written after scanning ~600 unclaimed issues across the major
AI repositories (see `target-list.md`).

## The trap

The obvious plan — find every unclaimed issue and send a patch for each — optimises for
the wrong variable. It produces a busy contribution graph and very little standing. Merge
count is not the thing that compounds; **recognition** is, and recognition comes from
work other people have to reckon with.

Concretely, the things that carry weight later are mostly *status*, not *output*:

| What compounds | How you get it |
|---|---|
| Named in `MAINTAINERS` / `CODEOWNERS` | Repeated substantive merges in one subsystem, then ask |
| Credited in release notes | Ship a whole feature, not a patch |
| Cited by downstream projects | Build the thing others depend on |
| Reviewer on others' PRs | Earned after maintainers trust your judgement |
| A maintainer who will vouch for you | Only from someone who has merged your work many times |

Three of those five are unreachable through volume alone.

## What to do instead

1. **Pick one or two projects and go deep.** From the scan, `huggingface/peft` and
   `huggingface/diffusers` are the realistic candidates — small enough to become visible
   in, important enough to matter, with maintainers who actively promote contributors.
   PyTorch and vLLM are more prestigious and much slower to gain standing in.

2. **Own a seam, not a ticket.** The scan surfaced a clean one: **FSDP2 + LoRA/QLoRA
   correctness**, spanning `peft#3800`, `peft#3802`, `peft#3803` and `accelerate#3874`.
   Fixed as a coherent set with tests and a design note, that is a story — "FSDP2
   fine-tuning is correct in the HF stack now". Four unrelated patches are not.

3. **Ship one *named* thing.** A model/pipeline integration in `diffusers` (`#12257` Wan
   2.2 S2V, `#7219` SUPIR, `#10043` F5-TTS) lands in release notes with your name on it
   and is documented. It is the most legible single artifact on the list.

4. **Produce a quantified win.** `vllm#31624` (checkpoints taking 5+ minutes to load)
   yields a number. Numbers travel further than descriptions.

5. **Convert contribution into role.** After several substantive merges, ask to be added
   as a reviewer for that subsystem. This is a normal request in these projects.

6. **Write it up.** A short paper or technical report on the technique, citing your own
   implementation, extends the reach of the work well past the repo.

## Sequencing

- **Months 0–2:** land 3–5 substantive merges in one project; build the relationship.
- **Months 2–5:** own the seam; ship the named integration.
- **Months 5–8:** request reviewer status; start reviewing others' work.
- **Months 6–12:** write up the results.

## The counter-argument, stated fairly

Breadth is not worthless. Many small patches across many repos is a fast way to learn
review conventions, get your name into a lot of changelogs, and find the project you
actually want to invest in. It is a reasonable *first month*. It is a poor *year*.
