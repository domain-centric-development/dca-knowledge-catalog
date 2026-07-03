---
type: Section
title: "Ansatz 1: DomainGateway Pattern"
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

### Konzept

Ein **DomainGateway** ist ein schmales, read-only Interface im Domain Layer, das in der **Ubiquitous Language** formuliert ist. Es erlaubt dem Domain Service, gezielt Daten nachzuladen, ohne die Dependency Rule zu verletzen.

**Wichtige Abgrenzung:**
- Ein DomainGateway ist ein **taktisches DDD-Pattern** — es gehört in den Domain Layer
- Es ist **kein OutputPort** — OutputPorts gehören zum Application Layer (Hexagonal Architecture)
- Es ist **kein Repository** — Repositories verwalten Aggregate Roots mit vollem Lifecycle (CRUD)
- Ein DomainGateway ist **read-only** und liefert nur die Daten, die der Domain Service für seine Berechnung braucht

### Marker-Interface

```java
package de.sample.aiarchitecture.sharedkernel.marker.tactical;

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

**Einordnung im Shared Kernel:**

```
sharedkernel/marker/tactical/
├── DomainService.java
├── DomainGateway.java          ← NEU
├── AggregateRoot.java
├── Entity.java
├── Value.java
└── ...
```

### Naming-Konventionen

| Suffix       | Verwendung                                           | Beispiel                    |
|--------------|------------------------------------------------------|-----------------------------|
| `*Lookup`    | Einfache Datenabfrage (Key → Value)                  | `CategoryPriceLookup`       |
| `*Resolver`  | Auflösung mit Logik (z.B. Fallback, Hierarchie)     | `TaxRateResolver`           |
| `*Provider`  | Bereitstellung von Kontextdaten                      | `ExchangeRateProvider`      |

### Vollständiges Code-Beispiel

**1. DomainGateway Interface (Domain Layer)**

```java
package de.sample.aiarchitecture.pricing.domain.gateway;

import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.sharedkernel.domain.model.ProductId;
import de.sample.aiarchitecture.sharedkernel.marker.tactical.DomainGateway;
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
package de.sample.aiarchitecture.pricing.domain.model;

import de.sample.aiarchitecture.sharedkernel.marker.tactical.Value;

public record CategoryDiscount(String categoryName, int discountPercentage) implements Value {

    public CategoryDiscount {
        if (discountPercentage < 0 || discountPercentage > 100) {
            throw new IllegalArgumentException(
                "Discount percentage must be between 0 and 100");
        }
    }
}
```

**3. Domain Service mit DomainGateway (Domain Layer)**

```java
package de.sample.aiarchitecture.pricing.domain.service;

import de.sample.aiarchitecture.pricing.domain.gateway.CategoryPriceLookup;
import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.sharedkernel.domain.model.Price;
import de.sample.aiarchitecture.sharedkernel.domain.model.ProductId;
import de.sample.aiarchitecture.sharedkernel.marker.tactical.DomainService;

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

**4. Adapter-Implementierung (Adapter Layer)**

```java
package de.sample.aiarchitecture.pricing.adapter.outgoing.categorylookup;

import de.sample.aiarchitecture.pricing.domain.gateway.CategoryPriceLookup;
import de.sample.aiarchitecture.pricing.domain.model.CategoryDiscount;
import de.sample.aiarchitecture.sharedkernel.domain.model.ProductId;
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

**5. Wiring im Use Case (Application Layer)**

```java
package de.sample.aiarchitecture.pricing.application.calculatebundlediscount;

import de.sample.aiarchitecture.pricing.domain.gateway.CategoryPriceLookup;
import de.sample.aiarchitecture.pricing.domain.service.BundleDiscountService;
import de.sample.aiarchitecture.sharedkernel.domain.model.Price;

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

### Datenfluss

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
│      └──▶ Price (berechnet)                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Abgrenzung: DomainGateway vs. Repository

| Aspekt              | Repository                              | DomainGateway                            |
|---------------------|-----------------------------------------|------------------------------------------|
| **Marker**          | `extends OutputPort`                    | `extends DomainGateway`                  |
| **Layer**           | Application Layer (Output Port)         | Domain Layer (taktisches Pattern)        |
| **Verantwortung**   | Aggregate Lifecycle (CRUD)              | Read-only Datenabfrage                   |
| **Scope**           | Ganzes Aggregate Root                   | Schmaler Datenausschnitt                 |
| **Mutationen**      | `save()`, `deleteById()`               | Keine                                    |
| **Benutzt von**     | Use Cases (Application Layer)           | Domain Services (Domain Layer)           |
| **Implementiert von** | Outgoing Adapter                      | Outgoing Adapter                         |

### Vor- und Nachteile

**Vorteile:**
- Domain Service kann eigenständig entscheiden, welche Daten er wann braucht
- Interface ist in Ubiquitous Language formuliert — explizit im Domain Model
- Einfach testbar: Mock des DomainGateway im Unit Test
- Gut geeignet für komplexe Domänenlogik mit bedingten Datenabfragen

**Nachteile:**
- Führt eine Abhängigkeit in den Domain Layer ein (wenn auch abstrakt)
- Kann als "Hintertür" missbraucht werden — Disziplin nötig
- Mehr Klassen: Interface + Implementierung + Marker
- Nicht in allen DDD-Literaturquellen als Pattern etabliert

---

## Related markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainGateway](/marker/tactical/domaingateway.md)
- [DomainService](/marker/tactical/domainservice.md)
