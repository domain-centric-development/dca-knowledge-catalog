---
type: Section
title: "Approach 1: DomainGateway Pattern"
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### Concept

A **DomainGateway** is a narrow, read-only interface in the Domain Layer, phrased in the **Ubiquitous Language**. It allows the Domain Service to load specific data on demand without violating the Dependency Rule.

**Important distinctions:**
- A DomainGateway is a **tactical DDD pattern** — it belongs in the Domain Layer
- It is **not an OutputPort** — OutputPorts belong to the Application Layer (Hexagonal Architecture)
- It is **not a Repository** — Repositories manage Aggregate Roots with their full lifecycle (CRUD)
- A DomainGateway is **read-only** and returns only the data the Domain Service needs for its calculation

### Marker Interface

`DomainGateway` is one of the tactical building blocks the `dca-building-blocks` library ships — you
implement it, you do not write it:

```java
package dev.domaincentric.dca.buildingblocks.ddd.tactical;

/**
 * Marker interface for Domain Gateways.
 *
 * <p>A Domain Gateway is a narrow, read-only interface defined in the domain layer
 * that allows Domain Services to retrieve data needed for domain logic.
 * Unlike Repositories (which manage aggregate lifecycle via OutputPort),
 * Domain Gateways are tactical DDD patterns focused purely on data lookup.
 *
 * <p><b>Characteristics:</b>
 * <ul>
 *   <li>Read-only — no mutations, no save/delete operations
 *   <li>Narrow — only the data the domain logic needs, not entire aggregates
 *   <li>Named in Ubiquitous Language — e.g., CategoryPriceLookup, TaxRateResolver
 *   <li>Defined in domain layer, implemented by adapters
 *   <li>Should NOT have Spring annotations in the interface
 * </ul>
 *
 * <p><b>Naming conventions:</b> {@code *Lookup}, {@code *Resolver}, {@code *Provider}
 *
 * @see DomainService
 */
public interface DomainGateway {}
```

**Where it sits among the building blocks:**

```
dev.domaincentric.dca.buildingblocks.ddd.tactical     (the library; .NET: DomainCentric.BuildingBlocks.Ddd.Tactical → IDomainGateway)
├── DomainService
├── DomainGateway               ← this one
├── AggregateRoot
├── Entity
├── Value
└── ...
```

### Naming Conventions

| Suffix       | Usage                                                | Example                     |
|--------------|------------------------------------------------------|-----------------------------|
| `*Lookup`    | Simple data query (key → value)                      | `CategoryPriceLookup`       |
| `*Resolver`  | Resolution with logic (e.g. fallback, hierarchy)     | `TaxRateResolver`           |
| `*Provider`  | Provision of contextual data                         | `ExchangeRateProvider`      |

### Complete Code Example

**1. DomainGateway Interface (Domain Layer)**

```java
package com.company.project.pricing.domain.gateway;

import com.company.project.pricing.domain.model.CategoryDiscount;
import com.company.project.sharedkernel.domain.model.ProductId;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainGateway;
import java.util.Optional;

/**
 * Looks up category-based discount rates for products.
 */
public interface CategoryPriceLookup extends DomainGateway {

    Optional<CategoryDiscount> discountForProduct(ProductId productId);
}
```

**2. Domain Value Object (Domain Layer)**

```java
package com.company.project.pricing.domain.model;

import dev.domaincentric.dca.buildingblocks.ddd.tactical.Value;

public record CategoryDiscount(String categoryName, int discountPercentage) implements Value {

    public CategoryDiscount {
        if (discountPercentage < 0 || discountPercentage > 100) {
            throw new IllegalArgumentException(
                "Discount percentage must be between 0 and 100");
        }
    }
}
```

**3. Domain Service with DomainGateway (Domain Layer)**

```java
package com.company.project.pricing.domain.service;

import com.company.project.pricing.domain.gateway.CategoryPriceLookup;
import com.company.project.pricing.domain.model.CategoryDiscount;
import com.company.project.sharedkernel.domain.model.Price;
import com.company.project.sharedkernel.domain.model.ProductId;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainService;

public final class BundleDiscountService implements DomainService {

    private final CategoryPriceLookup categoryPriceLookup;

    public BundleDiscountService(CategoryPriceLookup categoryPriceLookup) {
        this.categoryPriceLookup = categoryPriceLookup;
    }

    public Price calculateBundleDiscount(ProductId productId, Price basePrice, int bundleSize) {
        int discountPercentage = categoryPriceLookup.discountForProduct(productId)
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

**4. Adapter Implementation (Adapter Layer)**

```java
package com.company.project.pricing.adapter.outgoing.categorylookup;

