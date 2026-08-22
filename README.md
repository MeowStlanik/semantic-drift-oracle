# Semantic Drift Oracle

Semantic Drift Oracle is a standalone GenLayer Intelligent Contract that tracks
the *meaning* of external documents rather than their bytes. It turns questions
such as “What is the maximum withdrawal fee?” into versioned, consensus-backed
facts that other contracts can query cheaply.

This repository is deliberately a contract primitive, not a frontend product.

## Why it matters

Terms of service, grant rules, API documentation, partner policies, and
regulatory text change quietly. A content hash detects cookie banners and date
changes as readily as a new obligation. This contract instead stores a short,
normalized answer per watched clause and classifies later observations as:

- `MATERIAL` — the value, duty, permission, threshold, deadline, support status,
  eligibility condition, or other substantive meaning changed;
- `COSMETIC` — wording changed, but the substantive fact is equivalent;
- `UNCHANGED` — no meaningful change;
- `BASELINE` — the first accepted observation.

## The primitive

1. An owner calls `watch(subscription_id, url, clauses_json,
   min_refresh_seconds)`. Each subscription must include one to three anchor
   clauses with an expected stable answer.
2. Anyone may call `refresh(subscription_id)`. Each subscription enforces its
   own deterministic refresh interval for owners and third parties alike.
3. Validators independently fetch and extract the same facts. Structural gates,
   confidence thresholds, anchor calibration, and a semantic comparison all
   have to pass.
4. On every post-baseline refresh, a second nondeterministic round independently
   classifies drift. Validators must match the leader's drift labels exactly.
5. Only accepted results enter storage. Raw page text is never persisted.

The current GenLayer guidance recommends custom `run_nondet_unsafe`
leader/validator pairs for serious validation logic, with independent evidence
rather than leader-output-only schema checks. This contract follows that model:
[Equivalence Principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle).

## Consensus design

### Round 1: source-grounded extraction

The leader renders the URL as text, truncates it to a documented 60,000-character
budget, and asks an LLM for one normalized record per clause:

```json
{
  "id": "withdrawal_fee",
  "value": "2%",
  "evidence_quote": "Maximum withdrawal fee: 2%.",
  "confidence": 96,
  "anchor_status": "NOT_ANCHOR"
}
```

The validator independently repeats the web fetch and extraction, then applies:

- exact clause-set and uniqueness checks;
- bounded values/evidence and confidence `>= 60`;
- mandatory `MATCH` on every anchor;
- a separate semantic comparison requiring equivalent values and supporting
  evidence, while allowing wording variation and at most 20 confidence points.

A malformed, low-confidence, uncalibrated, missing, added, or contradictory
answer is rejected.

### Round 2: materiality decision

For initialized clauses, the accepted new value is compared with the stored old
value under an explicit rubric. The validator independently reruns the
classification. The two maps of `{clause_id: drift}` must be exactly equal;
rationale prose may differ. This keeps the subjective explanation flexible but
the state transition strict.

See [docs/CONSENSUS.md](docs/CONSENSUS.md) for the invariants and threat model.

## State and composability

The contract stores:

- subscription configuration, owner, activity flag, interval, and aggregate
  counts;
- one current `ClauseState` per `(subscription_id, clause_id)`;
- immutable JSON audit snapshots keyed by subscription and snapshot number;
- `last_change_snapshot` and `last_material_snapshot` indexes for O(1)
  downstream checks.

Useful view methods:

| Method | Purpose |
| --- | --- |
| `latest(subscription_id, clause_id)` | Current normalized fact plus provenance |
| `changed_since(subscription_id, clause_id, snapshot)` | O(1) material/cosmetic change check |
| `get_snapshot(subscription_id, snapshot)` | Full accepted audit record |
| `get_subscription(subscription_id)` | Configuration and counters |
| `get_stats()` | Deployment smoke check and protocol limits |

Examples of composition include pausing an escrow after material partner-policy
drift, opening a DAO proposal when grant eligibility changes, or gating an
integration on documented API support.

## Quick start

Requirements: Python 3.12+; `uv` is recommended because it installs the pinned
test toolchain reliably.

```bash
python -m venv .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/genvm-lint check contracts/semantic_drift_oracle.py
.venv/bin/pytest tests/direct -v
```

The direct tests use the official `genlayer-test` in-memory VM, mocked web/LLM
calls, real GenLayer storage/decorators, captured validators, and pickling
validation. GenLayer documents this as the fast first testing layer, followed by
network tests where needed: [Testing Intelligent Contracts](https://docs.genlayer.com/developers/intelligent-contracts/testing).

Run the explicit network smoke test against a running localnet:

```bash
gltest tests/integration -v -s
```

## Registering a watch

`clauses_json` is a JSON array. An empty `anchor_expected` means a normal clause;
a non-empty value makes it a calibration anchor.

```json
[
  {
    "id": "withdrawal_fee",
    "question": "What is the maximum withdrawal fee?",
    "anchor_expected": ""
  },
  {
    "id": "document_title",
    "question": "What is the title of this document?",
    "anchor_expected": "Example Partner Terms"
  }
]
```

The owner chooses stable anchors that appear on the same page and are known in
advance. A changed or missing anchor intentionally blocks the refresh instead of
letting an uncalibrated observation update state.

## Deployment and release

GenLayer's current CLI supports direct contract deployment and Bradbury at
`https://rpc-bradbury.genlayer.com`: [CLI deployment](https://docs.genlayer.com/developers/intelligent-contracts/deploying/cli-deployment),
[network reference](https://docs.genlayer.com/developers/networks).

Deployment evidence is recorded in EVIDENCE.md. After any source change, the
contract must be redeployed and the recorded source hash/address updated before
resubmission; an older address must not be presented as matching the new source.
No private key or deployment credential belongs in this repository.

## Design boundaries

- Web availability and provenance remain source risks; consensus does not make a
  compromised website truthful.
- This version is non-custodial. It uses bounded inputs, permissionless rate
  limiting, and anchors rather than a native-token refresh bond. Keeping value
  transfer out of the primitive avoids custody and asynchronous refund failure
  modes; a bounty/bond adapter can compose above it.
- Refresh cadence is tracked per subscription via `last_refresh_at`; one watch
  cannot postpone another watch of the same URL by choosing a different
  interval. Consumers should still trust the subscription configuration they
  choose.
- The 60,000-character page budget and 12-clause limit bound LLM context and
  on-chain growth. Split large documents into multiple subscriptions.

See [docs/SECURITY.md](docs/SECURITY.md) and [docs/API.md](docs/API.md).
The exact local verification record is in [VERIFICATION.md](VERIFICATION.md).

## License

MIT
