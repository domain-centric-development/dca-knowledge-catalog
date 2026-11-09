---
type: Reference
title: DOMAIN LAYER RULES — Domain Service Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#domain-service-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#domain-service-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Domain Service Rules
- Domain Service is stateless
- Use when operation doesn't belong to Entity or Value Object
- Use when operation involves multiple domain objects
- Domain Service operates in domain language
- Domain Service is part of domain layer
- No dependencies on application or outer layers
- **A domain service is used by the application and by other domain services only.** The use case calls it
  and carries its outcome in the result. An aggregate, an entity or a value does not call it, nor does a read
  model, an adapter of either direction or the composition root — the composition root only constructs it and
  hands it to a use case. A read model computes on query through the aggregate and its values, never through a
  domain service: a decision belongs to the aggregate, or to the use case that asks the service
  (`DCA-ADV-021`, experimental; `DCA-ADV-019` holds the model's part of it, `DCA-HEX-012` the incoming
  adapter's)
