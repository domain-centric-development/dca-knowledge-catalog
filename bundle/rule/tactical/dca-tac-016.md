---
type: Rule
id: DCA-TAC-016
title: Repositories must only exist for Aggregate Roots
rule: A repository is the collection of one aggregate type; a repository for an entity would let callers bypass the root that guards the aggregate's invariants.
constraint: Repositories must only exist for Aggregate Roots.
selects: "Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded."
checks: "The aggregate is read from the type argument the interface binds: the first argument of the parameterised Repository marker it extends, or of an intermediate port that is itself assignable to the marker. That type must be assignable to AggregateRoot, and the interface's simple name must be that type's simple name plus 'Repository' - so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as AuditedRepository<T, ID> binds no aggregate of its own. When the marker is not generic or is used raw, the aggregate is resolved by name instead: among all classes under scan with the interface's simple name minus 'Repository' and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. The interface's methods play no role."
enforced_by: "TacticalPatternRules#DCA-TAC-016"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Repositories must only exist for Aggregate Roots

## Selection

Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded.

## Check

The aggregate is read from the type argument the interface binds: the first argument of the parameterised Repository marker it extends, or of an intermediate port that is itself assignable to the marker. That type must be assignable to AggregateRoot, and the interface's simple name must be that type's simple name plus 'Repository' - so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as AuditedRepository<T, ID> binds no aggregate of its own. When the marker is not generic or is used raw, the aggregate is resolved by name instead: among all classes under scan with the interface's simple name minus 'Repository' and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. The interface's methods play no role.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository whose name ends with Repository; an interface named exactly Repository excluded.

**Check.** The aggregate is read from the type argument the interface binds: the first argument of the generic repository role it implements. That type must be assignable to IAggregateRoot, and the interface's name - minus a leading I followed by an upper-case letter - must be that type's name plus 'Repository', so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as IAuditedRepository<TAggregate, TId> binds no aggregate of its own. When the role is not generic, is used raw, or the runtime type cannot be resolved, the aggregate is resolved by name instead: among all non-interface types below the root with the interface's name minus 'Repository' and in the same context - the nearest enclosing namespace carrying a [BoundedContext] or [SharedKernel] marker class, falling back to the first segment below the root namespace - at least one must exist and every one must be assignable to IAggregateRoot. The interface's methods play no role.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/tactical/dca-tac-016/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/tactical/dca-tac-016/overview.md)
- [`repositoryInterfaces`](/evidence/rule/tactical/dca-tac-016/repositoryinterfaces.md)
- [`boundAggregateArgument`](/evidence/rule/tactical/dca-tac-016/boundaggregateargument.md)
- [`fail`](/evidence/rule/tactical/dca-tac-016/fail.md)
- [`classesMatching`](/evidence/rule/tactical/dca-tac-016/classesmatching.md)
- [C# expression](/evidence/rule/tactical/dca-tac-016/c-expression.md)
