---
type: Decision
title: "Domain service data access: injected output port or passed-in data"
tags: [decision, tactical, domain-service, domain, gateway]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainservice.md, /marker/tactical/domaingateway.md, /marker/port-out/outputport.md, /marker/port-out/repository.md, /marker/port-out/store.md, /rule/advanced/dca-adv-012.md, /rule/advanced/dca-adv-011.md, /rule/advanced/dca-adv-010.md]
---

An aggregate answers from its own state. If an operation combines facts held elsewhere, the use case retrieves
those facts through output ports and supplies immutable snapshots to a domain service. The service owns the calculation;
the aggregate owns its invariant-preserving state transition. Presentation enrichment remains a separate value model.

## Default: supplied facts

Neither aggregate nor domain service receives a repository or remote port. Moving external lookup behind a resolver
or callback parameter does not transfer semantic responsibility into the aggregate. Supply facts or a calculated
assessment instead; save and publish in the use case's transaction after remote retrieval.

## Explicit exceptions and manual review

A domain-owned DomainGateway may represent a capability whose rationale is recorded explicitly. Local password
hashing is a computational capability, not a reason to hide cross-context retrieval. Pure algorithmic strategy
callbacks do not perform lookup. Review callback parameters for effects and ownership; DCA-TAC-002 checks fields
and cannot prove semantic responsibility. No new marker can prove it either.

## Anchors

- Markers: [DomainService](/marker/tactical/domainservice.md) · [DomainGateway](/marker/tactical/domaingateway.md) · [OutputPort](/marker/port-out/outputport.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [Store](/marker/port-out/store.md)
- Rules: [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/dca-adv-012.md) · [Domain Services must not carry framework metadata](/rule/advanced/dca-adv-011.md) · [Domain Services must reside in domain package](/rule/advanced/dca-adv-010.md) · [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/dca-tac-002.md)
- Guide: [Problem statement](/guide/domain-services-with-data-dependencies/problem-statement.md) · [Default rule: pure domain services](/guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md) · [DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md) · [Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/approach-2-strategy-callback-pattern.md) · [When to use which approach](/guide/domain-services-with-data-dependencies/comparison-when-to-use-which-approach.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- Related decision: [Where does the logic live](/decision/where-does-the-logic-live.md) — the companion fork for *placing* the behaviour before you decide how it gets its data
- Related pitfall: [Anemic domain model](/pitfall/anemic-domain-model.md)

- [Default construction and boundary validation](/pitfall/default-construction-bypasses-validation.md)
