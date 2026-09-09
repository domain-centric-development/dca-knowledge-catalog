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
- [ViewModels must reside in adapter.incoming.web packages](dca-nam-011.md) — ViewModels are presentation concerns and must reside in incoming web adapter packages.
