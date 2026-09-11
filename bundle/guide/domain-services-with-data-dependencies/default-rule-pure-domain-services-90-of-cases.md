---
type: Section
title: "Default Rule: Pure Domain Services (90% of Cases)"
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/topics/domain-services-with-data-dependencies.md
tags: [guide, section]
---

In most cases the right solution is: **the Application Service (Use Case) orchestrates.** It loads all required data through Output Ports and hands it to the Domain Service as parameters.

```java
// Application Layer — the Use Case orchestrates
public class CalculateBundleDiscountUseCase implements CalculateBundleDiscountInputPort {

    private final ProductPriceRepository productPriceRepository;
    private final BundleDiscountService bundleDiscountService;

    @Override
    public DiscountResult execute(DiscountCommand command) {
        ProductPrice productPrice = productPriceRepository
            .findByProductId(command.productId())
            .orElseThrow();

        // The Domain Service receives all data as parameters — pure, testable, simple
        Price discountedPrice = bundleDiscountService.calculateBundleDiscount(
            productPrice.price(),
            productPrice.category(),
            command.bundleSize()
        );

        return new DiscountResult(discountedPrice);
    }
}
```

```java
// Domain Layer — pure Domain Service, no dependencies
public final class BundleDiscountService implements DomainService {

    public Price calculateBundleDiscount(Price basePrice, Category category, int bundleSize) {
        int discountPercentage = category.bundleDiscountFor(bundleSize);
        return basePrice.applyDiscount(discountPercentage);
    }
}
```

**This is the preferred approach.** It keeps the Domain Service pure and testable. Only when the orchestration in the Use Case becomes too complex, or when the domain logic itself has to decide which data it needs, do the following alternatives come into play.

---

## Related mentions (heuristic)

- [DomainService](/marker/tactical/domainservice.md)
