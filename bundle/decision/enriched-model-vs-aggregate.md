---
type: Decision
title: Enriched value model or aggregate
tags: [decision, aggregate, domain]
review: reviewed
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, "/rule/retired.md#dca-tac-022"]
---

Choose an aggregate when the object owns identity, a lifecycle and invariants changed through commands.
Choose an enriched value model when it combines already known facts into a read result without acquiring a
new lifecycle or authority to mutate its sources. Enrichment may combine a local snapshot with facts obtained
through consumer-defined ports before assembly. It does not require a projection store or CQRS split.

An enriched model implements `Value` / `IValue`, carries no aggregate or entity references, and follows the
value rules for immutability and equality. A record is convenient but not required: an immutable class is valid.
Names follow the domain, with no mandatory `Enriched` prefix. For example, `ExtendedDocument` and
`DocumentWithCurrentPermissions` express the result's meaning without assigning it aggregate identity.

A factory may assemble the values from supplied facts; it does not fetch remote data or gain persistence
ownership. Keep coordination in the application and calculations on values or domain services as appropriate.
`DCA-TAC-022` was retired because a prefix alone cannot establish this semantic role; once marked as a value,
TAC-008..012 govern its structural shape. Selection by naming is not a substitute for choosing the model.

- [Value](/marker/tactical/value.md)
- [Retired rule identities](/rule/retired.md#dca-tac-022)
- [Plain query or dedicated read model](/decision/read-model-vs-domain-query.md)
- [Result shape and assembly](/decision/result-shape-and-assembly.md)
