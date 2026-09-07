---
type: Rule
id: DCA-LAY-004
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
enforced_by: "LayeredRules#DCA-LAY-004"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

```java
DcaRule.check(
    "DCA-LAY-004",
    "Transaction boundaries belong to the application layer",
    rationale,
    arch -> {
      String transactional = layout.frameworkAnnotations().transactional();
      List<String> allowedPatterns = new ArrayList<>(List.of(arch.allApplicationPatterns()));
      allowedPatterns.add(
          ".." + layout.adapterSubpackage() + "." + layout.outgoingSubpackage() + "..");
      String[] allowed = allowedPatterns.toArray(String[]::new);
      CollectedViolations violations = CollectedViolations.withoutHeader();
      violations.addAll(
          methods()
              .that()
              .areAnnotatedWith(transactional)
              .should()
              .beDeclaredInClassesThat()
              .resideInAnyPackage(allowed)
              .allowEmptyShould(true),
          arch.classes(),
          rationale);
      violations.addAll(
          classes()
              .that()
              .areAnnotatedWith(transactional)
              .should()
              .resideInAnyPackage(allowed)
              .allowEmptyShould(true),
          arch.classes(),
          rationale);
      violations.throwIfAny();
    })
```
