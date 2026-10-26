# ShelfPulse originality review

## Mechanism fingerprint

Owner-scoped item -> independently fetched, product-bound consecutive snapshots -> one-use observation IDs and strict period sequence -> two-low observation latch -> one replenishment quantity -> high-stock reset.

The model decides only whether a snapshot's product description is the same registered product. Ordinary code parses quantities and controls thresholds and state. The new invariant is that a single low snapshot, reused observation ID, repeated period, or skipped period cannot create or sustain a new replenishment signal.

## Closest workspace matches

- DonationDoor matches offered inventory to needs and reserves/reconciles allocations. ShelfPulse has no donors, recipients, matching, reservations, or acceptance flow.
- FridgeSpaceRound places requests into described shelf capacity. ShelfPulse has no spatial layout or placement algorithm.
- RecallMatch screens inventory against a fetched notice and composes item verdicts. ShelfPulse checks a product identity in a time-ordered stock feed and gates a replenishment latch.
- ChangePointWatch detects sustained changes with a baseline and per-dimension CUSUM. ShelfPulse uses exact quantities, a consecutive period counter, and a two-observation threshold latch; it has no baseline vector or cumulative score.

The distinction is the state transition and invariant, not the label or domain. Residual review risk remains because both this contract and ChangePointWatch consume observations over time; the algorithm and stored state differ as documented above.
