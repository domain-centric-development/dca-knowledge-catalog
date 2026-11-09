---
type: Rule
id: DCA-USE-021
title: "Use cases should be stateless (only final fields for dependencies)"
rule: "One instance of a use case serves every caller. A field it writes while it runs is shared by the next call and by concurrent ones, and one call's outcome depends on the call before. What a use case holds is set once, by its constructor: the ports and services it is wired with."
constraint: "Use cases should be stateless (only final fields for dependencies)."
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Every instance field - declared or inherited from a superclass - is final. Static fields are not an instance's state and are not inspected; field types are not inspected either, so a final field holding mutable state passes. An empty selection passes."
enforced_by: "UseCaseRules#DCA-USE-021"
status: enforced
maturity: experimental
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases should be stateless (only final fields for dependencies)

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Every instance field - declared or inherited from a superclass - is final. Static fields are not an instance's state and are not inspected; field types are not inspected either, so a final field holding mutable state passes. An empty selection passes.

## .NET reading

**Selection.** Concrete non-nested application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types - the use cases DCA-USE-019 selects, whatever their input.

**Check.** Every instance field - declared by the class or inherited from a base class - is readonly or const, and no auto-property has a setter: its backing field is read like any field, so a get-only or init-only property passes. A parameter of a primary constructor that the class captures is held in a compiler-generated field the language cannot make readonly; it is reported only when a method other than a constructor assigns it. Static fields and the types of the fields are not inspected, so a readonly field holding mutable state passes. An empty selection passes.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** Types that implement an input port (a trait extending UseCase).

**Check.** No method of their impls takes &mut self, and no field holds interior mutability (Cell, RefCell, Mutex, RwLock, an atomic). Planned: the suite does not implement it yet.

## Implementation

```java
DcaRule.of(
        "DCA-USE-021",
        "Use cases should be stateless (only final fields for dependencies)",
        "One instance of a use case serves every caller. A field it writes while it runs is"
            + " shared by the next call and by concurrent ones, and one call's outcome depends"
            + " on the call before. What a use case holds is set once, by its constructor: the"
            + " ports and services it is wired with",
        arch ->
            classes()
                .that(useCases(arch, layout))
                .should(haveOnlyFinalInstanceFields())
                .allowEmptyShould(true))
    .experimental()
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose"
            + " simple name ends with the configured use-case suffix.")
    .checking(
        "Every instance field - declared or inherited from a superclass - is final. Static"
            + " fields are not an instance's state and are not inspected; field types are not"
            + " inspected either, so a final field holding mutable state passes. An empty"
            + " selection passes.",
        "pass what a call needs through the command or keep it in a local; the constructor"
            + " sets only the collaborators")
```

## Helpers

### `useCases`

```java
/**
   * The documented use-case selection: a non-interface class in an application package that either
   * carries the configured use-case suffix or implements the input-port role.
   *
   * <p>Spelled inline, ArchUnit joins {@code and}/{@code or} left to right, so {@code
   * resideInAnyPackage(app).and().haveSimpleNameEndingWith(suffix).or().areAssignableTo(port)
   * .and().areNotInterfaces()} reads {@code ((inApplication ∧ suffix) ∨ isInputPort) ∧ ¬interface}
   * and selects every input-port implementation anywhere, adapters included — which is neither what
   * the rule texts say nor what the .NET twin does.
   */
  private static DescribedPredicate<JavaClass> useCases(DcaArchitecture arch, DcaLayout layout) {
    DescribedPredicate<JavaClass> inApplication = arch.inApplication();
    DescribedPredicate<JavaClass> named =
        JavaClass.Predicates.simpleNameEndingWith(layout.useCaseSuffix());
    DescribedPredicate<JavaClass> port = arch.layout().markers().is("inputPort");
    return inApplication
        .and(named.or(port))
        .and(DescribedPredicate.not(JavaClass.Predicates.INTERFACES))
        .as(
            "non-interface classes in an application package that implement the input port or end"
                + " with \"%s\"",
            layout.useCaseSuffix());
  }
```

### `haveOnlyFinalInstanceFields`

```java
private static ArchCondition<JavaClass> haveOnlyFinalInstanceFields() {
  return new ArchCondition<>("have only final instance fields, inherited ones included") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      for (JavaField field : TypeInspection.instanceFields(item)) {
        if (field.getModifiers().contains(JavaModifier.FINAL)
            || field.getModifiers().contains(JavaModifier.SYNTHETIC)) {
          continue;
        }
        events.add(
            SimpleConditionEvent.violated(
                item,
                item.getName()
                    + " has the non-final field '"
                    + field.getName()
                    + "'"
                    + (field.getOwner().equals(item)
                        ? ""
                        : " inherited from " + field.getOwner().getSimpleName())));
      }
    }
  };
}
```

### `TypeInspection.instanceFields`

