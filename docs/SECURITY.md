# Security notes

## Threats addressed

| Threat | Control |
| --- | --- |
| Malicious or mistaken leader | Independent validator fetch/extraction |
| Byte-level web variance | Semantic comparison of normalized facts |
| Prompt injection in page | Explicit untrusted-document delimiter and anchor circuit breaker |
| Hallucinated fact | Evidence quote, confidence gate, validator reproduction |
| Wrong/redirected page | 1–3 mandatory known anchors |
| Format-only consensus | Validator derives independent evidence before comparison |
| Materiality ambiguity | Explicit rubric and exact validator agreement on labels |
| Refresh spam | Per-URL interval for all callers, bounded clauses/page/context |
| State bloat | No raw pages; 12 clauses; bounded fields and immutable compact snapshots |
| Nondeterministic storage writes | All writes occur after consensus |

## Trust assumptions

The watched origin remains an authority for its own document. Consensus can
detect whether validators agree on what the page says; it cannot prove the
publisher is honest, detect every targeted response, or guarantee availability.

Subscription owners choose the URL, questions, and anchors. Downstream contracts
should bind to a reviewed subscription ID/owner/configuration. Do not discover an
arbitrary subscription by URL and assume it is trustworthy.

## Prompt injection

Web content is marked as untrusted and placed inside an explicit document
boundary. Validators independently render it, mandatory anchors must survive the
same path, and outputs are constrained before semantic comparison. These controls
reduce prompt-injection risk but do not eliminate model-level attacks. High-value
consumers should use stable, narrowly scoped sources and multiple subscriptions.

## Refresh economics

The core is intentionally non-custodial. Native-token slashing would require
custody, a burn/sink policy, and asynchronous outbound messages whose failure
semantics become part of the oracle's security boundary. A separate adapter can
require a bond, call `refresh`, and settle incentives based on snapshot deltas.

## Operational guidance

- Use one to three anchors that are stable, visible, and semantically distinct.
- Ask narrow clauses that yield short factual answers.
- Treat low-confidence/undetermined transactions as a safe failure, not as
  `UNCHANGED`.
- Pause a subscription before changing downstream policy.
- Review material events and source evidence before irreversible high-value acts.
