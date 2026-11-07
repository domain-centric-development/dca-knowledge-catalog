---
type: Template
title: "Use case skeleton (InputPort + UseCase + Command/Query + Result)"
tags: [template, application, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /marker/port-in/usecase.md, /marker/port-in/inputport.md, /marker/application/refusal.md, /marker/application/usecaseexception.md, /rule/errors/dca-err-008.md, /guide/rules.md, /guide/elements.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for one application-layer use case. A use case is a self-contained folder `application/{usecasename}/` (lowercase) with four files. Replace `{Name}` (PascalCase), `{usecasename}` (lowercase), `{context}`, `{basePackage}`. Use `Command` for writes, `Query` for reads.

A use case that can be refused carries its refusals the way its bounded context does — thrown as use-case exceptions, or returned as cases of a sealed result whose refusal cases implement `Refusal`. Both are equal; the context picks one for all its use cases. Either way the use case decides, then writes: every refusal comes before the first `save`, and the transaction boundary rolls back a returned `Refusal` as it rolls back a thrown exception. The Java node shows both variants. A foreign system's expected failure — an external system on the context map that refuses, times out or cannot be reached — is a refusal like any other, declared by its output port as an `OutputPortException`; the own database or broker failing stays an exception. A query that asks "which one, if any" answers *none* with an empty value, not a refusal; "not found" refuses only a caller that names a specific thing.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`use-case/java.md`](/template/use-case/java.md)

## Realizes / governed by

- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [InputPort](/marker/port-in/inputport.md) · [UseCaseException](/marker/application/usecaseexception.md) · [Refusal](/marker/application/refusal.md)
- Guide: [Layer rules](/guide/rules.md) · [Layer elements](/guide/elements.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md) · [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md)
- Recipe: [Add a use case](/recipe/add-a-use-case.md) · [Add a bulk operation](/recipe/add-a-bulk-operation.md) · [Add a read model](/recipe/add-a-read-model.md)
