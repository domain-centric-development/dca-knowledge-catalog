---
type: Section
title: Solution and Project Layout
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/language-mappings.md
tags: [guide, section]
---

Java keeps every context in one Gradle module and separates them by package; Spring Modulith (or the
`strategic` rules) makes the boundary real. .NET makes it physical: **one project per bounded context**,
plus one for the shared kernel, one for global infrastructure and one host. The folders inside a
context project are the layers, PascalCase.

| Java | .NET |
|---|---|
| `com.company.project.order` (package) | `Company.Project.Order` (project + namespace) |
| `order/domain/model/` | `Order/Domain/Model/` |
| `order/application/placeorder/` | `Order/Application/PlaceOrder/` |
| `order/application/{feature}/{usecase}/` | `Order/Application/{Feature}/{UseCase}/` |
| `order/application/shared/` | `Order/Application/Shared/` |
| `order/adapter/incoming/web/` · `api/` · `event/` | `Order/Adapter/Incoming/Web/` · `Api/` · `Event/` |
| `order/adapter/outgoing/persistence/` | `Order/Adapter/Outgoing/Persistence/` |
| `order/infrastructure/` (optional `@Configuration`) | `Order/Infrastructure/` — `AddOrderContext(this IServiceCollection)` |
| `order/api/` (published in-process contract) | `Order/Api/` |
| `order/events/` (published integration events) | `Order/Events/` |
| `sharedkernel/` | `Company.Project.SharedKernel/` |
| `infrastructure/` (global) | `Company.Project.Infrastructure/` (composition root) |
| `@SpringBootApplication` class | `Company.Project.Web/` — `Program.cs`, views, static assets |
| `src/test-architecture/` | `tests/Company.Project.ArchitectureTests/` |

Use case folders are lowercase in Java (`placeorder`) because Java packages are; PascalCase in C#
(`PlaceOrder`) because .NET namespaces are. Feature folders follow the same rule (`cartrecovery` /
`CartRecovery`). The rules read whatever the host language's convention produces.

## Related markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
