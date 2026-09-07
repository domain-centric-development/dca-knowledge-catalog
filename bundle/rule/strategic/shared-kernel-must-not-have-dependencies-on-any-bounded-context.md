---
type: Rule
id: DCA-STR-002
title: Shared Kernel must not have dependencies on any bounded context
rule: Shared Kernel must be context-independent — it is shared by all contexts and owned by none.
constraint: Shared Kernel must not have dependencies on any bounded context.
enforced_by: "StrategicPatternRules#DCA-STR-002"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-002",
    "Shared Kernel must not have dependencies on any bounded context",
    "Shared Kernel must be context-independent — it is shared by all contexts and owned by"
        + " none",
    arch -> {
      Optional<String> sharedKernel = arch.sharedKernelPackage();
      if (sharedKernel.isEmpty()) {
        return;
      }
      CollectedViolations violations = CollectedViolations.withoutHeader();
      for (Map.Entry<String, BoundedContext> ctx : arch.boundedContexts().entrySet()) {
        violations.addAll(
            noClasses()
                .that()
                .resideInAPackage(sharedKernel.get() + "..")
                .should()
                .dependOnClassesThat()
                .resideInAPackage(ctx.getKey() + "..")
                .allowEmptyShould(true),
            arch.classes(),
            "Shared Kernel must not depend on bounded context '"
                + ctx.getValue().name()
                + "' ("
                + ctx.getKey()
                + ") - Shared Kernel must be context-independent");
      }
      violations.throwIfAny();
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
