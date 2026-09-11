---
type: Decision
title: "Specification or query method: how to express a selection rule"
tags: [decision, tactical, specification, repository]
review: reviewed
owner: Christoph Bloemer
evidence: [/marker/tactical/specification.md, /marker/port-out/repository.md, /rule/advanced/dca-adv-017.md, /rule/advanced/dca-adv-018.md, /rule/tactical/dca-tac-017.md, /guide/elements.md, /guide/quick-reference/framework-annotations.md, /guide/spring-modulith/shared-kernel-in-spring-modulith.md]
---

You have a business rule that decides whether something qualifies — a "large order", a "premium customer", an "overdue invoice". The fork is how to express it: as a **Specification** (a first-class domain object with `isSatisfiedBy`, composable with `and`/`or`/`not`), or as a plain **repository query method** (`findOverdue()`). A Specification pays for itself when the rule is domain-meaningful, reused, or combined; a query method is the leaner choice when you just need rows back and the rule is a one-off.

## The discriminator

Ask, in order:

The first question decides **whether the rule becomes an object**; the third decides only **where it is
evaluated**. They are not two answers to the same question, and reading them as such is how two people
build the same rule in two shapes.

1. **Is the rule a named domain concept?** If "large order" is language the domain speaks, encapsulating it as a `LargeOrderSpecification` makes the rule explicit, testable, and reusable. If it is an incidental filter with no domain name, a query method is honest and simpler. **This question alone decides whether a Specification exists.**
2. **Do you combine it with other rules?** Specifications compose: `largeOrder.and(internationalOrder)`. If you need to mix and match conditions, the Specification pattern is what makes that clean. A query method per combination explodes into `findLargeAndInternational()`, `findLargeAndDomestic()`, …
3. **Do you evaluate it in memory on an object you already hold, or select from a store?** This decides **how the rule is applied, never whether it is named**. In memory, the use case holds the candidate and asks the Specification (`spec.isSatisfiedBy(candidate)`). Against a store, the use case hands the Specification to the Repository (`findBy(specification)`) and the adapter decides how to answer it — in memory today, pushed down into the query later, without the use case changing.

**A named rule that selects from a store is both, not either.** The Specification names the rule once, in the
domain; the Repository accepts it, so the fetch stays at the persistence boundary. Answering such a case with a
finder named after the rule (`findOverdue()`) puts a domain concept in the port's method name, where it cannot be
composed, tested on a candidate you already hold, or reused in a guard — and a second reading of the same rule
then lives in a second method name. Answering it with a Specification the use case evaluates over *every* row is
the opposite mistake: the rule is named, and the fetch is gone.

The parameter is not what makes a rule incidental. A threshold, a date or a limit supplied by the caller is an
argument of the rule, not evidence that the rule has no name: "stock is below the reorder level" stays a named
concept whoever supplies the level. What makes a rule incidental is that the *domain does not speak of it* —
an ad-hoc filter the caller happens to want, with no term behind it.

A quick tell: if the same rule appears in a use-case guard *and* in a filter *and* in a validation, it wants to be one Specification, not three copies.

## Options

| | Specification | Repository query method |
|---|---|---|
| Use when | rule is a named domain concept, reused, or composed — including when it selects from a store, and then handed to the Repository | selection the domain has no name for |
| Shape | domain object, `boolean isSatisfiedBy(T)` | method on a Repository interface |
| Composition | `and` / `or` / `not` combinators | none — one method per query |
| Evaluation | in memory, on a candidate you hold | at the persistence boundary |
| Lives in | domain package | application output-port interface (impl in adapter) |

**Default: a Specification whenever the domain has a name for the rule, a query method when it does not.** A
one-shot fetch is not by itself a reason to leave a named rule unnamed — a Repository takes the Specification and
the fetch stays where it belongs. The two also combine the other way round: a query method may pre-filter cheaply
and a Specification refine in memory. The invariant to keep either way: the *rule* named once, the *fetch* at the
persistence boundary.

## Consequences

- A Specification is a domain citizen: it implements the `Specification<T>` marker, its name must end with `Specification`, and it carries no Spring annotations (ArchUnit-enforced — see anchors).
- Composition is built in via `and`/`or`/`not` returning composite specifications, so complex rules stay declarative instead of branching.
- A query method stays on the Repository interface in the application layer with its implementation in the adapter — it must still return Aggregate Roots, since it *is* a Repository method.
- A Repository that accepts Specifications needs one entry point (`findBy(specification)`), not one per rule. It may answer it in memory at first; pushing the same Specification down into the store later is an adapter change, and no use case or rule moves.

## Anchors

- Markers: [Specification&lt;T&gt;](/marker/tactical/specification.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Rules: [Specifications must end with 'Specification'](/rule/advanced/dca-adv-017.md) · [Specifications must not have Spring annotations](/rule/advanced/dca-adv-018.md) · [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md)
- Guide: [Layer elements](/guide/elements.md) · [Framework annotation rules](/guide/quick-reference/framework-annotations.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Recipes: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Template: [Specification skeleton](/template/specification.md)
- Related decision: [Repository vs Store](/decision/repository-vs-store.md)
