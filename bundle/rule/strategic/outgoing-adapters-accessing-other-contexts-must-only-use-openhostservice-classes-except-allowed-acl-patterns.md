---
type: Rule
id: DCA-STR-006
title: "Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)"
rule: "Cross-context communication goes through the published api/ and events/ packages, never through another context's domain or application layer."
constraint: "Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)."
enforced_by: "StrategicPatternRules#DCA-STR-006"
status: enforced
rule_set: strategic
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-006",
    "Outgoing adapters accessing other contexts must only use OpenHostService classes (except"
        + " allowed ACL patterns)",
    "Cross-context communication goes through the published api/ and events/ packages, never"
        + " through another context's domain or application layer",
    arch -> {
      Map<String, BoundedContext> contexts = arch.boundedContexts();
      for (Map.Entry<String, BoundedContext> source : contexts.entrySet()) {
        for (Map.Entry<String, BoundedContext> target : contexts.entrySet()) {
          if (target.getKey().equals(source.getKey())) {
            continue;
          }
          noClasses()
              .that()
              .resideInAPackage(layout.outgoingAdapterPattern(source.getKey()))
              .should()
              .dependOnClassesThat()
              .resideInAPackage(layout.domainPattern(target.getKey()))
              .allowEmptyShould(true)
              .because(
                  "Outgoing adapters in '"
                      + source.getValue().name()
                      + "' must not access domain layer of '"
                      + target.getValue().name()
                      + "' - use api/ or events/ packages instead")
              .check(arch.classes());
          noClasses()
              .that()
              .resideInAPackage(layout.outgoingAdapterPattern(source.getKey()))
              .should()
              .dependOnClassesThat()
              .resideInAPackage(layout.applicationPattern(target.getKey()))
              .allowEmptyShould(true)
              .because(
                  "Outgoing adapters in '"
                      + source.getValue().name()
                      + "' must not access application layer of '"
                      + target.getValue().name()
                      + "' - use api/ or events/ packages instead")
              .check(arch.classes());
        }
      }
    })
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
