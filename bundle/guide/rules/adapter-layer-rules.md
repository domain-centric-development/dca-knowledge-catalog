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
- Where the application runs as several instances behind a load balancer without sticky sessions, state a later
  request needs travels with that request or lives in a store every instance reads. A server session is held by
  one instance, and the next request reaches another one. Whether the application runs that way is the
  project's operational decision; a single instance or sticky sessions keep the server session usable
- In such an application a message for the page after a redirect travels in a cookie that is encrypted and
  signed. The cookie is addressed to one page: only that page reads it, reading removes it, and a message for
  another page waits until that page is shown or expires after a few minutes. It holds the code from the page's enum of the
  incoming adapter (code and text per value) and a number where the sentence names one — never the sentence. The
  page maps the code and ignores a code it does not know. The key comes from configuration and every instance
  shares it; a key generated per process makes the cookie unreadable on the next instance. A flash attribute
  (Spring MVC) is kept in the server session by default and needs a flash-map manager that writes this cookie;
  `TempData` (ASP.NET Core) is such a cookie by default and needs a data-protection key ring the instances share
- Where no cookie may be set, the code travels in the redirect address (`?notice=saved`). The address is
  forgeable — a crafted link shows any notice and any number — and every redirect on the way must forward it
- A page adapter translates a refusal in one place: one method of the adapter turns the refusal and its notice
  code into the redirect, and every handler that can meet the refusal calls it — never the same `catch` in each
  handler. A handler repeats only the use-case call; what a refusal looks like to the user is decided once
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
