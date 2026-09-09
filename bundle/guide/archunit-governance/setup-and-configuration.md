---
type: Section
title: Setup and Configuration
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: dca-guide/archunit-governance.md
tags: [guide, section]
---

The DCA rules ship as a library — `dev.domaincentric:dca-archunit` — pinned to the building blocks
your code implements (`dev.domaincentric:dca-building-blocks`). A project adds one dependency and one
test class; the rule categories below explain what that class checks and serve as templates for the
project-specific rules you add next to it.

### Gradle Dependency

```kotlin
dependencies {
    implementation("dev.domaincentric:dca-building-blocks:0.1.2")
    testImplementation("dev.domaincentric:dca-archunit:0.3.0")     // brings ArchUnit
    testImplementation("org.junit.jupiter:junit-jupiter")
}
```

### Maven Dependency

```xml
<dependency>
    <groupId>dev.domaincentric</groupId>
    <artifactId>dca-archunit</artifactId>
    <version>0.3.0</version>
    <scope>test</scope>
</dependency>
```

### Basic Test Class Structure

```java
package com.company.project;

import dev.domaincentric.dca.archunit.DcaLayout;
import dev.domaincentric.dca.archunit.junit.DcaArchitectureTest;

/**
 * Runs the whole DCA rule catalog against this code base.
 * Every rule appears as one dynamic test, named "[DCA-TAC-001] Aggregate roots must …".
 */
class ArchitectureTest extends DcaArchitectureTest {

    @Override
    protected DcaLayout layout() {
        return DcaLayout.forBasePackage("com.company.project");
    }
}
```

That is the complete test. `DcaLayout` tells the rules where your code lives; its defaults are the
package conventions of this guide (`domain`, `application`, `adapter/incoming`, `adapter/outgoing`,
`infrastructure`, `*UseCase`, `*InputPort`). Deviations are declared, not hidden:

```java
DcaLayout.forBasePackage("com.company.project")
    .withIncomingSubpackage("in")                 // adapter/in instead of adapter/incoming
    .withOutgoingSubpackage("out")
    .withUseCaseSuffix("ApplicationService")
    .withControllerSuffix("Page")
    .allowingInDomain("org.jmolecules..")         // extra third-party packages tolerated in the domain
    .withFrameworkAnnotations(FrameworkAnnotations.jakarta());   // default: spring()
```

The rules never name a framework. Where a rule needs one — the optional stereotype of a use case, the
annotations a domain model must not carry, the transactional annotation, the controller stereotypes,
a module system's declarations — it reads a *role* from `FrameworkAnnotations`: `injectable`,
`webController`, `restController`, `transactional`, `eventListener`, `moduleDeclaration`,
`publishedInterface`, `persistenceEntity`, `injectionSite`, `persistenceMapping`. Each role is a list of fully qualified annotation names.
Presets fill them: `spring()` (the default), `jakarta()` (CDI scopes, JAX-RS, JTA, JPA), `quarkus()`,
`micronaut()`, and `none()` for a hand-wired application. Adjust a single role when your platform
has its own annotation:

```java
DcaLayout.forBasePackage("com.company.project")
    .withFrameworkAnnotations(
        FrameworkAnnotations.jakarta().withRestController("com.company.platform.Endpoint"));
```

A role may hold several annotations because frameworks overlap: the Spring preset accepts Spring's
`@Transactional` and JTA's `jakarta.transaction.Transactional` alike (Spring honours both), the
Micronaut preset its own and JTA's. A rule that requires the role accepts any of them; a rule that
forbids it forbids all of them.

An empty role is not an error: a rule that forbids it has nothing to forbid, a rule that requires it
selects nothing, and the rules about transactions then count only the explicit `TransactionBoundary`.

Usually you name no preset at all: `DcaLayout.forBasePackage` detects the framework on the test class
path and picks the matching preset — Spring when it finds nothing — and the test report names the
choice as its first entry: `framework annotations: quarkus (detected; also jakarta)`, `spring
(default)`, `spring (default; undecided: micronaut, quarkus)` when two frameworks of equal standing are
present and none is chosen, `jakarta (explicit)`. A wrong default is therefore visible instead of silently selecting
nothing. To choose by hand without code, put `dca.framework=micronaut` into `dca-archunit.properties`;
an explicit `withFrameworkAnnotations(...)` in code wins over both. A framework the library does not
know ships its preset in a library of its own — one class implementing
`FrameworkAnnotationsProvider`, one `META-INF/services` line — and is detected, selectable and reported
like a built-in.

Without JUnit — from any test framework or a build step:

```java
DcaArchitecture arch = DcaArchitecture.load(DcaLayout.forBasePackage("com.company.project"));
DcaRules.checkAll(arch);          // throws on the first violated rule; checkAll(arch, selection) to tune
```

Which rules run, and how strictly, is the subject of [Tuning the Rule Catalog](#tuning-the-rule-catalog).

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

### .NET: ArchUnitNET

The same catalog exists for C# — `DomainCentric.ArchRules` on ArchUnitNET, with the xUnit base
class `DomainCentric.ArchRules.Xunit`. Rule ids are identical to the Java library's, so a team, a
review checklist or a knowledge base can speak of `DCA-TAC-001` in either language.

```
dotnet add package DomainCentric.BuildingBlocks            # production projects
dotnet add package DomainCentric.ArchRules.Xunit           # the architecture test project
```

```csharp
using System.Reflection;
using DomainCentric.ArchRules;
using DomainCentric.ArchRules.Xunit;

public sealed class ArchitectureTest : DcaArchitectureTest
{
    protected override DcaLayout Layout => DcaLayout.ForRootNamespace("Company.Project");

    protected override IEnumerable<Assembly> Assemblies =>
        new[] { typeof(Company.Project.Cart.CartContext).Assembly, typeof(Program).Assembly };
}
```

Every rule runs as its own theory case named by id. The rules work on namespaces, so one project
per bounded context is fine — pass all assemblies. Differences worth knowing:

- **Debug builds only.** `DcaArchitecture.Load` refuses optimized assemblies: the compiler emits async
  state machines as structs there, and ArchUnitNET drops them, which would hide every dependency
  that occurs only inside an `async` method. `dotnet test` builds Debug by default.
- **Context declaration** is a marker class in the context's root namespace carrying
  `[BoundedContext]`, not a `package-info`.
- **Framework types by role, too.** `FrameworkTypes.AspNetCore()` is the default (controller base
  class, `[ApiController]`, page-model base, `TransactionScope`); `FrameworkTypes.None()` leaves every
  role empty, a `with` expression adjusts one. .NET has no injectable stereotype, so the **Java rules
  that check only a container stereotype** are listed as *not applicable*; six `DCA-NET`
  rules exist only for .NET (synchronous domain, `Async` suffix on port methods, one `ExecuteAsync`,
  records for values and ids).
- **No baseline dial** (`frozen`): ArchUnitNET has no `FreezingArchRule`; lower such rules to a warning
  instead. The `dca-archunit.properties` keys are otherwise the same.

---

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