import com.company.project.pricing.domain.gateway.CategoryPriceLookup;
import com.company.project.pricing.domain.model.CategoryDiscount;
import com.company.project.sharedkernel.domain.model.ProductId;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
class InMemoryCategoryPriceLookup implements CategoryPriceLookup {

    private final Map<ProductId, CategoryDiscount> categoryDiscounts;

    InMemoryCategoryPriceLookup(Map<ProductId, CategoryDiscount> categoryDiscounts) {
        this.categoryDiscounts = categoryDiscounts;
    }

    @Override
    public Optional<CategoryDiscount> discountForProduct(ProductId productId) {
        return Optional.ofNullable(categoryDiscounts.get(productId));
    }
}
```

**5. Wiring in the Use Case (Application Layer)**

```java
package com.company.project.pricing.application.calculatebundlediscount;

import com.company.project.pricing.domain.gateway.CategoryPriceLookup;
import com.company.project.pricing.domain.service.BundleDiscountService;
import com.company.project.sharedkernel.domain.model.Price;

public class CalculateBundleDiscountUseCase implements CalculateBundleDiscountInputPort {

    private final BundleDiscountService bundleDiscountService;

    public CalculateBundleDiscountUseCase(CategoryPriceLookup categoryPriceLookup) {
        this.bundleDiscountService = new BundleDiscountService(categoryPriceLookup);
    }

    @Override
    public DiscountResult execute(DiscountCommand command) {
        Price discountedPrice = bundleDiscountService.calculateBundleDiscount(
            command.productId(),
            command.basePrice(),
            command.bundleSize()
        );
        return new DiscountResult(discountedPrice);
    }
}
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Adapter Layer                                                               │
│                                                                             │
│  InMemoryCategoryPriceLookup ──implements──▶ CategoryPriceLookup (Domain)  │
│                                                                             │
└──────────────────────────────────────────────────┬──────────────────────────┘
                                                   │
┌──────────────────────────────────────────────────┼──────────────────────────┐
│ Application Layer                                │                          │
│                                                  │                          │
│  CalculateBundleDiscountUseCase                  │ injects                  │
│      │                                           │                          │
│      │ creates with gateway ─────────────────────┘                          │
│      ▼                                                                      │
└──────┼──────────────────────────────────────────────────────────────────────┘
       │
┌──────┼──────────────────────────────────────────────────────────────────────┐
│ Domain Layer                                                                │
│      ▼                                                                      │
│  BundleDiscountService                                                      │
│      │                                                                      │
│      │──▶ CategoryPriceLookup.discountForProduct(productId)                │
│      │                          │                                           │
│      │◀── CategoryDiscount ◀────┘                                           │
│      │                                                                      │
│      └──▶ Price (calculated)                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Distinction: DomainGateway vs. Repository

| Aspect              | Repository                              | DomainGateway                            |
|---------------------|-----------------------------------------|------------------------------------------|
| **Marker**          | `extends OutputPort`                    | `extends DomainGateway`                  |
| **Layer**           | Application Layer (Output Port)         | Domain Layer (tactical pattern)          |
| **Responsibility**  | Aggregate lifecycle (CRUD)              | Read-only data query                     |
| **Scope**           | Whole Aggregate Root                    | Narrow slice of data                     |
| **Mutations**       | `save()`, `deleteById()`               | None                                     |
| **Used by**         | Use Cases (Application Layer)           | Domain Services (Domain Layer)           |
| **Implemented by**  | Outgoing Adapter                        | Outgoing Adapter                         |

### Pros and Cons

**Pros:**
- The Domain Service can decide on its own which data it needs and when
- The interface is phrased in the Ubiquitous Language — explicit in the domain model
- Easy to test: mock the DomainGateway in the unit test
- Well suited for complex domain logic with conditional data queries

**Cons:**
- Introduces a dependency into the Domain Layer (albeit an abstract one)
- Can be abused as a "back door" — discipline required
- More classes: interface + implementation + marker
- Not established as a pattern in all DDD literature

---

## Related mentions (heuristic)

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
- [DomainService](/marker/tactical/domainservice.md)
