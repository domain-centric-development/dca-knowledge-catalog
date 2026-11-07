---
type: Reference
title: ERROR HANDLING RULES — What a result does not do for you
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#what-a-result-does-not-do-for-you"
---

[Full node and context](/guide/rules/error-handling-rules.md#what-a-result-does-not-do-for-you). This is an evidence excerpt; retain the parent selection and caveats.

### What a result does not do for you

These hold where a context returns its refusals.

- **An ignored result swallows a refusal.** Neither Java nor C# warns about a call whose result nobody reads. A
  caller that ignores the result treats every refusal as success, and nothing says so. Test helpers are where it
  happens first: a helper that adds an item to arrange a test asserts the success case
  (`assertInstanceOf(Added.class, …)`), or a refused arrangement passes and the test asserts on a state that
  never came about.
- **A caller with nobody to answer throws, on purpose.** An event consumer has no one to show a refusal to, and an
  open host service whose own contract has no such case cannot pass it on. Such a caller turns the case back into
  an exception — `IllegalStateException`, with the case's values in the message — so the delivery's retry or the
  calling context's failure handling sees it. A foreign system that did not answer is the typical case: thrown back,
  the delivery is tried again once the system is back. Dropping the case there is the ignored result again.
- **The thrown path stays.** Results narrow the exception channel; they do not remove it. Every adapter keeps the
  handler for malformed input and for the unexpected. A domain exception that reaches the handler is unexpected
  too: the use case catches the concrete domain exceptions it can raise, so one it does not name is a defect of the
  use case, and the handler answers it generically, never with words of its own per type. An adapter therefore has
  two styles side by side: the switch for cases, the handler for the rest.
- **Case names repeat across results.** `OrderNotFound` in `CancelOrderResult` and in `ShipOrderResult` are two
  types. A switch that meets both is written with the result's name in front (`CancelOrderResult.OrderNotFound`);
  the qualified name is longer and unambiguous.
