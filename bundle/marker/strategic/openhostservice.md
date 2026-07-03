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

## Referenced by ADRs

- [ADR-019: Open Host Service Pattern for Cross-Context Communication](/adr/adr-019-open-host-service-pattern.md)

## Discussed in

- [Context Relationships](/book/10-bounded-contexts/context-relationships.md)
- [External Reference Implementation](/book/appendix-b-reference-implementation/external-reference-implementation.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
