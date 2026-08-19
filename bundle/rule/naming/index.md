# naming

- [Application layer InputPort implementations must end with 'UseCase'](application-layer-inputport-implementations-must-end-with-usecase.md) — InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture).
- [Controller classes must end with 'Controller'](controller-classes-must-end-with-controller.md) — @Controller annotated classes should follow naming conventions.
- [Converters must reside in the adapter layer](converters-must-reside-in-the-adapter-layer.md) — Converters/Mappers translate between layers and should be in adapters.
- [Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)](domain-classes-must-not-use-technical-suffixes-manager-helper-util-impl.md) — Domain names come from the ubiquitous language - name services by their specialty, not by technical role.
- [DTOs must reside in the adapter layer, not in domain or application](dtos-must-reside-in-the-adapter-layer-not-in-domain-or-application.md) — DTOs are adapter concerns (presentation or external API) - not in domain or application.
- [InputPort interfaces must end with 'InputPort'](inputport-interfaces-must-end-with-inputport.md) — Input port interfaces should follow consistent naming conventions (Hexagonal Architecture).
- [No technical bucket packages - package by domain concept](no-technical-bucket-packages-package-by-domain-concept.md) — Packages are named after domain concepts from the ubiquitous language, not technical patterns.
- [Repository Interfaces must end with 'Repository'](repository-interfaces-must-end-with-repository.md) — Repository interfaces should follow consistent naming conventions (DDD pattern).
- [REST Controllers must end with 'Resource' (REST best practice)](rest-controllers-must-end-with-resource-rest-best-practice.md) — @RestController annotated classes should end with 'Resource' following RESTful naming conventions.
- [Use case classes must be annotated with @Service](use-case-classes-must-be-annotated-with-service.md) — Use case classes must be Spring-managed beans.
- [ViewModels must reside in adapter.incoming.web packages](viewmodels-must-reside-in-adapter-incoming-web-packages.md) — ViewModels are presentation concerns and must reside in incoming web adapter packages.
