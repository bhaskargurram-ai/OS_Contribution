# weaviate #12959 — HNSW `AddMulti` panics on a nil or empty multivector

**Status:** branch pushed (`2f6fb89`), PR not yet opened
**Branch:** `bhaskargurram-ai/weaviate` → `fix/hnsw-addmulti-nil-multivector`
**Open the PR:** https://github.com/weaviate/weaviate/compare/main...bhaskargurram-ai:weaviate:fix/hnsw-addmulti-nil-multivector?expand=1

Repo policy: a PR must be linked to an issue the maintainers have triaged, otherwise it is
closed (and repeat offenders are blocked). #12959 is a triaged bug report with the panic
trace, so it qualifies — **keep the `Fixes #12959` line**. Commit subjects carry a
`gh-NNNN` tag (done). `golangci-lint` is a CI gate; the package is clean. The PR template
has a "What's being changed" section and a review checklist — both filled in below.

Title:

```
gh-12959 hnsw: reject nil or empty multivectors in AddMultiBatch
```

Body (paste as-is):

---

Fixes #12959.

### What's being changed:

`AddMulti` / `AddMultiBatch` index `vectors[i][0]` before checking that `vectors[i]` has
any entries: the MUVERA encoder is initialised from the first document's first vector, the
dimension tracker reads the same element, and a document that is nil or empty then iterates
zero times through the dimension check. A nil or empty multivector therefore panics the
goroutine with `index out of range [0] with length 0` instead of returning an error the
caller could act on.

This validates every document up front, right after the existing empty-batch guard, and
returns an error naming the offending docID:

```
addMultiBatch called with a nil or empty multivector at docID 2
```

No behaviour changes for well-formed input; the check is a `len()` per document.

### Tests

`TestAddMultiRejectsNilOrEmptyMultivector` (table-driven) covers a nil multivector, an empty
one, and a nil document in the middle of a batch, with and without MUVERA enabled. Each case
asserts the error and then inserts a well-formed document to show the index is still usable.
Without the fix every case panics with the index-out-of-range trace from the issue; with it
all five pass.

### Review checklist

- [x] Documentation has been updated, if necessary. Link to changed documentation: not
  necessary — error path only.
- [x] Chaos pipeline run or not necessary. Link to pipeline: not necessary.
- [x] All new code is covered by tests where it is reasonable.
- [x] Performance tests have been run or not necessary. Not necessary — one `len()` per
  document on the insert path.

### AI assistance

This change was produced with AI assistance. I reviewed every line, reproduced the panic,
ran the tests, and can defend the change.

---

## Verification performed

| Check | Result |
|---|---|
| Reproduced on `main` | panic `index out of range [0] with length 0` via the new test |
| New test fails without fix | all 5 subtests panic |
| New test passes with fix | 5/5 |
| `go test ./adapters/repos/db/vector/hnsw/ -run TestAddMulti` | pass |
| `gofmt -l` on both files | clean |
| `go vet` on the package | clean |
| `golangci-lint run ./adapters/repos/db/vector/hnsw/` (v2.14.0, go1.27 build) | 0 issues |

`golangci-lint run ./adapters/repos/db/vector/hnsw/...` additionally reports two `govet`
printf findings in `distancer/dot_product_amd64_test.go` and `distancer/hamming_test.go` —
pre-existing, in files this branch does not touch.

Diff is 109 insertions, 0 deletions across 2 files.
