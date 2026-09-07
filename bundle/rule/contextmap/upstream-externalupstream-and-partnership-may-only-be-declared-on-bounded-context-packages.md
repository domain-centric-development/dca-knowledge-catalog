---
type: Rule
id: DCA-MAP-001
title: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages"
rule: "Context map declarations are reserved for bounded contexts — only a context can be downstream of, or partner with, another."
constraint: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages."
enforced_by: "ContextMapRules#DCA-MAP-001"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-001",
    "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context"
        + " packages",
    "Context map declarations are reserved for bounded contexts — only a context can be"
        + " downstream of, or partner with, another",
    arch -> {
      CollectedViolations violations = CollectedViolations.withoutHeader();
      for (String pkg : arch.packagesBelowBase()) {
        if (arch.packageAnnotation(pkg, BoundedContext.class).isPresent()) {
          continue;
        }
        requireNoDeclaration(violations, arch, pkg, Upstream.class, "@Upstream");
        requireNoDeclaration(
            violations, arch, pkg, ExternalUpstream.class, "@ExternalUpstream");
        requireNoDeclaration(violations, arch, pkg, Partnership.class, "@Partnership");
      }
      violations.throwIfAny();
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
