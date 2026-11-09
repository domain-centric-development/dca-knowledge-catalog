---
type: Rule
id: DCA-LAY-008
title: Application layer must not use persistence or transaction APIs
rule: "A use case declares its transaction with the configured transactional annotation or draws its boundary through the transaction-boundary port or a decorator around the use case, never through a persistence context, a connection or a transaction scope of its own. A persistence or transaction API in the application layer binds the use cases to one persistence technology and hides where the boundary is; the boundary's implementation is the single place that knows how to open and commit a transaction."
constraint: Application layer must not use persistence or transaction APIs.
selects: Types the layout places in the application layer of every module root.
checks: "No dependency on a type whose fully qualified name starts with one of the configured persistence and transaction API prefixes - in a signature, a field, an annotation or a method body. The configured transactional annotation, which DCA-LAY-004 places in the application layer, passes, and so do the types nested in it: a use case may declare its transaction. A transaction drawn programmatically - a transaction scope, a user transaction, a connection - is reported; it goes through the transaction-boundary port. The default names the platform's common persistence, data-access and transaction APIs; another persistence library is not reported unless the layout setting for persistence APIs names it, and the domain and adapter layers are not selected. An empty list checks nothing; an empty selection passes."
enforced_by: "LayeredRules#DCA-LAY-008"
status: enforced
maturity: experimental
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# Application layer must not use persistence or transaction APIs

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Types the layout places in the application layer of every module root.

## Check

No dependency on a type whose fully qualified name starts with one of the configured persistence and transaction API prefixes - in a signature, a field, an annotation or a method body. The configured transactional annotation, which DCA-LAY-004 places in the application layer, passes, and so do the types nested in it: a use case may declare its transaction. A transaction drawn programmatically - a transaction scope, a user transaction, a connection - is reported; it goes through the transaction-boundary port. The default names the platform's common persistence, data-access and transaction APIs; another persistence library is not reported unless the layout setting for persistence APIs names it, and the domain and adapter layers are not selected. An empty list checks nothing; an empty selection passes.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** Every application crate.

**Check.** No dependency on a configured persistence or transaction crate (sqlx, diesel, sea-orm, rusqlite, tokio-postgres, mongodb by default). Planned: the suite does not implement it yet.

## Implementation

```java
DcaRule.of(
        "DCA-LAY-008",
        "Application layer must not use persistence or transaction APIs",
        "A use case declares its transaction with the configured transactional annotation or"
            + " draws its boundary through the transaction-boundary port or a decorator around"
            + " the use case, never through a persistence context, a connection or a"
            + " transaction scope of its own. A persistence or transaction API"
            + " in the application layer binds the use cases to one persistence technology and"
            + " hides where the boundary is; the boundary's implementation is the single place"
            + " that knows how to open and commit a transaction",
        arch -> {
          List<String> prefixes = arch.layout().persistenceApiPrefixes();
          // Declarative is allowed: the transactional annotation DCA-LAY-004 places in the
          // application layer, and the types nested in it (its attribute enums), pass.
          List<String> declarative = arch.layout().frameworkAnnotations().transactional();
          DescribedPredicate<JavaClass> persistenceApi =
              DescribedPredicate.describe(
                  "a configured persistence or transaction API",
                  c -> {
                    String name = c.getBaseComponentType().getName();
                    return prefixes.stream().anyMatch(name::startsWith)
                        && declarative.stream()
                            .noneMatch(a -> name.equals(a) || name.startsWith(a + "$"));
                  });
          return noClasses()
              .that(arch.inApplication())
              .should()
              .dependOnClassesThat(persistenceApi)
              .allowEmptyShould(true);
        })
    .experimental()
    .selecting("Types the layout places in the application layer of every module root.")
    .checking(
        "No dependency on a type whose fully qualified name starts with one of the configured"
            + " persistence and transaction API prefixes - in a signature, a field, an annotation or"
            + " a method body. The configured transactional annotation, which DCA-LAY-004 places in"
            + " the application layer, passes, and so do the types nested in it: a use case may"
            + " declare its transaction. A transaction drawn programmatically - a transaction scope,"
            + " a user transaction, a connection - is reported; it goes through the"
            + " transaction-boundary port. The default names the platform's common persistence,"
            + " data-access and transaction APIs; another persistence library is not reported unless"
            + " the layout setting for persistence APIs names it, and the domain and adapter layers"
            + " are not selected. An empty list checks nothing; an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## .NET reading

### C# expression

```csharp
DcaRule.Of(
        "DCA-LAY-008",
        "Application layer must not use persistence or transaction APIs",
        "A use case declares its transaction with the configured transactional annotation or"
            + " draws its boundary through the transaction-boundary port or a decorator around"
            + " the use case, never through a persistence context, a connection or a"
            + " transaction scope of its own. A persistence or transaction API"
            + " in the application layer binds the use cases to one persistence technology and"
            + " hides where the boundary is; the boundary's implementation is the single place"
            + " that knows how to open and commit a transaction",
        arch =>
        {
            var prefixes = arch.Layout.PersistenceApiPrefixes;
            // Declarative is allowed: the transactional attribute DCA-LAY-004 places in the
            // application layer, and the types nested in it, pass.
            var declarative = arch.Layout.FrameworkTypes.TransactionalAttribute;
            bool IsDeclarative(string name) =>
                FrameworkTypes.IsSet(declarative)
                && (name == declarative || name.StartsWith(declarative + "+", StringComparison.Ordinal));
            return SelectionArchRule.ForEach(
                "types in the application layer should not depend on a persistence or transaction API",
                () => arch.Types.Where(arch.InApplication),
                type =>
            {
                var apis = type.Dependencies
                    .Select(d => d.Target.FullName)
                    .Where(name => prefixes.Any(p => name.StartsWith(p, StringComparison.Ordinal)) && !IsDeclarative(name))
                    .Distinct()
                    .OrderBy(n => n, StringComparer.Ordinal)
                    .ToList();
                return apis.Count > 0
                    ? [$"{type.FullName} depends on {string.Join(", ", apis)}"]
                    : (IEnumerable<string>)[];
            });
        })
    .Experimental()
    .Selecting("Types the layout places in the application layer of every module root.")
    .Checking(
        "No dependency on a type whose fully qualified name starts with one of the configured"
            + " persistence and transaction API prefixes - in a signature, a field, an annotation or"
            + " a method body. The configured transactional annotation, which DCA-LAY-004 places in"
            + " the application layer, passes, and so do the types nested in it: a use case may"
            + " declare its transaction. A transaction drawn programmatically - a transaction scope,"
            + " a user transaction, a connection - is reported; it goes through the"
            + " transaction-boundary port. The default names the platform's common persistence,"
            + " data-access and transaction APIs; another persistence library is not reported unless"
            + " the layout setting for persistence APIs names it, and the domain and adapter layers"
            + " are not selected. An empty list checks nothing; an empty selection passes.",
        "Program the use case against an output port, declare the transaction with the configured transactional attribute or draw it through the transaction-boundary port, and move the API call into an outgoing adapter.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
