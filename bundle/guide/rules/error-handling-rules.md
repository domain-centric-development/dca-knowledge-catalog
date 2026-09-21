---
type: Section
title: ERROR HANDLING RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

Every failure carries its own type, and only the adapter turns it into an answer.

### The three kinds of failure

- **A broken rule of the model** is a `DomainException`, declared in the domain layer beside the type that
  raises it: `InsufficientStockException`, `CartAlreadyCompletedException`, `PasswordTooWeakException`.
- **A request the application cannot serve** is a `UseCaseException`, declared in the application layer beside
  the use case that raises it: `OrderNotFoundException`, `DuplicateSkuException`,
  `PaymentProviderUnavailableException`. Not found, not the caller's, a precondition on a second aggregate,
  a uniqueness rule only the store can see.
- **A malformed call** stays the platform's own argument exception. A null check or a range check in a value
  object states what a caller must never pass. That is a programming-error contract, not a business rule.

Both base types come from the building blocks (`ddd.tactical.DomainException`,
`application.UseCaseException`) and are abstract with a message and a cause. Neither carries a code, a status
or an annotation.

**The cut: would a domain expert have a word for this failure?** `InsufficientStock`, `CartAlreadyCompleted`,
`PasswordTooWeak` — yes, so each is a domain exception with that word in its name. "Must not be null", "must
be positive", "must not exceed 255 characters" — no, so those stay `IllegalArgumentException`.

The two kinds sit next to each other in one method, and telling them apart is the point:

```java
public void decreaseStock(final int amount) {
    if (amount < 0) {
        throw new IllegalArgumentException("Amount cannot be negative");            // malformed call
    }
    if (amount > this.availableQuantity.value()) {                                   // business rule
        throw new InsufficientStockException(this.productId, amount, this.availableQuantity.value());
    }
    ...
}
```

A negative amount is a defect in the caller. A quantity the warehouse does not have is a legitimate request
with a business answer, and the exception carries the figures the rule compared so the caller can say what
happened.

### Where a failure is declared

- A domain exception lives in the domain package, beside the model. No separate `exception/` package.
- A use-case exception lives in the use-case package, or in `application/shared` when several use cases of the
  context raise it.
- **A failure the store detects is declared in the application layer too**, beside the port whose contract it
  is, and raised by whichever adapter implements that port. That is what lets a use case react to a lost race
  without knowing which store it is talking to.

```java
// order/application/shared/OrderRepository.java
public interface OrderRepository extends Repository<Order, OrderId> {

    /** @throws DuplicateOrderNumberException if another order already carries that number */
    @Override
    Order save(Order order);
}
```

### The adapter answers

Neither base type knows a status code, a header or a message shape. The incoming adapter maps type to
protocol answer, in **one place per context**:

```java
@RestControllerAdvice(basePackages = "com.company.project.order.adapter.incoming.api")
public class OrderApiExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    public ProblemDetail handleOrderNotFound(final OrderNotFoundException exception) {
        return problem(HttpStatus.NOT_FOUND, "Order not found", exception.getMessage());
    }

    @ExceptionHandler(InsufficientStockException.class)
    public ProblemDetail handleInsufficientStock(final InsufficientStockException exception) {
        return problem(HttpStatus.CONFLICT, "Not enough stock", exception.getMessage());
    }

    @ExceptionHandler(UseCaseException.class)
    public ProblemDetail handleUseCaseFailure(final UseCaseException exception) {
        return problem(HttpStatus.UNPROCESSABLE_ENTITY, "Request cannot be served", exception.getMessage());
    }

    private static ProblemDetail problem(final HttpStatus status, final String title, final String detail) {
        final ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setTitle(title);
        return problem;
    }
}
```

The answer is an RFC 9457 problem document — `ProblemDetail` in Spring, `ProblemDetails` in ASP.NET Core.
No project needs an error DTO of its own.

**The status follows the failure, not the base type.** A position missing from a cart is a rule of the model
and still answers `404`, because what the caller has to do about it is ask for something that exists. As a
starting point: `404` for something that is not there, `409` for a conflict with existing state, `422` for a
rule that refused an understood request, `400` for a value the model does not accept at all.

Page controllers of the same context catch the two base types and render the message into the form it came
from. One use case, several protocols, one decision site each.

Two things the adapter must not do: expose a stack trace or an internal detail to the outside, and catch
`Exception` or `RuntimeException` around a use case call. A blanket catch answers a defect of this
application the same way as a refusal the customer caused.

### When a result variant is the better channel

Some outcomes are part of what a use case promises its caller, and then the caller should be made to handle
them. A `ChangePasswordResult` with a closed set of outcomes does that: the outcome is a value, the compiler
keeps the caller honest, and nothing is thrown.

The two channels live side by side. The model's refusals travel as exceptions, because a behaviour method on
an aggregate cannot return an outcome without polluting every call site. The use case decides per operation
which channel its own failures take. What the base types change there is the `catch`: the use case names the
rule it converts (`catch (PasswordTooWeakException e)`) instead of a generic type that would also swallow a
defect.

### What the rules check

| Id | Rule |
|---|---|
| `DCA-ERR-001` | Exceptions declared in the domain layer must extend `DomainException` |
| `DCA-ERR-002` | Domain and use-case exceptions reside in the layer whose failure they name |
| `DCA-ERR-003` | Exceptions declared in the application layer must extend `UseCaseException` |
| `DCA-ERR-004` | Domain and use-case exceptions must not carry prohibited framework metadata |
| `DCA-ERR-005` | Domain and use-case exception names must stay in the language of their layer |
| `DCA-ERR-006` | Diagnostic: incoming adapter packages that drive a use case without translating its failures |

`DCA-ERR-004` is why the handler above carries the status and the exception does not: `@ResponseStatus` on a
domain exception is the adapter's decision taken in the domain layer. `DCA-ERR-005` forbids the simple-name
suffixes `Error`, `Fault`, `Failure` and the words `Http`, `Status`, `Response` in the name.

What no rule can decide: a `throw` and a `catch` are not part of the import model. Whether a specific refusal
should have been a domain exception, and whether an adapter catches too widely, stays with review.
`DCA-ERR-006` therefore only lists incoming adapter packages that name neither base type, and never fails.
A package on that list is not a finding by itself — an event consumer whose failed reaction belongs to the
delivery machinery's retry is a good answer — but each entry should have one.

## Related mentions (heuristic)

- [UseCaseException](/marker/application/usecaseexception.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [DomainException](/marker/tactical/domainexception.md)
