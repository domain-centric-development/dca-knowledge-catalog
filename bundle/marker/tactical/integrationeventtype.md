---
type: Marker
title: "@IntegrationEventType"
category: tactical
kind: annotation
signature: "public @interface IntegrationEventType"
methods: ["String name()", "int version()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/tactical/IntegrationEventType.java
tags: [tactical, marker]
---

The mandatory contract identity every IntegrationEvent carries: a stable logical type name plus schema version, decoupled from the Java class name.

## Governed by

- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- [Integration Events must not have a version field](/rule/advanced/integration-events-must-not-have-a-version-field.md)

## Referenced by ADRs

- [ADR-006: Domain Events as Immutable Records](/adr/adr-006-domain-events-immutable-records.md)
- [ADR-027: Integration-Event Contract Identity via @IntegrationEventType](/adr/adr-027-integration-event-contract-identity.md)
