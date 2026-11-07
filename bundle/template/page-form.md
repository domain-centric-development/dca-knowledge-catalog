---
type: Template
title: "Form skeleton (the form object of a page adapter, named after its command)"
tags: [template, adapter, dto, naming, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/naming/dca-nam-007.md, /rule/hexagonal/dca-hex-011.md, /guide/rules/domain-layer-rules.md, /guide/rules/error-handling-rules.md, /guide/rules/application-layer-rules.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for the **form object** of a [page controller](/template/page-controller.md): the type a server-rendered page's form binds to when the person submits it. Replace `{Operation}` / `{Aggregate}` / `{context}` / `{basePackage}`.

## The name is derived, not chosen

One form object per command, named after the command:

| Command (application) | Form (web adapter) |
|---|---|
| `{Operation}{Aggregate}Command` | `{Operation}{Aggregate}Form` |
| `CreateEntryCommand` | `CreateEntryForm` |
| `RenameEntryCommand` | `RenameEntryForm` |

The command's name comes from the use case, and the use case's from the operation the glossary names (see [Name an operation in the glossary](/decision/name-an-operation-in-the-glossary.md)). So the form has nothing left to decide: not `EntryForm` after the aggregate, not `NewEntryForm` after the page, not `EntryInput`. Two commands are two forms, also when their fields are the same today — a create and an edit form change apart once one of them gains a field. A command whose every field comes from the path or the session — a button that completes or deletes the thing the page shows — has no form object; the form exists where the person types something.

## What it is

- **The page's fields as the person typed them.** Text the person types is a `String`, as submitted, empty and absent included. A control whose value the browser already restricts — a number field, a checkbox, a choice of fixed options — may bind to the type that control yields; what does not parse is refused by the binding, and the page re-renders with it, as the page controller shows.
- **Not a domain type.** No value object, no typed id, no enum of the model in its fields. It holds what arrived, not what the model accepted.
- **Not the command.** The command holds the value objects the use case works with; the form holds the raw input they are built from. A form passed into the application would make the use case parse a page.
- **No rule of its own.** No Bean Validation or DataAnnotations that repeat a value object's rule: the rule is checked once, in the value object (see [A rule checked at the edge and again in the value object](/pitfall/a-rule-checked-at-the-edge-and-in-the-value-object.md)).
- **In the page adapter's package**, `adapter/incoming/web/`, next to the controller and its [ViewModel](/template/view-model.md). Neither the application nor the domain knows it.

## The translation

The page controller translates the form into the command: each raw field into the value object that carries its rule, the path's id into the typed id, then the command. Where a value object refuses the input, the refusal is answered at the controller's one translation site for it, and the page shows it at the field it came from, with the form as submitted so the person corrects rather than retypes. The form itself translates nothing and decides nothing.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`page-form/java.md`](/template/page-form/java.md)

## Realizes / governed by

- Rules: [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md) · [Incoming Adapters must depend on input port interfaces, not on use case classes](/rule/hexagonal/dca-hex-011.md)
- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) — a rule is checked once, in the value object · [Error handling rules](/guide/rules/error-handling-rules.md) — the adapter answers · [Application layer rules](/guide/rules/application-layer-rules.md) — use-case and command names
- Decision: [Name an operation in the glossary](/decision/name-an-operation-in-the-glossary.md)
- Pitfalls: [A rule checked at the edge and again in the value object](/pitfall/a-rule-checked-at-the-edge-and-in-the-value-object.md) · [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Adapter DTO in the application layer](/pitfall/dto-in-application-layer.md)
- Related templates: [Page controller](/template/page-controller.md) · [ViewModel](/template/view-model.md) · [Value object](/template/value-object.md)
