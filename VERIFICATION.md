# Verification record

Release 1.0.1 passed two local verification passes before deployment.

## Steward regression

Refresh cadence is enforced per subscription using `last_refresh_at` plus that
subscription's `min_refresh_seconds`. A faster subscription watching the same
URL cannot reset a shared timestamp and delay a slower subscription.

## Pass 1

* Python contract syntax: passed.
* GenVM linter: passed.
* Direct GenLayer tests: passed.

## Pass 2

* Python contract syntax: passed again.
* GenVM linter: passed again.
* Direct GenLayer tests: passed again.

## Deployment

* Source SHA-256: `9eb1fc151f4d16272612b9d5cc32383268baf92dd319b85bc7552972263c2e4c`
* Contract address: `0xAaed6a9179a0d2477C8fa90EB276082742138647`
* Deployment transaction: `0x325166cb4bcac11baef61e37504d40938457a91c33b76baf3956b8e70b891a13`
