---
type: Reference
title: Setup and Configuration — Basic Test Class Structure
tags: [reference]
evidence_for: "/guide/archunit-governance/setup-and-configuration.md#basic-test-class-structure"
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md#basic-test-class-structure). This is an evidence excerpt; retain the parent selection and caveats.

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
    .withTimestampTypes("com.company.platform.Timestamp")   // what a domain event stores its time in
    .allowingInDomain("org.jmolecules..")         // extra third-party packages tolerated in the domain
    .withFrameworkAnnotations(FrameworkAnnotations.jakarta());   // default: spring()
```

The rules never name a framework. Where a rule needs one — the optional stereotype of a use case, the
annotations a domain model must not carry, the transactional annotation, the controller stereotypes,
a module system's declarations — it reads a *role* from `FrameworkAnnotations`: `injectable`,
`webController`, `restController`, `transactional`, `eventListener`, `moduleDeclaration`,
`publishedInterface`, `persistenceEntity`, `injectionSite`, `persistenceMapping`, `transportStatus`,
and the two the rules match as class dependencies rather than as annotations, `transactionApi` and
`transactionManager`. Each role is a list of fully qualified names.
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

The same idea covers the building blocks themselves. The rules do not name `AggregateRoot`,
`Repository` or `InputPort` as types either — they read a *role* from `DcaMarkers`, resolved by fully
qualified name, and the default vocabulary is the one the building blocks ship. A code base that
already has its own markers, or another library's, keeps them and says so once:

```java
DcaLayout.forBasePackage("com.company.project")
    .withMarkers(
        DcaMarkers.dca()
            .named("company")
            .withAggregateRoot("com.company.platform.ddd.AggregateRoot")
            .withRepository("com.company.platform.ddd.Repository"));
```

It is then governed by the whole catalog, instead of switching off the rules that would have selected
nothing. `withRole("aggregateRoot", "...")` sets a role by name where the code is generated rather
than written. A role names one type and must not be blank: an empty role would select nothing
and report success, which is the failure mode these rules exist to prevent. Selection is by
assignability, so the marker may be an interface or a base class. A code base that marks its building
blocks with annotations instead points the role at the annotation —
`withValue(DcaMarker.ofAnnotation("com.company.platform.ddd.ValueObject"))` — or, while a migration has
both, at either: `DcaMarker.anyOf(DcaMarker.ofType(...), DcaMarker.ofAnnotation(...))`. The annotation
counts on the class and on its supertypes. A package never names a building block: it says where a
type sits, not what it is, and the role refuses it. The test report
names the vocabulary in use — `building block markers: dca (library default)`, or the name and the
roles that differ — so a wrong vocabulary is visible instead of silently selecting nothing.

Three roles name annotations rather than supertypes: `boundedContext` and `sharedKernel` on a
`package-info`, `integrationEventType` on an integration event. A project's own `@BoundedContext(name,
description)` serves like the library's; the rules read its members by name from the compiled class,
so `CLASS` retention is enough, and a member the rules need and the annotation lacks is reported with
package and member. When no package declares a shared kernel, `{base}.sharedkernel` (the configured
sub-package) is taken as one. The relationship annotations (`@Upstream`, `@ExternalUpstream`,
`@Partnership`, `@OpenHostService`) stay the library's: the rules read their nested values.

Commands and queries are roles too. The rules recognise them by name by default — a use case's input
ending in `Command` or `Query` — and a code base that names every input `…Command`, the read-only
ones included, would have its queries reported as commands. It points the roles at what tells them
apart in its code: `DcaMarkers.dca().withCommand(DcaMarker.ofType("com.company.platform.Command"))`, or
an annotation. Renaming the read-only inputs `…Query` is the other way out.

The layers are found the same way. By default a layer is its package below a module root —
`domain`, `application`, `adapter.incoming`, `adapter.outgoing`, `infrastructure`. A code base whose
packages say it differently names the package, or the annotation it already uses for the layer:

```java
DcaLayout.forBasePackage("com.company.project")
    .withOutgoingAdapter(DcaMarker.anyOf(
        DcaMarker.ofPackage("adapter.out"),
        DcaMarker.ofAnnotation("com.company.platform.arch.OutgoingAdapterLayer")));
```

An annotation on a `package-info` holds for the whole package tree below it; one on a single class
places that class, wherever it sits. The annotation wins over the path, and the report lists every
package where it overrides one, and every package that declares another layer than a package above
it — one layer per subtree. In .NET the attribute sits on the type, as an assembly attribute that
names a namespace (it holds for that namespace and the ones below), or on the whole assembly; the
type's own wins, then the named namespace, then the assembly, then the path. The library ships no annotations of its own for layers or roles; it
reads the ones a project has. Which kind fits which: a layer by package or annotation, a building
block by supertype or annotation, a command and a query also by name. `DCA-LAY-007` (experimental)
lists the classes of a module that sit in no layer — a mapper beside the adapter packages, a class
whose layer is declared only on its neighbour — because every rule written for a layer passes over
them.

A few conventions are settings of the layout, so a code base that chose differently says so once
instead of switching rules off:

```java
DcaLayout.forBasePackage("com.company.project")
    .withExcludedPackages("com.company.project.boot")   // a start-up module named like a layer
    .withInputPortSuffix("UseCase")                      // DCA-NAM-003: interfaces named *UseCase
    .withLocalOutputPorts("com.company.project.platform.LocalPort"); // DCA-USE-013: never remote
```

A local output port is one that never leaves the process — a hasher, a clock, a metrics port — so a
use case may call it inside its transaction; selection is by assignability, so one own supertype
covers them all.

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
