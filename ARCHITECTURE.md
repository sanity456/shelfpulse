# ShelfPulse architecture

## Protocol

1. An owner registers one item description, a low-stock threshold, and a target level.
2. The owner submits a unique observation key and HTTPS URL for a stock snapshot.
3. GenVM fetches bounded JSON. Deterministic parsing requires exactly the registered product description, a consecutive positive period, and an integer quantity. GenLayer independently judges whether the fetched description is semantically the same product as the registered item.
4. Validators rerun the fetch and judgment and compare every returned field, including period, quantity, match, content hash, and URL. Any disagreement fails closed.
5. Code increments the low-stock streak only when quantity is at or below threshold. One low snapshot leaves the item in `MONITORING`; two consecutive lows set `RESTOCK_DUE` and compute `target_stock - quantity`. A later above-threshold snapshot clears the signal.

## State and invariants

Records are keyed by owner and item ID. Observation IDs are one-use and periods must increase exactly by one, preventing skipped periods and stale replay. The owner is the only writer for an item. A `RESTOCK_DUE` record does not emit a second order quantity on each later low observation; the due state remains until stock recovers above the threshold.

## Consensus boundary

The leader and each validator fetch the same URL and parse the same closed JSON schema. The LLM returns exactly one field, `match`, from `MATCH`, `MISMATCH`, or `UNCLEAR`. The validator independently repeats the task and compares the canonical result object exactly. The contract stores only the independently agreed product-identity verdict and deterministic values from the fetched JSON. Inputs and source content are public and untrusted.

## Mechanism comparison

DonationDoor reserves quantities from semantic offers against recipient needs; ShelfPulse allocates no inventory and matches no offers. FridgeSpaceRound places described containers into physical shelf capacity; ShelfPulse makes no placement decision. RecallMatch joins a recall notice to inventory; ShelfPulse uses successive item-specific snapshots to control a replenishment latch. ChangePointWatch accumulates semantic dimension signals with CUSUM; ShelfPulse uses exact stock quantities, consecutive period IDs, and one resettable two-observation latch without baselines or cumulative scores.
