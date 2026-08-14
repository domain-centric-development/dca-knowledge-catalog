---
type: Marker
title: IdentityProvider
category: port-out
kind: interface
signature: public interface IdentityProvider extends OutputPort
extends: [OutputPort]
methods: ["Identity getCurrentIdentity()", "UserId userId()", "IdentityType type()", "Optional<String> email()", "Set<String> roles()", "String name()", "boolean isAnonymous()", "boolean isRegistered()"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/IdentityProvider.java
tags: [port-out, marker]
---

Port for retrieving the current user's identity.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Discussed in

- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
