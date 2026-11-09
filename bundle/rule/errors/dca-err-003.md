---
type: Rule
id: DCA-ERR-003
title: Exceptions declared in the application layer must extend UseCaseException or OutputPortException
rule: "A use case that cannot serve a request reports why through its type, so that one incoming adapter can map each outcome onto its protocol and another adapter can map the same outcome onto a different one; an output port that declares a failure in its contract names it the same way, so the use case can catch exactly that outcome."
constraint: Exceptions declared in the application layer must extend UseCaseException or OutputPortException.
selects: "Classes in <module>.application.. of every module root that are assignable to Throwable and not to DomainException - the exception types the application layer declares itself. The base types live in the building blocks and are not selected. A subtype of DomainException declared in an application package is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type."
checks: "Each extends UseCaseException - a failure an input port declares, raised by the use case - or OutputPortException - a failure an output port declares, raised by its adapter - directly or through an intermediate base class. Extending PortException or InputPortException directly does not count: they classify, they are not extended by a project. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-003"
status: enforced
maturity: released
rule_set: errors
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Exceptions declared in the application layer must extend UseCaseException or OutputPortException

## Selection

Classes in <module>.application.. of every module root that are assignable to Throwable and not to DomainException - the exception types the application layer declares itself. The base types live in the building blocks and are not selected. A subtype of DomainException declared in an application package is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type.

## Check

Each extends UseCaseException - a failure an input port declares, raised by the use case - or OutputPortException - a failure an output port declares, raised by its adapter - directly or through an intermediate base class. Extending PortException or InputPortException directly does not count: they classify, they are not extended by a project. An empty selection passes.

## .NET reading

**Selection.** Types under <Module>.Application of every module root that are assignable to Exception and not to DomainException - the exception types the application layer declares itself. The base types live in the building blocks and are not selected. A subtype of DomainException declared in an application namespace is not selected either: it is misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits it - move the failure to the domain, do not change its base type.

**Check.** Each derives from UseCaseException - a failure an input port declares, raised by the use case - or OutputPortException - a failure an output port declares, raised by its adapter - directly or through an intermediate base class. Deriving from PortException or InputPortException directly does not count: they classify, they are not derived from by a project. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a test, reformulated for Rust (source-test).

**Selection.** Types in every application crate that implement std::error::Error and not DomainFailure.

**Check.** Each implements UseCaseFailure or OutputPortFailure. Implementing only the classification traits PortFailure or InputPortFailure does not count: a type implements the leaf it is.

## Implementation

```java
DcaRule.of(
        "DCA-ERR-003",
        "Exceptions declared in the application layer must extend UseCaseException or"
            + " OutputPortException",
        "A use case that cannot serve a request reports why through its type, so that one"
            + " incoming adapter can map each outcome onto its protocol and another adapter can"
            + " map the same outcome onto a different one; an output port that declares a"
            + " failure in its contract names it the same way, so the use case can catch exactly"
            + " that outcome",
        arch ->
            classes()
                .that(arch.inApplication())
                .and()
                .areAssignableTo(Throwable.class)
                .and(DescribedPredicate.not(arch.layout().markers().is("domainException")))
                .should(
                    LayerConditions.be(
                        arch.layout()
                            .markers()
                            .is("useCaseException")
                            .or(arch.layout().markers().is("outputPortException"))))
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.application.. of every module root that are assignable to Throwable"
            + " and not to DomainException - the exception types the application layer declares"
            + " itself. The base types live in the building blocks and are not selected. A"
            + " subtype of DomainException declared in an application package is"
            + " not selected either: it is misplaced rather than mis-based, and DCA-ERR-002"
            + " owns that case with the remedy that fits it - move the failure to the domain,"
            + " do not change its base type.")
    .checking(
        "Each extends UseCaseException - a failure an input port declares, raised by the use"
            + " case - or OutputPortException - a failure an output port declares, raised by its"
            + " adapter - directly or through an intermediate base class. Extending PortException"
            + " or InputPortException directly does not count: they classify, they are not"
            + " extended by a project. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ERR-003",
    "Exceptions declared in the application layer must extend UseCaseException or OutputPortException",
    "A use case that cannot serve a request reports why through its type, so that one incoming"
        + " adapter can map each outcome onto its protocol and another adapter can map the same"
        + " outcome onto a different one; an output port that declares a failure in its contract names it"
        + " the same way, so the use case can catch exactly that outcome",
    arch => SelectionArchRule.ForEach(
        "exceptions declared in the application layer should extend UseCaseException or OutputPortException",
        // A subtype of DomainException here is misplaced, not mis-based: DCA-ERR-002 owns it and says
        // to move it to the domain. This rule's remedy would turn a broken rule of the model into a
        // use-case failure.
        () => ProjectExceptions(arch)
            .Where(arch.InApplication)
            .Where(t => !arch.Layout.Markers.Is(nameof(DcaMarkers.DomainException), t)),
        t => arch.Layout.Markers.Is(nameof(DcaMarkers.UseCaseException), t) || arch.Layout.Markers.Is(nameof(DcaMarkers.OutputPortException), t)
            ? []
            : [$"{t.FullName} extends neither UseCaseException nor OutputPortException"]))
    .Selecting(
        "Types under <Module>.Application of every module root that are assignable to Exception and "
        + "not to DomainException - the exception types the application layer declares itself. The "
        + "base types live in the building blocks and are not selected. A subtype of "
        + "DomainException declared in an application namespace is not selected either: it is "
        + "misplaced rather than mis-based, and DCA-ERR-002 owns that case with the remedy that fits "
        + "it - move the failure to the domain, do not change its base type.")
    .Checking(
        "Each derives from UseCaseException - a failure an input port declares, raised by the use case - "
        + "or OutputPortException - a failure an output port declares, raised by its adapter - directly "
        + "or through an intermediate base class. Deriving from PortException or InputPortException "
        + "directly does not count: they classify, they are not derived from by a project. An empty "
        + "selection passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [InputPortException](/marker/application/inputportexception.md)
- [OutputPortException](/marker/application/outputportexception.md)
- [PortException](/marker/application/portexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
