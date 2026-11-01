---
type: Pitfall
title: A rule checked at the edge and again in the value object
tags: [pitfall, tactical, value-object, adapter, error-handling]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, /guide/rules/domain-layer-rules.md, /guide/rules/adapter-layer-rules.md, /guide/rules/error-handling-rules.md]
---

The incoming adapter checks a rule the value object already carries. A request record says `@NotBlank @Size(max = 200) String title`, a form field `[Required, MaxLength(200)]`, and the `Title` value object refuses a blank title and one over 200 characters as well. Or the adapter goes the other way and makes the value object's check unreachable: `@RequestParam(defaultValue = "")` turns a missing field into an empty one, so the value object never sees null — and nobody wrote down what it would do with one. It reads as defence in depth.

## Why it is wrong

- Two copies of one rule drift. The product raises the limit to 250 characters; the value object changes, the annotation does not, and a valid title is refused at the edge with a message the domain never chose.
- The edge decides what the domain should. Whether a missing value is valid is a rule a domain expert could change. A default at the adapter answers that question in the wrong place: should null become valid, the adapter has to change too, and should it stay invalid, the value object was never asked.
- Two failures answer one rule. The annotation produces a binding error, the value object a named failure; the page or the API now has two ways to say "the title is invalid", rendered by two mechanisms, tested twice or once.
- A value object without its own null refusal is only valid as long as every caller behaves. The next adapter — a message consumer, a batch import — has no annotation, and an NPE reaches the caller as a server fault instead of a refusal.

## Do instead

Check the rule once, in the value object built from input, and let it refuse everything the rule refuses — a missing value included — with the rule's named failure. The adapter checks only the shape of the input: does the body parse, does a number or an id parse, is the path segment there. It hands the raw value on unchanged, absent as absent, and its one translation site answers the value object's failure like every other refusal.

Bean Validation, DataAnnotations or FluentValidation stay where no value object carries the rule: a sort parameter, a page size, a field the adapter consumes itself.

A null check on a value that only code passes — a reference the use case holds, an amount computed inside the model — is a different thing: a contract for the caller, answered with the platform's argument exception. The origin of the value decides which of the two a check is.

## Anchors

- Marker: [Value](/marker/tactical/value.md)
- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) (value object rules) · [Adapter layer rules](/guide/rules/adapter-layer-rules.md) (input adapter rules) · [Error handling rules](/guide/rules/error-handling-rules.md)
- Related decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
- Related pitfalls: [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md) · [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Default construction can bypass value validation](/pitfall/default-construction-bypasses-validation.md)
- Templates: [Page controller](/template/page-controller.md) · [REST resource](/template/rest-resource.md)
