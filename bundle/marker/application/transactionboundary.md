---
type: Marker
title: TransactionBoundary
category: application
kind: interface
signature: public interface TransactionBoundary
package: dev.domaincentric.dca.buildingblocks.application
methods: ["<T> T inTransaction(Supplier<T> work)", "default void inTransaction(Runnable work)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/TransactionBoundary.java
tags: [application, marker]
---

Explicit transaction boundary inside a use case — an application-layer execution abstraction,
**not** an output port.

An output port describes a capability the application needs from the outside world (store an
aggregate, look up a price, publish an event). A transaction is no such interaction: it defines
the execution semantics of several of them. The interface therefore lives beside the use cases
and does not extend `OutputPort`; the implementation is infrastructure - a thin wrapper
around the platform's programmatic transaction API (Spring's `TransactionTemplate` is one
implementation, JTA's `UserTransaction` another).

The default boundary is the use case itself, declared with the framework's transactional
annotation: load, mutate, save, publish — all inside one short transaction. That default breaks
down as soon as the use case also talks to the outside world (payment provider, remote catalog,
mail gateway): a remote call inside the transaction holds a database connection for the duration
of the call, and under load the connection pool runs dry; a rollback after a successful remote
call cannot undo the remote effect either.

`TransactionBoundary` lets the use case draw the boundary by hand — remote reads before,
the transactional core inside, remote effects after (preferably as a reaction to an integration
event):

```java
Article article = articleDataPort.getArticleData(productId);   // remote read, no transaction
return transactionBoundary.inTransaction(() -> {               // short transaction
  ShoppingCart cart = carts.findById(cartId).orElseThrow();
  cart.addItem(productId, quantity, article.price());
  carts.save(cart);
  events.publishAndClearEvents(cart);
  return AddItemToCartResult.from(cart);
});
```

Domain events published inside `inTransaction(Supplier)` see the same transaction as
the save; after-commit listeners fire when it commits.

**Nesting.** A call inside a running transaction joins it (the "required" propagation every
transaction manager offers) — there is one commit, at the outermost boundary. A failure in an
inner block marks the shared transaction rollback-only even when the outer block catches the
exception: the outermost `inTransaction` then rolls back and throws instead of committing
half of the work. Implementations must preserve this; an in-memory implementation emulates it
with a rollback-only flag.

**Rules of thumb:**

- No remote call inside a transaction — neither in an annotated use case nor inside `inTransaction`.
- One aggregate per transaction; cross-aggregate consistency is eventual.
- Use the annotation when the whole use case is local; use `TransactionBoundary` when
it is not.

## Related mentions in guides (heuristic)

- [ELEMENTS](/guide/readme/elements.md)
- [RULES](/guide/readme/rules.md)
