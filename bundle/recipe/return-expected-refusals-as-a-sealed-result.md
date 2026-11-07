---
type: Recipe
title: Return expected refusals as a sealed result
tags: [recipe, application, use-case, error-handling, adapter]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/error-handling-rules.md, /guide/rules/transaction-rules.md, /pitfall/a-refusal-returned-after-a-write.md, /guide/testing-levels/the-use-case-once-each-adapter-its-translation.md, /decision/failure-channel-exception-or-result.md, /marker/port-in/usecase.md, /marker/tactical/domainexception.md, /marker/application/refusal.md, /marker/application/outputportexception.md, /marker/application/transactionboundary.md, /rule/usecase/dca-use-006.md, /rule/usecase/dca-use-007.md, /rule/usecase/dca-use-015.md, /rule/errors/dca-err-006.md, /rule/errors/dca-err-008.md]
---

A use case can be refused in ways its caller answers: the addressed thing is not there, it is not the caller's, the input is refused, a rule of the model refuses the change, a foreign system behind an output port refused or did not answer. In a bounded context that returns its refusals, each of those is a **case of the use case's result**, and the incoming adapter answers it in an exhaustive switch. Every other failure stays an exception. Throwing the refusals is the equal alternative — the [domain exception skeleton](/template/domain-exception.md) and the throwing variants of the templates show it; a context picks one and keeps it. What each costs: [Failure channel: exception or a case of the use case's result](/decision/failure-channel-exception-or-result.md).

## Steps

1. **Check the context's choice.** Every use case of a context returns its expected refusals as cases, or every one throws them. The project records the choice per context. In a context that throws, follow the [domain exception skeleton](/template/domain-exception.md) instead; moving a context over is one change for all its use cases, never one use case at a time.
2. **List the refusals.** For the operation, name every outcome a caller answers: those the use case finds itself (a port returned nothing, the caller does not own it, a precondition on a second aggregate) the concrete `DomainException`s the model can raise during the call, and the concrete `OutputPortException`s the ports it calls declare — a foreign system's expected failure among them. A failure of the system's own database or broker is not on the list: it stays an exception. A "which one, if any" query is not refused when there is none: it answers with an empty value in a plain result; "not found" is a refusal only where the caller names a specific thing by its id. An operation with none and a single outcome keeps a plain `{Name}Result` record — stop here. One that ends in several successes and no refusal (`Sent`, `AlreadySent`) may seal its result all the same; none of its cases carries `Refusal`, since a marked success would be rolled back.
3. **Write the sealed result** in the use-case package. One success case named for what happened (`Created`, `Cancelled`, `Found`), one case per refusal named after the refusal (`{Name}NotFound`, `{Rule}Violated`) and implementing the marker `Refusal`, each nested in the result, immutable, carrying typed ids and the figures the rule compared — never a message, a status or display text, never an aggregate or an entity.

   ```java
   // {basePackage}.{context}.application.{operation}
   public sealed interface {Operation}Result
           permits {Operation}Result.{Done}, {Operation}Result.{Name}NotFound, {Operation}Result.{Rule}Violated {

       record {Done}({Name}Id id) implements {Operation}Result {}

       record {Name}NotFound({Name}Id id) implements {Operation}Result, Refusal {}

       record {Rule}Violated({Name}Id id, int limit, int requested) implements {Operation}Result, Refusal {}
   }
   ```

   C#: a closed union — until C# `union` types are released, OneOf: `[GenerateOneOf] public sealed partial class {Operation}Result : OneOfBase<{Operation}Result.{Done}, …>` with nested `sealed record` cases, each refusal case `: IRefusal`. Rust: an `enum` with `#[must_use]`, its refusing variants named by the `Refusal` trait.
4. **Let the input port return it.** `{Operation}InputPort extends UseCase<{Operation}Command, {Operation}Result>` — the signature now says how the operation can end.
5. **Return the cases from the use case — decide, then write.** A refusal the use case finds is returned directly. A domain exception is caught once, by its concrete type, and turned into its case. Every refusal comes before the first write. The use case never constructs a domain exception and never catches a base type:

   ```java
   Optional<{Name}> found = repository.findById(id);
   if (found.isEmpty()) {
       return new {Name}NotFound(id);
   }
   {Name} aggregate = found.get();
   try {
       aggregate.{behaviour}(command.amount());
   } catch ({Rule}ViolatedException violated) {
       return new {Rule}Violated(violated.id(), violated.limit(), violated.requested());
   }
   repository.save(aggregate);
   eventPublisher.publishAndClearEvents(aggregate);
   return new {Done}(aggregate.id());
   ```

   A failure an output port declares as its contract is an `OutputPortException` the adapter throws; the use case catches the concrete type and returns its case — inside the transaction too. Two kinds: a uniqueness only the store sees, and the expected failure of a foreign system — an external system on the context map — that refused, timed out or could not be reached. The adapter catches the client's own failure and throws the declared one:

   ```java
   // in the use case — the port declares {System}UnavailableException extends OutputPortException
   try {
       confirmation = {system}Port.{request}(...);
   } catch ({System}UnavailableException unavailable) {
       return new {System}Unavailable(unavailable.{reference}());
   }
   ```

   **The net.** The transaction boundary rolls back when the work returns a `Refusal` — `TransactionBoundary.inTransaction`, and the interceptor around a declarative `@Transactional` use case — so a returned refusal undoes what was written before it, as a thrown exception would. It catches a violation of "decide, then write" ([A refusal returned after a write](/pitfall/a-refusal-returned-after-a-write.md)); it is no reason to write first. A step after the commit only reads; a remote effect made before the local write keeps its compensation.
6. **Switch in every incoming adapter, without a `default`.** Each call site switches over the result and names every case; a `default` would let a new case compile into whatever it does. The answer to each case — status, problem document, page notice — is written once per context in an adapter class the switches call, so a case answers the same everywhere. C# with OneOf: `result.Match(done => …, notFound => …, violated => …)`; the functions are positional, so check their order against the type parameters.
7. **Keep the exception handler for the rest.** One handler per context stays for malformed input and the unexpected; a domain exception no use case names is unexpected and answered generically. Never a handler for `PortException` or `InputPortException`. Remove the handlers and `*Exception` classes of the refusals that are now cases.
8. **Answer where nobody can.** A caller with no one to show a refusal to — an event consumer, an open host service whose own contract has no such case — turns the case back into an exception (`IllegalStateException` with the case's values) so the delivery's retry or the calling context sees it — a foreign system that did not answer is then tried again with the next delivery. Never drop the case.
9. **Test the seam.** The port test asserts the returned case and its values. The adapter test's stubbed input port returns the case, never throws it. Every test helper that runs the use case to arrange state asserts the success case — an ignored result swallows a refusal, and neither Java nor C# warns about it.
10. **Verify** — compile (a missed case is a compile error in Java, a missing function in `Match`, a warning with a C# `union`), then the project's architecture suite.

## Rules to satisfy (build-time checklist)

- [Result models must end with `Result` and reside in the application package](/rule/usecase/dca-use-006.md) — the sealed result and its nested cases
- [Commands/Queries/Results should be immutable (records)](/rule/usecase/dca-use-007.md) — every case a record
- [Results must not expose aggregate roots or entities](/rule/usecase/dca-use-015.md) — a case carries ids and figures
- [Diagnostic: incoming adapter packages that drive a use case without translating its failures](/rule/errors/dca-err-006.md) — an adapter that only switches counts as translating: an exhaustive switch over the result is its answer
- [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md) — lists every sealed result without a case implementing `Refusal` and never fails; a result whose outcomes are all successes is correct on that list, one whose refusing case is unmarked commits where it should roll back

## Not the answer

- **A `default` branch in the switch.** It compiles every new case into the same answer — the defect the result was meant to remove.
- **A domain exception constructed in the use case.** A refusal the application finds is its own case, not the model's failure.
- **One use case of the context returning, the next throwing.** The context's adapters then answer the same kind of failure in two styles.
- **A `catch (DomainException e)` around the model call.** It turns a defect into a refusal; catch the concrete types the call can raise. The same for `OutputPortException`.
- **A refusal case without `Refusal`.** The boundary does not see it, and a write before it commits.
- **A save before the last point that can refuse.** The net rolls it back; the order is still wrong.
- **A case for the own database or broker failing.** Own infrastructure has to be there; its failure stays an exception. Only a foreign system's failure the port declares is a case.
- **A refusal case for "there is none" on a "which one, if any" query.** Absence is a normal answer there: an empty value.
- **A result that carries a status code or the words a page shows.** The adapter decides the answer, as with an exception.

## Anchors

- Decision: [Failure channel: exception or a case of the use case's result](/decision/failure-channel-exception-or-result.md) · [Result shape and assembly](/decision/result-shape-and-assembly.md)
- Guide: [Error handling rules](/guide/rules/error-handling-rules.md) · [The use case once, each adapter its translation](/guide/testing-levels/the-use-case-once-each-adapter-its-translation.md)
- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [Refusal](/marker/application/refusal.md) · [DomainException](/marker/tactical/domainexception.md) · [OutputPortException](/marker/application/outputportexception.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Pitfall: [A refusal returned after a write](/pitfall/a-refusal-returned-after-a-write.md)
- Sibling recipes: [Add a use case](/recipe/add-a-use-case.md) · [Test a use case](/recipe/test-a-use-case.md) · [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
