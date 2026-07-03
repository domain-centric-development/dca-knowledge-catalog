---
type: Section
title: INTEGRATION PATTERNS
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

### Same Bounded Context
- Direct method calls within aggregate
- Domain events for cross-aggregate communication
- Use case coordinates multiple aggregates
- Eventual consistency between aggregates

### Different Bounded Contexts
- Anti-Corruption Layer for external models
- Open Host Service for synchronous queries
- Domain events via message broker
- REST API with DTOs
- Shared Kernel (minimal, coordinated)

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

For modulith deployments (single JVM), an in-process service avoids network overhead:

```java
// adapter/incoming/openhost/ProductCatalogService.java
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

**Important:** As an incoming adapter, the OHS calls **use cases (input ports)**, not repositories directly.

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
- ✅ REST API in `adapter/incoming/api/` (canonical OHS)
- ✅ In-process OHS in `adapter/incoming/openhost/` (modulith optimization)
- ✅ OHS returns DTOs, never domain objects
- ✅ Consumer defines own output port specifying exactly what it needs
- ✅ Consumer's adapter in `adapter/outgoing/{context}/` is the ONLY place that imports OHS
- ❌ Use cases never import OHS directly (violates hexagonal architecture)
- ❌ Application layer never imports from other bounded contexts

> **Note:** For multi-service integration patterns, see [Deployment Patterns](./deployment-patterns.md)

### Composite Adapter Pattern

When a context needs data from **multiple** Open Host Services, use a **Composite Adapter** to aggregate the data in one place.

```
Context A (Consumer)                    Provider Contexts
┌─────────────────────────────────┐    ┌───────────────────┐
│ application/shared/             │    │ ProductCatalog    │
│   ArticleDataPort               │    │ (OHS - names)     │
│   (output port)                 │    └───────────────────┘
└────────────────┬────────────────┘    ┌───────────────────┐
                 │ implements          │ Pricing           │
                 ▼                     │ (OHS - prices)    │
┌─────────────────────────────────┐    └───────────────────┘
│ adapter/outgoing/product/       │    ┌───────────────────┐
│   CompositeArticleDataAdapter   │───▶│ Inventory         │
│   - ProductCatalogService       │    │ (OHS - stock)     │
│   - PricingService              │    └───────────────────┘
│   - InventoryService            │
└─────────────────────────────────┘
```

**Example:**
```java
// adapter/outgoing/product/CompositeArticleDataAdapter.java
@Component
public class CompositeArticleDataAdapter implements ArticleDataPort {

    private final ProductCatalogService productCatalogService;  // OHS
    private final PricingService pricingService;                // OHS
    private final InventoryService inventoryService;            // OHS

    @Override
    public Map<ProductId, ArticleData> getArticleData(Collection<ProductId> productIds) {
        // Bulk fetch from each OHS
        Map<ProductId, PriceInfo> prices = pricingService.getPrices(productIds);
        Map<ProductId, StockInfo> stocks = inventoryService.getStock(productIds);

        Map<ProductId, ArticleData> result = new HashMap<>();
        for (ProductId productId : productIds) {
            Optional<ProductInfo> productInfo = productCatalogService.getProductInfo(productId);
            if (productInfo.isPresent()) {
                result.put(productId, combineData(productId, productInfo.get(),
                    prices.get(productId), stocks.get(productId)));
            }
        }
        return result;
    }
}
```

**Rules:**
- ✅ Composite adapter is the **ONLY** place that imports from multiple OHS
- ✅ Aggregates data from multiple sources into context-specific DTO
- ✅ Use cases depend on port interface, not the adapter
- ✅ Isolates cross-context coupling to adapter layer
- ❌ Use cases never import OHS directly

### Resolver Pattern

When **domain logic** needs external data (e.g., current prices) without infrastructure dependencies, use a **Resolver** - a functional interface injected into domain methods.

```
Application Layer                      Domain Layer
┌───────────────────────────────┐     ┌─────────────────────────────────┐
│ Use Case                      │     │ Aggregate                       │
│ - fetches data via port       │     │ - calculateTotal(Resolver)      │
│ - builds resolver from data   │────▶│ - validateItems(Resolver)       │
│ - passes resolver to domain   │     │ - confirm(Resolver)             │
└───────────────────────────────┘     └─────────────────────────────────┘
```

**Example:**
```java
// Domain - Functional interface for resolving prices
@FunctionalInterface
public interface ArticlePriceResolver {
    ArticlePrice resolve(ProductId productId);

