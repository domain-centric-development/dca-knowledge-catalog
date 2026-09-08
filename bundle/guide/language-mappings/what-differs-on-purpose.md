---
type: Section
title: What Differs on Purpose
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/language-mappings.md
tags: [guide, section]
---

- **Async ports, synchronous domain.** Every .NET port method is `Task`-based and takes a
  `CancellationToken`; aggregates, values and domain services never are. The Java ports are synchronous.
- **Physical modules.** A .NET context is a project; a Java context is a package. Both are verified
  the same way, but only the .NET compiler refuses a cross-context reference to an `internal` type.
- **No `package-info`.** The context marker class is the one file a Java reader will not recognise.
- **No baseline dial** in .NET governance; lower a rule to a warning instead.
- **Transactions are explicit** in .NET (`ITransactionBoundary`, or a decorator around `IUseCase`);
  Java may use `@Transactional`. The Java rule `DCA-USE-012` guards Spring's after-commit relay, which
  is skipped silently without an active transaction; it is *not applicable* in .NET, where after-save
  delivery is the job of the integration-event outbox adapter, not of the use case.
- **Container attributes** (`@Upstreams`, `@Partnerships`) do not exist in C# — attributes repeat.

Everything not listed here is the same architecture, spelled the way the language spells it.

## Related markers

- [@Partnerships](/marker/strategic/partnerships.md)
- [@Upstreams](/marker/strategic/upstreams.md)
