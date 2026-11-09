---
type: Decision
title: "Failure channel: exception or a case of the use case's result"
tags: [decision, error-handling, domain, application, use-case, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/error-handling-rules.md, /guide/rules/transaction-rules.md, /guide/testing-levels/the-use-case-once-each-adapter-its-translation.md, /marker/tactical/domainexception.md, /marker/application/usecaseexception.md, /marker/application/portexception.md, /marker/application/inputportexception.md, /marker/application/outputportexception.md, /marker/application/refusal.md, /marker/application/transactionboundary.md, /rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-006.md, /rule/errors/dca-err-008.md, /decision/result-shape-and-assembly.md, /pitfall/business-rule-reported-as-an-argument-error.md, /pitfall/a-refusal-returned-after-a-write.md]
---

Something did not work out, and the layer that noticed has to tell the layer that asked. Two channels carry that message: an **exception** that travels past every frame until someone catches it, or a **case of the result** the use case returns, which the caller takes apart in an exhaustive switch. For an expected refusal both are complete and neither is the default; **the choice is made once per bounded context**, and the project records it. Every other failure is thrown in both.

## The kinds of failure

```text
RuntimeException
├── DomainException              # a rule of the model (domain)
└── PortException                # abstract: a failure a port's contract declares (application)
    ├── InputPortException       # abstract: declared by an input port, caught by its caller
    │   └── UseCaseException     # thrown only by a use case; concrete failures extend this
    └── OutputPortException      # abstract: declared by an output port, thrown by its adapter, caught by the use case
```

Plus, in a context that returns its refusals, the cases of a sealed result, each refusal case marked `Refusal`. A concrete use-case failure extends `UseCaseException`, never `InputPortException` directly. An incoming adapter never catches `PortException` or `InputPortException` generically.

| Kind of failure | Context that throws | Context that returns | Raised by | Example |
|---|---|---|---|---|
| A broken rule of the model | `DomainException`, passed to the handler | `DomainException`, caught by its concrete type in the use case and returned as its case | aggregate, entity, value object, domain service | `{Rule}ViolatedException` / case `{Rule}Violated` |
| An expected refusal the use case finds itself: not found, not the caller's, input it refuses, a precondition on a second aggregate | a `UseCaseException` subtype | a case of the use case's result | the use case | `{Name}NotFoundException` / case `{Name}NotFound` |
| A failure an output port's contract declares (a uniqueness only the store sees) | an `OutputPortException` subtype the adapter throws; the use case catches it and throws its own `UseCaseException` | the same, caught by the use case and returned as its case | the outgoing adapter | `Duplicate{Name}Exception` |
| A foreign system behind an output port — an external system on the context map — refuses, times out or cannot be reached | an `OutputPortException` subtype the port declares and the adapter throws; the use case catches it and throws its own `UseCaseException` | the same, caught by the use case and returned as its case, marked `Refusal` | the outgoing adapter | `{System}UnavailableException` / case `{System}Unavailable` |
| A failure of the system's own infrastructure (its database, its broker), a defect | the platform's exception, to the handler as the unexpected — never an `OutputPortException` | the same | anyone | a lost connection to the own database, a broker timeout |
| No match for a "which one, if any" query | no failure: an empty value in the plain result | the same | the use case | the caller's active session, if any |
| A malformed call | the platform's argument exception | the same | anyone | a null where code must pass a value |
| A stop: cancellation, interruption | passes through untranslated, never a case | the same | the platform | `OperationCanceledException`, `InterruptedException` |

Ask, in order:

1. **Would a caller answer it?** A refusal the caller shows, retries differently or offers an alternative for is expected; the context's choice decides whether it is thrown or returned. A failure nobody between the raise and the adapter's handler can do anything about is not; it is thrown in both.
2. **Own infrastructure or a foreign system?** The system's own database and broker have to be there; their failure is unexpected and thrown in both styles. A foreign system — one the context map declares as an external system — refusing, timing out or being unreachable is expected behaviour of the integration: the output port declares it, and a caller answers it. Which system is foreign is read from the context map, not judged per failure. A foreign failure the port does not declare stays unexpected.
3. **Who found it — the model, an output port's adapter, or the use case?** The model throws, always: a value object's constructor can only throw, and an aggregate's behaviour method that returned an outcome would make every caller unpack a case a correct call never produces. An output port's adapter throws the `OutputPortException` its port declares. A refusal the use case finds itself is the application's; **a use case never constructs a domain exception**. Where the context returns, the use case catches the concrete domain and output-port exceptions it can raise — never a base type, which would also catch a defect — and returns their cases. A domain exception it does not name is unexpected: the handler answers it generically.
4. **Is absence a normal answer?** A query that asks whether there is one ("which one, if any") answers *none* with an empty value, never a refusal. "Not found" is a refusal only where the caller names a specific thing — by its id.
5. **Is it a caller contract rather than a failure?** An argument guard on a value only code passes stays the platform's argument exception. On a value built from input the same check is the rule the product names, and its refusal is expected.

## Who owns "not found"

Whoever searches owns the failure. The repository is an output port of the application, and its lookup by id answers
an empty optional; only the use case sees that answer, so only the use case can say "this id does not exist". The
domain never takes part in the lookup — a domain service is handed its aggregates — so a missing aggregate is never a
domain failure: it is the use case's refusal, a `UseCaseException` subtype or a `Refusal` case of its result. Classic
DDD places the repository in the domain, which is why it may answer differently; here, where the repository lives
decides where "not found" lives.

The boundary: a part *inside* an aggregate, named by its local id, is searched by the aggregate in its own state.
"Only what the aggregate holds can be removed" is a rule of the model, so its absence is a `DomainException`
the use case catches by its concrete type and answers in the context's style. A name cannot tell the two apart —
`{Part}NotFound` is right in the domain, `{Aggregate}NotFound` in the application.

