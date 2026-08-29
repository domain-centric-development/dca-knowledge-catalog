---
type: Marker
title: "@Partnership"
category: strategic
kind: annotation
signature: "public @interface Partnership"
methods: ["String context()", "String rationale()"]
resource: dca-ecommerce-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/strategic/Partnership.java
tags: [strategic, marker]
---

Declares a Partnership between two bounded contexts: both teams coordinate the evolution of a shared contract and succeed or fail together on it.

## Governed by

- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric](/rule/contextmap/partnership-declarations-must-reference-an-existing-bounded-context-never-themselves-and-must-be-symmetric.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
