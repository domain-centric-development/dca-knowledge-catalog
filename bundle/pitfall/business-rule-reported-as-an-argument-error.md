---
type: Pitfall
title: A business rule reported as an argument error
tags: [pitfall, error-handling, domain, application]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-006.md, /marker/tactical/domainexception.md, /marker/application/usecaseexception.md, /template/domain-exception.md]
---

A broken rule of the model leaves the domain as the platform's own argument or state exception — `IllegalArgumentException`, `IllegalStateException`, `ArgumentException`, `InvalidOperationException` — and the incoming adapter catches that generic type and answers with one status and the exception's message. It reads as economical: no new type, one handler, done.

## Why it is wrong

- The adapter cannot tell the cases apart. A refused quantity, an unknown id and a duplicate key all arrive as the same type, so the adapter settles for one answer where the protocol has three. Which one the caller gets then depends on the order of the catch blocks.
- The same type is what the runtime raises for programming errors. An unexpected null or a broken assumption inside the application arrives through the same channel and is answered as "your request was wrong" — a server fault reported as a client fault, and hidden from every alert that watches for server faults.
- The reason lives in a string. A caller that wants to react to one outcome has to match on a message, which is neither part of the contract nor stable across a rewording.
- The model loses a word it has. "The reservation is already confirmed" is a sentence a domain expert says; reducing it to an argument check removes that word from the code.

## What forbids it

- [Exceptions declared in the domain layer must extend DomainException](/rule/errors/dca-err-001.md)
- [Exceptions declared in the application layer must extend UseCaseException](/rule/errors/dca-err-003.md)
- [Domain and use-case exceptions reside in the layer whose failure they name](/rule/errors/dca-err-002.md)
- [Diagnostic: incoming adapters that drive a use case without translating its failures](/rule/errors/dca-err-006.md) — lists the adapters that name neither failure type. It cannot see a `catch`, so it never fails; the judgement stays with review.

## Do instead

Give each outcome a type in the layer that owns it: a `DomainException` subtype for a rule of the model, a `UseCaseException` subtype for a failure of the request (not found, not owned by this caller, a precondition elsewhere). Let the incoming adapter map type to answer in one place, and let everything it does not know become a server fault with no message.

Argument guards stay as they are. A null check or a range check in a constructor is a contract for the caller, not a rule of the model, and the platform's argument exception is the right answer there. The test is the name: if a domain expert has a word for the failure, it is a domain exception with that word in its name.

## Anchors

- Markers: [DomainException](/marker/tactical/domainexception.md) · [UseCaseException](/marker/application/usecaseexception.md)
- Template: [Domain exception skeleton](/template/domain-exception.md)
- Related pitfall: [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Anemic domain model](/pitfall/anemic-domain-model.md)
