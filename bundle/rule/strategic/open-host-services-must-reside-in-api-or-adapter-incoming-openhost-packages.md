---
type: Rule
id: DCA-STR-005
title: Open Host Services must reside in api or adapter.incoming.openhost packages
rule: "Open Host Services expose context capabilities via api/ packages (published named interface) or adapter.incoming.openhost/ packages."
constraint: Open Host Services must reside in api or adapter.incoming.openhost packages.
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
    "Open Host Services must reside in api or adapter.incoming.openhost packages",
    "Open Host Services expose context capabilities via api/ packages (published named"
        + " interface) or adapter.incoming.openhost/ packages",
    arch ->
        classes()
            .that()
            .areAnnotatedWith(OpenHostService.class)
            .should()
            .resideInAnyPackage("..api..", openHostAdapterPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [@OpenHostService](/marker/strategic/openhostservice.md)
