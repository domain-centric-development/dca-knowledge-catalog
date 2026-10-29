---
type: Reference
title: "Setup and Configuration — .NET: ArchUnitNET"
tags: [reference]
evidence_for: "/guide/archunit-governance/setup-and-configuration.md#net-archunitnet"
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md#net-archunitnet). This is an evidence excerpt; retain the parent selection and caveats.

### .NET: ArchUnitNET

The same catalog exists for C# — `DomainCentric.ArchRules` on ArchUnitNET, with the xUnit base
class `DomainCentric.ArchRules.Xunit`. Rule ids are identical to the Java library's, so a team, a
review checklist or a knowledge base can speak of `DCA-TAC-001` in either language.

```text
dotnet add package DomainCentric.BuildingBlocks            # production projects
dotnet add package DomainCentric.ArchRules.Xunit           # the architecture test project
```

```csharp
using System.Reflection;
using DomainCentric.ArchRules;
using DomainCentric.ArchRules.Xunit;

public sealed class ArchitectureTest : DcaArchitectureTest
{
    protected override DcaLayout Layout => DcaLayout.ForRootNamespace("Company.Project");

    protected override IEnumerable<Assembly> Assemblies =>
        new[] { typeof(Company.Project.Cart.CartContext).Assembly, typeof(Program).Assembly };
}
```

Every rule runs as its own theory case named by id. The rules work on namespaces, so one project
per bounded context is fine — pass all assemblies. Differences worth knowing:

- **Debug builds only.** `DcaArchitecture.Load` refuses optimized assemblies: the compiler emits async
  state machines as structs there, and ArchUnitNET drops them, which would hide every dependency
  that occurs only inside an `async` method. `dotnet test` builds Debug by default.
- **Context declaration** is a marker class in the context's root namespace carrying
  `[BoundedContext]`, not a `package-info`.
- **Framework types by role, too.** `FrameworkTypes.AspNetCore()` is the default (controller base
  class, `[ApiController]`, page-model base, `TransactionScope`); `FrameworkTypes.None()` leaves every
  role empty, a `with` expression adjusts one. .NET has no injectable stereotype, so the **Java rules
  that check only a container stereotype** are listed as *not applicable*; six `DCA-NET`
  rules exist only for .NET (synchronous domain, `Async` suffix on port methods, an awaitable and
  cancellable use-case contract, records for values and ids, no persistence framework in the
  application layer). Two of those six — the synchronous domain and the persistence-free application
  layer — say something about architecture rather than about C#; Java has no twin for them yet, and
  their `checks` texts say so.
- **No baseline dial** (`frozen`): ArchUnitNET has no `FreezingArchRule`; lower such rules to a warning
  instead. The `dca-archunit.properties` keys are otherwise the same.

---
