---
type: Section
title: "Approach 2: Strategy/Callback Pattern"
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### Concept

The Domain Service receives the data retrieval as a **functional parameter** (Strategy). The Application Service passes a lambda or method reference that supplies the data. The Domain Layer defines no interface — the dependency exists only at call time.

### Complete Code Example

**1. Domain Service with Functional Parameter (Domain Layer)**

```java
package de.sample.aiarchitecture.pricing.domain.service;

import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.sharedkernel.domain.model.Price;
import de.sample.aiarchitecture.sharedkernel.domain.model.ProductId;
import de.sample.aiarchitecture.sharedkernel.marker.tactical.DomainService;
import java.util.Optional;
import java.util.function.Function;

public final class BundleDiscountService implements DomainService {

    public Price calculateBundleDiscount(
            ProductId productId,
            Price basePrice,
            int bundleSize,
            Function<ProductId, Optional<CategoryDiscount>> discountLookup) {

        int discountPercentage = discountLookup.apply(productId)
            .map(CategoryDiscount::discountPercentage)
            .map(base -> base + bonusForBundleSize(bundleSize))
            .orElse(bonusForBundleSize(bundleSize));

        return basePrice.applyDiscount(discountPercentage);
    }

    private int bonusForBundleSize(int bundleSize) {
        if (bundleSize >= 10) return 15;
        if (bundleSize >= 5) return 10;
        if (bundleSize >= 3) return 5;
        return 0;
    }
}
```

**2. Wiring in the Use Case (Application Layer)**

```java
package de.sample.aiarchitecture.pricing.application.calculatebundlediscount;

import de.sample.aiarchitecture.pricing.application.shared.ProductPriceRepository;
import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.pricing.domain.service.BundleDiscountService;
import de.sample.aiarchitecture.sharedkernel.domain.model.Price;

public class CalculateBundleDiscountUseCase implements CalculateBundleDiscountInputPort {

    private final ProductPriceRepository productPriceRepository;
    private final BundleDiscountService bundleDiscountService = new BundleDiscountService();

    public CalculateBundleDiscountUseCase(ProductPriceRepository productPriceRepository) {
        this.productPriceRepository = productPriceRepository;
    }

    @Override
    public DiscountResult execute(DiscountCommand command) {
        Price discountedPrice = bundleDiscountService.calculateBundleDiscount(
            command.productId(),
            command.basePrice(),
            command.bundleSize(),
            productId -> productPriceRepository.findByProductId(productId)
                .map(pp -> new CategoryDiscount(pp.category(), pp.categoryDiscountPercentage()))
        );
        return new DiscountResult(discountedPrice);
    }
}
```

### Variant: Dedicated Functional Interface Instead of `java.util.function.Function`

If the signature `Function<ProductId, Optional<CategoryDiscount>>` is too generic, a dedicated functional interface can improve readability:

```java
package de.sample.aiarchitecture.pricing.domain.service;

import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.sharedkernel.domain.model.ProductId;
import java.util.Optional;

@FunctionalInterface
public interface CategoryDiscountLookup {
    Optional<CategoryDiscount> lookup(ProductId productId);
}
```

The Domain Service then uses:

```java
public Price calculateBundleDiscount(
        ProductId productId,
        Price basePrice,
        int bundleSize,
        CategoryDiscountLookup discountLookup) {

    int discountPercentage = discountLookup.lookup(productId)
        // ...
}
```

The call in the Use Case stays identical — Java's lambda compatibility ensures that the lambda automatically matches the functional interface.

**Recommendation:** Use a dedicated functional interface when:
- The method is used more than once
- The generic signature `Function<A, B>` hurts readability
- You want to document the method (Javadoc on the interface)

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Application Layer                                                           │
│                                                                             │
│  CalculateBundleDiscountUseCase                                             │
│      │                                                                      │
│      │ calls with lambda: productId -> repository.find(...)                │
│      │                                    │                                 │
│      ▼                                    ▼                                 │
└──────┼──────────────────────────────┬─────┼─────────────────────────────────┘
       │                              │     │
┌──────┼──────────────────────────────┼─────┼─────────────────────────────────┐
│ Domain Layer                        │     │                                 │
│      ▼                              │     │                                 │
│  BundleDiscountService              │     │                                 │
│      │                              │     │                                 │
│      │──▶ discountLookup.apply(id) ─┘     │                                 │
│      │         (lambda callback)          │                                 │
│      │                                    │                                 │
│      │◀── CategoryDiscount ◀──────────────┘                                 │
│      │                                                                      │
│      └──▶ Price (calculated)                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pros and Cons

**Pros:**
- **Zero dependencies** in the Domain Layer — not even an abstract interface
- The Domain Service remains a true pure object (stateless, no fields)
- Maximum testability: define the lambda inline in the test
- No additional marker interface needed
- Lightweight — no additional classes

**Cons:**
- The method signature becomes longer and more complex
- Less explicit: `Function<ProductId, Optional<CategoryDiscount>>` is not immediately understandable
- Callback logic can clutter the Use Case
- No place for Javadoc on the contract (with `java.util.function.Function`)
- With several data sources: parameter explosion

---

## Related markers

- [DomainService](/marker/tactical/domainservice.md)
