---
type: Section
title: Factory for Cross-Context Assembly
chapter: Integration Patterns
source: guide
resource: dca-guide/architecture/integration-patterns.md
tags: [guide, section]
---

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

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)
