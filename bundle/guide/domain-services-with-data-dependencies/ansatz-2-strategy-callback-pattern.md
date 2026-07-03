---
type: Section
title: "Ansatz 2: Strategy/Callback Pattern"
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### Konzept

Der Domain Service erhält die Datenbeschaffung als **funktionalen Parameter** (Strategy). Der Application Service übergibt ein Lambda oder eine Method Reference, die die Daten liefert. Der Domain Layer definiert kein Interface — die Abhängigkeit existiert nur zur Aufrufzeit.

### Vollständiges Code-Beispiel

**1. Domain Service mit funktionalem Parameter (Domain Layer)**

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

**2. Wiring im Use Case (Application Layer)**

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

### Variante: Eigenes Functional Interface statt `java.util.function.Function`

Wenn die Signatur von `Function<ProductId, Optional<CategoryDiscount>>` zu generisch ist, kann ein eigenes Functional Interface die Lesbarkeit verbessern:

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

Der Domain Service verwendet dann:

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

Der Aufruf im Use Case bleibt identisch — Java's Lambda-Kompatibilität sorgt dafür, dass das Lambda automatisch zum Functional Interface passt.

**Empfehlung:** Verwende ein eigenes Functional Interface wenn:
- Die Methode mehr als einmal verwendet wird
- Die generische Signatur `Function<A, B>` die Lesbarkeit verschlechtert
- Du die Methode dokumentieren willst (Javadoc auf dem Interface)

### Datenfluss

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Application Layer                                                           │
│                                                                             │
│  CalculateBundleDiscountUseCase                                             │
│      │                                                                      │
│      │ ruft auf mit Lambda: productId -> repository.find(...)              │
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
│      │         (Lambda-Callback)          │                                 │
│      │                                    │                                 │
│      │◀── CategoryDiscount ◀──────────────┘                                 │
│      │                                                                      │
│      └──▶ Price (berechnet)                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vor- und Nachteile

**Vorteile:**
- **Zero Abhängigkeiten** im Domain Layer — nicht mal ein abstraktes Interface
- Domain Service bleibt ein echtes Pure Object (stateless, no fields)
- Maximale Testbarkeit: Lambda im Test inline definieren
- Kein zusätzliches Marker-Interface nötig
- Leichtgewichtig — keine zusätzlichen Klassen

**Nachteile:**
- Methodensignatur wird länger und komplexer
- Weniger explizit: `Function<ProductId, Optional<CategoryDiscount>>` ist nicht sofort verständlich
- Callback-Logik kann im Use Case unübersichtlich werden
- Kein Platz für Javadoc am Contract (bei `java.util.function.Function`)
- Bei mehreren Datenquellen: Parameter-Explosion

---

## Related markers

- [DomainService](/marker/tactical/domainservice.md)
