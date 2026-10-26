# ShelfPulse local audit

Status: local checks complete; not deployed or submission-ready yet.

Intended defenses include creator-scoped records, strict JSON bounds, source URL validation, independent source refetch and semantic comparison, closed model output, unique observation IDs, exact period sequencing, and a two-consecutive-low latch. The contract does not verify source authority or physical inventory.

Workspace comparison is recorded in `ORIGINALITY.md`. Residual distinctiveness risk: this is an observation-over-time contract, as is ChangePointWatch, although the core state mechanism differs (two consecutive exact low-stock readings versus baseline-relative CUSUM). This similarity should be considered before investing in a public submission.

Local results: GenVM lint and SDK validation pass (3 lint checks; 4 contract methods, including 2 writes); standard typecheck passes with 0 diagnostics; direct suite passes (8 tests). Cases cover two-observation triggering, reset, replay/period ordering, owner isolation, semantic mismatch, HTTP/empty/oversized/invalid-UTF-8 evidence, forged leader fields, and invalid snapshots.

Three gates: technical readiness PASS for local source checks and the pinned-runner StudioNet compatibility probe; distinctiveness PASS with the residual overlap noted above; contract evidence readiness FAIL because ShelfPulse itself has not been deployed or demonstrated live.

Runner compatibility probe (not ShelfPulse): a separate minimal contract deployed on StudioNet; deploy and write receipts reached `FINALIZED` with leader execution `SUCCESS`, and a read returned `smoke-ok`. This confirms runner/network and CLI calldata compatibility only; it is not evidence for ShelfPulse behavior.

Not checked: ShelfPulse StudioNet execution, real external-source behavior, deployed-source equality, public repository accessibility, and Explorer/transaction evidence. This audit is not a submission-readiness or acceptance guarantee. Before live release, verify all of those items, require `FINALIZED` plus execution `SUCCESS`, and read back final state. The evidence source is caller-provided and is not authenticated by this contract.
