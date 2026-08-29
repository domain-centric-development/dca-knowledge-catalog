---
type: Marker
title: "@IntegrationEventType"
category: tactical
kind: annotation
signature: "public @interface IntegrationEventType"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
methods: ["String name()", "int version()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/IntegrationEventType.java
tags: [tactical, marker]
---

The mandatory contract identity every IntegrationEvent carries: a stable logical type name plus schema version, decoupled from the Java class name.

## Governed by

- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- [Integration Events must not have a version field](/rule/advanced/integration-events-must-not-have-a-version-field.md)
