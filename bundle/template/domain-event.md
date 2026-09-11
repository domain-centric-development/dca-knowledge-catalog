---
type: Template
title: "Domain event skeleton (record implementing DomainEvent)"
tags: [template, domain, domain-event]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /marker/tactical/domainevent.md, /marker/tactical/baseaggregateroot.md, /rule/advanced/dca-adv-001.md, /rule/advanced/dca-adv-008.md, /rule/advanced/dca-adv-004.md, /rule/advanced/dca-adv-002.md, /rule/advanced/dca-adv-007.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a domain event: an immutable fact about something that happened, internal to one bounded context. Model it as a Java `record` implementing `DomainEvent`, named in the **past tense**, with no `Event` suffix and no `version` field (that is reserved for integration events). The aggregate registers it; the use case publishes and clears it after persistence. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`. The domain layer is framework-free — no Spring annotations.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-event/java.md`](/template/domain-event/java.md)

## Realizes / governed by

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- Rules: [Domain Events must implement DomainEvent Marker Interface and be records](/rule/advanced/dca-adv-001.md) · [Domain Events must have a timestamp field](/rule/advanced/dca-adv-008.md) · [Domain Events must not have Spring annotations](/rule/advanced/dca-adv-004.md) · [Domain Events must reside in domain package](/rule/advanced/dca-adv-002.md) · [Domain Events that are not Integration Events must not have a version field](/rule/advanced/dca-adv-007.md)
- Guide: [Layer rules](/guide/rules.md) · [Integration patterns](/guide/integration-patterns.md)
- Decision: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
