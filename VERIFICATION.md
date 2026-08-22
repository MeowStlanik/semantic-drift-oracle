# Verification record

Release 1.0.1 was gated by two local verification passes and two independent
Bradbury code-hash checks.

## Steward regression

Refresh cadence is enforced per subscription using `last_refresh_at` plus that
subscription's `min_refresh_seconds`. A faster subscription watching the same
URL cannot reset a shared timestamp and delay a slower subscription.

## Pass 1

- Python contract syntax: passed.
- GenVM linter: passed.
- Direct GenLayer tests: passed.

## Pass 2

- Python contract syntax: passed again.
- GenVM linter: passed again.
- Direct GenLayer tests: passed again.

## Deployment match

- Source SHA-256: `9eb1fc151f4d16272612b9d5cc32383268baf92dd319b85bc7552972263c2e4c`
- Contract address: `0xA1993e6357C6242c051cd96d6Bd8d63Ed488b557`
- Deployment transaction: `0x80d7798862dec85a146ef83ebce92c8d87941d9d43a3d3fccefa6987b2308faa`
- Bradbury code SHA-256 pass 1: matched.
- Bradbury code SHA-256 pass 2: matched.
