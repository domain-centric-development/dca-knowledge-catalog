---
type: Section
title: Problem Statement
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/domain-services-with-data-dependencies.md
tags: [guide, section]
---

Domain Services are by definition **stateless** and belong to the Domain Layer — the innermost ring of the architecture. They have **no outward dependencies**. But what happens when a Domain Service needs additional data to perform its calculation?

**Concrete example:** A `BundleDiscountService` is supposed to calculate a discount that depends on the product's category. The category-to-price mapping, however, does not live in the current Aggregate — it has to be loaded on demand.

```java
// The problem: the Domain Service needs data it does not have
public final class BundleDiscountService implements DomainService {

    public Price calculateBundleDiscount(ProductId productId, Price basePrice) {
        // Where does the category information come from?
        // The Domain Layer must not know any Repositories or Adapters!
        CategoryDiscount discount = ???;
        return applyDiscount(basePrice, discount);
    }
}
```

The Dependency Rule forbids the Domain Layer to access the Application Layer or Adapters. Yet the Domain Service has to get hold of the data.

---

## Related markers

- [DomainService](/marker/tactical/domainservice.md)
