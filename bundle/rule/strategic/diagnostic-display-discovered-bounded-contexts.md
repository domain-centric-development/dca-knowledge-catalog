---
type: Rule
id: DCA-STR-001
title: "Diagnostic: Display discovered bounded contexts"
rule: Making the discovered contexts visible shows which packages the strategic rules govern.
constraint: "Diagnostic: Display discovered bounded contexts."
enforced_by: "StrategicPatternRules#DCA-STR-001"
status: informational
rule_set: strategic
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-001",
    "Diagnostic: Display discovered bounded contexts",
    "Making the discovered contexts visible shows which packages the strategic rules govern",
    arch -> {
      System.out.println("=== Discovered Bounded Contexts ===");
      for (Map.Entry<String, BoundedContext> e : arch.boundedContexts().entrySet()) {
        System.out.println("  " + e.getValue().name() + ": " + e.getKey());
        if (!e.getValue().description().isEmpty()) {
          System.out.println("    Description: " + e.getValue().description());
        }
      }
      System.out.println("=== Shared Kernel ===");
      System.out.println("  Package: " + arch.sharedKernelPackage().orElse("<none>"));
      System.out.println("==================================");
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
