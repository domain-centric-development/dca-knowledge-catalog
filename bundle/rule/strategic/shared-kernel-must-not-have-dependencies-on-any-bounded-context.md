---
type: Rule
id: DCA-STR-002
title: Shared Kernel must not have dependencies on any bounded context
rule: Shared Kernel must be context-independent — it is shared by all contexts and owned by none.
constraint: Shared Kernel must not have dependencies on any bounded context.
enforced_by: "StrategicPatternRules#DCA-STR-002"
status: enforced
rule_set: strategic
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-002",
    "Shared Kernel must not have dependencies on any bounded context",
    "Shared Kernel must be context-independent — it is shared by all contexts and owned by"
        + " none",
    arch ->
        arch.sharedKernelPackage()
            .ifPresent(
                sharedKernel -> {
                  for (Map.Entry<String, BoundedContext> ctx :
                      arch.boundedContexts().entrySet()) {
                    noClasses()
                        .that()
                        .resideInAPackage(sharedKernel + "..")
                        .should()
                        .dependOnClassesThat()
                        .resideInAPackage(ctx.getKey() + "..")
                        .allowEmptyShould(true)
                        .because(
                            "Shared Kernel must not depend on bounded context '"
                                + ctx.getValue().name()
                                + "' ("
                                + ctx.getKey()
                                + ") - Shared Kernel must be context-independent")
                        .check(arch.classes());
                  }
                }))
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
