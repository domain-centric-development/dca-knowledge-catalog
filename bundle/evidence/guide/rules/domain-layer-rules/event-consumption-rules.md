---
type: Reference
title: DOMAIN LAYER RULES — Event Consumption Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#event-consumption-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#event-consumption-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Event Consumption Rules
- Event Consumer in adapter/incoming/messaging receives integration events
- Anti-Corruption Layer (ACL) protects domain from external formats
- ACL converts events to domain commands; it belongs to the incoming adapter, and an own
  `acl/` package there is a convention, not a rule
- Event Consumer calls Input Port, never domain directly
- A request is not an event. A press, a request file or a message that asks for something can be refused, can wait
  and can fail, so it is a command: it gets a lifecycle — an aggregate, or a process manager — and its outcomes raise
  the events. An event is a fact nobody refuses. A file or a queue as an inbox is a legitimate transport for
  commands; the port does not change with the transport
- Consuming bounded context maintains its own model
- Eventual consistency between bounded contexts via events
- Assume at-least-once delivery: consumers deduplicate per effect (the effect and the event ID, recorded in the effect's transaction) or make the operation naturally idempotent
- Consumers tolerate out-of-order arrival (check event version/timestamp, never assume sequence)
- Permanently failing events go to a dead-letter queue — never dropped silently
- An event handler modifies at most one aggregate, in its own transaction
