# Consensus specification

## Accepted extraction invariants

An extraction can enter state only if both the leader proposal and the
validator's independent extraction satisfy all of these rules:

1. The result is an object with one `clauses` array.
2. The array contains exactly the registered clause IDs, once each.
3. `value` and `evidence_quote` are non-empty and bounded.
4. `confidence` is an integer in `[60, 100]`.
5. Normal clauses report `NOT_ANCHOR`; every anchor reports `MATCH`.
6. A validator-side semantic comparison accepts the two independently grounded
   outputs under the contract's explicit principle.

This is substantive validation. The validator fetches the source and derives its
own answer before seeing whether the leader should be accepted. Format-only
validation is insufficient.

## Accepted drift invariants

For every initialized clause, both leader and validator independently classify
the same `(question, old_value, new_value)` tuple. Each result must contain
exactly one allowed label per clause. The maps of clause ID to label must be
identical.

Rationales are stored for auditability but excluded from equality because prose
is nondeterministic. The label controls state indexes and counters.

## Deterministic boundary

Web rendering, LLM extraction, semantic comparison, and materiality
classification occur only inside `run_nondet_unsafe` leader/validator functions.
Storage writes occur only after consensus returns an accepted result. The
transaction timestamp is deterministic GenVM context and is stored only after
consensus.

## Anchor calibration

Anchors are clauses with a known expected answer registered alongside ordinary
clauses. They travel through the same fetch and extraction path. If either the
leader or a validator cannot reproduce the expected meaning at sufficient
confidence, that validator rejects the entire extraction.

Anchors detect several bad states early: wrong page, redirect/login content,
prompt injection, broken rendering, model confusion, and genuine disappearance
of a supposedly stable page fact. They are a circuit breaker, not proof that all
other clauses are correct.

## Failure behavior

- Leader error: validator rejects the proposal.
- Validator I/O, JSON, or LLM error: caught and returned as disagreement.
- Low confidence or missing evidence: rejected.
- Failed anchor: rejected.
- Extraction semantic disagreement: rejected.
- Drift-label disagreement: rejected.

No storage mutation occurs until the corresponding consensus call succeeds.

## Why two rounds

Combining extraction and drift into one unconstrained LLM result would allow a
leader to hide an extraction disagreement behind a plausible drift label. Two
rounds establish the new fact first, then apply a separate state-transition
rubric. This separation also makes each validator testable in isolation.
