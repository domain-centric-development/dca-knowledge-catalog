---
type: Rule
id: DCA-TAC-014
title: Repository interfaces must reside in the application layer's shared output-port package
rule: "Repository interfaces are output ports in the application layer (Hexagonal Architecture)."
constraint: Repository interfaces must reside in the application layer's shared output-port package.
enforced_by: "TacticalPatternRules#DCA-TAC-014"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-014",
    "Repository interfaces must reside in the application layer's shared output-port package",
    "Repository interfaces are output ports in the application layer (Hexagonal Architecture)",
    arch ->
        // areAssignableTo, not implement: ArchUnit's implement() matches non-interfaces only.
        classes()
            .that()
            .areInterfaces()
            .and()
            .areAssignableTo(Repository.class)
            .and()
            .doNotHaveSimpleName(REPOSITORY_SUFFIX)
            .should()
            .resideInAnyPackage(arch.allSharedOutputPortPatterns())
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
