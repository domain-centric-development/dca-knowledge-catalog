---
type: Marker
title: "@OpenHostService"
category: strategic
kind: annotation
signature: "public @interface OpenHostService"
methods: ["String context()", "String description()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/strategic/OpenHostService.java
tags: [strategic, marker]
---

Marks a class as an Open Host Service in Domain-Driven Design.

## Governed by

- [Open Host Services must reside in api or adapter.incoming.openhost packages](/rule/strategic/open-host-services-must-reside-in-api-or-adapter-incoming-openhost-packages.md)
- [Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)](/rule/strategic/outgoing-adapters-accessing-other-contexts-must-only-use-openhostservice-classes-except-allowed-acl-patterns.md)

## Discussed in

- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
