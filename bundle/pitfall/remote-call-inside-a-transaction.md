---
type: Pitfall
title: "Remote call inside a transaction"
tags: [pitfall, application, use-case, port-out, persistence, performance]
---

A `@Transactional` use case (or the body of an explicit transaction block) that calls an output port which may leave the process — another bounded context's API, a payment provider, a mail gateway, a remote catalog. In the monolith the call is in-process and nothing hurts; in the distributed deployment the same code holds a database connection for a network round trip.

## Why it is wrong

- The connection is pinned for the whole remote call. Under load the pool is exhausted by requests that are not touching the database at all; the symptom appears far from the cause.
- A rollback after a successful remote call cannot undo the remote effect: the card is charged, the mail is sent, the order is gone from the database.
- The transaction's duration is now bounded by somebody else's latency and availability.

## What forbids it

- [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md) — only `Repository`, `Store` and the event publishers may be called inside a declaratively transactional use case.
- [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md) — a publishing use case needs a boundary; the explicit form exists exactly so remote reads can stay outside it.

## Do instead

Remote **reads** first, outside any transaction; then one short transaction with the explicit boundary — load, mutate, save, publish; remote **effects** after the commit, as a reaction to an integration event (retry, idempotent). Read-only use cases that call remote ports run without a transaction at all.

```java
Article article = articleDataPort.getArticleData(productId);   // remote read — no transaction
return transactionBoundary.inTransaction(() -> {               // short transaction
  ShoppingCart cart = carts.findById(cartId).orElseThrow();
  cart.addItem(productId, quantity, article.price());
  carts.save(cart);
  events.publishAndClearEvents(cart);
  return AddItemToCartResult.from(cart);
});
```

- Decision: [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md)

## Anchors

- Rules: [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/declaratively-transactional-use-cases-must-not-call-remote-capable-output-ports.md) · [Use cases that publish domain events must have a transaction boundary](/rule/usecase/use-cases-that-publish-domain-events-must-have-a-transaction-boundary.md)
- Markers: [TransactionBoundary](/marker/application/transactionboundary.md) · [OutputPort](/marker/port-out/outputport.md)
- Guide: [Layer rules](/guide/readme/rules.md)
