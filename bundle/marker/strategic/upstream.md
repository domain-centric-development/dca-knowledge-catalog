---
type: Marker
title: "@Upstream"
category: strategic
kind: annotation
signature: "public @interface Upstream"
methods: ["String context()", "Translation translation()", "Consumes[] via()", "String rationale()", "Status status()"]
resource: dca-ecommerce-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/strategic/Upstream.java
tags: [strategic, marker]
---

Declares that this bounded context consumes another bounded context as its upstream.

## Governed by

- [Anti-Corruption Layer: upstream contract types must stay inside the matching adapter](/rule/contextmap/anti-corruption-layer-upstream-contract-types-must-stay-inside-the-matching-adapter.md)
- [Conformist: upstream contract types must never reach the domain layer](/rule/contextmap/conformist-upstream-contract-types-must-never-reach-the-domain-layer.md)
- [Cross-context dependencies on published interfaces require an Upstream declaration](/rule/contextmap/cross-context-dependencies-on-published-interfaces-require-an-upstream-declaration.md)
- [Diagnostic: Display declared context map](/rule/contextmap/diagnostic-display-declared-context-map.md)
- [External system contract types must respect the declared translation and interaction](/rule/contextmap/external-system-contract-types-must-respect-the-declared-translation-and-interaction.md)
- [ExternalUpstream declarations must be well-formed and unique per name and interaction](/rule/contextmap/externalupstream-declarations-must-be-well-formed-and-unique-per-name-and-interaction.md)
- [Implemented Upstream declarations must be backed by an actual code dependency](/rule/contextmap/implemented-upstream-declarations-must-be-backed-by-an-actual-code-dependency.md)
- [Upstream declarations and Spring Modulith allowedDependencies must agree](/rule/contextmap/upstream-declarations-and-spring-modulith-alloweddependencies-must-agree.md)
- [Upstream declarations must be unique per context and channel, and via must not be empty](/rule/contextmap/upstream-declarations-must-be-unique-per-context-and-channel-and-via-must-not-be-empty.md)
- [Upstream declarations must reference an existing bounded context and never the declaring context itself](/rule/contextmap/upstream-declarations-must-reference-an-existing-bounded-context-and-never-the-declaring-context-itself.md)
- [Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)

## Discussed in

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
