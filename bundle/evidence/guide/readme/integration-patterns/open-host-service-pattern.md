---
type: Reference
title: INTEGRATION PATTERNS — Open Host Service Pattern
tags: [reference]
evidence_for: "/guide/readme/integration-patterns.md#open-host-service-pattern"
---

[Full node and context](/guide/readme/integration-patterns.md#open-host-service-pattern). This is an evidence excerpt; retain the parent selection and caveats.

### Open Host Service Pattern

For synchronous cross-context queries, use the Open Host Service pattern.

```
PROVIDER CONTEXT (Product)               CONSUMER CONTEXT (Cart)
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ adapter/incoming/api/        │        │ adapter/outgoing/product/    │
│   ProductCatalogApi          │◄───────│   ProductDataAdapter         │
│   @RestController (REST)     │ calls  │   (implements ProductDataPort)│
│   OR @OpenHostService        │        └───────────────┬──────────────┘
│   (in-process modulith)      │                        │ implements
└──────────────────────────────┘                        ▼
                                        ┌──────────────────────────────┐
                                        │ application/shared/          │
                                        │   ProductDataPort            │
                                        │   (output port)              │
                                        └───────────────┬──────────────┘
                                                        │ uses
                                                        ▼
                                        ┌──────────────────────────────┐
                                        │ application/additemtocart/   │
                                        │   AddItemToCartUseCase       │
                                        │   (uses port, NOT OHS)       │
                                        └──────────────────────────────┘
```

#### Provider: REST API (Canonical)

The canonical DDD Open Host Service is a **REST API** with a published language:

```java
// adapter/incoming/api/ProductCatalogApi.java
@RestController
@RequestMapping("/api/v1/products")
public class ProductCatalogApi {

    private final GetProductByIdInputPort getProductUseCase;

    public record ProductInfoDto(String id, String name, BigDecimal price, int stock) {}

    @GetMapping("/{productId}")
    public ResponseEntity<ProductInfoDto> getProduct(@PathVariable String productId) {
        return getProductUseCase.execute(new GetProductQuery(ProductId.of(productId)))
            .map(r -> new ProductInfoDto(r.productId().value(), r.name(), r.price().amount(), r.stock()))
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
```

#### Provider: In-Process Service (Modulith Optimization)

For modulith deployments (single JVM), an in-process service avoids network overhead. It lives in the
context's published `api/` package — the in-process contract, next to `events/` — not in the adapter
tree: an Open Host Service is the *relationship* a context publishes, and the transport (in-process
call, REST, gRPC, MCP) is a detail. The REST variant above is simply the same relationship as an
incoming adapter.

```java
// api/ProductCatalogService.java  (published package of the Product context)
@OpenHostService(context = "Product Catalog", description = "...")
@Service
public class ProductCatalogService {
    private final GetProductByIdInputPort getProductByIdInputPort;  // Use case, NOT repository

    public record ProductInfo(ProductId productId, String name, Price price, int availableStock) {}

    public Optional<ProductInfo> getProductInfo(ProductId productId) {
        var response = getProductByIdInputPort.execute(new GetProductByIdQuery(productId.value()));
        if (!response.found()) return Optional.empty();
        return Optional.of(new ProductInfo(
            productId, response.name(),
            Price.of(Money.of(response.priceAmount(), Currency.getInstance(response.priceCurrency()))),
            response.stockQuantity()
        ));
    }
}
```

**Important:** Like an incoming adapter, the OHS calls **use cases (input ports)**, not repositories directly.

#### Consumer: Output Port + Adapter (Same for Both)

The consumer-side pattern is **identical** regardless of transport:

```java
// application/shared/ProductDataPort.java - Consumer defines what it needs
public interface ProductDataPort extends OutputPort {
    record ProductData(ProductId id, Price price, boolean hasStock) {}
    Optional<ProductData> getProductData(ProductId id, int quantity);
}

// adapter/outgoing/product/ProductDataAdapter.java - REST variant
@Component
public class ProductDataAdapter implements ProductDataPort {
    private final RestTemplate restTemplate;  // For REST API

    public Optional<ProductData> getProductData(ProductId id, int qty) {
        var response = restTemplate.getForObject("/api/v1/products/" + id.value(), ProductInfoDto.class);
        if (response == null) return Optional.empty();
        return Optional.of(new ProductData(id, Price.of(response.price()), response.stock() >= qty));
    }
}

// OR: adapter/outgoing/product/ProductDataAdapter.java - In-process variant (modulith)
@Component
public class ProductDataAdapter implements ProductDataPort {
    private final ProductCatalogService productCatalogService;  // In-process OHS

    public Optional<ProductData> getProductData(ProductId id, int qty) {
        return productCatalogService.getProductInfo(id)
            .map(info -> new ProductData(id, info.price(), info.stock() >= qty));
    }
}

// application/additemtocart/AddItemToCartUseCase.java - Uses port only (unchanged)
@Service
public class AddItemToCartUseCase {
    private final ProductDataPort productDataPort;  // NOT ProductCatalogService or RestTemplate

    public AddItemToCartResult execute(AddItemToCartCommand cmd) {
        ProductData data = productDataPort.getProductData(cmd.productId(), cmd.qty())
            .orElseThrow(() -> new IllegalArgumentException("Product not found"));
        // ...
    }
}
```

**Key Point:** Only the adapter implementation changes when migrating from modulith to microservices. Use cases and ports remain identical.

**Rules:**
- ✅ REST API as an incoming adapter, e.g. `adapter/incoming/api/` (canonical OHS over the network; the sub-package is the project's choice)
- ✅ In-process OHS in the context's published `api/` package (modulith optimization)
- ✅ OHS returns DTOs, never domain objects
- ✅ Consumer defines own output port specifying exactly what it needs
- ✅ Consumer's adapter in `adapter/outgoing/{context}/` is the ONLY place that imports OHS
- ❌ Use cases never import OHS directly (violates hexagonal architecture)
- ❌ Application layer never imports from other bounded contexts

> **Note:** For multi-service integration patterns, see [Deployment Patterns](/guide/deployment-patterns.md)
