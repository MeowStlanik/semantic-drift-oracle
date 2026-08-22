# Changelog

## 1.0.1

- Enforce `min_refresh_seconds` from each subscription's own `last_refresh_at`.
- Remove the shared per-URL refresh timestamp that allowed a fast watcher to
  postpone a slower watcher of the same URL.
- Add a regression test covering 300-second and 3,600-second subscriptions on
  the same URL.
- Update API/security documentation to describe per-subscription cadence.

## 1.0.0

- Initial standalone Semantic Drift Oracle contract.
- Two-stage extraction/materiality consensus.
- Mandatory anchor calibration and confidence/evidence gates.
- Versioned facts, audit snapshots, and O(1) change indexes.
- Direct validator tests, network smoke test, CI, and guarded release automation.
