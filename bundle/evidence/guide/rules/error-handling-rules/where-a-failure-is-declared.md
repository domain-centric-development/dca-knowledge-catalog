---
type: Reference
title: ERROR HANDLING RULES — Where a failure is declared
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#where-a-failure-is-declared"
---

[Full node and context](/guide/rules/error-handling-rules.md#where-a-failure-is-declared). This is an evidence excerpt; retain the parent selection and caveats.

### Where a failure is declared

- A domain exception lives in the domain package, beside the model. No separate `exception/` package.
- In a context that returns its refusals, an expected refusal is a case nested in the result of the use case that
  returns it, in the use-case package. It has no `*Exception` file of its own.
- A use-case exception lives in the use-case package, or in `application/shared` when several use cases of the
  context raise it.
- **A failure the store detects is an output-port exception**, declared in the application layer beside the port
  whose contract it is, and thrown by whichever adapter implements that port. That is what lets a use case react
  to a lost race without knowing which store it is talking to. The port declares it, so every adapter of the port
  throws it. A foreign system's expected failure is declared the same way, beside the port that reaches the
  system. The use case catches it — inside the transaction too, the boundary rolls back — and turns it into the
  refusal its caller answers: a case of its result, or a use-case exception of its own where the context throws.

```java
// order/application/shared/OrderRepository.java
public interface OrderRepository extends Repository<Order, OrderId> {

    /** @throws DuplicateOrderNumberException if another order already carries that number */
    @Override
    Order save(Order order);
}
```
