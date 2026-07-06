---
type: Decision
title: "Specification or query method: how to express a selection rule"
tags: [decision, tactical, specification, repository]
---

You have a business rule that decides whether something qualifies — a "large order", a "premium customer", an "overdue invoice". The fork is how to express it: as a **Specification** (a first-class domain object with `isSatisfiedBy`, composable with `and`/`or`/`not`), or as a plain **repository query method** (`findOverdue()`). A Specification pays for itself when the rule is domain-meaningful, reused, or combined; a query method is the leaner choice when you just need rows back and the rule is a one-off.

## The discriminator

Ask, in order:

1. **Is the rule a named domain concept?** If "large order" is language the domain speaks, encapsulating it as a `LargeOrderSpecification` makes the rule explicit, testable, and reusable. If it is an incidental filter with no domain name, a query method is honest and simpler.
2. **Do you combine it with other rules?** Specifications compose: `largeOrder.and(internationalOrder)`. If you need to mix and match conditions, the Specification pattern is what makes that clean. A query method per combination explodes into `findLargeAndInternational()`, `findLargeAndDomestic()`, …
3. **Do you evaluate it in memory on an object you already hold, or select from a store?** Specifications shine at **in-memory evaluation** of a candidate you already loaded (`spec.isSatisfiedBy(order)`), and as reusable rule objects. A query method is the right tool when the point is to **fetch matching aggregates** from a Repository efficiently.

A quick tell: if the same rule appears in a use-case guard *and* in a filter *and* in a validation, it wants to be one Specification, not three copies.

## Options

| | Specification | Repository query method |
|---|---|---|
| Use when | rule is a named domain concept, reused, or composed | one-off selection, or you need matching aggregates fetched from a store |
| Shape | domain object, `boolean isSatisfiedBy(T)` | method on a Repository interface |
| Composition | `and` / `or` / `not` combinators | none — one method per query |
| Evaluation | in memory, on a candidate you hold | at the persistence boundary |
| Lives in | domain package | application output-port interface (impl in adapter) |

**Default: a query method for simple, one-shot fetches; a Specification when the rule is domain-meaningful, reused, or composed.** The two also combine well: a Repository can accept a Specification, or a query method can pre-filter cheaply and a Specification refine in memory. Prefer whichever keeps the *rule* named once and the *fetch* efficient.

## Consequences

- A Specification is a domain citizen: it implements the `Specification<T>` marker, its name must end with `Specification`, and it carries no Spring annotations (ArchUnit-enforced — see anchors).
- Composition is built in via `and`/`or`/`not` returning composite specifications, so complex rules stay declarative instead of branching.
- A query method stays on the Repository interface in the application layer with its implementation in the adapter — it must still return Aggregate Roots, since it *is* a Repository method.

## Anchors

- Markers: [Specification&lt;T&gt;](/marker/tactical/specification.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Rules: [Specifications must end with 'Specification'](/rule/advanced/specifications-must-end-with-specification.md) · [Specifications must not have Spring annotations](/rule/advanced/specifications-must-not-have-spring-annotations.md) · [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- ADRs: [ADR-013 Specification Pattern for Business Rules](/adr/adr-013-specification-pattern.md) · [ADR-002 Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- Book: [Specification Pattern](/book/11-shared-kernel/specification-pattern.md) · [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md) · [Repository Interfaces](/book/06-application-layer/repository-interfaces.md)
- Recipes: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Template: [Specification skeleton](/template/specification.md)
- Related decision: [Repository vs Store](/decision/repository-vs-store.md)
