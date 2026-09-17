---
type: Rule
id: DCA-MAP-010
title: External system contract types must respect the declared translation and interaction
rule: "An external system's contract types are confined to the adapter where the exchange crosses the boundary (ACL) or at least kept out of the domain (Conformist)."
constraint: External system contract types must respect the declared translation and interaction.
selects: "Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext whose contractPackages() is not empty, reading translation() and interaction(). status() is not consulted: this is a placement check on code that exists, so a PLANNED declaration is checked too - one without any dependent code passes. A declaration without contractPackages() (wire-level contract, no vendor SDK) is skipped - it only documents the relationship."
checks: "With ANTI_CORRUPTION_LAYER, no class below the declaring context's package outside the matching adapter - <context>.adapter.outgoing.. for OUTBOUND, <context>.adapter.incoming.. for INBOUND - depends on a class in any of the contract packages. With any other translation (CONFORMIST), no class in <context>.domain.. does. That the adapter actually translates the contract is not established."
enforced_by: "ContextMapRules#DCA-MAP-010"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ContextMapRules.cs
---

# External system contract types must respect the declared translation and interaction

## Selection

Every @ExternalUpstream declaration on the package-info of every package carrying @BoundedContext whose contractPackages() is not empty, reading translation() and interaction(). status() is not consulted: this is a placement check on code that exists, so a PLANNED declaration is checked too - one without any dependent code passes. A declaration without contractPackages() (wire-level contract, no vendor SDK) is skipped - it only documents the relationship.

## Check

With ANTI_CORRUPTION_LAYER, no class below the declaring context's package outside the matching adapter - <context>.adapter.outgoing.. for OUTBOUND, <context>.adapter.incoming.. for INBOUND - depends on a class in any of the contract packages. With any other translation (CONFORMIST), no class in <context>.domain.. does. That the adapter actually translates the contract is not established.

## .NET reading

**Selection.** Every [ExternalUpstream] declaration on the marker class of every namespace carrying [BoundedContext] whose ContractNamespaces is not empty, reading Translation and Interaction. Status is not consulted: this is a placement check on code that exists, so a Planned declaration is checked too - one without any dependent code passes. A declaration without ContractNamespaces (wire-level contract, no vendor SDK) is skipped - it only documents the relationship.

**Check.** With AntiCorruptionLayer, no type below the declaring context's namespace outside the matching adapter - <context>.Adapter.Outgoing for Outbound, <context>.Adapter.Incoming for Inbound - depends on a type in any of the contract namespaces or below. With any other translation (Conformist), no type in <context>.Domain does. That the adapter actually translates the contract is not established.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-010",
        "External system contract types must respect the declared translation and interaction",
        "An external system's contract types are confined to the adapter where the exchange"
            + " crosses the boundary (ACL) or at least kept out of the domain (Conformist)",
        arch -> {
          CollectedViolations violations = CollectedViolations.withoutHeader();
          // Without contractPackages (wire-level contract, no vendor SDK) there is nothing to
          // check — the declaration then only documents the relationship.
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
              if (e.contractPackages().length == 0) {
                continue;
              }
              if (e.translation() == Upstream.Translation.ANTI_CORRUPTION_LAYER) {
                String allowedAdapter =
                    e.interaction() == ExternalUpstream.Interaction.OUTBOUND
                        ? layout.outgoingAdapterPattern(pkg)
                        : layout.incomingAdapterPattern(pkg);
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(pkg + "..")
                        .and()
                        .resideOutsideOfPackage(allowedAdapter)
                        .should()
                        .dependOnClassesThat()
                        .resideInAnyPackage(e.contractPackages())
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' declares ANTI_CORRUPTION_LAYER towards external system '"
                        + e.name()
                        + "' ("
                        + e.interaction()
                        + ") — its contract types ("
                        + String.join(", ", e.contractPackages())
                        + ") must not leave "
                        + allowedAdapter);
              } else {
                violations.addAll(
                    noClasses()
                        .that()
                        .resideInAPackage(layout.domainPattern(pkg))
                        .should()
                        .dependOnClassesThat()
                        .resideInAnyPackage(e.contractPackages())
                        .allowEmptyShould(true),
                    arch.classes(),
                    "Context '"
                        + source
                        + "' conforms to external system '"
                        + e.name()
                        + "', but conformism does not suspend domain purity — the domain"
                        + " layer stays free of its contract types");
              }
            }
          }
          violations.throwIfAny();
        })
    .selecting(
        "Every @ExternalUpstream declaration on the package-info of every package"
            + " carrying @BoundedContext whose contractPackages() is not empty, reading"
            + " translation() and interaction(). status() is not consulted: this is a"
            + " placement check on code that exists, so a PLANNED declaration is checked too"
            + " - one without any dependent code passes. A declaration without"
            + " contractPackages() (wire-level contract, no vendor SDK) is skipped - it only"
            + " documents the relationship.")
    .checking(
        "With ANTI_CORRUPTION_LAYER, no class below the declaring context's package"
            + " outside the matching adapter - <context>.adapter.outgoing.. for OUTBOUND,"
            + " <context>.adapter.incoming.. for INBOUND - depends on a class in any of the"
            + " contract packages. With any other translation (CONFORMIST), no class in"
            + " <context>.domain.. does. That the adapter actually translates the contract"
            + " is not established.")
