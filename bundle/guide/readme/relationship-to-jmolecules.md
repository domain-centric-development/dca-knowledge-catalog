---
type: Section
title: Relationship to jMolecules
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
tags: [guide, section]
---

[jMolecules](https://github.com/xmolecules/jmolecules) is a set of technology-independent
annotations and interfaces expressing DDD and architectural concepts in Java. Ten of its markers
have a direct counterpart in DCA's building blocks: aggregate root, entity, value object,
identifier, domain event, repository, factory, domain service, and the two event kinds.

**A project that already uses jMolecules keeps it.** DCA's rules select building blocks through
roles resolved by fully qualified name, so pointing the roles at `org.jmolecules.ddd.types.*` puts
the whole rule catalog on an existing jMolecules model without migrating a single type. That is the
same mechanism a project with its own hand-written markers uses.

What DCA adds on top of the shared vocabulary is the part the rules need and jMolecules does not
carry: a typed port hierarchy with a common root, the `Store` beside the `Repository`, the
`TransactionBoundary` as an execution abstraction that is deliberately not a port, the layered
failure types, strategic relationships that name a translation strategy and a rationale, a rendered
context map — and one rule id that means the same thing in Java and in .NET. What jMolecules has and
DCA does not is the tooling around the annotations: a ByteBuddy plugin, and Spring, JPA and Jackson
integrations.

The two developed independently and neither derives from the other. They are not alternatives to
choose between: the markers are the cheap half, and DCA's value is in what checks them.

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
