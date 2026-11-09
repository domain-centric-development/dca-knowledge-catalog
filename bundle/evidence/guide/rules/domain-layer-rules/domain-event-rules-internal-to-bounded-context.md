---
type: Reference
title: "DOMAIN LAYER RULES — Domain Event Rules (Internal to Bounded Context)"
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#domain-event-rules-internal-to-bounded-context"
---

[Full node and context](/guide/rules/domain-layer-rules.md#domain-event-rules-internal-to-bounded-context). This is an evidence excerpt; retain the parent selection and caveats.

### Domain Event Rules (Internal to Bounded Context)
- Domain Events are immutable
- Domain Events use past tense naming (e.g., OrderCreated, not CreateOrder)
- A domain event's name is the term plus the past participle of the operation's code word in the
  glossary: the operation *place* on an order gives `OrderPlaced`, never `OrderSubmitted` beside it
- Domain Events represent something that happened in the domain
- Domain Events are part of the domain model: `{context}/domain/model/`, or an own
  `{context}/domain/event/` segment once the model package grows. `DCA-ADV-002` requires the
  domain layer, not a segment within it
- Domain Events enable eventual consistency within bounded context
- Domain Events emitted by aggregates during state changes
- Domain Events published by use cases via DomainEventPublisher (Output Port)
- Domain Events handled asynchronously when crossing aggregates: a listener that drives an input port is a
  transactional listener — after the commit, in its own transaction, from a durably captured publication
  ([Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md))
- A synchronous listener runs in the publishing transaction and calls output ports only (the translator,
  a metrics port)
- A stored domain event is read by the next deployment: tolerant reading, two-step renames, no version number
- Domain Events must not contain behavior, only data
- Domain Events belong to the domain layer, not adapters
