---
type: Recipe
title: Build DCA without a framework
tags: [recipe, bootstrap, infrastructure, port]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/usecase.md, /marker/port-out/outputport.md, /rule/layered/dca-lay-001.md, /rule/usecase/dca-use-016.md, /guide/dependency-structure/the-composition-root.md, /guide/package-structure.md]
---

DCA does not need a container. A command-line tool, a library-sized service or a language without a DCA rule library
(Python, Go, TypeScript) can carry the same layers, ports and building blocks. Three things a framework did now
become code of the project: the building blocks, the wiring, and the layer check. This recipe takes a stdlib-only
Python package as its worked case; the steps hold for any language.

## Steps

1. **Lay out the package as DCA does.** Per bounded context `domain/`, `application/`, `adapter/incoming/`,
   `adapter/outgoing/`; one `infrastructure/` for the composition root and the process host; the building blocks and
   the shared kernel beside the contexts. Every module sits in exactly one layer — a module outside every layer is a
   finding, with one exception per recorded reason (a version stamp other tools read by path).
2. **Write the building blocks once, by the names the libraries use.** `Value`, `Id`, `Entity`, `AggregateRoot`,
   `DomainEvent`, `DomainService`, `DomainException`, `UseCase`, `OutputPort`, `Repository`, `Store`,
   `UseCaseException`. In Python:
   - a value is a frozen dataclass by its base — `Value.__init_subclass__` applies `dataclasses.dataclass(frozen=True)`
     and `typing.dataclass_transform(frozen_default=True)` tells the type checker; a subclass declares its fields and
     carries no decorator of its own, the closest form to Java's `record … implements Value`;
   - a port is a `typing.Protocol` (structural) or an `abc.ABC` (nominal); an adapter satisfies a protocol by shape.
3. **Keep the domain free of bare primitives where they carry meaning.** A string with a format is a value, a flag
   is an enum, a moment is a value — the libraries' domain rules, held by review or by the project's own check.
4. **Write the composition root by hand — Pure DI.** One module in `infrastructure/` constructs the outgoing
   adapters, passes them to the use cases' constructors, passes the use cases to the incoming adapters, and calls the
   entry point. It holds no rule and no condition over a business value. Where a use case needs a second operation,
   the root hands the second use case in behind the first one's output port
   ([Hand a use case a second operation](/recipe/hand-a-use-case-a-second-operation.md)).
5. **Check the layers yourself.** Without `dca-archunit` / `DomainCentric.ArchRules`, a small script over the
   imports enforces the same direction (domain imports nothing of the application or adapters; the application
   nothing of adapters or infrastructure; an incoming adapter no infrastructure) and reports under the libraries'
   rule ids, so a finding reads the same in every language. Structural ports add one check the type checker does not
   make: **every output port has an implementation, and it lives in an outgoing adapter** — the composition root
   holds only the bridge that hands a port a second use case. `mypy` only sees a fit where an adapter is assigned to
   the port type.
6. **Let the type checker carry the rest.** `mypy --strict` (or the language's strict mode) holds the ports'
   signatures, the frozen values and the typed ids; run it with the layer check in the same build step.
7. **Verify** — the layer check, the type checker and the tests in one command, red on the first finding.

## Rules to satisfy (build-time checklist)

The same ids, held by the project's own check:

- [Diagnostic: The rules of the Layered Architecture should be followed](/rule/layered/dca-lay-001.md)
- [Use cases must not invoke other use cases](/rule/usecase/dca-use-016.md)

## Anchors

- Guide: [The composition root](/guide/dependency-structure/the-composition-root.md) · [Java package structure](/guide/package-structure.md)
- Markers: [UseCase](/marker/port-in/usecase.md) · [OutputPort](/marker/port-out/outputport.md)
- Sibling recipes: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md) · [Host a long-running process](/recipe/host-a-long-running-process.md)
