---
type: Reference
title: ERROR HANDLING RULES — The kinds of failure
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#the-kinds-of-failure"
---

[Full node and context](/guide/rules/error-handling-rules.md#the-kinds-of-failure). This is an evidence excerpt; retain the parent selection and caveats.

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
