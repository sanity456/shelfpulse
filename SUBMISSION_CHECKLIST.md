# Submission checklist

- [x] Local GenVM lint and SDK validation pass.
- [x] Standard typecheck passes with no diagnostics.
- [x] Direct tests pass, including forged leader fields, access control, period and snapshot replay, source failures, invalid UTF-8, and mismatch handling (8 passed).
- [x] StudioNet pinned-runner compatibility probe passed (separate trivial contract only; not a ShelfPulse live test).
- [ ] StudioNet deployment and live two-period demonstration are complete; all writes are `FINALIZED` with execution `SUCCESS`.
- [ ] Deployed contract source matches the pinned public commit byte-for-byte.
- [ ] Public repository, pinned source, manifest, contract Explorer page, and key transaction links are verified while logged out.
- [ ] Portal note is under 1,000 characters and states that the source is caller-provided and not authenticated.
