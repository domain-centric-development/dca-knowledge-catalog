---
type: Rule
id: DCA-STR-005
title: "Open Host Services must be published: in the api package or as an incoming adapter"
rule: "An Open Host Service is the protocol a context publishes for other contexts - in-process as its api/ package, over the network as an incoming adapter (REST, gRPC, MCP). It belongs at the context boundary, never in the domain or application layer; the adapter's sub-package is irrelevant."
constraint: "Open Host Services must be published: in the api package or as an incoming adapter."
enforced_by: "StrategicPatternRules#DCA-STR-005"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.of(
    "DCA-STR-005",
    "Open Host Services must be published: in the api package or as an incoming adapter",
    "An Open Host Service is the protocol a context publishes for other contexts - in-process"
        + " as its api/ package, over the network as an incoming adapter (REST, gRPC, MCP). It"
        + " belongs at the context boundary, never in the domain or application layer; the"
        + " adapter's sub-package is irrelevant",
    arch ->
        classes()
            .that()
            .areAnnotatedWith(OpenHostService.class)
            .should()
            .resideInAnyPackage(
                ".." + layout.apiSubpackage() + "..",
                ".." + layout.adapterSubpackage() + "." + layout.incomingSubpackage() + "..")
            .allowEmptyShould(true))
```

## Applies to markers

- [@OpenHostService](/marker/strategic/openhostservice.md)
