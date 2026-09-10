---
type: Reference
title: Core Rule Categories — 8. Context Map Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#8-context-map-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#8-context-map-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 8. Context Map Rules

Context relationships are declared on each context's `package-info.java` (`@Upstream`,
`@ExternalUpstream`, `@Partnership`). Because the declarations are plain annotations, ArchUnit can
check them against the real dependency graph — the context map becomes *executable*.

```java
@Test
void implemented_upstreams_are_backed_by_code() {
    for (var context : boundedContextPackages()) {
        for (Upstream upstream : packageAnnotations(context, Upstream.class)) {
            if (upstream.status() != Upstream.Status.IMPLEMENTED) continue;   // PLANNED is exempt
            String target = contextPackage(upstream.context());
            classes().that().resideInAPackage(context + "..")
                .should().dependOnClassesThat().resideInAPackage(target + "..")
                .because("Context '" + context + "' declares @Upstream(" + upstream.context()
                    + ") as IMPLEMENTED — a declaration without a dependency is stale; mark it PLANNED or remove it")
                .check(classes);
        }
    }
}

@Test
void cross_context_dependencies_require_a_declaration() {
    for (var context : boundedContextPackages()) {
        Set<String> declared = declaredUpstreamsAndPartners(context);
        for (var other : boundedContextPackages()) {
            if (other.equals(context) || declared.contains(other)) continue;
            noClasses().that().resideInAPackage(context + "..")
                .should().dependOnClassesThat().resideInAPackage(other + "..")
                .because("Context '" + context + "' depends on '" + other
                    + "' without declaring it — add @Upstream(context = ..., translation = ..., via = ...)")
                .check(classes);
        }
    }
}

@Test
void conformist_contract_types_never_reach_the_domain() {
    for (var context : boundedContextPackages()) {
        for (Upstream upstream : packageAnnotations(context, Upstream.class)) {
            if (upstream.translation() != Upstream.Translation.CONFORMIST) continue;
            noClasses().that().resideInAPackage(context + ".domain..")
                .should().dependOnClassesThat().resideInAPackage(contextPackage(upstream.context()) + "..")
                .because("Conformism does not suspend domain purity — the domain layer stays free of upstream types")
                .check(classes);
        }
    }
}
```

The full set (13 rules) also verifies that declarations are well-formed (target exists, never self,
unique per channel), that `@Partnership` is symmetric, that Anti-Corruption-Layer contract types stay
inside the translating adapter, and — when Spring Modulith is used — that `@Upstream` declarations and
`allowedDependencies` agree. A companion test renders `docs/context-map.md` (table + Mermaid) from the
same annotations, so the diagram can never contradict the code.

`packageAnnotations()` reads repeatable annotations from the `package-info` class:

```java
static <T extends Annotation> List<T> packageAnnotations(String packageName, Class<T> type) {
    try {
        return List.of(Class.forName(packageName + ".package-info").getAnnotationsByType(type));
    } catch (ClassNotFoundException e) {
        return List.of();
    }
}
```

---