    record ArticlePrice(Money price, boolean isAvailable, int availableStock) implements Value {}
}

// Domain - Aggregate uses resolver
public class ShoppingCart extends BaseAggregateRoot<ShoppingCart, CartId> {

    public Money calculateTotal(ArticlePriceResolver resolver) {
        Money total = Money.zero();
        for (CartItem item : items) {
            ArticlePrice price = resolver.resolve(item.productId());
            total = total.add(price.price().multiply(item.quantity()));
        }
        return total;
    }

    public CartValidationResult validateForCheckout(ArticlePriceResolver resolver) {
        List<ValidationError> errors = new ArrayList<>();
        for (CartItem item : items) {
            ArticlePrice price = resolver.resolve(item.productId());
            if (!price.isAvailable()) {
                errors.add(ValidationError.productUnavailable(item.productId()));
            }
        }
        return errors.isEmpty() ? CartValidationResult.valid()
                                : CartValidationResult.withErrors(errors);
    }
}

// Application - Use case builds resolver from fetched data
@Service
public class CheckoutCartUseCase implements CheckoutCartInputPort {
    private final ArticleDataPort articleDataPort;  // Output port

    @Override
    public CheckoutCartResult execute(CheckoutCartCommand command) {
        ShoppingCart cart = cartRepository.findById(command.cartId())...;

        // Fetch data via port
        Map<ProductId, ArticleData> articleData =
            articleDataPort.getArticleData(cart.productIds());

        // Build resolver from fetched data
        ArticlePriceResolver resolver = productId -> {
            ArticleData data = articleData.get(productId);
            return new ArticlePrice(data.currentPrice(), data.isAvailable(), data.availableStock());
        };

        // Domain uses resolver - no infrastructure dependency
        CartValidationResult validation = cart.validateForCheckout(resolver);
        if (!validation.isValid()) {
            throw new ValidationException(validation.errors());
        }

        cart.checkout();
        return CheckoutCartResult.success(cart.id());
    }
}
```

**Benefits:**
- ✅ Domain remains **framework-independent** - no external service calls
- ✅ **Fresh data** - resolver provides current prices at execution time
- ✅ **Testable** - easily mock resolver in domain tests
- ✅ **Explicit dependency** - domain method signature shows data need

**Rules:**
- ✅ Resolver is a `@FunctionalInterface` in domain layer
- ✅ Resolver's return type (`ArticlePrice`) is a domain Value Object
- ✅ Use case fetches data via port, builds resolver, passes to domain
- ❌ Domain never calls external services directly
- ❌ Resolver never used to modify external state (read-only)

### Enriched Read Model Pattern

When you need to **combine persisted data with fresh external data** for rich domain logic (e.g., comparing original price to current price), create an **Enriched Read Model**.

```
Persisted Data                Fresh External Data        Enriched Read Model
┌─────────────────┐          ┌─────────────────┐        ┌─────────────────────────┐
│ CheckoutLineItem│    +     │ CheckoutArticle │   =    │ EnrichedCheckoutLineItem│
│ - unitPrice     │          │ - currentPrice  │        │ - hasPriceChanged()     │
│ - quantity      │          │ - isAvailable   │        │ - priceDifference()     │
│ - productName   │          │ - availableStock│        │ - isValidForCheckout()  │
└─────────────────┘          └─────────────────┘        └─────────────────────────┘
```

**Example:**
```java
// Enriched line item - combines persisted with current data
public record EnrichedCheckoutLineItem(
    CheckoutLineItem lineItem,     // Persisted at checkout start
    CheckoutArticle currentArticle  // Fresh from external services
) implements Value {

    public Money currentLineTotal() {
        return currentArticle.currentPrice().multiply(lineItem.quantity());
    }

    public boolean hasPriceChanged() {
        return !lineItem.unitPrice().equals(currentArticle.currentPrice());
    }

    public Money priceDifference() {
        return currentArticle.currentPrice().subtract(lineItem.unitPrice());
    }

    public boolean isValidForCheckout() {
        return currentArticle.isAvailable() &&
               currentArticle.availableStock() >= lineItem.quantity();
    }
}

