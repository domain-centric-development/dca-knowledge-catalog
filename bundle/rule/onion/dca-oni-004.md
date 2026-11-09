---
type: Rule
id: DCA-ONI-004
title: Domain layer must stay synchronous
rule: "Asynchrony is an I/O concern of ports and adapters; a synchronous domain model stays testable, deterministic and free of sync-over-async hazards."
constraint: Domain layer must stay synchronous.
selects: Types the layout places in the domain layer of every module root.
checks: "No dependency on one of the configured asynchronous types, on a type nested in one or on a generic form of one - in a signature, a field, an annotation or a method body. The default names the platform's standard asynchronous types; other awaitables, asynchronous sequences and a library's own reactive types are not checked unless the layout setting for asynchronous types names them. The application and adapter layers are not selected. An empty list checks nothing; an empty selection passes."
enforced_by: "OnionRules#DCA-ONI-004"
status: enforced
maturity: experimental
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/OnionRules.cs
---

# Domain layer must stay synchronous

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Types the layout places in the domain layer of every module root.

## Check

No dependency on one of the configured asynchronous types, on a type nested in one or on a generic form of one - in a signature, a field, an annotation or a method body. The default names the platform's standard asynchronous types; other awaitables, asynchronous sequences and a library's own reactive types are not checked unless the layout setting for asynchronous types names them. The application and adapter layers are not selected. An empty list checks nothing; an empty selection passes.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** Every domain crate.

**Check.** No async fn, no .await and no type from a configured async runtime (std::future::Future implementors returned, tokio, async-std, futures by default). Planned: the suite does not implement it yet.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-004",
        "Domain layer must stay synchronous",
        "Asynchrony is an I/O concern of ports and adapters; a synchronous domain model stays"
            + " testable, deterministic and free of sync-over-async hazards",
        arch -> {
          List<String> asynchronous = arch.layout().asynchronousTypes();
          DescribedPredicate<JavaClass> asynchronousType =
              DescribedPredicate.describe(
                  "a configured asynchronous type",
                  c -> isOrIsNestedIn(c.getBaseComponentType().getName(), asynchronous));
          return noClasses()
              .that(arch.inDomain())
              .should()
              .dependOnClassesThat(asynchronousType)
              .allowEmptyShould(true);
        })
    .experimental()
    .selecting("Types the layout places in the domain layer of every module root.")
    .checking(
        "No dependency on one of the configured asynchronous types, on a type nested in one or"
            + " on a generic form of one - in a signature, a field, an annotation or a method"
            + " body. The default names the platform's standard asynchronous types; other"
            + " awaitables, asynchronous sequences and a library's own reactive types are not"
            + " checked unless the layout setting for asynchronous types names them. The"
            + " application and adapter layers are not selected. An empty list checks nothing;"
            + " an empty selection passes.")
```

## Helpers

### `isOrIsNestedIn`

```java
/** The type itself, a generic form of it or a type nested in it. */
  private static boolean isOrIsNestedIn(String name, List<String> types) {
    for (String type : types) {
      if (name.equals(type) || name.startsWith(type + "$")) {
        return true;
      }
    }
    return false;
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inDomain()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## .NET reading

### C# expression

```csharp
DcaRule.Of(
        "DCA-ONI-004",
        "Domain layer must stay synchronous",
        "Asynchrony is an I/O concern of ports and adapters; a synchronous domain model stays"
            + " testable, deterministic and free of sync-over-async hazards",
        arch => SelectionArchRule.ForEach(
            "types in the domain layer should not depend on an asynchronous type",
            () => arch.Types.Where(arch.InDomain),
            type =>
            {
                var asynchronous = type.Dependencies
                    .Select(d => d.Target.FullName)
                    .Where(name => IsOrIsNestedIn(name, arch.Layout.AsynchronousTypes))
                    .Distinct()
                    .OrderBy(n => n, StringComparer.Ordinal)
                    .ToList();
                return asynchronous.Count > 0
                    ? [$"{type.FullName} depends on {string.Join(", ", asynchronous)}"]
                    : (IEnumerable<string>)[];
            }))
    .Experimental()
    .Selecting("Types the layout places in the domain layer of every module root.")
    .Checking(
        "No dependency on one of the configured asynchronous types, on a type nested in one or"
            + " on a generic form of one - in a signature, a field, an annotation or a method"
            + " body. The default names the platform's standard asynchronous types; other"
            + " awaitables, asynchronous sequences and a library's own reactive types are not"
            + " checked unless the layout setting for asynchronous types names them. The"
            + " application and adapter layers are not selected. An empty list checks nothing;"
            + " an empty selection passes.",
        "Move the awaiting code into a use case or adapter and pass plain values into the domain.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
