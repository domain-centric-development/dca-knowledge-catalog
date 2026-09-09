---
type: Reference
title: "ELEMENTS — Adapter Layer (Interface Adapters)"
tags: [reference]
evidence_for: "/guide/readme/elements.md#adapter-layer-interface-adapters"
---

[Full node and context](/guide/readme/elements.md#adapter-layer-interface-adapters). This is an evidence excerpt; retain the parent selection and caveats.

### Adapter Layer (Interface Adapters)

#### Input Adapters (Driving/Primary)
- **Controller** - Handles HTTP/framework requests
- **Event Consumer** - Handles external events/messages
- **CLI Handler** - Command-line interface
- **GraphQL Resolver** - GraphQL query/mutation handler
- **Scheduled Job** - Time-triggered operations

#### Output Adapters (Driven/Secondary)
- **Repository Adapter** - Persistence implementation
- **Event Publisher Adapter** - Event publishing implementation
- **External API Client** - Third-party service integration
- **Presenter** - Formats use case output for external world
- **Gateway** - Database/external system translation

#### Adapter Components
- **Mapper** - Translation between layers
- **DTO** - Data transfer across boundaries
- **View Model** - Presentation data structure
- **Database Entity** - ORM/persistence model
- **Integration Event** - DTO representing domain event for cross-context communication
- **Event Mapper** - Converts domain events to/from integration events
- **Anti-Corruption Layer (ACL)** - Protects domain from external event formats
