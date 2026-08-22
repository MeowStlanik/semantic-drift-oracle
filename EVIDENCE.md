# Release evidence

## Semantic Drift Oracle 1.0.1

- Repository: `https://github.com/MeowStlanik/semantic-drift-oracle`
- Immutable source: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/main/contracts/semantic_drift_oracle.py`
- Direct tests: `https://github.com/MeowStlanik/semantic-drift-oracle/tree/main/tests/direct`
- Consensus design: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/main/docs/CONSENSUS.md`
- Security analysis: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/main/docs/SECURITY.md`
- Contract address: `0xA1993e6357C6242c051cd96d6Bd8d63Ed488b557`
- Deployment transaction: `0x80d7798862dec85a146ef83ebce92c8d87941d9d43a3d3fccefa6987b2308faa`
- Explorer transaction: `https://explorer-bradbury.genlayer.com/tx/0x80d7798862dec85a146ef83ebce92c8d87941d9d43a3d3fccefa6987b2308faa`
- Explorer contract: `https://explorer-bradbury.genlayer.com/address/0xA1993e6357C6242c051cd96d6Bd8d63Ed488b557`
- Source SHA-256: `9eb1fc151f4d16272612b9d5cc32383268baf92dd319b85bc7552972263c2e4c`
- Deployment/source match: **verified twice from Bradbury on-chain contract code**.

## Steward cadence fix

`refresh(subscription_id)` enforces cadence from that subscription's own
`last_refresh_at` and `min_refresh_seconds`. There is no shared URL timestamp
whose reset can postpone another subscription watching the same URL.

The release gate runs the direct verification twice before deployment and then
fetches the deployed contract code from Bradbury twice. Both on-chain SHA-256
checks must equal the local contract SHA-256 before GitHub publication is
allowed.
