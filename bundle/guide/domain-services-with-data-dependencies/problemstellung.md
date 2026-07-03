---
type: Section
title: Problemstellung
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

Domain Services sind per Definition **stateless** und gehören zum Domain Layer — dem innersten Ring der Architektur. Sie haben **keine Abhängigkeiten nach außen**. Aber was passiert, wenn ein Domain Service zusätzliche Daten braucht, um seine Berechnung durchzuführen?

**Konkretes Beispiel:** Ein `BundleDiscountService` soll einen Rabatt berechnen, der von der Kategorie des Produkts abhängt. Die Kategorie-Preis-Zuordnung liegt aber nicht im aktuellen Aggregate — sie muss nachgeladen werden.

```java
// Das Problem: Der Domain Service braucht Daten, die er nicht hat
public final class BundleDiscountService implements DomainService {

    public Price calculateBundleDiscount(ProductId productId, Price basePrice) {
        // Woher kommt die Kategorie-Information?
        // Der Domain Layer darf keine Repositories oder Adapter kennen!
        CategoryDiscount discount = ???;
        return applyDiscount(basePrice, discount);
    }
}
```

Die Dependency Rule verbietet es dem Domain Layer, auf den Application Layer oder Adapter zuzugreifen. Trotzdem muss der Domain Service an die Daten kommen.

---

## Related markers

- [DomainService](/marker/tactical/domainservice.md)
