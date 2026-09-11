---
type: Section
title: Declaring Contexts and Relationships
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

Java declares a context on its root package; C# has no namespace-level attributes, so the declaration
sits on **one marker class directly in the context's root namespace**. The rules discover contexts by
finding that class. Java package `ddd.strategic` (+ `.relationships`), .NET `Ddd.Strategic` (+ `.Relationships`).

| Java (`package-info.java`) | C# (marker class) |
|---|---|
| `@BoundedContext(name, description)` | `[BoundedContext(name, Description = …)]` |
| `@SharedKernel(description)` | `[SharedKernel(Description = …)]` |
| `@OpenHostService(context, description)` | `[OpenHostService(context, Description = …)]` |
| `@Upstream(context, translation, via)` — repeatable via `@Upstreams` | `[Upstream(context, translation, params via)]` — `AllowMultiple` |
| `@ExternalUpstream(name, translation, interaction, contractPackages, …)` | `[ExternalUpstream(name, translation, interaction) { ContractNamespaces, Protocol, Exchanges, Rationale, Status }]` |
| `@Partnership(context, rationale)` | `[Partnership(context, Rationale = …)]` |
| `Upstream.Translation.ANTI_CORRUPTION_LAYER / CONFORMIST` | `Translation.AntiCorruptionLayer / Conformist` |
| `Upstream.Consumes.API / EVENTS` | `Consumes.Api / Events` |
| `Upstream.Status.IMPLEMENTED / PLANNED` | `UpstreamStatus.Implemented / Planned` |
| `ExternalUpstream.Interaction.OUTBOUND / INBOUND` | `Interaction.Outbound / Inbound` |

```java
// com/company/project/cart/package-info.java
@BoundedContext(name = "Shopping Cart", description = "Carts and their items")
@Upstream(context = "product", translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
          via = Upstream.Consumes.API, rationale = "Product data is translated into cart's own types")
@Partnership(context = "checkout", rationale = "CartCompletionTrigger contract evolves jointly")
package com.company.project.cart;
```

```csharp
// Company.Project.Cart/CartContext.cs
namespace Company.Project.Cart;

[BoundedContext("Shopping Cart", Description = "Carts and their items")]
[Upstream("Product", Translation.AntiCorruptionLayer, Consumes.Api,
          Rationale = "Product data is translated into cart's own types")]
[Partnership("Checkout", Rationale = "ICartCompletionTrigger contract evolves jointly")]
public static class CartContext { }
```

The context map — tables plus a Mermaid diagram rendered from these declarations — exists in both
libraries (`ContextMapRenderer`), and the `contextmap` rules verify that declarations and real
dependencies agree.

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [@Upstream](/marker/strategic/upstream.md)
- [@Upstreams](/marker/strategic/upstreams.md)
