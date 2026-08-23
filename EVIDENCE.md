# Release evidence

## Semantic Drift Oracle 1.0.1

* Repository: `https://github.com/MeowStlanik/semantic-drift-oracle`
* Immutable source: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/20fb374df7b849cf07ed54a50bc6d26dca1a1888/contracts/semantic_drift_oracle.py`
* Direct tests: `https://github.com/MeowStlanik/semantic-drift-oracle/tree/20fb374df7b849cf07ed54a50bc6d26dca1a1888/tests/direct`
* Consensus design: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/20fb374df7b849cf07ed54a50bc6d26dca1a1888/docs/CONSENSUS.md`
* Security analysis: `https://github.com/MeowStlanik/semantic-drift-oracle/blob/20fb374df7b849cf07ed54a50bc6d26dca1a1888/docs/SECURITY.md`
* Contract address: `0xAaed6a9179a0d2477C8fa90EB276082742138647`
* Deployment transaction: `0x325166cb4bcac11baef61e37504d40938457a91c33b76baf3956b8e70b891a13`
* Explorer transaction: `https://explorer-bradbury.genlayer.com/tx/0x325166cb4bcac11baef61e37504d40938457a91c33b76baf3956b8e70b891a13`
* Explorer contract: `https://explorer-bradbury.genlayer.com/address/0xAaed6a9179a0d2477C8fa90EB276082742138647`
* Source SHA-256: `9eb1fc151f4d16272612b9d5cc32383268baf92dd319b85bc7552972263c2e4c`

## Steward cadence fix

`refresh(subscription_id)` enforces cadence from that subscription's own
`last_refresh_at` and `min_refresh_seconds`. There is no shared URL timestamp
whose reset can postpone another subscription watching the same URL.
