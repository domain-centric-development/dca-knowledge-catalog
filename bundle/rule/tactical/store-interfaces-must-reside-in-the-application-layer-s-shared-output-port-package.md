---
type: Rule
id: DCA-TAC-019
title: Store interfaces must reside in the application layer's shared output-port package
rule: "Store interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Store interfaces must reside in the application layer's shared output-port package.
enforced_by: "TacticalPatternRules#DCA-TAC-019"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-019",
    "Store interfaces must reside in the application layer's shared output-port package",
    "Store interfaces are output ports in the application layer (Hexagonal Architecture)",
    arch ->
        classes()
            .that()
            .areInterfaces()
            .and()
            .areAssignableTo(Store.class)
            .and()
            .doNotHaveSimpleName(STORE_SUFFIX)
            .should()
            .resideInAPackage(layout.sharedOutputPortPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [Store](/marker/port-out/store.md)
