# ShelfPulse

ShelfPulse is a reusable GenLayer contract that turns two consecutive, independently checked low-stock snapshots into one replenishment signal. A registered item has a deterministic threshold and target level. Each observation is fetched from a caller-supplied HTTPS JSON snapshot; validators independently confirm that its product description refers to the registered item. Code reads the exact numeric fields, enforces consecutive periods and unique observation IDs, and emits a single `RESTOCK_DUE` state until a later above-threshold observation resets it.

## GenLayer's role and boundary

Validators resolve the semantic product-identity question that deterministic code cannot safely decide from descriptions. The source must provide JSON with exactly `item_description`, `period`, and `quantity`. Numeric state, threshold checks, order quantity, period progression, replay protection, and lifecycle are deterministic. Callers choose the evidence URL and can publish misleading snapshots; the contract does not authenticate a retailer, prove inventory, place a purchase order, move money, or guarantee delivery.

The mechanism is a two-period confirmation latch with period and observation-ID replay protection. It is distinct from DonationDoor's semantic offer/need allocation, FridgeSpaceRound's spatial placement, RecallMatch's notice-to-inventory screening, and ChangePointWatch's cumulative change detection.

## Interface

Writes: `register_item`, `record_observation`

Views: `get_item`, `get_observation`

One deployment supports multiple creator-scoped items. See `ARCHITECTURE.md`, `ORIGINALITY.md`, and `SECURITY.md` for the mechanism comparison and limits.

## Local checks

```text
genvm-lint check contracts/shelf_pulse.py
genvm-lint typecheck contracts/shelf_pulse.py --strict
python -m pytest tests/direct -q -p no:cacheprovider
```

MIT licensed.
