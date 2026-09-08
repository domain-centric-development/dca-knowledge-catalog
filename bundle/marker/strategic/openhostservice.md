---
type: Marker
title: "@OpenHostService"
category: strategic
kind: annotation
signature: "public @interface OpenHostService"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships
methods: ["String context()", "String description() default \"\""]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/relationships/OpenHostService.java
tags: [strategic, marker]
---

Marks a class as an Open Host Service in Domain-Driven Design.

An Open Host Service is the protocol a bounded context publishes for other bounded contexts to
consume — a relationship pattern, not a transport. In-process it is the context's `api`
package; over the network it is an incoming adapter (REST, gRPC, MCP, ...). Either way it
translates domain objects into a published language (DTOs), the way a REST controller translates
domain objects to JSON.

**Architectural rules:**

- Open Host Services live at the context boundary: in `api/` or anywhere under `adapter/incoming/` — never in the domain or application layer
- They must return DTOs, never domain objects
- Outgoing adapters of other contexts may only depend on a context's published `api/`
and `events/` packages
- Application-layer use cases never import another context's Open Host Service directly —
they go through their own output ports

**Usage:**

```java
@OpenHostService(
    context = "Product Catalog",
    description = "Provides product information for other contexts"
)
@Service
public class ProductCatalogService {
    // Returns DTOs, not domain objects
    public Optional<ProductInfo> getProductInfo(ProductId id) { ... }
}
```

## Governed by

- [Open Host Services must be published: in the api package or as an incoming adapter](/rule/strategic/open-host-services-must-be-published-in-the-api-package-or-as-an-incoming-adapter.md)

## Discussed in

- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
