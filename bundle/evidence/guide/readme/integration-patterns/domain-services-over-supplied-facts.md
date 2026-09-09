---
type: Reference
title: INTEGRATION PATTERNS — Domain services over supplied facts
tags: [reference]
evidence_for: "/guide/readme/integration-patterns.md#domain-services-over-supplied-facts"
---

[Full node and context](/guide/readme/integration-patterns.md#domain-services-over-supplied-facts). This is an evidence excerpt; retain the parent selection and caveats.

### Domain services over supplied facts

An aggregate answers questions about its own state. When a calculation combines facts from other aggregates or
contexts, the use case retrieves them through output ports and passes immutable snapshots to a domain service.
Moving a lookup behind a resolver/callback parameter does not change who owns the calculation. Neither the aggregate
nor the service receives a repository or remote port. A domain-owned `DomainGateway` is an explicit exception with
an effect and dependency rationale; a pure algorithmic strategy is different from a hidden external lookup.

```java
// Domain service: the use case has already retrieved the article facts.
public final class CartPricing implements DomainService {
    public record Line(ProductId productId, Quantity quantity) implements Value {}

    public Money calculateTotal(List<Line> lines, Map<ProductId, ArticlePrice> facts) {
        Money total = Money.euro(0);
        for (Line line : lines) {
            total = total.add(facts.get(line.productId()).price().multiply(line.quantity().value()));
        }
        return total;
    }
}
```

The service owns the external-fact calculation; the aggregate owns the state transition. Pass the assessment or facts
into that transition, then save and publish in the use case. Presentation enrichment stays a separate value model.
`DCA-TAC-002` checks fields, not semantic responsibility: callback parameters need manual review. No marker proves
that an operation belongs on a particular object.
