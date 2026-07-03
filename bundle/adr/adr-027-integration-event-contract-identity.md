---
type: ADR
title: "ADR-027: Integration-Event Contract Identity via @IntegrationEventType"
adr: 27
status: accepted
pattern: "An integration event's contract identity — stable logical name plus schema version — is declared as a class property via the `@IntegrationEventType` annotation, never as instance data. Use cases publish through the new `IntegrationEventPublisher` output port. The outbox store deliberately carries no marker."
resource: ai-architecture-sample/docs/architecture/adr/adr-027-integration-event-contract-identity.md
tags: [adr, events]
---

An integration event's contract identity — stable logical name plus schema version — is declared as a class property via the `@IntegrationEventType` annotation, never as instance data. Use cases publish through the new `IntegrationEventPublisher` output port. The outbox store deliberately carries no marker.

**Consequences:** Positive: · Negative:

## Applies to markers

- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
