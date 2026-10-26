# Security notes

- Source URLs, fetched content, product descriptions, and stock values are public. A caller can control the URL and may publish false data.
- Validators independently refetch and compare every result field; unavailable or ambiguous sources cannot advance state.
- Responses are capped at 24,000 bytes and must be UTF-8 JSON with an exact schema and bounded integer fields.
- Only the item owner can submit observations. Unique observation IDs and consecutive periods prevent replay and skipped-period submissions.
- The contract emits a coordination signal only. It does not buy stock, transfer assets, authenticate the source, or verify physical inventory.
- A mutable URL may change between validator fetches. Exact field comparison causes disagreement to fail closed; production integrations should use immutable source snapshots.
