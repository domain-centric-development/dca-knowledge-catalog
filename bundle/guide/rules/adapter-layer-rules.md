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
- Input Adapter uses no infrastructure (`DCA-HEX-004`) — a capability the use case needs is declared as an Output Port there; the adapter may use the identity port to resolve the caller; its own mechanics stay inside the adapter
- Controller extracts data from HTTP request
- Controller creates Input Data/DTO
- The adapter turns raw input into the types the input port takes: an id arrives in the command as the id's
  value type, parsed at the edge (or by the value type's own factory), never as text the use case parses. Text
  that does not parse is a malformed call the adapter answers itself; the use case never sees it
- Controller delegates to use case
- Controller is thin, no business logic
- Controller handles framework-specific concerns
- One controller method per use case (preferred)
- A state-changing use case is reached only by an unsafe HTTP method (`POST`, `PUT`, `DELETE`) — never by `GET`; links do not create sessions, orders or carts. Prefetching, crawlers and cross-site navigation would otherwise trigger the change
- State a later request needs travels with that request or lives in a store every instance reads. A message
  for the page after a redirect is a fixed code in the redirect URL (`?notice=saved`), never the sentence: the
  page maps the code through an enum of the incoming adapter (code and text per value) and ignores a code it does
  not know. A server session, a flash attribute (Spring MVC) or `TempData` (ASP.NET Core, without a
  data-protection key ring the instances share) is held by one instance, and behind a load balancer without
  sticky sessions the next request reaches another one
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
- A value an adapter publishes from an enum is spelled explicitly — a code per value on the enum or a mapping in
  the adapter — never derived from the member's name (`name()`, `toString()`, `ToString()`): renaming a member
  is a refactoring inside the code and must not change what a client reads or what a store holds
- External types don't leak to domain

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
