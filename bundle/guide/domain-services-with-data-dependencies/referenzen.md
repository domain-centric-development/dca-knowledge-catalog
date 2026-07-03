---
type: Section
title: Referenzen
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

- **PricingService** (pure Domain Service): `ai-architecture-sample/../product/domain/service/PricingService.java`
- **ProductPriceRepository** (Repository als OutputPort): `ai-architecture-sample/../pricing/application/shared/ProductPriceRepository.java`
- **DomainService Marker**: `ai-architecture-sample/../sharedkernel/marker/tactical/DomainService.java`
- **OutputPort Marker**: `ai-architecture-sample/../sharedkernel/marker/port/out/OutputPort.java`
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) — Eric Evans (2003), Chapter 5
- [Implementing Domain-Driven Design](https://www.informit.com/store/implementing-domain-driven-design-9780321834577) — Vaughn Vernon (2013), Chapter 7

## Related markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [DomainService](/marker/tactical/domainservice.md)
