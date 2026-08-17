# Contract API

## Write methods

### `watch(subscription_id, url, clauses_json, min_refresh_seconds)`

Registers a unique subscription. The caller becomes owner.

- `subscription_id`: 1–64 characters; letters, digits, `-`, `_`.
- `url`: HTTP(S), maximum 2,048 characters.
- `clauses_json`: 1–12 unique clauses and 1–3 anchors.
- `min_refresh_seconds`: 300–2,592,000 seconds.

Clause object:

```json
{
  "id": "webhook_v2",
  "question": "Does the API support webhook v2?",
  "anchor_expected": ""
}
```

### `refresh(subscription_id)`

Permissionless. Executes extraction consensus and, after the baseline, drift
consensus. The configured interval applies per URL to owners and third parties.

### `set_active(subscription_id, active)`

Owner-only circuit breaker. Historical snapshots remain readable.

## View methods

### `latest(subscription_id, clause_id)` / `get_clause(...)`

Returns current normalized value, evidence, confidence, anchor metadata, latest
drift, and change indexes.

### `changed_since(subscription_id, clause_id, snapshot)`

Returns:

```json
{
  "changed": true,
  "materially_changed": true,
  "last_change_snapshot": 4,
  "last_material_snapshot": 4,
  "latest_snapshot": 5
}
```

### `get_snapshot(subscription_id, snapshot)`

Returns the complete accepted audit snapshot: timestamp, URL, clause results,
drift rationales, and per-snapshot counts.

### `get_subscription(subscription_id)`

Returns owner/configuration, latest snapshot, and aggregate counters.

### `get_stats()`

Returns the subscription count and protocol bounds. Used by the release script
as a no-argument post-deployment smoke call.
