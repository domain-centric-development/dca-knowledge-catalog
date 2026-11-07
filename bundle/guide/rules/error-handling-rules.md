---
type: Section
title: ERROR HANDLING RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

Every failure carries its own type, and only the adapter turns it into an answer. An expected refusal a caller
answers is thrown or returned as a case of the use case's result — one way per bounded context; every other failure
is an exception.

### The kinds of failure

- **A broken rule of the model** is a `DomainException`, declared in the domain layer beside the type that
  raises it: `InsufficientStockException`, `CartAlreadyCompletedException`, `PasswordTooWeakException`. The
  model throws it.
- **A failure a port's contract declares** is a `PortException`, declared in the application layer. The base is
  abstract and has one abstract branch per side of the application:
  - **`InputPortException`** — declared by an input port, caught by its caller. Its concrete failures extend
    `UseCaseException`, which only a use case throws: an expected refusal where the context throws its refusals
    (`OrderNotFoundException`, `PaymentProviderUnavailableException`). A concrete use-case failure extends
    `UseCaseException`, never `InputPortException` directly.
  - **`OutputPortException`** — declared by an output port's contract, thrown by the adapter that implements the
    port, caught by the use case: an expected conflict only the store sees, a uniqueness
    (`DuplicateOrderNumberException`), or the expected failure of a foreign system behind the port, which refused
    or did not answer (`PaymentGatewayUnavailableException`). A failure of the system's own infrastructure — its
    database lost the connection, its broker timed out — is not one; it stays the platform's exception and travels
    as the unexpected. See [Own infrastructure, a foreign system](#own-infrastructure-a-foreign-system).
- **An expected refusal of a use case** is one its caller answers: not found, not the caller's, input the use case
  refuses, a business rule of the model, a foreign system that refused or did not answer. A context that throws its
  refusals declares it as a use-case exception
  (`OrderNotFoundException`); a context that returns them makes it a case of the use case's result, marked
  `Refusal` (`OrderNotFound`). See [An expected refusal, thrown or returned](#an-expected-refusal-thrown-or-returned).
- **A malformed call** stays the platform's own argument exception. A null check or a range check on a value
  one piece of code hands another states what a caller must never pass. That is a programming-error contract,
  not a business rule.

```text
RuntimeException
├── DomainException              # a rule of the model (domain)
└── PortException                # abstract: a failure a port's contract declares (application)
    ├── InputPortException       # abstract: declared by an input port, caught by its caller
    │   └── UseCaseException     # thrown only by a use case; concrete failures extend this
    └── OutputPortException      # abstract: declared by an output port, thrown by its adapter, caught by the use case
```

An incoming adapter never catches `PortException` or `InputPortException` generically. Either would catch a
failure the use case should have turned into a refusal — an `OutputPortException` that escaped it — together with
the use case's own, and answer both alike.

**The origin decides.** The same check means two things depending on where the value comes from. A value that
only code passes — an amount computed inside the model, a reference the use case holds — fails by a defect in
the caller, and an argument exception says so. A value built from input — a title typed into a form, a quantity
in a request — fails by an ordinary request, and its bounds are the rule the product names (a title of 1 to 200
characters). Such a value object refuses everything the rule refuses with the rule's named failure, a missing
value included: an absent title is refused like an empty one, not with an NPE and not with a `requireNonNull`.

The base types come from the building blocks (`ddd.tactical.DomainException`; `application.PortException`,
`InputPortException`, `UseCaseException`, `OutputPortException`) and are abstract with a message and a cause. None
carries a code, a status or an annotation. The marker `Refusal` comes from there too.

**The cut: would a domain expert have a word for this failure?** `InsufficientStock`, `CartAlreadyCompleted`,
`PasswordTooWeak` — yes, so each is a domain exception with that word in its name. "Must not be null", "must
be positive", "must not exceed 255 characters" on a value only code passes — no, so those stay
`IllegalArgumentException`. On a value built from input the expert has the word: the title is invalid.

**The name is the broken rule, in the domain's words; the suffix is the project's.** `InsufficientStock`
says what the domain refuses; `InvalidInput` or `ValidationError` says only that something failed. The
suffix follows the platform by default — `Exception`, as both Java and .NET expect — and a project may
drop it where its language reads better without (`InsufficientStock`). The project records the
choice, and every failure of the project follows it: a run that has to pick the suffix picks differently
each time. A case of a result carries no suffix at all: it is a value, not an exception (`OrderNotFound`).

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
happened. The caller says it — **the exception's message is never what a person reads.** It is for the log; the
words on a page or in an answer are the incoming adapter's, made from the failure's type and its values. A
message passed through ties the user's language to the domain's and closes the door on a translation.

**A failure carries ids and figures, never what a page shows.** Thrown or returned, its fields are the typed
identities and the values the rule compared. Not the caller's raw input: input that does not even parse into the id is a malformed call,
not this failure. Not display data either: a name or a description of the thing the id refers to is resolved by
the translation site, through the queries it already has. A failure that carries the name decides for every
surface what it shows.

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

### Own infrastructure, a foreign system

**Own infrastructure throws; a foreign system's expected failure is a refusal.** The system's own infrastructure —
its database, its broker — has to be there. When it fails, nothing in the request is wrong and no caller can answer
it: the failure stays the platform's exception, the transaction rolls back, and the delivery machinery or the
operator takes over. A foreign system behind an output port — a payment provider, a mail provider — is different.
That it refuses, times out or cannot be reached is expected behaviour of the integration, and the caller has an
answer for it: choose another provider, try again later, carry on without the mail.

- The output port declares that failure in its contract, as an `OutputPortException` subtype named in the port's
  language (`PaymentGatewayUnavailableException`).
- The adapter catches the client's own failure — the timeout, the refused connection, the error status — and throws
  the declared one. It decides nothing else.
- The use case catches the declared failure and turns it into its own refusal: a case of its result, marked
  `Refusal` (`PaymentProviderUnavailable`), where the context returns; its own use-case exception
  (`PaymentProviderUnavailableException`) where the context throws. Either way the transaction rolls back.

**Which systems are foreign is read from the context map, not decided per failure.** A system the context declares
as an external system it talks to (`@ExternalUpstream`) is foreign; every other piece of infrastructure is the
system's own. A failure of a foreign system that the port does not declare stays unexpected — the declaration is the
list of what the caller is meant to answer.

A caller with nobody to answer — an event consumer — throws the case back as an exception, so the delivery is
retried later; see [What a result does not do for you](#what-a-result-does-not-do-for-you).

### An expected refusal, thrown or returned

An expected refusal is one a caller answers: the addressed thing does not exist, it is not the caller's, the use
case refuses the input, a business rule of the model refused the change, a foreign system refused or did not
answer. Everything else — a defect, the system's own database or broker that does not answer, a malformed call, a
stop — nobody can handle where it happens, and it travels as an exception to the place that can.

DCA carries an expected refusal one of two ways. Both are complete, and neither is the default:

- **Thrown.** The refusal is an exception: the model's domain exception, passed through, or a use-case exception
  the use case raises. The input port's signature names the success only. The context's exception handler maps
  each type to its answer. A new refusal compiles at every call site; a test or a review holds that the handler
  answers it.
- **Returned.** The refusal is a case of the use case's sealed result. The signature says how the operation can
  end, a switch over the result names every case, and a new refusal is a compile error at every call site that
  must answer it. Every caller reads the result, also one with nobody to answer, and the use case catches each
  refusal of the model it can raise.

**The choice is made per bounded context, and the project records it.** Every use case of a context carries its
refusals the same way. No context mixes a returned refusal with a thrown one, so its call sites have one style and a
review checks one shape. Two contexts of one project may choose differently.

The record is a line in the project's technical description, where everyone who builds, plans or reviews reads it:
`Refusals: thrown` or `Refusals: returned` for the whole project, and `Refusals (<context>): returned` for a context
that departs from it. A context without its own line follows the project's. Unrecorded, each piece of work picks a
style again, and a context drifts into both.

```
Refusals: thrown
Refusals (ordering): returned
```

**The model throws in both.** An aggregate refuses inside a behaviour method, and a method that returned an outcome
instead would make every caller unpack a case a correct call never produces. A value object's constructor can only
throw. So the model's refusals stay `DomainException`s. A context that throws lets them pass to its handler. A
context that returns catches the concrete ones the use case can raise, once, and returns the case:
`catch (OrderAlreadyShippedException e)`, never a base type that would also catch a defect.

**A use case never constructs a domain exception.** A refusal the use case finds itself — a port returned nothing,
the caller does not own what it names — is the application's, not the model's: a use-case exception where the
context throws, a case of the result where it returns, never a `DomainException` thrown from the application layer.

### Absence is not always a refusal

**"Which one, if any" answers *none* with an empty value.** A query that asks whether there is one — the caller's
active session, an open order, the current draft — has "none" among its normal answers. It returns an empty value
(`Optional.empty()`, `null` in C#, `None` in Rust) inside its plain result, not a refusal case and not an exception.
The caller shows the empty state or goes on without it.

**"Not found" is a refusal only where the caller demands a specific thing.** A query or a command that names one
thing by its id — `GetOrderById`, `CancelOrder` — refuses when that thing does not exist: `OrderNotFound` where the
context returns, `OrderNotFoundException` where it throws. The test is the caller's question: "give me this one" can
fail, "is there one?" cannot.

### The shape of a result

This section and the next two show the returned form; the throwing form is the one the sections above describe,
and the differences are named where they arise.

The input port returns `<Operation>Result`. When the operation can end in more than one way, the result is sealed:
one case per outcome. A success case is named for what happened (`Cancelled`, `Placed`, `Found`), a refusal case
after the refusal (`OrderNotFound`, `OrderAlreadyShipped`). The cases are nested in the result and carry ids and
figures. Not every outcome is a refusal: a reminder that was `Sent` or `AlreadySent`, a merge that `Merged` or found
`NothingToMerge`, ends in two successes, and that alone is reason enough for a sealed result. An operation with one
outcome keeps a plain result record.

```java
// order/application/cancelorder/CancelOrderResult.java
public sealed interface CancelOrderResult
        permits CancelOrderResult.Cancelled, CancelOrderResult.OrderNotFound,
                CancelOrderResult.OrderAlreadyShipped {

    record Cancelled(OrderId orderId) implements CancelOrderResult {}

    record OrderNotFound(OrderId orderId) implements CancelOrderResult, Refusal {}

    record OrderAlreadyShipped(OrderId orderId, Instant shippedAt) implements CancelOrderResult, Refusal {}
}
```

The use case returns the case it finds and turns the model's refusal into its case:

```java
// order/application/cancelorder/CancelOrderUseCase.java
@Service
@Transactional
public class CancelOrderUseCase implements CancelOrderInputPort {

    private final OrderRepository orders;
    private final DomainEventPublisher eventPublisher;

    @Override
    public CancelOrderResult execute(CancelOrderCommand command) {
        Optional<Order> found = orders.findByIdForCustomer(command.orderId(), command.customerId());
        if (found.isEmpty()) {
            return new OrderNotFound(command.orderId());                  // the application's finding
        }
        Order order = found.get();
        try {
            order.cancel();
        } catch (OrderAlreadyShippedException shipped) {                  // the model's refusal, caught once
            return new OrderAlreadyShipped(shipped.orderId(), shipped.shippedAt());
        }
        orders.save(order);
        eventPublisher.publishAndClearEvents(order);
        return new Cancelled(order.id());
    }
}
```

Thrown, the same use case returns a plain `CancelOrderResult` record, raises `OrderNotFoundException` — a use-case
exception — where this one returns `OrderNotFound`, and lets `OrderAlreadyShippedException` pass without a `catch`.
The order of the steps is the same: every refusal comes before `save`.

The adapter switches over the result, **without a `default`**. A `default` would let a new case compile and fall
into whatever the branch does; without it the compiler refuses a switch that misses a case:

```java
@PostMapping("/{orderId}/cancellation")
public ResponseEntity<?> cancel(@PathVariable UUID orderId) {
    CancelOrderCommand command = new CancelOrderCommand(new OrderId(orderId), currentCustomer());
    return switch (cancelOrder.execute(command)) {
        case Cancelled cancelled -> ResponseEntity.ok(CancellationDto.from(cancelled));
        case OrderNotFound refusal -> OrderProblems.orderNotFound(refusal.orderId());
        case OrderAlreadyShipped refusal -> OrderProblems.alreadyShipped(refusal.orderId(), refusal.shippedAt());
    };
}
```

The same in the other languages:

- **C#** needs a closed union. Until C# `union` types are released (C# 15), a library gives one: OneOf's
  `[GenerateOneOf] public sealed partial class CancelOrderResult : OneOfBase<Cancelled, OrderNotFound,
  OrderAlreadyShipped>`, the cases nested `sealed record`s, each refusal case implementing `IRefusal`, a use case that simply `return`s a case (an implicit
  conversion), and an adapter that calls `result.Match(cancelled => …, notFound => …, shipped => …)`. `Match` is
  exhaustive by arity, not by name: its functions are positional, two of the same shape can be swapped and still
  compile, and the error for a missing one names a parameter, not the case. A C# `union` closes that gap: a
  `switch` over it warns about a case it does not handle. A closed class hierarchy without either gives no
  exhaustiveness at all.
- **Rust** spells the result as an `enum` with one variant per case and the adapter as a `match` without a `_`
  arm; the `Refusal` trait says which variants refuse. `#[must_use]` on the enum turns an ignored result into a warning.

### The adapter answers

No base type and no case knows a status code, a header or a message shape. The incoming adapter maps the
outcome to the protocol's answer and writes the words itself — from the failure's values, never from an exception's
message. **The answer to each case is written once per context**: the switches at the call sites name the case,
and a class of the adapter writes the answer they all return (`OrderProblems` above). What is still thrown goes to
**one exception handler per context**:

```java
@RestControllerAdvice(basePackages = "com.company.project.order.adapter.incoming.api")
public class OrderApiExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail handleMalformedCall(final IllegalArgumentException exception) {
        return problem(HttpStatus.BAD_REQUEST, "Request not understood", null);
    }

    @ExceptionHandler(UseCaseException.class)
    public ProblemDetail handleUseCaseFailure(final UseCaseException exception) {
        return problem(HttpStatus.SERVICE_UNAVAILABLE, "Request cannot be served now", null);
    }

    private static ProblemDetail problem(final HttpStatus status, final String title, final String detail) {
        final ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setTitle(title);
        return problem;
    }
}
```

A context that throws its refusals maps them here too, one `@ExceptionHandler` per type, with the words and the
status a switch arm would have written:

```java
    @ExceptionHandler(OrderNotFoundException.class)
    public ProblemDetail handleOrderNotFound(final OrderNotFoundException exception) {
        return problem(HttpStatus.NOT_FOUND, "Order not found",
                "There is no order " + exception.orderId().value() + ".");
    }

    @ExceptionHandler(OrderAlreadyShippedException.class)
    public ProblemDetail handleAlreadyShipped(final OrderAlreadyShippedException exception) {
        return problem(HttpStatus.CONFLICT, "Order already shipped",
                "Order " + exception.orderId().value() + " left the warehouse on " + exception.shippedAt() + ".");
    }
```

Either way, the answer to each refusal is written once per context: in the handler where the context throws, in
the class the switches call where it returns.

The answer is an RFC 9457 problem document — `ProblemDetail` in Spring, `ProblemDetails` in ASP.NET Core.
No project needs an error DTO of its own.

**The status follows the failure, not the base type.** A position missing from a cart is a rule of the model
and still answers `404`, because what the caller has to do about it is ask for something that exists. As a
starting point: `404` for something that is not there, `409` for a conflict with existing state, `422` for a
rule that refused an understood request, `400` for a value the model does not accept at all, `503` for a foreign
system that did not answer.

**`404` belongs to the addressed resource.** It answers a path that names nothing. A reference in the request
body that parses but names nothing — an id posted to a resource that exists — answers `422`: the request was
understood, and what it refers to does not exist. A `404` there would claim something false about the resource
the path addresses, and the caller would look for the error in the wrong place. A reference that does not parse
at all is a malformed call and answers `400`, before any use case runs.

Page controllers of the same context switch over the same results — or, where the context throws, catch the same
types — and render the page's own words into the form it came from: a text the page keeps per refusal, or a message
key its translations resolve, filled with the refusal's values. One use case, several protocols, one answer per case on each, and every sentence in the language of the
surface that shows it.

Two things the adapter must not do: expose a stack trace or an internal detail to the outside, and catch
`Exception` or `RuntimeException` around a use case call. A blanket catch answers a defect of this
application the same way as a refusal the customer caused.

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

### A refusal and the transaction

**Decide, then write.** A use case writes only once it can no longer refuse: it loads, asks the model, refuses or
goes on, and saves last. A refusal that can only come after a write is a cut that changes two aggregates in one
transaction — the second refuses what the first already did. That is a design question, not a rollback question.

**A returned refusal rolls back like a thrown exception.** A thrown refusal rolls the transaction back because it
leaves the boundary as an exception. A returned one leaves it as a value, and without a net it would commit
whatever the use case wrote before it. So every refusal case of a result implements the marker `Refusal` from the
building blocks, and the transaction boundary rolls back when the work returns one: `TransactionBoundary`
(`ITransactionBoundary` in .NET) does, and so does the interceptor that marks a declarative `@Transactional` use case
rollback-only on a returned `Refusal`. A refusal rolls back wherever in the use case it arises, thrown or returned.
The refusal cases of `CancelOrderResult` above carry the marker for that reason. The net catches a violation of
"decide, then write"; it does not make the violation good code.

**A step after the commit only reads.** What runs once the transaction has committed — a step after
`inTransaction` returns, a listener after the commit — is out of the rollback's reach. It reads and reports; a
change it would refuse is already stored.

**A remote effect keeps its compensation.** A remote effect made before the local write — a payment, a reservation
at another system — was never undone by a thrown exception either; a rollback reaches only the local store. A
refusal after such an effect, thrown or returned, calls the compensation the
[transaction rules](#transaction-boundary-placement) describe.

### A stop is not a failure

A run cancelled from outside — a shutdown signal, an interrupt, a deadline — is neither a broken rule, nor a
refusal, nor a request the application cannot serve. It is a case of its own: **a stop passes through untranslated.**

- Any port may raise it, when the work it waits for is cancelled.
- No adapter translates it into a domain or use-case exception, no use case catches it, and no use case returns it
  as a case of its result.
- The entry point that owns the process or the request turns it into the end: an exit code, an aborted response,
  a message left for redelivery.

Both platforms model it so, and cooperatively — the work is asked to stop, never killed:

- **.NET** hands a `CancellationToken` through every port call; a cancelled operation raises
  `OperationCanceledException`.
- **Java** signals a stop by interruption; a blocking call raises `InterruptedException`. Code that is not the
  thread's owner never swallows it: it rethrows, or restores the flag with `Thread.currentThread().interrupt()`.

A `catch` that turns a stop into a failure is the defect to look for in review: the request then answers with an
error for something nobody did wrong, and a retry repeats work the owner wanted to end. A use case that must leave
its state clean on a stop keeps its steps inside one transaction, which the stop rolls back.

### What the rules check

| Id | Rule |
|---|---|
| `DCA-ERR-001` | Exceptions declared in the domain layer must extend `DomainException` |
| `DCA-ERR-002` | Domain and port exceptions reside in the layer whose failure they name |
| `DCA-ERR-003` | Exceptions declared in the application layer must extend `UseCaseException` or `OutputPortException` |
| `DCA-ERR-004` | Domain and port exceptions must not carry prohibited framework metadata |
| `DCA-ERR-005` | Domain and port exception names must stay in the language of their layer |
| `DCA-ERR-006` | Diagnostic: incoming adapter packages that drive a use case without translating its failures |
| `DCA-ERR-007` | Diagnostic: failures that carry display data or objects instead of ids and figures |
| `DCA-ERR-008` | Diagnostic: closed use-case results without a case marked as a refusal (experimental) |

`DCA-ERR-004` is why the handler above carries the status and the exception does not: `@ResponseStatus` on a
domain exception is the adapter's decision taken in the domain layer. `DCA-ERR-005` forbids the simple-name
suffixes `Error`, `Fault`, `Failure` and the words `Http`, `Status`, `Response` in the name.

What no rule can decide: a `throw` and a `catch` are not part of the import model. Whether a specific refusal
should have been a domain exception, and whether an adapter catches too widely, stays with review.
`DCA-ERR-006` therefore only lists incoming adapter packages that name neither base type, and never fails.
A package on that list is not a finding by itself — an event consumer whose failed reaction belongs to the
delivery machinery's retry is a good answer — but each entry should have one.

In a context that returns results, the compiler holds what `DCA-ERR-006` can only list: a switch that misses a
case does not compile. The diagnostic reads the exception channel only, so an adapter that answers every refusal
by a switch and names neither base type appears on its list. The entry's answer is then the switch.

A closed result describes the outcomes of an operation; some are refusals, some are not. `Sent | AlreadySent` holds
no refusal and needs none: marking `AlreadySent` would roll back a success. Whether a case refuses is domain
knowledge the type does not show, so `DCA-ERR-008` lists every closed result without a case marked `Refusal` and
never fails. Each entry asks one question: is none of these outcomes a refusal? If one is, it carries the marker,
or the transaction commits where a thrown refusal rolled back. The marker says "refused" with or without a
transaction — a read-only use case refuses too; the rollback acts only where something was written.

## Related mentions (heuristic)

- [InputPortException](/marker/application/inputportexception.md)
- [OutputPortException](/marker/application/outputportexception.md)
- [PortException](/marker/application/portexception.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)
- [UseCaseException](/marker/application/usecaseexception.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [DomainException](/marker/tactical/domainexception.md)

## Evidence slices

- [Overview](/evidence/guide/rules/error-handling-rules/overview.md)
- [The kinds of failure](/evidence/guide/rules/error-handling-rules/the-kinds-of-failure.md)
- [Where a failure is declared](/evidence/guide/rules/error-handling-rules/where-a-failure-is-declared.md)
- [Own infrastructure, a foreign system](/evidence/guide/rules/error-handling-rules/own-infrastructure-a-foreign-system.md)
- [An expected refusal, thrown or returned](/evidence/guide/rules/error-handling-rules/an-expected-refusal-thrown-or-returned.md)
- [Absence is not always a refusal](/evidence/guide/rules/error-handling-rules/absence-is-not-always-a-refusal.md)
- [The shape of a result](/evidence/guide/rules/error-handling-rules/the-shape-of-a-result.md)
- [The adapter answers](/evidence/guide/rules/error-handling-rules/the-adapter-answers.md)
- [What a result does not do for you](/evidence/guide/rules/error-handling-rules/what-a-result-does-not-do-for-you.md)
- [A refusal and the transaction](/evidence/guide/rules/error-handling-rules/a-refusal-and-the-transaction.md)
- [A stop is not a failure](/evidence/guide/rules/error-handling-rules/a-stop-is-not-a-failure.md)
- [What the rules check](/evidence/guide/rules/error-handling-rules/what-the-rules-check.md)
