---
type: Rule
id: DCA-LAY-004
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
selects: "Two mechanisms. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Programmatic: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template, manager or user transaction) or on TransactionBoundary, at any depth of the dependency (field, parameter, call); implementations of TransactionBoundary itself are not selected. With both roles empty only TransactionBoundary dependencies are selected."
checks: "Each annotated method is declared in, and each annotated class and each dependent class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere. An annotation, a transaction-API dependency or a TransactionBoundary dependency in a domain, incoming-adapter or infrastructure package is reported; all findings are collected into one violation. Which transaction a boundary opens is not checked."
enforced_by: "LayeredRules#DCA-LAY-004"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# Transaction boundaries belong to the application layer

## Selection

Two mechanisms. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Programmatic: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template, manager or user transaction) or on TransactionBoundary, at any depth of the dependency (field, parameter, call); implementations of TransactionBoundary itself are not selected. With both roles empty only TransactionBoundary dependencies are selected.

## Check

Each annotated method is declared in, and each annotated class and each dependent class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere. An annotation, a transaction-API dependency or a TransactionBoundary dependency in a domain, incoming-adapter or infrastructure package is reported; all findings are collected into one violation. Which transaction a boundary opens is not checked.

## .NET reading

**Selection.** Types under scan that have any dependency on a configured transaction type - TransactionScope (by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's IDbContextTransaction) - or on ITransactionBoundary; a field, a local, a method call or a using block all count. Implementations of ITransactionBoundary itself are not selected. With no transaction type configured only ITransactionBoundary dependencies are selected.

**Check.** Each resides in an application namespace of some module root (<module>.Application or below) or in an outgoing adapter namespace of some module root (<module>.Adapter.Outgoing or below). A use in a domain, incoming-adapter or infrastructure namespace is reported, one finding per type and transaction type; all findings are collected into one violation. The check is per type, not per method; which transaction a boundary opens is not checked.

## Implementation

```java
DcaRule.check(
        "DCA-LAY-004",
        "Transaction boundaries belong to the application layer",
        rationale,
        arch -> {
          List<String> transactional = layout.frameworkAnnotations().transactional();
          List<String> transactionApi = layout.frameworkAnnotations().transactionApi();
          List<String> allowedPatterns =
              new ArrayList<>(List.of(arch.allApplicationPatterns()));
          allowedPatterns.add(
              ".." + layout.adapterSubpackage() + "." + layout.outgoingSubpackage() + "..");
          String[] allowed = allowedPatterns.toArray(String[]::new);
          CollectedViolations violations = CollectedViolations.withoutHeader();
          violations.addAll(
              methods()
                  .that(AnnotationRoles.annotatedWithAny(transactional))
                  .should()
                  .beDeclaredInClassesThat()
                  .resideInAnyPackage(allowed)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          violations.addAll(
              classes()
                  .that(AnnotationRoles.annotatedWithAny(transactional))
                  .should()
                  .resideInAnyPackage(allowed)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          // Programmatic boundaries: the configured transaction APIs and DCA's own
          // TransactionBoundary port. The boundary's implementations are the one legitimate
          // site that depends on both, wherever they live.
          DescribedPredicate<JavaClass> programmaticBoundary =
              DescribedPredicate.describe(
                  "a configured transaction API or TransactionBoundary",
                  c ->
                      transactionApi.contains(c.getName())
                          || c.isAssignableTo(TransactionBoundary.class));
          violations.addAll(
              noClasses()
                  .that()
                  .resideOutsideOfPackages(allowed)
                  .and()
                  .areNotAssignableTo(TransactionBoundary.class)
                  .should()
                  .dependOnClassesThat(programmaticBoundary)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          violations.throwIfAny();
        })
    .selecting(
        "Two mechanisms. Declarative: methods and classes under scan that carry one of the"
            + " configured transactional annotations directly (meta-annotations do not count)."
            + " Programmatic: classes under scan that depend on one of the configured"
            + " transaction-API types (role transactionApi - a transaction template, manager or"
            + " user transaction) or on TransactionBoundary, at any depth of the dependency"
            + " (field, parameter, call); implementations of TransactionBoundary itself are not"
            + " selected. With both roles empty only TransactionBoundary dependencies are"
            + " selected.")
    .checking(
        "Each annotated method is declared in, and each annotated class and each dependent"
            + " class resides in, an application package of some module root"
            + " (<module>.application..) or an outgoing adapter package (..adapter.outgoing..)"
            + " anywhere. An annotation, a transaction-API dependency or a TransactionBoundary"
            + " dependency in a domain, incoming-adapter or infrastructure package is reported;"
            + " all findings are collected into one violation. Which transaction a boundary"
            + " opens is not checked.")
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

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
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

### `AnnotationRoles.annotatedWithAny`

```java
/** Directly annotated with any annotation of the role; never true for an empty role. */
  static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String> role) {
    if (role.isEmpty()) {
      return DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)");
    }
    DescribedPredicate<CanBeAnnotated> predicate =
        CanBeAnnotated.Predicates.annotatedWith(role.get(0));
    for (String fqn : role.subList(1, role.size())) {
      predicate = predicate.or(CanBeAnnotated.Predicates.annotatedWith(fqn));
    }
    return predicate.as("annotated with any of " + role);
  }

