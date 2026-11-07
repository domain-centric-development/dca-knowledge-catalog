---
type: Rule
id: DCA-TAC-026
title: The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id
rule: "An object loaded by its id alone is reachable by anyone who knows or guesses the id - the insecure direct object reference of broken access control (OWASP Top 10, A01). An aggregate marked as owned belongs to someone; its repository offers a lookup scoped to the owner, so a use case acting for a caller can load it through the caller and an unscoped lookup is never the only way in. Whether the use case calls the scoped lookup, and whether it proved the caller's right to a change of owner, is logic the rule does not see."
constraint: The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id.
selects: "Concrete classes anywhere under scan assignable to both the owned role (by default Owned of the building blocks) and the aggregate-root role, each with the repository interfaces that bind it: the first type argument of the repository marker or of an intermediate port assignable to it, or - where the binding is raw - the interface in the same context named after the aggregate plus the repository suffix. An owned aggregate without a repository is not selected."
checks: "The owner id type is the type argument the aggregate binds on the owned marker, through its interfaces and superclasses; an aggregate that leaves it raw or a type variable is reported. The aggregate's id type is the second type argument of the repository's binding, or else the return type of the aggregate's id(). At least one method of the repository, inherited ones included, takes a parameter whose raw type is the aggregate's id type and a further parameter whose raw type is the owner id type - in either position, under any name, other parameters allowed - and returns a type that involves the aggregate: the aggregate itself, an Optional of it or another container, a nullable return included. A method that answers only yes or no does not count. Where the id type cannot be resolved, any parameter assignable to the id role stands for it. Whether a use case calls the scoped lookup or the unscoped findById is not checked; a generic intermediate port whose parameters are type variables is not seen through. An empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-026"
status: enforced
maturity: experimental
rule_set: tactical
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Concrete classes anywhere under scan assignable to both the owned role (by default Owned of the building blocks) and the aggregate-root role, each with the repository interfaces that bind it: the first type argument of the repository marker or of an intermediate port assignable to it, or - where the binding is raw - the interface in the same context named after the aggregate plus the repository suffix. An owned aggregate without a repository is not selected.

## Check

The owner id type is the type argument the aggregate binds on the owned marker, through its interfaces and superclasses; an aggregate that leaves it raw or a type variable is reported. The aggregate's id type is the second type argument of the repository's binding, or else the return type of the aggregate's id(). At least one method of the repository, inherited ones included, takes a parameter whose raw type is the aggregate's id type and a further parameter whose raw type is the owner id type - in either position, under any name, other parameters allowed - and returns a type that involves the aggregate: the aggregate itself, an Optional of it or another container, a nullable return included. A method that answers only yes or no does not count. Where the id type cannot be resolved, any parameter assignable to the id role stands for it. Whether a use case calls the scoped lookup or the unscoped findById is not checked; a generic intermediate port whose parameters are type variables is not seen through. An empty selection passes.

## .NET reading

**Selection.** Concrete classes below the root namespace assignable to both the owned role (by default IOwned of the building blocks) and the aggregate-root role, with their runtime type in the loaded assemblies, each with the repository interfaces that bind it: the first type argument of the generic repository role, or - where the binding is raw or unresolved - the interface in the same context named after the aggregate plus the repository suffix, with or without the leading I. An owned aggregate without a repository is not selected.

**Check.** The owner id type is the type argument of the generic interface the aggregate implements that carries the owned role; an aggregate that implements only the non-generic role, or binds a generic parameter, is reported. The aggregate's id type is the second type argument of the repository's binding, or else the type of the aggregate's Id property. At least one method of the repository, inherited interface methods included, takes a parameter of exactly the aggregate's id type and a further parameter of exactly the owner id type - in either position, under any name, other parameters such as a cancellation token allowed - and returns a type that involves the aggregate: the aggregate itself, nullable, in a Task or ValueTask or another generic container. A method that answers only yes or no does not count. Where the id type cannot be resolved, any parameter assignable to the id role stands for it. Whether a use case calls the scoped lookup or the unscoped FindByIdAsync is not checked; a generic intermediate port whose parameters are generic parameters is not seen through. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (trait-bound, source-test).

**Selection.** Types that implement both Owned and AggregateRoot, each with the repository traits that bind it through Repository<T>. The owner id type is the type the impl Owned block binds to OwnerId (the trait requires it, and requires AggregateRoot as supertrait); the aggregate's id is the type its impl Entity binds to Id. An owned aggregate without a repository trait is not selected.

**Check.** At least one method the repository trait declares itself takes a parameter whose type (through references) is the aggregate's id type and a further parameter whose type is the owner id type - either position, any name - and returns a type that names the aggregate, through Result, Option or another wrapper. A method that answers only yes or no does not count; the inherited find_by_id takes the id alone. An owner id type the suite cannot resolve (a type outside the workspace, a type alias) is reported. Whether a use case calls the scoped lookup is not checked; a lookup declared only in a generic intermediate trait is not seen. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/tactical/dca-tac-026/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [Owned<OWNER>](/marker/tactical/owned.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/tactical/dca-tac-026/overview.md)
- [`repositoryInterfaces`](/evidence/rule/tactical/dca-tac-026/repositoryinterfaces.md)
- [`ownedAggregateRoots`](/evidence/rule/tactical/dca-tac-026/ownedaggregateroots.md)
- [`typeArgument`](/evidence/rule/tactical/dca-tac-026/typeargument.md)
- [`simpleName`](/evidence/rule/tactical/dca-tac-026/simplename.md)
- [`repositoriesOf`](/evidence/rule/tactical/dca-tac-026/repositoriesof.md)
- [`aggregateIdOf`](/evidence/rule/tactical/dca-tac-026/aggregateidof.md)
- [`isScopedLookup`](/evidence/rule/tactical/dca-tac-026/isscopedlookup.md)
- [`fail`](/evidence/rule/tactical/dca-tac-026/fail.md)
- [`classesMatching`](/evidence/rule/tactical/dca-tac-026/classesmatching.md)
- [`boundAggregateArgument`](/evidence/rule/tactical/dca-tac-026/boundaggregateargument.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/tactical/dca-tac-026/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/tactical/dca-tac-026/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/tactical/dca-tac-026/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/tactical/dca-tac-026/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/tactical/dca-tac-026/c-expression.md)
