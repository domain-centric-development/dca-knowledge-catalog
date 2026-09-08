---
type: Rule
id: DCA-STR-005
title: "Open Host Services must be published: in the api package or as an incoming adapter"
rule: "An Open Host Service is the protocol a context publishes for other contexts - in-process as its api/ package, over the network as an incoming adapter (REST, gRPC, MCP). It belongs at the context boundary, never in the domain or application layer; the adapter's sub-package is irrelevant."
constraint: "Open Host Services must be published: in the api package or as an incoming adapter."
selects: "Classes annotated with @OpenHostService anywhere on the classpath under scan, in any module or none."
checks: "Each resides in a package whose path contains the configured api segment (..api..) or the configured incoming-adapter segments (..adapter.incoming..), at any depth and in any sub-package. One annotated in a domain, application or outgoing-adapter package is reported. Which module publishes it, and whether anyone consumes it, is not checked."
enforced_by: "StrategicPatternRules#DCA-STR-005"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

## Selection

Classes annotated with @OpenHostService anywhere on the classpath under scan, in any module or none.

## Check

Each resides in a package whose path contains the configured api segment (..api..) or the configured incoming-adapter segments (..adapter.incoming..), at any depth and in any sub-package. One annotated in a domain, application or outgoing-adapter package is reported. Which module publishes it, and whether anyone consumes it, is not checked.

## .NET reading

**Selection.** Types - classes or interfaces - carrying [OpenHostService] anywhere below the root namespace, in any module or none.

**Check.** Each resides in a namespace whose path contains the configured Api segment or the configured incoming-adapter segments (Adapter.Incoming), at any depth and in any sub-namespace. One attributed in a Domain, Application or outgoing-adapter namespace is reported. Which module publishes it, and whether anyone consumes it, is not checked.

## Implementation

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
                    ".."
                        + layout.adapterSubpackage()
                        + "."
                        + layout.incomingSubpackage()
                        + "..")
                .allowEmptyShould(true))
    .selecting(
        "Classes annotated with @OpenHostService anywhere on the classpath under scan, in any"
            + " module or none.")
    .checking(
        "Each resides in a package whose path contains the configured api segment (..api..) or"
            + " the configured incoming-adapter segments (..adapter.incoming..), at any depth"
            + " and in any sub-package. One annotated in a domain, application or"
            + " outgoing-adapter package is reported. Which module publishes it, and whether"
            + " anyone consumes it, is not checked.")
```

## Applies to markers

- [@OpenHostService](/marker/strategic/openhostservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
