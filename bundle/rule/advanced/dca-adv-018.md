---
type: Rule
id: DCA-ADV-018
title: Specifications must not carry prohibited framework metadata
rule: "Domain objects carry no metadata for container management, persistence or transaction coordination."
constraint: Specifications must not carry prohibited framework metadata.
selects: "Non-interface types in domain packages that are assignable to the configured specification role or whose simple name ends with Specification. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types."
checks: "Direct or meta-annotations: types prohibit injectable, persistenceEntity and transactional roles; fields prohibit injectionSite and persistenceMapping; methods prohibit transactional and eventListener, plus injectionSite except on events; constructors prohibit injectionSite. Unclassified annotations are allowed by this check. Empty configured roles select no metadata; wiring is not established."
enforced_by: "AdvancedPatternRules#DCA-ADV-018"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Specifications must not carry prohibited framework metadata

## Selection

Non-interface types in domain packages that are assignable to the configured specification role or whose simple name ends with Specification. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types.

## Check

Direct or meta-annotations: types prohibit injectable, persistenceEntity and transactional roles; fields prohibit injectionSite and persistenceMapping; methods prohibit transactional and eventListener, plus injectionSite except on events; constructors prohibit injectionSite. Unclassified annotations are allowed by this check. Empty configured roles select no metadata; wiring is not established.

## .NET reading

**Selection.** Non-interface types in domain namespaces that are assignable to the configured specification role or whose simple name ends with Specification. Exclusive ownership: events, services, factories, specifications, then domain-model types.

**Check.** Configured attribute namespaces classify the attribute type or any base type: types prohibit container, persistence and transaction roles; fields and properties prohibit injection and persistence; methods prohibit transaction and, except on events, injection; constructors prohibit injection. There is no default event-listener attribute role. Unclassified attributes are allowed; runtime types that cannot load are skipped.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-018",
        "Specifications must not carry prohibited framework metadata",
        "Domain objects carry no metadata for container management, persistence or transaction coordination",
        arch -> DomainMetadata.check(arch, "DCA-ADV-018"))
    .selecting(
        "Non-interface types in domain packages that are assignable to the configured specification role or whose simple name ends with Specification. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types.")
    .checking(
        "Direct or meta-annotations: types prohibit injectable, persistenceEntity and transactional roles; fields prohibit injectionSite and persistenceMapping; methods prohibit transactional and eventListener, plus injectionSite except on events; constructors prohibit injectionSite. Unclassified annotations are allowed by this check. Empty configured roles select no metadata; wiring is not established.")