```

## Helpers

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```

### `CollectedViolations.addAll`

```java
/**
   * Evaluates one ArchUnit rule and records each of its violation details, suffixed with the
   * explanation of what the rule was checking — the detail alone ({@code Class A depends on B})
   * does not say why that dependency is wrong.
   */
  void addAll(ArchRule rule, JavaClasses classes, String explanation) {
    for (String detail : rule.evaluate(classes).getFailureReport().getDetails()) {
      add(explanation.isEmpty() ? detail : detail + " - " + explanation);
    }
  }

/** Evaluates one ArchUnit rule and records its violation details as they are. */
  void addAll(ArchRule rule, JavaClasses classes) {
    addAll(rule, classes, "");
  }
```

### `CollectedViolations.throwIfAny`

```java
/**
   * Throws the collected violations as one {@link DcaRuleViolation}; nothing when there are none.
   */
  void throwIfAny() {
    if (!violations.isEmpty()) {
      throw new DcaRuleViolation(header, violations);
    }
  }
```

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `classes()`, `contextName()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-MAP-010",
        "External system contract types must respect the declared translation and interaction",
        "An external system's contract types are confined to the adapter where the exchange crosses the boundary"
            + " (ACL) or at least kept out of the domain (Conformist)",
        arch =>
        {
            // Without ContractNamespaces (wire-level contract, no vendor SDK) there is nothing to check —
            // the declaration then only documents the relationship.
            var violations = new List<string>();
            foreach (var ns in arch.BoundedContextNamespaces)
            {
                var source = ShortName(arch, ns);
                foreach (var e in arch.NamespaceAttributes<ExternalUpstreamAttribute>(ns))
                {
                    if (e.ContractNamespaces.Length == 0)
                    {
                        continue;
                    }
                    if (e.Translation == Translation.AntiCorruptionLayer)
                    {
                        var allowedAdapter = e.Interaction == Interaction.Outbound
                            ? OutgoingAdapterNamespace(ns)
                            : IncomingAdapterNamespace(ns);
                        foreach (var type in TypesBelow(arch, ns).Where(t => !IsBelow(t, allowedAdapter)))
                        {
                            if (e.ContractNamespaces.Any(c => DependsOnNamespace(type, c)))
                            {
                                violations.Add("Context '" + source + "' declares AntiCorruptionLayer towards external system '"
                                    + e.Name + "' (" + e.Interaction + ") — " + type.FullName + " uses its contract types ("
                                    + string.Join(", ", e.ContractNamespaces) + ") outside " + allowedAdapter);
                            }
                        }
                    }
                    else
                    {
                        foreach (var type in TypesBelow(arch, DomainNamespace(ns)))
                        {
                            if (e.ContractNamespaces.Any(c => DependsOnNamespace(type, c)))
                            {
                                violations.Add("Context '" + source + "' conforms to external system '" + e.Name
                                    + "', but conformism does not suspend domain purity — " + type.FullName
                                    + " in the domain layer uses its contract types");
                            }
                        }
                    }
                }
            }
            DcaRule.Fail("External system contract types must respect the declared translation and interaction", violations);
        })
    .Selecting(
        "Every [ExternalUpstream] declaration on the marker class of every namespace"
            + " carrying [BoundedContext] whose ContractNamespaces is not empty, reading"
            + " Translation and Interaction. Status is not consulted: this is a placement"
            + " check on code that exists, so a Planned declaration is checked too - one"
            + " without any dependent code passes. A declaration without ContractNamespaces"
            + " (wire-level contract, no vendor SDK) is skipped - it only documents the"
            + " relationship.")
    .Checking(
        "With AntiCorruptionLayer, no type below the declaring context's namespace"
            + " outside the matching adapter - <context>.Adapter.Outgoing for Outbound,"
            + " <context>.Adapter.Incoming for Inbound - depends on a type in any of the"
            + " contract namespaces or below. With any other translation (Conformist), no type in"
            + " <context>.Domain does. That the adapter actually translates the contract"
            + " is not established.")
```

## Related mentions (heuristic)

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
