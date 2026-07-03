---
type: Section
title: Setup and Configuration
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### Maven Dependency

```xml
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.2.1</version>
    <scope>test</scope>
</dependency>
```

### Gradle Dependency

```gradle
testImplementation 'com.tngtech.archunit:archunit-junit5:1.2.1'
```

### Basic Test Class Structure

```java
package com.company.project.architecture;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

/**
 * Architecture tests for Domain-Centric Architecture.
 *
 * These tests automatically verify architectural rules on every build.
 * Violations will fail the test suite.
 */
@AnalyzeClasses(
    packages = "com.company.project",
    importOptions = {
        ImportOption.DoNotIncludeTests.class,
        ImportOption.DoNotIncludeJars.class
    }
)
public class ArchitectureTest {

    @ArchTest
    static final ArchRule example_rule =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
                .resideInPackage("..infrastructure..");
}
```

**Key Annotations:**
- `@AnalyzeClasses` - Defines which packages to analyze
- `@ArchTest` - Marks a field or method as an architecture test
- `importOptions` - Excludes tests and external libraries from analysis

---
