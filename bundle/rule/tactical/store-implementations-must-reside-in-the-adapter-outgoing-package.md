---
type: Rule
id: DCA-TAC-020
title: Store implementations must reside in the adapter.outgoing package
rule: Store implementations are outgoing adapters in bounded contexts.
constraint: Store implementations must reside in the adapter.outgoing package.
enforced_by: "TacticalPatternRules#DCA-TAC-020"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-020",
    "Store implementations must reside in the adapter.outgoing package",
    "Store implementations are outgoing adapters in bounded contexts",
    arch ->
        classes()
            .that()
            .areNotInterfaces()
            .and()
            .areAssignableTo(Store.class)
            .should()
            .resideInAPackage(layout.outgoingAdapterPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [Store](/marker/port-out/store.md)
