---
type: Rule
id: DCA-LAY-004
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
enforced_by: "LayeredRules#DCA-LAY-004"
status: enforced
rule_set: layered
implementations: [java]
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
      String[] allowed = {
        layout.applicationPattern(),
        ".." + layout.adapterSubpackage() + "." + layout.outgoingSubpackage() + ".."
      };
      methods()
          .that()
          .areAnnotatedWith(transactional)
          .should()
          .beDeclaredInClassesThat()
          .resideInAnyPackage(allowed)
          .because(rationale)
          .allowEmptyShould(true)
          .check(arch.classes());
      classes()
          .that()
          .areAnnotatedWith(transactional)
          .should()
          .resideInAnyPackage(allowed)
          .because(rationale)
          .allowEmptyShould(true)
          .check(arch.classes());
    })
```
