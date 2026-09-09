---
type: Rule
id: DCA-ADV-016
title: "Factories should be stateless (only final fields for dependencies)"
rule: "Factories should be stateless (only final fields for dependencies)."
constraint: "Factories should be stateless (only final fields for dependencies)."
selects: "Non-interface classes in <module>.domain.. of every module root that are assignable to Factory."
checks: "Every field - declared or inherited from a superclass, static fields included - is final. Field types are not inspected. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-016"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Factories should be stateless (only final fields for dependencies)

## Selection

Non-interface classes in <module>.domain.. of every module root that are assignable to Factory.

## Check

Every field - declared or inherited from a superclass, static fields included - is final. Field types are not inspected. An empty selection passes.

## .NET reading

**Selection.** Non-interface types in <module>.Domain of every module root that are assignable to IFactory.

**Check.** Every field - declared by the type or inherited from a base type, static fields included - is readonly or const. A settable auto-property is reported through its backing field. Field types are not inspected. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-016",
        "Factories should be stateless (only final fields for dependencies)",
        "Factories should be stateless (only final fields for dependencies)",
        arch ->
            classes()
                .that()
                .implement(Factory.class)
                .and()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should(haveOnlyFinalFieldsIncludingInherited())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.. of every module root that are assignable to"
            + " Factory.")
    .checking(
        "Every field - declared or inherited from a superclass, static fields included - is final."
            + " Field types are not inspected. An empty selection passes.")
```

## Helpers

### `haveOnlyFinalFieldsIncludingInherited`

```java
/**
   * Like ArchUnit's {@code haveOnlyFinalFields()}, but over {@code getAllFields()}: a mutable field
   * a domain service or factory inherits from a base class is state all the same.
   */
  private static ArchCondition<JavaClass> haveOnlyFinalFieldsIncludingInherited() {
    return new ArchCondition<>("have only final fields, inherited ones included") {
      @Override
      public void check(JavaClass item, ConditionEvents events) {
        item.getAllFields().stream()
            .filter(f -> !f.getModifiers().contains(JavaModifier.FINAL))
            .filter(f -> !f.getOwner().isEquivalentTo(Object.class))
            .forEach(
                f ->
                    events.add(
                        SimpleConditionEvent.violated(
                            item,
                            item.getSimpleName()
                                + " has non-final field '"
                                + f.getName()
                                + "'"
                                + (f.getOwner().equals(item)
                                    ? ""
                                    : " inherited from " + f.getOwner().getSimpleName()))));
      }
    };
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-016",
    "Factories should be stateless (only readonly fields for dependencies)",
    "Factories should be stateless (only readonly fields for dependencies)",
    arch => DcaRule.Fail(
        "Factories must have only readonly fields:",
        NonReadonlyFieldViolations(
            arch,
            t => t is not Interface && InDomain(arch, t) && t.IsAssignableTo(typeof(IFactory).FullName!))))
    .Selecting(
        "Non-interface types in <module>.Domain of every module root that are assignable to "
        + "IFactory.")
    .Checking(
        "Every field - declared by the type or inherited from a base type, static fields included "
        + "- is readonly or const. A settable auto-property is reported through its backing field. "
        + "Field types are not inspected. An empty selection passes.")
```

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