```java
/**
   * The instance fields of a class, inherited ones included, sorted by name so that reports are
   * stable across runs. Static fields — constants, counters — are not part of an object's state.
   */
  static List<JavaField> instanceFields(JavaClass type) {
    return type.getAllFields().stream()
        .filter(field -> !field.getModifiers().contains(JavaModifier.STATIC))
        .sorted(Comparator.comparing(JavaField::getName))
        .toList();
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-021",
        "Use cases should be stateless (only final fields for dependencies)",
        "One instance of a use case serves every caller. A field it writes while it runs is shared by the next"
            + " call and by concurrent ones, and one call's outcome depends on the call before. What a use case"
            + " holds is set once, by its constructor: the ports and services it is wired with",
        arch =>
        {
            const BindingFlags instance = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
            return SelectionArchRule.ForEach(
                "operations should hold only fields their constructor sets",
                () => arch.Types.Where(t => OperationPolicy.Operation(t, arch)).OrderBy(t => t.FullName, StringComparer.Ordinal),
                type =>
                {
                    var violations = new List<string>();
                    var runtime = arch.RuntimeType(type)!;
                    for (var current = runtime; current is not null && current != typeof(object); current = current.BaseType)
                    {
                        foreach (var field in current.GetFields(instance).Where(f => !f.IsInitOnly && !f.IsLiteral))
                        {
                            if (CapturedParameter(field) is { } parameter)
                            {
                                if (WrittenOutsideConstructors(current, field))
                                {
                                    violations.Add($"{type.FullName} assigns its constructor parameter '{parameter}' outside the constructor");
                                }

                                continue;
                            }

                            violations.Add(field.Name.StartsWith("<", StringComparison.Ordinal)
                                ? $"{type.FullName} has property '{CapturedName(field.Name)}' with a setter"
                                : $"{type.FullName} has non-readonly field '{field.Name}'");
                        }
                    }

                    return violations;
                });
        })
    .Experimental()
    .Selecting(
        "Concrete non-nested application operations selected by IInputPort marker or configured use-case"
            + " suffix, with loadable runtime types - the use cases DCA-USE-019 selects, whatever their input.")
    .Checking(
        "Every instance field - declared by the class or inherited from a base class - is readonly or const, and"
            + " no auto-property has a setter: its backing field is read like any field, so a get-only or init-only"
            + " property passes. A parameter of a primary constructor that the class captures is held in a"
            + " compiler-generated field the language cannot make readonly; it is reported only when a method other"
            + " than a constructor assigns it. Static fields and the types of the fields are not inspected, so a"
            + " readonly field holding mutable state passes. An empty selection passes.",
        "pass what a call needs through the command or keep it in a local; the constructor sets only the collaborators")
```

### C# helper OperationPolicy

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using ArchUnitNET.Domain;
using ArchUnitNET.Domain.Extensions;
using DomainCentric.BuildingBlocks.Hexagonal.Ports.In;

namespace DomainCentric.ArchRules.Rules;

internal static class OperationPolicy
{
    internal static bool Operation(IType type, DcaArchitecture arch) => type is Class { IsAbstract: false }
        && arch.RuntimeType(type) is { IsNested: false }
        && arch.InApplication(type)
        && (arch.Layout.Markers.Is(nameof(DcaMarkers.InputPort), type) || type.Name.EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal));

    internal static void Invocation(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var caller in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(caller)!;
            var own = runtime.GetInterfaces().SelectMany(t => new[] { t.FullName, t.IsGenericType ? t.GetGenericTypeDefinition().FullName : t.FullName }).ToHashSet();
            for (var parent = runtime; parent is not null; parent = parent.BaseType)
            {
                own.Add(parent.FullName);
            }

            Walk(caller, caller, arch, own, new HashSet<IType>(), new List<string>(), violations);
        }
        DcaRule.Fail("Use cases must not invoke other use cases", violations.Distinct().ToList());
    }

    private static void Walk(IType caller, IType current, DcaArchitecture arch, HashSet<string?> own,
        HashSet<IType> seen, List<string> via, List<string> violations)
    {
        if (!seen.Add(current))
        {
            return;
        }

        foreach (var target in current.Dependencies.Select(d => d.Target).Distinct())
        {
            if (own.Contains(target.FullName))
            {
                continue;
            }

            if (arch.Layout.Markers.Is(nameof(DcaMarkers.InputPort), target) || Operation(target, arch))
            {
                violations.Add($"{caller.FullName} -> {target.FullName}" + (via.Count == 0 ? "" : $" [via {string.Join(" -> ", via)}]"));
            }
            else if (target is not Interface && arch.InApplication(target)
                && arch.ModuleRootOf(caller.Namespace.FullName) == arch.ModuleRootOf(target.Namespace?.FullName ?? ""))
            {
                Walk(caller, target, arch, own, seen, via.Concat(new[] { target.FullName }).ToList(), violations);
            }
        }
    }

    internal static void Surface(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(type)!;
            var methods = runtime.GetInterfaces().Where(i => arch.Layout.Markers.Is(nameof(DcaMarkers.InputPort), i))
                .SelectMany(i => runtime.GetInterfaceMap(i).TargetMethods).ToHashSet();
            foreach (var method in runtime.GetMethods(BindingFlags.Public | BindingFlags.Instance))
            {
                if (method.DeclaringType == typeof(object) || method.DeclaringType == typeof(ValueType)
                    || method.GetBaseDefinition().DeclaringType == typeof(object)
                    || method.IsDefined(typeof(CompilerGeneratedAttribute), false) || methods.Contains(method))
                {
                    continue;
                }
                // Property accessors (auto or computed) are reported once, as their property, below.
                if (method.IsSpecialName && (method.Name.StartsWith("get_", StringComparison.Ordinal) || method.Name.StartsWith("set_", StringComparison.Ordinal)))
                {
                    continue;
                }

                violations.Add($"{type.FullName} exposes {method} outside its input port");
            }
            foreach (var property in runtime.GetProperties(BindingFlags.Public | BindingFlags.Instance))
            {
                foreach (var accessor in property.GetAccessors().Where(a => !methods.Contains(a)))
                {
                    violations.Add($"{type.FullName} exposes property {property.Name} ({accessor.Name}) outside its input port");
                }
            }
        }
        DcaRule.Fail("Use cases expose no public operation outside their input port", violations.Distinct().ToList());
    }
}
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
