---
type: Pitfall
title: A refusal returned after a write
tags: [pitfall, application, use-case, persistence, error-handling]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/error-handling-rules.md, /guide/rules/transaction-rules.md, /decision/failure-channel-exception-or-result.md, /rule/usecase/dca-use-012.md, /rule/errors/dca-err-008.md, /marker/application/refusal.md, /marker/application/transactionboundary.md, /pitfall/modifying-two-aggregates-in-one-transaction.md]
---

A use case saves something and only then finds the refusal: it saves the first aggregate, loads the second, and the second refuses — `return new {Rule}Violated(…)` after `repository.save(first)`. In a context that returns its refusals, the refusal leaves the transaction as a value, not as an exception. A transaction boundary that rolls back only on an exception commits the first write, and the caller is told "refused" about an operation that half happened.

## Why it is wrong

- **The order is the defect.** A use case writes only once it can no longer refuse. A refusal that can only come after a write means the operation changes something and then says no — usually two aggregates in one transaction, the second refusing what the first already did.
- **The returned form removes the accidental rollback.** A thrown refusal rolled the write back because it left the boundary as an exception; moving a context from thrown to returned refusals silently turns the same code into a partial commit, unless the boundary knows a returned refusal.
- **The caller cannot tell.** The case says "refused"; the store says "changed". No answer the adapter writes can be right for both.

## What catches it

- **The net.** Every refusal case implements the marker `Refusal` (`IRefusal` in .NET), and the transaction boundary rolls back when the work returns one — explicitly drawn or the interceptor around a declarative `@Transactional` use case. With the net in place the write is undone, exactly as a thrown exception would undo it. A refusal case without the marker, or a boundary without the net, commits it.
- **The transaction rule** — [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) puts a boundary there at all, and [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md) lists every sealed result with no case marked `Refusal` and asks whether none of its outcomes refuses — a result of successes alone is correct there, one with an unmarked refusing case is this pitfall; which way the use case orders its steps no rule sees.

The net makes the pitfall harmless for the data. It stays a design smell: the use case still asks after it acts.

## Do instead

Decide, then write: load, ask the model and every port that can refuse, refuse or go on, and save last. When the refusal can only be known after the first change, the operation spans two aggregates — split it, with the second change as a reaction in its own transaction ([Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md)). A remote effect made before the local write is outside every rollback: it keeps its compensation, thrown refusal or returned.

## Anchors

- Decision: [Failure channel: exception or a case of the use case's result](/decision/failure-channel-exception-or-result.md)
- Guide: [Error handling rules](/guide/rules/error-handling-rules.md) · [Transaction rules](/guide/rules/transaction-rules.md)
- Markers: [Refusal](/marker/application/refusal.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Rules: [Use cases that save an aggregate or publish domain events must have a transaction boundary](/rule/usecase/dca-use-012.md) · [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md)
- Recipe: [Return expected refusals as a sealed result](/recipe/return-expected-refusals-as-a-sealed-result.md)
- Related pitfall: [Modifying two aggregates in one transaction](/pitfall/modifying-two-aggregates-in-one-transaction.md)
