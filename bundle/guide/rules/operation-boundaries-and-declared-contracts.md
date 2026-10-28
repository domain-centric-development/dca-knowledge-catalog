---
type: Section
title: Operation boundaries and declared contracts
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

Ordinary use cases do not invoke other use cases, whether directly, through an
input port, or through an application helper. Shared collaborators that do not call
operations remain valid. `DCA-USE-016` follows dependencies within the module's
application layer and reports `Caller -> Target [via Helper]`. A flow that needs a
second operation gets it through an output port (see
[A flow that needs a second operation](#a-flow-that-needs-a-second-operation)).

Existing code that already chains use cases can be admitted one coordinator at a time
while it moves there, with a caller-side exception, for example
`dca.rule.DCA-USE-016.ignore=^com\.example\.module\.application\.coordinate\.CoordinatorUseCase -> `.
This permits the coordinator to invoke operations; it does not permit an operation
to invoke the coordinator, and `DCA-CYC-005` still detects coordination cycles,
including two operations inside the same feature. No coordinator marker is implied.
The exception is a way out for existing code, not a second form for new code. When a
reliable exception cannot be expressed, use WARN with a recorded reason and review the
coordinator's transaction boundaries and partial-failure semantics manually.
Reflection, container lookups and calls through interfaces outside the InputPort
hierarchy also require manual review.

### A flow that needs a second operation

**A command from outside ends at a use case. A use case that needs a second operation asks its own output port for
it.** How the second operation gets behind that port depends on how the flow runs:

- **In the same process and the same transaction** — both steps succeed or fail together. The composition root
  implements the first use case's output port with the second use case.
- **Later, in a transaction of its own** — the second step may run after the first committed, and may be retried.
  The first use case raises a domain event; a transactional listener drives the second use case (see
  [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md)).

The synchronous case, in a context that applies a price list line by line through the existing `ChangePrice` use
case. The first use case states what it needs, in its own words:

```java
// com/company/project/pricing/application/applypricelist/PriceSetter.java
public interface PriceSetter extends OutputPort {
    void setPrice(ProductId product, Money amount);
}

// com/company/project/pricing/application/applypricelist/ApplyPriceListUseCase.java
@Service
@Transactional
public class ApplyPriceListUseCase implements ApplyPriceListInputPort {

    private final PriceSetter prices;                   // its own port — it does not know ChangePrice

    @Override
    public ApplyPriceListResult execute(ApplyPriceListCommand command) {
        for (var line : command.lines()) {              // the decisions: which lines, in which order
            prices.setPrice(line.productId(), line.amount());
        }
        return new ApplyPriceListResult(command.lines().size());
    }
}
```

The composition root puts the second use case behind that port:

```java
// com/company/project/pricing/infrastructure/PricingConfiguration.java
@Configuration
class PricingConfiguration {

    @Bean
    PriceSetter priceSetter(ChangePriceInputPort changePrice) {
        return (product, amount) -> changePrice.execute(new ChangePriceCommand(product, amount));
    }
}
```

Each part does one thing. `ApplyPriceListUseCase` decides and is tested against a fake `PriceSetter`.
`ChangePriceUseCase` stays as it is and knows nothing of price lists. The composition root translates a call into a
command and decides nothing. With `@Transactional` on both, the inner call joins the outer transaction: a failure on
the fiftieth line rolls back the whole list.

The lambda lives in `infrastructure/`, never in `adapter/outgoing/`: an outgoing adapter must not depend on an input
port (`DCA-HEX-013`). An incoming adapter that calls two use cases in a row is no alternative either. It makes the
order of the steps a decision of the adapter, and no use-case test sees it.

The input port describes the complete effective public instance surface (`DCA-USE-017`).
Declared and inherited business methods, unrelated-interface methods and public
properties/getters/setters must be in the input-port contract. Constructors, Object
members and compiler-generated members are exempt; a property accessor is not exempt
merely because it has a special runtime name. Ordinary, inherited and explicit
input-port implementations are valid. In .NET, `DCA-NET-003` separately validates
`IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken)` returning `Task<T>` through
the interface map; it does not count declared public methods.

For every declared ACL interaction, the matching adapter must contain a class that
uses that upstream's channel contract and the declaring context's own domain or
application model (`DCA-MAP-008`). Two translators for different upstreams may share
an adapter package. Evidence for one upstream does not satisfy another interaction.
This identifies a structural translation site, without proving translation quality.

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [OutputPort](/marker/port-out/outputport.md)
