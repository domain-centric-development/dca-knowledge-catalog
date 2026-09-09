---
type: Rule
id: DCA-ONI-003
title: Domain models must not carry prohibited framework metadata
rule: "Domain objects carry no metadata for container management, persistence or transaction coordination."
constraint: Domain models must not carry prohibited framework metadata.
selects: "Non-interface domain models in domain packages. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types."
checks: "Direct or meta-annotations: types prohibit injectable, persistenceEntity and transactional roles; fields prohibit injectionSite and persistenceMapping; methods prohibit transactional and eventListener, plus injectionSite except on events; constructors prohibit injectionSite. Unclassified annotations are allowed by this check. Empty configured roles select no metadata; wiring is not established."
enforced_by: "OnionRules#DCA-ONI-003"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/OnionRules.cs
---

# Domain models must not carry prohibited framework metadata

## Selection

Non-interface domain models in domain packages. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types.

## Check

Direct or meta-annotations: types prohibit injectable, persistenceEntity and transactional roles; fields prohibit injectionSite and persistenceMapping; methods prohibit transactional and eventListener, plus injectionSite except on events; constructors prohibit injectionSite. Unclassified annotations are allowed by this check. Empty configured roles select no metadata; wiring is not established.

## .NET reading

**Selection.** Domain.Model types except events, services, factories and specifications, which have exclusive ADV ownership.

**Check.** Configured attribute namespaces classify an attribute or any base attribute type. Types prohibit container, persistence and transaction roles; fields and properties prohibit injection and persistence; methods prohibit transaction and injection; constructors prohibit injection. Unclassified metadata is allowed. Missing runtime types are skipped; wiring is not established.

## Implementation

```java
DcaRule.check(
        "DCA-ONI-003",
        "Domain models must not carry prohibited framework metadata",
        "Domain objects carry no metadata for container management, persistence or transaction coordination",
        arch -> DomainMetadata.check(arch, "DCA-ONI-003"))
    .selecting(
        "Non-interface domain models in domain packages. Metadata ownership is exclusive: events, services, factories, specifications, then domain.model types.")
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
        || !owner(type).equals(id)
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
    throw new AssertionError(
        id + ": prohibited domain metadata\n" + String.join("\n", violations));
}
```

### `DomainMetadata.owner`

```java
static String owner(JavaClass type) {
  String tactical = "dev.domaincentric.dca.buildingblocks.ddd.tactical.";
  if (type.isAssignableTo(tactical + "DomainEvent")) return "DCA-ADV-004";
  if (type.isAssignableTo(tactical + "DomainService")) return "DCA-ADV-011";
  if (type.isAssignableTo(tactical + "Factory")) return "DCA-ADV-015";
  if (type.getSimpleName().endsWith("Specification")) return "DCA-ADV-018";
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
DcaRule.Check("DCA-ONI-003", "Domain models must not carry prohibited framework metadata",
        "Domain metadata does not configure infrastructure concerns",
        arch => DomainMetadata.Check(arch, "DCA-ONI-003"))
    .Selecting("Domain.Model types except events, services, factories and specifications, which have exclusive ADV ownership.")
    .Checking("Configured attribute namespaces classify an attribute or any base attribute type. Types prohibit container, persistence and transaction roles; fields and properties prohibit injection and persistence; methods prohibit transaction and injection; constructors prohibit injection. Unclassified metadata is allowed. Missing runtime types are skipped; wiring is not established.")
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
    internal static string Owner(IType type)
    {
        if (type.IsAssignableTo(typeof(IDomainEvent).FullName!)) return "DCA-ADV-004";
        if (type.IsAssignableTo(typeof(IDomainService).FullName!)) return "DCA-ADV-011";
        if (type.IsAssignableTo(typeof(IFactory).FullName!)) return "DCA-ADV-015";
        return type.Name.EndsWith("Specification", StringComparison.Ordinal) ? "DCA-ADV-018" : "DCA-ONI-003";
    }

    internal static void Check(DcaArchitecture arch, string id)
    {
        var roles = arch.Layout.FrameworkTypes;
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => t is not Interface && Owner(t) == id
            && Regex.IsMatch(t.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllDomainPatterns()))))
        {
            if (id == "DCA-ONI-003" && !Regex.IsMatch(type.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllDomainModelPatterns()))) continue;
            var runtime = arch.RuntimeType(type);
            if (runtime is null) continue;
            Inspect(runtime, violations, roles.ContainerAttributeNamespaces, roles.PersistenceAttributeNamespaces, roles.TransactionAttributeNamespaces);
            const BindingFlags flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
            foreach (var field in runtime.GetFields(flags)) Inspect(field, violations, roles.InjectionAttributeNamespaces, roles.PersistenceAttributeNamespaces);
            foreach (var property in runtime.GetProperties(flags)) Inspect(property, violations, roles.InjectionAttributeNamespaces, roles.PersistenceAttributeNamespaces);
            foreach (var method in runtime.GetMethods(flags)) Inspect(method, violations, roles.TransactionAttributeNamespaces,
                id == "DCA-ADV-004" ? Array.Empty<string>() : roles.InjectionAttributeNamespaces);
            foreach (var ctor in runtime.GetConstructors(flags)) Inspect(ctor, violations, roles.InjectionAttributeNamespaces);
        }
        DcaRule.Fail(id + ": prohibited domain metadata", violations);
    }

    private static void Inspect(MemberInfo target, List<string> violations, params IReadOnlyList<string>[] roles)
    {
        foreach (var attribute in target.GetCustomAttributesData())
        {
            for (var type = attribute.AttributeType; type is not null; type = type.BaseType)
            {
                if (!roles.SelectMany(r => r).Any(prefix => DcaLayout.IsBelow(type.Namespace ?? "", prefix))) continue;
                violations.Add($"{target.DeclaringType?.FullName ?? (target as Type)?.FullName}.{target.Name} carries prohibited metadata {attribute.AttributeType.FullName}");
                break;
            }
        }
    }
}
```

## Related mentions (heuristic)

- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Factory](/marker/tactical/factory.md)
- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
