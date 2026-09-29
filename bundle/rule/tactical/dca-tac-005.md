---
type: Rule
id: DCA-TAC-005
title: Entities must not be instantiated directly from outside the aggregate
rule: Entities are created through their aggregate root so that the root can enforce its invariants.
constraint: Entities must not be instantiated directly from outside the aggregate.
selects: "Constructor calls to non-root Entity types, records included."
checks: "The caller is the entity itself or an AggregateRoot, Entity or Factory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected."
enforced_by: "TacticalPatternRules#DCA-TAC-005"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Entities must not be instantiated directly from outside the aggregate

## Selection

Constructor calls to non-root Entity types, records included.

## Check

The caller is the entity itself or an AggregateRoot, Entity or Factory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.

## .NET reading

**Selection.** Constructor calls to non-root IEntity types, records and structs included.

**Check.** The caller is the entity itself or an IAggregateRoot, IEntity or IFactory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/tactical/dca-tac-005/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/tactical/dca-tac-005/overview.md)
- [`nonRootEntities`](/evidence/rule/tactical/dca-tac-005/nonrootentities.md)
- [`fail`](/evidence/rule/tactical/dca-tac-005/fail.md)
- [`classesMatching`](/evidence/rule/tactical/dca-tac-005/classesmatching.md)
- [C# expression](/evidence/rule/tactical/dca-tac-005/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/tactical/dca-tac-005/c-helper-intraclasscalls.md)
