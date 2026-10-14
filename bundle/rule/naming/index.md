# naming

- [Application layer InputPort implementations must end with 'UseCase'](dca-nam-001.md) — InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture).
- [Diagnostic: use cases without injectable stereotypes](dca-nam-002.md) — Use cases may be registered by configuration or annotated; static references cannot prove wiring.
- [InputPort interfaces must end with 'InputPort'](dca-nam-003.md) — Input port interfaces should follow consistent naming conventions (Hexagonal Architecture).
- [Repository Interfaces must end with 'Repository' (name-based discovery)](dca-nam-004.md) — Repository interfaces should follow consistent naming conventions (DDD pattern).
- [Controller classes must end with 'Controller'](dca-nam-005.md) — Classes carrying the web-controller stereotype should follow naming conventions.
- [REST Controllers must end with 'Resource' (REST best practice)](dca-nam-006.md) — Classes carrying the REST-controller stereotype should end with 'Resource' following RESTful naming conventions.
- [DTOs must reside in the adapter layer, not in domain or application](dca-nam-007.md) — DTOs are adapter concerns (presentation or external API) - not in domain or application.
- [Converters must reside in the adapter layer](dca-nam-008.md) — Converters/Mappers translate between layers and should be in adapters.
- [No technical bucket packages - package by domain concept](dca-nam-009.md) — Packages are named after domain concepts from the ubiquitous language, not technical patterns.
- [Domain classes must not use technical suffixes (Helper, Util, Impl, Implementation)](dca-nam-010.md) — Domain names come from the ubiquitous language - name services by their specialty, not by technical role.
- [ViewModels must reside in the configured web adapter package](dca-nam-011.md) — A ViewModel is shaped for the protocol of one incoming adapter and belongs in it. It has no reading in the domain or ...
- [Diagnostic: use cases and input ports named after a trigger rather than an effect](dca-nam-012.md) — A use case is named after its effect, never after its trigger or its caller. When and by whom it runs is the business...
- [Use cases, input ports and published operations must not be named after a field they write](dca-nam-013.md) — An operation speaks the domain, not data access. A name after the field it writes (setLimit, updateStatus) says how t...
