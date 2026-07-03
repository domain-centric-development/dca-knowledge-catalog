---
type: Section
title: Complete Test Suites
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### Suite 1: Layer Dependency Test

```java
package com.company.project.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.library.Architectures.layeredArchitecture;

/**
 * Verifies layer dependency rules for Domain-Centric Architecture.
 */
@AnalyzeClasses(packages = "com.company.project", importOptions = ImportOption.DoNotIncludeTests.class)
public class LayerDependencyTest {

    @ArchTest
    static final ArchRule layered_architecture_is_respected =
        layeredArchitecture()
            .consideringAllDependencies()

            .layer("Domain").definedBy("..domain..")
            .layer("Application").definedBy("..application..")
            .layer("Adapter").definedBy("..adapter..")
            .layer("Infrastructure").definedBy("..infrastructure..")
            .layer("SharedKernel").definedBy("..sharedkernel..")

            .whereLayer("Domain").mayOnlyAccessLayers("SharedKernel")
            .whereLayer("Application").mayOnlyAccessLayers("Domain", "SharedKernel")
            .whereLayer("Adapter").mayOnlyAccessLayers("Application", "Domain", "SharedKernel")
            .whereLayer("Infrastructure").mayAccessAnyLayer()
            .whereLayer("SharedKernel").mayNotAccessAnyLayer()

            .because("Dependencies must follow Domain-Centric Architecture rules");
}
```

### Suite 2: Framework Independence Test

```java
package com.company.project.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

/**
 * Ensures domain and application remain framework-independent.
 */
@AnalyzeClasses(packages = "com.company.project", importOptions = ImportOption.DoNotIncludeTests.class)
public class FrameworkIndependenceTest {

    @ArchTest
    static final ArchRule domain_is_framework_independent =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
                .resideInAnyPackage(
                    "org.springframework..",
                    "jakarta..",
                    "javax..",
                    "org.hibernate.."
                );

    @ArchTest
    static final ArchRule domain_does_not_use_jpa =
        noMethods()
            .that().areDeclaredInClassesThat().resideInAPackage("..domain..")
            .should().beAnnotatedWith("jakarta.persistence.Entity")
            .orShould().beAnnotatedWith("jakarta.persistence.Id");

    @ArchTest
    static final ArchRule shared_kernel_is_framework_independent =
        noClasses()
            .that().resideInAPackage("..sharedkernel..")
            .should().dependOnClassesThat()
                .resideInAnyPackage("org.springframework..", "jakarta..", "javax..");
}
```

### Suite 3: DDD Pattern Test

```java
package com.company.project.architecture;

import com.company.project.sharedkernel.domain.marker.*;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

/**
 * Verifies DDD tactical patterns are correctly implemented.
 */
@AnalyzeClasses(packages = "com.company.project", importOptions = ImportOption.DoNotIncludeTests.class)
public class DddPatternTest {

    @ArchTest
    static final ArchRule value_objects_are_immutable =
        classes()
            .that().implement(Value.class)
            .should().haveOnlyFinalFields()
            .because("Value Objects must be immutable");

    @ArchTest
    static final ArchRule domain_events_are_immutable =
        classes()
            .that().implement(DomainEvent.class)
            .should().haveOnlyFinalFields()
            .because("Domain Events represent past facts and must be immutable");

    @ArchTest
    static final ArchRule entities_have_identity =
        classes()
            .that().implement(Entity.class)
            .should().haveMethod("getId")
            .because("Entities must have identity");

    @ArchTest
    static final ArchRule aggregates_are_in_domain_model =
        classes()
            .that().implement(AggregateRoot.class)
            .should().resideInAPackage("..domain.model..")
            .because("Aggregates belong in the domain model");
}
```

### Suite 4: Naming Convention Test

```java
package com.company.project.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

/**
 * Enforces naming conventions across the codebase.
 */
@AnalyzeClasses(packages = "com.company.project", importOptions = ImportOption.DoNotIncludeTests.class)
public class NamingConventionTest {

    @ArchTest
    static final ArchRule input_ports_follow_naming =
        classes()
            .that().areInterfaces()
            .and().resideInAPackage("..application..")
            .and().haveSimpleNameEndingWith("InputPort")
            .should().bePublic()
            .because("Input ports should be public interfaces");

    @ArchTest
    static final ArchRule repositories_follow_naming =
        classes()
            .that().areInterfaces()
            .and().haveSimpleNameEndingWith("Repository")
            .should().resideInAPackage("..application..")
            .because("Repository interfaces belong in application layer");

    @ArchTest
    static final ArchRule use_cases_follow_naming =
        classes()
            .that().areNotInterfaces()
            .and().haveSimpleNameEndingWith("UseCase")
            .should().resideInAPackage("..application..")
            .because("Use cases belong in application layer");
}
```

---

## Related markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Value](/marker/tactical/value.md)
