# tokenizers #2447 — 1.0.0rc2 refuses byte-level vocabs that 0.23.x loaded

**Status:** branch pushed (`3ac91f99`), PR not yet opened
**Branch:** `bhaskargurram-ai/tokenizers` → `fix/byte-level-exempt-unreachable-byte-atoms`
**Open the PR:** https://github.com/huggingface/tokenizers/compare/main...bhaskargurram-ai:tokenizers:fix/byte-level-exempt-unreachable-byte-atoms?expand=1

Repo policy (`CONTRIBUTING.md`): open it **as a draft first**, no "AI slop", keep the diff
focused, tests come with the fix, no 500-line descriptions. The body below is deliberately
short. The issue was filed by a maintainer (xenova) three days ago and has no PR; a commenter
measured which Hub vocabs are affected — the body cites that split.

Title:

```
Exempt bytes no UTF-8 string can hold from the byte-level atom check
```

Body (paste as-is):

---

Fixes #2447.

The v1 byte-level BPE loader requires an atom for every byte `0x00..=0xFF`. That
invariant exists because a word containing a byte with no atom could not be encoded
(`byte_internal[b]` would be `u32::MAX` and go straight into the symbol stream). But words
arrive as `&str`, so 13 bytes can never occur: `0xC0`, `0xC1` and `0xF5..=0xFF` are
neither lead nor continuation bytes in valid UTF-8. Several published vocabs leave out
exactly those 13 (ModernBERT-base, pythia-160m / gpt-neox-20b, deepseek-coder-1.3b) and
loaded on 0.23.x but are refused by 1.0.0rc2.

This narrows the check to the 243 bytes a string can contain. A missing atom for a byte
that *can* occur (`0x0B` in bloomz-560m, `0xF1` in starcoder2) is still refused with the
same error naming the byte — the encode path has no fallback for it, and on 0.23.x such a
byte was silently dropped rather than encoded, so restoring that would be a separate
decision.

Tests: `byte_level_exempts_bytes_no_utf8_string_holds` builds a vocab missing the 13 bytes
and encodes ASCII, `é` and `U+10FFFF` (the largest lead byte a string holds, `0xF4`);
`byte_level_still_requires_every_reachable_byte` checks `0x0B`, `0x80` and `0xF1` are
still refused by name. The first fails on `main`.

`cargo test --workspace --lib`, `cargo clippy --workspace --all-targets --all-features -D warnings`
and `cargo fmt --check` pass.

AI assistance was used for this change; I have read and can defend every line.

---

## Verification performed

| Check | Result |
|---|---|
| New test fails without fix | `byte_level_exempts_bytes_no_utf8_string_holds` panics on `unwrap` (ByteAtomOutOfVocabulary) |
| New tests pass with fix | 2/2, plus the 16 existing byte_level tests |
| `cargo test --workspace --lib --no-fail-fast` | all crates pass (233 + 42 + 6 tests) |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | clean |
| `cargo fmt --all -- --check` | clean |
| tk-serialize test expecting the "Byte atom" refusal for a 4-token vocab | still passes (that vocab lacks reachable bytes) |

Diff is 58 insertions, 2 deletions across 2 files.
