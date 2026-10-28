---
type: Recipe
title: Hand a use case a second operation
tags: [recipe, application, port-out, use-case, infrastructure]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-016.md, /rule/hexagonal/dca-hex-013.md, /rule/cycles/dca-cyc-005.md, /marker/port-out/outputport.md, /marker/port-in/usecase.md, /guide/rules/operation-boundaries-and-declared-contracts.md, /guide/dependency-structure/the-composition-root.md]
---

A use case needs what another use case already does — apply a list line by line through an existing operation, start
a sub-run, settle a step. It never calls that use case: a command from outside ends at a use case, and a use case that
needs a second operation asks its **own output port** for it. Who stands behind the port is decided where objects are
put together, in the composition root.

## Steps

1. **Decide how the two steps run together.**
   - Both must succeed or fail together, in one process and one transaction → steps 2–5.
   - The second may run later, in its own transaction, and be retried → no port: the first use case raises a domain
     event and a transactional listener drives the second ([Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)).
   - Neither, because the "second operation" is only a mechanical step of the first (a flag, a lookup) → it is no
     operation; keep it inside the first use case or behind the output port it already has.
2. **Declare the port in the first use case's words.** An interface extending `OutputPort` beside the first use case
   (or in `application/shared/` when several use it), named for what the first use case needs, not for the use case
   behind it: `PriceSetter.setPrice(product, amount)`, not `ChangePriceCaller`. Its parameters are the first use
   case's types; it knows no command of the second.
3. **Let the first use case decide.** It depends on the port only; the order of the steps, what a failure of one step
   means for the rest, and what it counts all stay in its `execute`. Test it against a fake port.
4. **Implement the port in the composition root.** In `{context}/infrastructure/` — a `@Bean` in the context's
   `@Configuration` (Spring), a registration in `Add{Context}Context()` (.NET), a line in the hand-written root (no
   container). The implementation takes the second use case's input port and turns a call into its command:

   ```java
   @Bean
   PriceSetter priceSetter(ChangePriceInputPort changePrice) {
       return (product, amount) -> changePrice.execute(new ChangePriceCommand(product, amount));
   }
   ```

   It translates and decides nothing: no `if` over a business value, no loop. A condition that wants in is a decision
   of the first use case.
5. **Check the transaction.** In-process, the second use case's boundary joins the first's (`@Transactional`
   `REQUIRED`; an ambient transaction in .NET). The first use case draws the boundary; a failure in any step rolls
   back all of them. If that is wrong for the domain, step 1 picked the wrong branch.
6. **Verify** — the architecture suite. `DCA-USE-016` stays silent because the first use case knows no input port;
   `DCA-HEX-013` because the implementation lives in `infrastructure/`, not in an outgoing adapter.

## Rules to satisfy (build-time checklist)

- [Use cases must not invoke other use cases](/rule/usecase/dca-use-016.md) — the first use case depends on its output port only
- [Outgoing Adapters must not depend on input ports](/rule/hexagonal/dca-hex-013.md) — the bridge is no outgoing adapter
- [Feature and use case packages within a module's application layer must not have cyclic dependencies](/rule/cycles/dca-cyc-005.md) — the second use case never reaches back to the first

## Not the answer

- **An incoming adapter that calls two use cases in a row.** The order of the steps becomes a decision of the
  adapter, outside every use-case test, and the two run in two transactions.
- **The bridge in `adapter/outgoing/`.** That is the direction `DCA-HEX-013` forbids: an adapter that drives the
  application from the driven side.
- **A `DCA-USE-016` exception for a new coordinator.** The caller-side exception admits existing code while it moves;
  it is not a second form for new code.

## Anchors

- Guide: [A flow that needs a second operation](/guide/rules/operation-boundaries-and-declared-contracts.md) · [The composition root](/guide/dependency-structure/the-composition-root.md) · [Reacting to an event](/guide/integration-patterns/reacting-to-an-event.md)
- Markers: [OutputPort](/marker/port-out/outputport.md) · [UseCase](/marker/port-in/usecase.md)
- A process that outlives one transaction: [A process that spans several transactions](/guide/integration-patterns/a-process-that-spans-several-transactions.md)
- Sibling recipes: [Add a use case](/recipe/add-a-use-case.md) · [Test a use case](/recipe/test-a-use-case.md)
