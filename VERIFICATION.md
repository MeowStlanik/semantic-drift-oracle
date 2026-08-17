# Verification record

Verified on 2026-08-17 with Python 3.12.13.

## Final source — pass 1

- Python bytecode compilation: passed.
- `genvm-lint 0.11.0 check`: passed all lint and SDK validation checks.
- `genvm-lint 0.11.0 typecheck`: no type errors.
- `genlayer-test 0.29.2` direct suite: 17 passed.

## Final source — pass 2

- Python bytecode compilation: passed.
- `genvm-lint 0.11.0 check`: passed all lint and SDK validation checks.
- `genvm-lint 0.11.0 typecheck`: no type errors.
- `genlayer-test 0.29.2` direct suite: 17 passed in a fresh pytest process.

The direct suite deploys the contract through the GenLayer in-memory VM using
the pinned stable GenVM runner, exercises real storage/decorators and mocked
nondeterministic operations, explicitly executes captured validator functions,
and enables pickling validation on the baseline path.

## Network scope

`tests/integration/test_deployment.py` is included for a real localnet/studionet
deployment smoke test. It was not executed in this build environment because no
GenLayer account/local Studio was available. The release script makes external
deployment a user-controlled step and refuses to publish evidence until
Bradbury deployment, schema retrieval, and a no-argument `get_stats()` call all
succeed.

The linter reports a newer prerelease runner hash, but the corresponding latest
GitHub release asset returned HTTP 404 during testing. The contract therefore
keeps the stable `py-genlayer` dependency used by the current official examples
instead of claiming verification against an unavailable runner.
