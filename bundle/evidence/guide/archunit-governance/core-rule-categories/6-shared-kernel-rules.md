---
type: Reference
title: Core Rule Categories — 6. Shared Kernel Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#6-shared-kernel-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#6-shared-kernel-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 6. Shared Kernel Rules

Ensure Shared Kernel remains independent and minimal.

```java
// Contexts are discovered, not enumerated. Discovery needs the imported classes, so the
// rule is a method-style test — a static-field rule is built before any classes exist.
@ArchTest
static void shared_kernel_should_not_depend_on_any_context(JavaClasses classes) {
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat(
            resideInAnyPackage(boundedContextPatterns(classes))
                .and(not(resideInAPackage("..sharedkernel.."))))
        .because("Shared Kernel must be independent - no dependencies on bounded contexts")
        .check(classes);
}

// Every bounded context marks its root package once:
//
//   @BoundedContext
//   package com.company.project.order;
//
// The helper turns those markers into ArchUnit package patterns. A context added
// tomorrow is discovered on the next run — nothing to register.
private static String[] boundedContextPatterns(JavaClasses classes) {
    return StreamSupport.stream(classes.spliterator(), false)
        .filter(c -> c.getSimpleName().equals("package-info"))
        .filter(c -> c.isAnnotatedWith(BoundedContext.class))
        .map(c -> c.getPackageName() + "..")
        .distinct()
        .sorted()
        .toArray(String[]::new);
}

@ArchTest
static final ArchRule shared_kernel_should_not_use_frameworks =
    noClasses()
        .that().resideInAPackage("..sharedkernel..")
        .should().dependOnClassesThat()
            .resideInAnyPackage(
                "org.springframework..",
                "jakarta..",
                "javax..",
                "org.hibernate.."
            )
        .because("Shared Kernel must be framework-agnostic");

// Discovered, not enumerated: one rule per context, forbidding every other context.
// A context added tomorrow is covered without being registered here.
@ArchTest
static void bounded_contexts_should_not_depend_on_each_other(JavaClasses classes) {
    var contexts = List.of(boundedContextPatterns(classes));   // the helper defined above
    for (String source : contexts) {
        String[] others = contexts.stream().filter(c -> !c.equals(source)).toArray(String[]::new);
        if (others.length == 0) continue;
        noClasses()
            .that().resideInAPackage(source)
            .should().dependOnClassesThat().resideInAnyPackage(others)
            .allowEmptyShould(true)
            .because("Bounded contexts must not have direct dependencies on each other")
            .check(classes);
    }
}
```

**Three traps worth naming, because each produces a rule that can never fail.**

*Enumerating contexts.* `resideInAPackage("..order..")` versus a hand-written list of the other
three works until somebody adds a fifth context — which is then unguarded, silently. Discover the
contexts instead (a marker annotation on `package-info.java` is enough) and generate one rule per
context. The rule set then grows with the codebase.

*Excluding the shared kernel by pattern.* A shared kernel has its own `domain/` package, so
forbidding `..sharedkernel..` from depending on `..domain..` forbids it from using **its own**
`Money` and `ProductId`. The same cuts the other way: every context's domain must be able to reach
`sharedkernel.domain..`, so a per-context isolation rule must not treat the shared kernel as a
foreign context. Discovery solves this for free — the shared kernel carries a different marker than
a bounded context, so it never lands among the forbidden targets and needs no allow-list.

*Selecting by declaration.* If the isolation rule iterates over the *declared* contexts — the
packages that carry the marker — a module that owns `domain/`, `application/` and `adapter/` but
declares nothing is outside the rule twice over: its imports are never checked, and nobody is
forbidden to import its internals. It passes the whole suite for lack of a subject. Select
**structurally** instead: every package that owns a layer is a module, declared or not, and is both
a source and a forbidden target. What the marker decides is membership of the context map, not
whether the module is isolated. The allow-list is a package convention too — a module's `api/`
(synchronous, in-process) and `events/` (asynchronous) packages are the only part of it a neighbour's
adapter may depend on. Package names, not framework annotations, so the rule holds without any
module system on the class path, and a module that deliberately is *not* a bounded context (one that
borrows a foreign system's language, say) needs no declaration to be governed.

*And use `dependOnClassesThat`, never `accessClassesThat`.* ArchUnit counts an access as a method
call or field access. A field, parameter or record component of a forbidden type is a dependency,
not an access, so an isolation rule written with `accessClassesThat` stays green while a class holds
the forbidden type outright.
