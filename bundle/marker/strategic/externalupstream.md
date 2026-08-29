---
type: Marker
title: "@ExternalUpstream"
category: strategic
kind: annotation
signature: "public @interface ExternalUpstream"
methods: ["String name()", "Upstream.Translation translation()", "Interaction interaction()", "String protocol()", "String exchanges()", "String rationale()", "Upstream.Status status()"]
resource: dca-ecommerce-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/strategic/ExternalUpstream.java
tags: [strategic, marker]
---

Declares that this bounded context consumes an external system — one that lives outside this codebase — as its upstream.

## Governed by

- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [Distinct external system names must not collide after mermaid id normalization](/rule/contextmap/distinct-external-system-names-must-not-collide-after-mermaid-id-normalization.md)
- [External system contract types must respect the declared translation and interaction](/rule/contextmap/external-system-contract-types-must-respect-the-declared-translation-and-interaction.md)
- [ExternalUpstream declarations must be well-formed and unique per name and interaction](/rule/contextmap/externalupstream-declarations-must-be-well-formed-and-unique-per-name-and-interaction.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