## Per bounded context, not per use case

**Every use case of a context carries its refusals the same way. No context mixes a returned refusal with a thrown one.** The context's adapters then have one style at the call site, a review checks one shape, and a rule could check it. Deciding per use case gives every adapter two styles for the same kind of failure and leaves the next reader guessing which one a new use case takes. Two contexts of one project may choose differently.

| | Thrown | Returned |
|---|---|---|
| The input port's signature | names the success only | names every way the operation can end |
| A new refusal | compiles everywhere; a test or a review holds that the handler answers it | a compile error at every call site that must answer it |
| The use case | throws its own refusals, lets the model's pass | returns its own, catches the model's and the output ports' once |
| The adapter | one exception handler per context, one entry per refusal | a switch at each call site without `default`, the answers in one class per context; the handler stays for the rest |
| The seam between port test and adapter test | the failure type the stub throws | the result type; the compiler holds it |
| The cost | a refusal nobody maps reaches the caller as a server error | every caller reads the result; an ignored result swallows a refusal |

## The transaction

- **Decide, then write.** A use case writes only once it can no longer refuse: every refusal, thrown or returned, comes before the first `save`. A refusal that can only come after a write is a wrong cut — two aggregates changed in one transaction.
- **A returned refusal rolls back like a thrown exception.** Every refusal case implements the marker `Refusal` (`IRefusal` in .NET, a trait in Rust). The transaction boundary rolls back when the work returns one, and the interceptor around a declarative `@Transactional` use case marks the transaction rollback-only on it. A refusal rolls back wherever it arises. The net catches a violation of "decide, then write"; it does not make it good code.
- **An output-port exception may be caught inside the transaction.** The use case returns or throws its refusal; the boundary rolls back either way.
- **A step after the commit only reads.** A rollback no longer reaches it.
- **A remote effect keeps its compensation.** A remote effect made before the local write was never undone by a thrown exception either; a refusal after it, thrown or returned, calls the compensation.

## The shape of a returned result

- The input port returns `{Operation}Result`. With an expected refusal it is sealed: a success case named for what happened (`Created`, `Cancelled`, `Found`) and one case per refusal named after the refusal, nested in the result, carrying ids and figures, implementing `Refusal` — no `Exception` suffix, no file of its own. Not every outcome is a refusal: an operation that ends in several successes (`Sent`, `AlreadySent`) may seal its result for those alone, with no case marked. An operation with one outcome keeps a plain result record.
- **Java:** `sealed interface` + nested `record` cases; the adapter's `switch` has **no `default`**, so a new case is a compile error at every call site.
- **C#:** a closed union. Until C# `union` types are released, a library such as OneOf (`OneOfBase<…>`, `Match` with one function per case). `Match` is exhaustive by arity, not by name — functions are positional, two of the same shape can be swapped. A closed class hierarchy without either gives no exhaustiveness.
- **Rust:** an `enum` and a `match` without a `_` arm; `#[must_use]` on the enum warns about an ignored result.

## Consequences where a context returns

- **A new refusal breaks the build where it must be answered.** The port's signature says how the operation can end.
- **The answer to each case is written once per context**, in an adapter class every switch calls; the switch itself is per call site.
- **The thrown path stays.** Every adapter keeps one exception handler for malformed input and the unexpected — a domain exception the use case does not name included. Results narrow the exception channel; they do not remove it.
- **An ignored result swallows a refusal.** Java and C# have no must-use check; a caller, and first of all a test helper that arranges state, that drops the result treats every refusal as success. Test helpers assert the success case.
- **A caller with nobody to answer throws on purpose.** An event consumer, or an open host service whose contract has no such case, turns the case back into an exception so the delivery's retry or the calling context sees it. A foreign system that did not answer is the typical case: thrown back, the delivery is tried again later.
- **Case names repeat across results** (`{Name}NotFound` in several); a switch that meets two qualifies them by their result type.
- **Governance moves to the compiler.** The error-handling rules select exception types; a case is none. The diagnostic that lists adapters translating no failure type lists an adapter that answers only by switching; its answer is the switch.

## Anchors

- Guide: [Error handling rules](/guide/rules/error-handling-rules.md) · [Transaction rules](/guide/rules/transaction-rules.md) · [The use case once, each adapter its translation](/guide/testing-levels/the-use-case-once-each-adapter-its-translation.md)
- Markers: [DomainException](/marker/tactical/domainexception.md) · [PortException](/marker/application/portexception.md) · [InputPortException](/marker/application/inputportexception.md) · [OutputPortException](/marker/application/outputportexception.md) · [UseCaseException](/marker/application/usecaseexception.md) · [Refusal](/marker/application/refusal.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Rules: [Exceptions declared in the domain layer must extend DomainException](/rule/errors/dca-err-001.md) · [Domain and port exceptions reside in the layer whose failure they name](/rule/errors/dca-err-002.md) · [Exceptions declared in the application layer must extend UseCaseException or OutputPortException](/rule/errors/dca-err-003.md) · [Diagnostic: incoming adapter packages that drive a use case without translating its failures](/rule/errors/dca-err-006.md) · [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md)
- Recipe: [Return expected refusals as a sealed result](/recipe/return-expected-refusals-as-a-sealed-result.md)
- Template: [Domain exception skeleton](/template/domain-exception.md) · [Use case skeleton](/template/use-case.md)
- Pitfall: [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md) · [A refusal returned after a write](/pitfall/a-refusal-returned-after-a-write.md)
- Related decision: [Result shape and assembly](/decision/result-shape-and-assembly.md) · [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
