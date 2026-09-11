---
type: Template
title: "Use case skeleton (InputPort + UseCase + Command/Query + Result)"
tags: [template, application, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /marker/port-in/usecase.md, /marker/port-in/inputport.md, /guide/rules.md, /guide/elements.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for one application-layer use case. A use case is a self-contained folder `application/{usecasename}/` (lowercase) with four files. Replace `{Name}` (PascalCase), `{usecasename}` (lowercase), `{context}`, `{basePackage}`. Use `Command` for writes, `Query` for reads.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`use-case/java.md`](/template/use-case/java.md)

## Realizes / governed by

- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [InputPort](/marker/port-in/inputport.md)
- Guide: [Layer rules](/guide/rules.md) · [Layer elements](/guide/elements.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md)
- Recipe: [Add a use case](/recipe/add-a-use-case.md) · [Add a bulk operation](/recipe/add-a-bulk-operation.md) · [Add a read model](/recipe/add-a-read-model.md)