static DescribedPredicate<CanBeAnnotated> annotatedWithAny(List<String>... roles) {
  DescribedPredicate<CanBeAnnotated> predicate = null;
  for (List<String> role : roles) {
    if (role.isEmpty()) {
      continue;
    }
    predicate = predicate == null ? annotatedWithAny(role) : predicate.or(annotatedWithAny(role));
  }
  return predicate == null
      ? DescribedPredicate.<CanBeAnnotated>alwaysFalse()
          .as("annotated with a configured annotation (none configured)")
      : predicate;
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

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-LAY-004",
    "Transaction boundaries belong to the application layer",
    rationale,
    arch =>
    {
        // Structural, over every module root: the application layer and the outgoing adapters
        // (which implement the transaction boundary) of any module, at any depth.
        var allowed = new Regex(
            DcaLayout.AnyOf(arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())));
        // The configured transaction APIs (TransactionScope plus TransactionApiTypes) and DCA's own
        // ITransactionBoundary port. The boundary's implementations are the one legitimate site that
        // depends on both, wherever they live.
        var types = Layout.FrameworkTypes;
        var transactionApis = new HashSet<string>(types.TransactionApiTypes, StringComparer.Ordinal);
        if (FrameworkTypes.IsSet(types.TransactionScope)) transactionApis.Add(types.TransactionScope);
        bool IsBoundary(IType t) => t.FullName == BoundaryPort || t.ImplementsInterface(BoundaryPort);
        bool Programmatic(IType target) => transactionApis.Contains(target.FullName) || IsBoundary(target);
        var violations = arch.Types
            .Where(t => t.Namespace is null || !allowed.IsMatch(t.Namespace.FullName))
            .Where(t => !IsBoundary(t))
            .SelectMany(t => t.Dependencies.Select(d => d.Target).Where(Programmatic).Select(target => target.FullName).Distinct()
                .Select(target => $"{t.FullName} uses {target} outside the application layer"))
            .ToList();
        DcaRule.Fail($"Transaction boundaries belong to the application layer\nbecause {rationale}", violations);
    })
    .Selecting(
        "Types under scan that have any dependency on a configured transaction type - TransactionScope "
        + "(by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default "
        + "CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's "
        + "IDbContextTransaction) - or on ITransactionBoundary; a field, a local, a method call or a using "
        + "block all count. Implementations of ITransactionBoundary itself are not selected. With no "
        + "transaction type configured only ITransactionBoundary dependencies are selected.")
    .Checking(
        "Each resides in an application namespace of some module root (<module>.Application or "
        + "below) or in an outgoing adapter namespace of some module root "
        + "(<module>.Adapter.Outgoing or below). A use in a domain, incoming-adapter or "
        + "infrastructure namespace is reported, one finding per type and transaction type; all "
        + "findings are collected into one violation. The check is per type, not per method; which "
        + "transaction a boundary opens is not checked.")
```

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
