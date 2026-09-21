---
type: Rule
id: DCA-TAC-009
title: "Value Object classes should be final (immutability)"
rule: "Value objects should be immutable (final classes) - Vernon's DDD recommendation."
constraint: "Value Object classes should be final (immutability)."
selects: "Non-interface, non-record, non-enum classes in <module>.domain.model.. of every module root that are assignable to Value."
checks: "The class carries the final modifier. Records, interfaces and enums are not selected, so a record value object always passes and an enum value object is never reported - an enum with constant-specific class bodies is compiled abstract and cannot be made final. A value object outside <module>.domain.model.. is never reported, and an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-009"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Object classes should be final (immutability)

## Selection

Non-interface, non-record, non-enum classes in <module>.domain.model.. of every module root that are assignable to Value.

## Check

The class carries the final modifier. Records, interfaces and enums are not selected, so a record value object always passes and an enum value object is never reported - an enum with constant-specific class bodies is compiled abstract and cannot be made final. A value object outside <module>.domain.model.. is never reported, and an empty selection passes.

## .NET reading

**Selection.** Classes - record classes included, structs and enums not - in <module>.Domain.Model of every module root that are assignable to IValue; compiler-generated classes excluded.

**Check.** The class is sealed or abstract. A non-sealed record class is reported like a non-sealed class; structs and enums are never selected and so always pass, as does a value object outside <module>.Domain.Model. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-009",
        "Value Object classes should be final (immutability)",
        "Value objects should be immutable (final classes) - Vernon's DDD recommendation",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .and()
                .areAssignableTo(arch.layout().markers().value())
                .and()
                .areNotInterfaces()
                .and()
                .areNotRecords()
                .and()
                .areNotEnums()
                .should()
                .haveModifier(JavaModifier.FINAL)
                .allowEmptyShould(true))
    .selecting(
        "Non-interface, non-record, non-enum classes in <module>.domain.model.. of every "
            + "module root that are assignable to Value.")
    .checking(
        "The class carries the final modifier. Records, interfaces and enums are not "
            + "selected, so a record value object always passes and an enum value object is "
            + "never reported - an enum with constant-specific class bodies is compiled "
            + "abstract and cannot be made final. A value object outside "
            + "<module>.domain.model.. is never reported, and an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-009",
    "Value Object classes should be sealed (immutability)",
    "Value objects should be immutable and not extensible - Vernon's DDD recommendation;"
    + " .NET: a sealed class, a sealed record, or a struct",
    arch =>
    {
        var violations = new List<string>();
        foreach (var valueObject in arch.Classes)
        {
            if (valueObject.IsCompilerGenerated
                || !ResidesInAny(valueObject, arch.AllDomainModelPatterns())
                || !IsAssignableTo(arch, valueObject, arch.Layout.Markers.Value))
            {
                continue;
            }

            if (valueObject.IsSealed != true && valueObject.IsAbstract != true)
            {
                violations.Add($"{valueObject.FullName} is a Value Object {(valueObject.IsRecord == true ? "record" : "class")} that is not sealed");
            }
        }

        DcaRule.Fail("Value Object classes and records must be sealed (or be structs).", violations);
    })
    .Selecting(
        "Classes - record classes included, structs and enums not - in "
        + "<module>.Domain.Model of every module root that are assignable to IValue; "
        + "compiler-generated classes excluded.")
    .Checking(
        "The class is sealed or abstract. A non-sealed record class is reported like "
        + "a non-sealed class; structs and enums are never selected and so always pass, "
        + "as does a value object outside <module>.Domain.Model. An empty selection passes.")
```

## Applies to markers

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
