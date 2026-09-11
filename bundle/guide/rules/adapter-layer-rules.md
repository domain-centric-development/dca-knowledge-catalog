---
type: Section
title: ADAPTER LAYER RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

### Input Adapter Rules
- Input Adapter calls Input Port
- Input Adapter uses no infrastructure — a technical need is declared as an Output Port (`DCA-HEX-004`)
- Controller extracts data from HTTP request
- Controller creates Input Data/DTO
- Controller delegates to use case
- Controller is thin, no business logic
- Controller handles framework-specific concerns
- One controller method per use case (preferred)
- A state-changing use case is reached only by an unsafe HTTP method (`POST`, `PUT`, `DELETE`) — never by `GET`; links do not create sessions, orders or carts. Prefetching, crawlers and cross-site navigation would otherwise trigger the change
- Every browser form that changes state carries a CSRF token; cookie-authenticated endpoints without one are a defect. Token-authenticated APIs (`Authorization: Bearer`) are exempt only if they neither read nor issue cookies

### Output Adapter Rules
- Output Adapter implements Output Port
- Output Adapter may use global and own-module infrastructure, never another module's (`DCA-HEX-005`)
- Repository Adapter implements Repository Interface
- Adapter translates between domain and external world
- Adapter contains framework-specific code
- Adapter handles data transformation
- Adapter protects domain from external changes
- Multiple adapters can implement same port
- Adapters are replaceable

### Presenter Rules
- Presenter implements Output Port (in some variants)
- Presenter formats use case output
- Presenter creates View Models
- Presenter knows about UI needs
- Presenter has no business logic
- Use case doesn't know about presenter implementation

### Mapper Rules
- Mapper translates between domain and persistence
- Mapper translates between domain and DTOs
- Mapper in adapter layer, not domain
- One mapper per aggregate (typical)

### General Adapter Rules
- Adapters depend on ports (interfaces)
- Adapters never depend on other adapters
- Adapters can be tested with integration tests
- Adapters handle technical concerns
- Domain types don't leak to external world
- External types don't leak to domain

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
