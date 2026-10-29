---
type: Reference
title: Setup and Configuration — Adding Project-Specific Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/setup-and-configuration.md#adding-project-specific-rules"
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md#adding-project-specific-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Adding Project-Specific Rules

The library covers the architecture; your project has rules of its own (a forbidden legacy package, a
naming rule for a protocol). Write them with plain ArchUnit next to the catalog test:

```java
package com.company.project;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

@AnalyzeClasses(
    packages = "com.company.project",
    importOptions = {
        ImportOption.DoNotIncludeTests.class,
        ImportOption.DoNotIncludeJars.class
    }
)
public class ProjectRulesTest {

    @ArchTest
    static final ArchRule no_legacy_persistence =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
                .resideInPackage("com.company.legacy..");
}
```

**Key Annotations:**
- `@AnalyzeClasses` - Defines which packages to analyze
- `@ArchTest` - Marks a field or method as an architecture test
- `importOptions` - Excludes tests and external libraries from analysis

The rule categories below are written in this plain form: they show what each `DCA-*` rule
checks and how to express a rule of the same kind yourself.