```

## Helpers

### `DomainMetadata.check`

```java
static void check(DcaArchitecture arch, String id) {
  FrameworkAnnotations roles = arch.layout().frameworkAnnotations();
  List<String> violations = new ArrayList<>();
  for (JavaClass type : arch.classes()) {
    if (type.isInterface()
        || !owner(type, arch.layout().markers(), arch.layout().specificationSuffix()).equals(id)
        || !JavaClass.Predicates.resideInAnyPackage(arch.allDomainPatterns()).test(type))
      continue;
    if (id.equals("DCA-ONI-003")
        && !JavaClass.Predicates.resideInAnyPackage(arch.allDomainModelPatterns()).test(type))
      continue;
    inspect(
        type,
        type.getName(),
        violations,
        roles.injectable(),
        roles.persistenceEntity(),
        roles.transactional());
    type.getFields()
        .forEach(
            field ->
                inspect(
                    field,
                    field.getFullName(),
                    violations,
                    roles.injectionSite(),
                    roles.persistenceMapping()));
    type.getMethods()
        .forEach(
            method ->
                inspect(
                    method,
                    method.getFullName(),
                    violations,
                    roles.transactional(),
                    roles.eventListener(),
                    id.equals("DCA-ADV-004") ? List.of() : roles.injectionSite()));
    type.getConstructors()
        .forEach(ctor -> inspect(ctor, ctor.getFullName(), violations, roles.injectionSite()));
  }
  if (!violations.isEmpty())
    throw new dev.domaincentric.dca.archunit.DcaRuleViolation(
        id + ": prohibited domain metadata", violations);
}
```

### `DomainMetadata.owner`

```java
static String owner(JavaClass type, DcaMarkers markers, String specificationSuffix) {
  if (type.isAssignableTo(markers.domainEvent())) return "DCA-ADV-004";
  if (type.isAssignableTo(markers.domainService())) return "DCA-ADV-011";
  if (type.isAssignableTo(markers.factory())) return "DCA-ADV-015";
  if (type.isAssignableTo(markers.specification())
      || type.getSimpleName().endsWith(specificationSuffix)) return "DCA-ADV-018";
  return "DCA-ONI-003";
}
```

### `DomainMetadata.inspect`

```java
private static void inspect(
    CanBeAnnotated target, String name, List<String> violations, List<String>... roles) {
  for (List<String> role : roles)
    for (String annotation : role) {
      if (target.isAnnotatedWith(annotation) || target.isMetaAnnotatedWith(annotation)) {
        violations.add(name + " carries prohibited metadata " + annotation);
      }
    }
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()`, `allDomainPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check("DCA-ADV-018", "Specifications must not carry prohibited framework metadata",
        "Domain objects carry no metadata for container management, persistence or transaction coordination",
        arch => DomainMetadata.Check(arch, "DCA-ADV-018"))
    .Selecting("Non-interface types in domain namespaces that are assignable to the configured specification role or whose simple name ends with Specification. Exclusive ownership: events, services, factories, specifications, then domain-model types.")
    .Checking("Configured attribute namespaces classify the attribute type or any base type: types prohibit container, persistence and transaction roles; fields and properties prohibit injection and persistence; methods prohibit transaction and, except on events, injection; constructors prohibit injection. There is no default event-listener attribute role. Unclassified attributes are allowed; runtime types that cannot load are skipped.")
```

### C# helper DomainMetadata

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;
using ArchUnitNET.Domain;
using ArchUnitNET.Domain.Extensions;
using DomainCentric.BuildingBlocks.Ddd.Tactical;

namespace DomainCentric.ArchRules.Rules;

/// <summary>Exclusive ownership and configurable role-by-target domain metadata policy.</summary>
internal static class DomainMetadata
{
    internal static string Owner(DcaArchitecture arch, IType type)
    {
        var markers = arch.Layout.Markers;
        if (type.IsAssignableTo(markers.DomainEvent)) return "DCA-ADV-004";
        if (type.IsAssignableTo(markers.DomainService)) return "DCA-ADV-011";
        if (type.IsAssignableTo(markers.Factory)) return "DCA-ADV-015";
        return AdvancedPatternRules.IsSpecificationRole(arch, type)
            || type.Name.EndsWith(arch.Layout.SpecificationSuffix, StringComparison.Ordinal)
            ? "DCA-ADV-018"
            : "DCA-ONI-003";
    }

    internal static void Check(DcaArchitecture arch, string id)
    {
        var roles = arch.Layout.FrameworkTypes;
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => t is not Interface && Owner(arch, t) == id
            && Regex.IsMatch(t.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllDomainPatterns()))))
        {
            if (id == "DCA-ONI-003" && !Regex.IsMatch(type.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllDomainModelPatterns()))) continue;
            var runtime = arch.RuntimeType(type);
            if (runtime is null) continue;
            Inspect(runtime, violations, roles.PersistenceAttributeTypes, roles.ContainerAttributeNamespaces, roles.PersistenceAttributeNamespaces, roles.TransactionAttributeNamespaces);
            const BindingFlags flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
            foreach (var field in runtime.GetFields(flags)) Inspect(field, violations, roles.PersistenceAttributeTypes, roles.InjectionAttributeNamespaces, roles.PersistenceAttributeNamespaces);
            foreach (var property in runtime.GetProperties(flags)) Inspect(property, violations, roles.PersistenceAttributeTypes, roles.InjectionAttributeNamespaces, roles.PersistenceAttributeNamespaces);
            foreach (var method in runtime.GetMethods(flags)) Inspect(method, violations, Array.Empty<string>(), roles.TransactionAttributeNamespaces,
                id == "DCA-ADV-004" ? Array.Empty<string>() : roles.InjectionAttributeNamespaces);
            foreach (var ctor in runtime.GetConstructors(flags)) Inspect(ctor, violations, Array.Empty<string>(), roles.InjectionAttributeNamespaces);
        }
        DcaRule.Fail(id + ": prohibited domain metadata", violations);
    }

    private static void Inspect(MemberInfo target, List<string> violations, IReadOnlyList<string> typeNames, params IReadOnlyList<string>[] roles)
    {
        foreach (var attribute in target.GetCustomAttributesData())
        {
            for (var type = attribute.AttributeType; type is not null; type = type.BaseType)
            {
                if (!typeNames.Contains(type.FullName ?? "") && !roles.SelectMany(r => r).Any(prefix => DcaLayout.IsBelow(type.Namespace ?? "", prefix))) continue;
                violations.Add($"{target.DeclaringType?.FullName ?? (target as Type)?.FullName}.{target.Name} carries prohibited metadata {attribute.AttributeType.FullName}");
                break;
            }
        }
    }
}
```

## Related mentions (heuristic)

- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
