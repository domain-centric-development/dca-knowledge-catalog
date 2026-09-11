---
type: Section
title: .NET Solution Structure
chapter: Java Package Structure
source: guide
resource: dca-guide/architecture/package-structure.md
tags: [guide, section]
---

The same shape in C#: **one project per bounded context**, folders for the layers, PascalCase
segments. A context is declared by a marker class in its root namespace (C# has no `package-info`).

```text
src/
├── Company.Project.{Context}/        one assembly per bounded context (namespace Company.Project.{Context})
│   ├── {Context}Context.cs           [BoundedContext], [Upstream], [Partnership] — the context declaration
│   ├── Domain/                       Model/, Event/, Service/, Specification/
│   ├── Application/                  {UseCase}/ or {Feature}/{UseCase}/ — I*InputPort, *UseCase, *Command, *Result
│   │   └── Shared/                   output ports, context-wide
│   ├── Adapter/
│   │   ├── Incoming/                 Web/, Api/, Event/ (call input ports)
│   │   └── Outgoing/                 Persistence/, Event/, … (implement output ports)
│   └── Infrastructure/               DI registration: Add{Context}Context()
├── Company.Project.SharedKernel/     [SharedKernel] marker class; Domain/Model, Application/Shared, shared adapters
├── Company.Project.Infrastructure/   composition root, cross-cutting concerns
└── Company.Project.Web/              the host (ASP.NET Core); controllers live in the contexts
tests/
└── Company.Project.ArchitectureTests/   DcaArchitectureTest subclass (Debug build), all context assemblies
```

Building blocks come from `DomainCentric.BuildingBlocks`, the rules from `DomainCentric.ArchRules.Xunit`
— the same rule ids as the Java library. Every rule speaks of namespaces where the Java text says
packages; a project boundary per context is the .NET way of making the module boundary physical.

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [@Upstream](/marker/strategic/upstream.md)
- [Specification<T>](/marker/tactical/specification.md)