// Enriched cart - collection with business logic
public record CheckoutCart(
    CartId cartId,
    CustomerId customerId,
    List<EnrichedCheckoutLineItem> items
) implements Value {

    public boolean hasAnyPriceChanges() {
        return items.stream().anyMatch(EnrichedCheckoutLineItem::hasPriceChanged);
    }

    public Money calculateCurrentSubtotal() {
        return items.stream()
            .map(EnrichedCheckoutLineItem::currentLineTotal)
            .reduce(Money::add)
            .orElse(Money.zero());
    }

    public boolean isValidForCheckout() {
        return !items.isEmpty() &&
               items.stream().allMatch(EnrichedCheckoutLineItem::isValidForCheckout);
    }

    public List<EnrichedCheckoutLineItem> invalidItems() {
        return items.stream()
            .filter(item -> !item.isValidForCheckout())
            .toList();
    }
}
```

**Benefits:**
- ✅ **Rich domain logic** - "Has price changed?" "Is stock sufficient?"
- ✅ **Single query point** - all validation/calculation in one place
- ✅ **Immutable** - Value Object, safe to pass around
- ✅ **Real-world metaphor** - like a smart shopping cart display

**Note:** Enriched Read Model is a Value Object, **not** an Aggregate. It has no lifecycle or events.

### Factory for Cross-Context Assembly

Use a **Factory** to assemble enriched domain objects from data fetched via ports.

```java
// Factory assembles enriched cart from multiple data sources
public class CheckoutCartFactory implements Factory {

    public CheckoutCart create(
        CartId cartId,
        CustomerId customerId,
        List<CheckoutLineItem> lineItems,
        Map<ProductId, CheckoutArticle> articleData
    ) {
        List<EnrichedCheckoutLineItem> enrichedItems = lineItems.stream()
            .map(item -> {
                CheckoutArticle article = articleData.get(item.productId());
                if (article == null) {
                    throw new IllegalArgumentException(
                        "Article data not found for: " + item.productId());
                }
                return new EnrichedCheckoutLineItem(item, article);
            })
            .toList();

        return new CheckoutCart(cartId, customerId, enrichedItems);
    }
}

// Use case uses factory
@Service
public class StartCheckoutUseCase implements StartCheckoutInputPort {
    private final CheckoutArticleDataPort articleDataPort;
    private final CheckoutCartFactory checkoutCartFactory;

    @Override
    public StartCheckoutResult execute(StartCheckoutCommand command) {
        // Fetch data via ports
        List<CheckoutLineItem> lineItems = ...;
        Map<ProductId, CheckoutArticle> articleData =
            articleDataPort.getArticleData(productIds);

        // Factory assembles enriched cart
        CheckoutCart checkoutCart = checkoutCartFactory.create(
            cartId, customerId, lineItems, articleData);

        // Domain validation
        if (!checkoutCart.isValidForCheckout()) {
            throw new ValidationException(checkoutCart.invalidItems());
        }

        // ...
    }
}
```

**Rules:**
- ✅ Factory is in **domain layer** (implements `Factory` marker)
- ✅ Factory is **framework-independent** (no Spring annotations)
- ✅ Application layer fetches data via ports, passes to factory
- ✅ Factory validates all required data is present
- ❌ Factory never fetches data itself (no port injection)

## Related markers

- [OutputPort](/marker/port-out/outputport.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
- [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- [Factory](/marker/tactical/factory.md)
