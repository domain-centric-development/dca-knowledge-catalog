---
type: Section
title: "Default-Regel: Pure Domain Services (90% der Fälle)"
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

In den meisten Fällen ist die richtige Lösung: **Der Application Service (Use Case) orchestriert.** Er lädt alle benötigten Daten über Output Ports und übergibt sie dem Domain Service als Parameter.

```java
// Application Layer — Use Case orchestriert
public class CalculateBundleDiscountUseCase implements CalculateBundleDiscountInputPort {

    private final ProductPriceRepository productPriceRepository;
    private final BundleDiscountService bundleDiscountService;

    @Override
    public DiscountResult execute(DiscountCommand command) {
        ProductPrice productPrice = productPriceRepository
            .findByProductId(command.productId())
            .orElseThrow();

        // Domain Service erhält alle Daten als Parameter — pure, testbar, einfach
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
// Domain Layer — Pure Domain Service, keine Abhängigkeiten
public final class BundleDiscountService implements DomainService {

    public Price calculateBundleDiscount(Price basePrice, Category category, int bundleSize) {
        int discountPercentage = category.bundleDiscountFor(bundleSize);
        return basePrice.applyDiscount(discountPercentage);
    }
}
```

**Das ist der bevorzugte Ansatz.** Er hält den Domain Service pure und testbar. Erst wenn die Orchestrierung im Use Case zu komplex wird oder die Domänenlogik selbst entscheiden muss, welche Daten sie braucht, kommen die folgenden Alternativen ins Spiel.

---

## Related markers

- [DomainService](/marker/tactical/domainservice.md)
