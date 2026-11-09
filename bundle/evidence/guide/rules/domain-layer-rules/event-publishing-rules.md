---
type: Reference
title: DOMAIN LAYER RULES — Event Publishing Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#event-publishing-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#event-publishing-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Event Publishing Rules
- Use cases call DomainEventPublisher (Output Port) to publish events
- `DomainEventPublisher` is the library port (`hexagonal.port.out`); the application implements it once, in the shared kernel
- DomainEventPublisherAdapter in adapter/outgoing/messaging
- Adapter converts domain events to integration events via mapper
- Message broker (Kafka, RabbitMQ) used for async delivery
- One topic per bounded context or per event type
- Order inside the use case: `save`, then `publishAndClearEvents` — same transaction, never before the save
- The publisher dispatches first and clears the aggregate afterwards; the clear is the acknowledgement that every listener saw the event. A throwing listener fails the use case and leaves the events on the aggregate
- Integration events go through a **transactional outbox**: the publication is written *inside* the aggregate's transaction (Spring Modulith's event publication registry, an outbox table, an in-process stand-in), made eligible atomically with commit and followed by an after-commit wakeup, discarded on rollback. Registering only after commit leaves a crash window between commit and outbox entry
- Delivery is asynchronous and at least once: failures are retried with backoff, permanently failing publications stay visible (`Failed`), outstanding ones are replayed on restart
