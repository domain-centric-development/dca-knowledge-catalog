---
type: Rule
id: DCA-LAY-004
title: Transaction boundaries belong to the application layer
rule: Transactions are an application-layer concern - domain and incoming adapters must not manage them.
constraint: Transaction boundaries belong to the application layer.
selects: "Three selections. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Transaction use: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template or user transaction, the types code runs a transaction with). Wiring: classes under scan that depend on one of the configured transaction-manager types (role transactionManager) or on TransactionBoundary. A dependency counts at any depth (field, parameter, call); implementations of TransactionBoundary itself are never selected. With the roles empty only TransactionBoundary dependencies are selected."
checks: "Annotations and transaction use: the method is declared in, or the class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere - a domain, incoming-adapter or infrastructure package is reported, the global infrastructure package included. Wiring: additionally allowed in the global infrastructure package (<base>.infrastructure.., the composition root that declares the manager) and in the shared kernel's infrastructure package (<base>.sharedkernel.infrastructure.., plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure package is reported. All findings are collected into one violation. Where manager and boundary dependencies are allowed the rule cannot tell wiring from a call: a class in the global or shared-kernel infrastructure package that obtains the manager and begins a transaction itself passes. Which transaction a boundary opens is not checked."
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

Three selections. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Transaction use: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template or user transaction, the types code runs a transaction with). Wiring: classes under scan that depend on one of the configured transaction-manager types (role transactionManager) or on TransactionBoundary. A dependency counts at any depth (field, parameter, call); implementations of TransactionBoundary itself are never selected. With the roles empty only TransactionBoundary dependencies are selected.

## Check

Annotations and transaction use: the method is declared in, or the class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere - a domain, incoming-adapter or infrastructure package is reported, the global infrastructure package included. Wiring: additionally allowed in the global infrastructure package (<base>.infrastructure.., the composition root that declares the manager) and in the shared kernel's infrastructure package (<base>.sharedkernel.infrastructure.., plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure package is reported. All findings are collected into one violation. Where manager and boundary dependencies are allowed the rule cannot tell wiring from a call: a class in the global or shared-kernel infrastructure package that obtains the manager and begins a transaction itself passes. Which transaction a boundary opens is not checked.

## .NET reading

**Selection.** Three selections. Declarative: types under scan that carry the configured transactional attribute, and types that declare a method carrying it - empty by default, because neither .NET preset configures one. Transaction use: types under scan that depend on a configured transaction-API type - TransactionScope (by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's IDbContextTransaction), the types code runs a transaction with. Wiring: types under scan that depend on one of the TransactionManagerTypes (empty by default) or on ITransactionBoundary. A field, a local, a method call or a using block all count; implementations of ITransactionBoundary itself are never selected. With no transaction type configured only ITransactionBoundary dependencies are selected.

**Check.** Declarative: the type resides in an application namespace of some module root or in an outgoing adapter namespace of some module root - the same places the transaction API is allowed, as in the Java twin. With no transactional attribute configured this selection is empty and the rule checks the other two only. Transaction use: the type resides in an application namespace of some module root (<module>.Application or below) or in an outgoing adapter namespace of some module root (<module>.Adapter.Outgoing or below) - a domain, incoming-adapter or infrastructure namespace is reported, the global one included. Wiring: additionally allowed in the global infrastructure namespace (<Root>.Infrastructure, the composition root that declares the manager) and in the shared kernel's infrastructure namespace (<Root>.SharedKernel.Infrastructure, plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure namespace is reported. One finding per type and transaction type, all collected into one violation. The check is per type, not per method. Where manager and boundary dependencies are allowed the rule cannot tell wiring from a call: a type in the global or shared-kernel infrastructure namespace that obtains the manager and begins a transaction itself passes. Which transaction a boundary opens is not checked.

## Implementation

```java
DcaRule.check(
        "DCA-LAY-004",
        "Transaction boundaries belong to the application layer",
        rationale,
        arch -> {
          List<String> transactional = layout.frameworkAnnotations().transactional();
          List<String> transactionApi = layout.frameworkAnnotations().transactionApi();
          List<String> transactionManager = layout.frameworkAnnotations().transactionManager();
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
          // Programmatic boundaries, two kinds. Using a transaction API (template, user
          // transaction) draws a boundary and is allowed exactly where the annotation is.
          // Depending on a transaction manager or on DCA's TransactionBoundary port is wiring
          // and plumbing as well: the composition root (the global infrastructure package) and
          // the shared kernel's infrastructure may do that too. The boundary's implementations
          // are exempt wherever they live.
          DescribedPredicate<JavaClass> usesTransactionApi =
              DescribedPredicate.describe(
                  "a configured transaction API", c -> transactionApi.contains(c.getName()));
          violations.addAll(
              noClasses()
                  .that()
                  .resideOutsideOfPackages(allowed)
                  .and()
                  .areNotAssignableTo(arch.layout().markers().transactionBoundary())
                  .should()
                  .dependOnClassesThat(usesTransactionApi)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          List<String> wiringAllowed = new ArrayList<>(allowedPatterns);
          wiringAllowed.add(layout.infrastructurePattern());
          wiringAllowed.add(
              layout.sharedKernelPackage() + "." + layout.infrastructureSubpackage() + "..");
          DescribedPredicate<JavaClass> managerOrBoundary =
              DescribedPredicate.describe(
                  "a configured transaction manager or TransactionBoundary",
                  c ->
                      transactionManager.contains(c.getName())
                          || c.isAssignableTo(arch.layout().markers().transactionBoundary()));
          violations.addAll(
              noClasses()
                  .that()
                  .resideOutsideOfPackages(wiringAllowed.toArray(String[]::new))
                  .and()
                  .areNotAssignableTo(arch.layout().markers().transactionBoundary())
                  .should()
                  .dependOnClassesThat(managerOrBoundary)
                  .allowEmptyShould(true),
              arch.classes(),
              rationale);
          violations.throwIfAny();
        })
    .selecting(
        "Three selections. Declarative: methods and classes under scan that carry one of the"
            + " configured transactional annotations directly (meta-annotations do not count)."
            + " Transaction use: classes under scan that depend on one of the configured"
            + " transaction-API types (role transactionApi - a transaction template or user"
            + " transaction, the types code runs a transaction with). Wiring: classes under scan"
            + " that depend on one of the configured transaction-manager types (role"
            + " transactionManager) or on TransactionBoundary. A dependency counts at any depth"
            + " (field, parameter, call); implementations of TransactionBoundary itself are never"
            + " selected. With the roles empty only TransactionBoundary dependencies are"
            + " selected.")
    .checking(
        "Annotations and transaction use: the method is declared in, or the class resides in,"
            + " an application package of some module root (<module>.application..) or an"
            + " outgoing adapter package (..adapter.outgoing..) anywhere - a domain,"
            + " incoming-adapter or infrastructure package is reported, the global"
            + " infrastructure package included. Wiring: additionally allowed in the global"
            + " infrastructure package (<base>.infrastructure.., the composition root that"
            + " declares the manager) and in the shared kernel's infrastructure package"
            + " (<base>.sharedkernel.infrastructure.., plumbing that hooks into the boundary);"
            + " a domain, incoming-adapter or module-infrastructure package is reported. All"
            + " findings are collected into one violation. Where manager and boundary"
            + " dependencies are allowed the rule cannot tell wiring from a call: a class in the"
            + " global or shared-kernel infrastructure package that obtains the manager and"
            + " begins a transaction itself passes. Which transaction a boundary opens is not"
            + " checked.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
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
        // Programmatic boundaries, two kinds. Using a transaction API (TransactionScope plus
        // TransactionApiTypes) draws a boundary and is allowed exactly in the application layer and the
        // outgoing adapters. Depending on a transaction manager (TransactionManagerTypes) or on DCA's
        // ITransactionBoundary port is wiring and plumbing as well: the composition root (the global
        // infrastructure namespace) and the shared kernel's infrastructure may do that too. The boundary's
        // implementations are exempt wherever they live.
        var allowed = new Regex(DcaLayout.AnyOf(arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())));
        var wiringAllowed = new Regex(DcaLayout.AnyOf(
            arch.AllApplicationPatterns().Concat(arch.AllOutgoingAdapterPatterns())
                .Append(Layout.InfrastructurePattern)
                .Append(DcaLayout.Below($"{Layout.SharedKernelNamespace}.{Layout.InfrastructureSegment}"))));
        var types = Layout.FrameworkTypes;
        var transactionApis = new HashSet<string>(types.TransactionApiTypes, StringComparer.Ordinal);
        if (FrameworkTypes.IsSet(types.TransactionScope)) transactionApis.Add(types.TransactionScope);
        var transactionManagers = new HashSet<string>(types.TransactionManagerTypes, StringComparer.Ordinal);
        bool IsBoundary(IType t) => t.FullName == BoundaryPort || t.ImplementsInterface(BoundaryPort);
        bool UsesApi(IType target) => transactionApis.Contains(target.FullName);
        bool ManagerOrBoundary(IType target) => transactionManagers.Contains(target.FullName) || IsBoundary(target);
        IEnumerable<string> Findings(Regex allowedHere, Func<IType, bool> programmatic) => arch.Types
            .Where(t => t.Namespace is null || !allowedHere.IsMatch(t.Namespace.FullName))
            .Where(t => !IsBoundary(t))
            .SelectMany(t => t.Dependencies.Select(d => d.Target).Where(programmatic).Select(target => target.FullName).Distinct()
                .Select(target => $"{t.FullName} uses {target} outside the application layer"));
        var violations = Findings(allowed, UsesApi).Concat(Findings(wiringAllowed, ManagerOrBoundary))
            .Concat(DeclarativeFindings(arch, allowed, types.TransactionalAttribute))
            .ToList();
        DcaRule.Fail($"Transaction boundaries belong to the application layer\nbecause {rationale}", violations);
    })
    .Selecting(
        "Three selections. Declarative: types under scan that carry the configured transactional "
        + "attribute, and types that declare a method carrying it - empty by default, because neither "
        + ".NET preset configures one. Transaction use: types under scan that depend on a configured transaction-API "
        + "type - TransactionScope (by default System.Transactions.TransactionScope) or one of the "
        + "TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the "
        + "persistence library's IDbContextTransaction), the types code runs a transaction with. Wiring: "
        + "types under scan that depend on one of the TransactionManagerTypes (empty by default) or on "
        + "ITransactionBoundary. A field, a local, a method call or a using block all count; "
        + "implementations of ITransactionBoundary itself are never selected. With no transaction type "
        + "configured only ITransactionBoundary dependencies are selected.")
    .Checking(
        "Declarative: the type resides in an application namespace of some module root or in an "
        + "outgoing adapter namespace of some module root - the same places the transaction API is "
        + "allowed, as in the Java twin. With no transactional attribute configured this selection is "
        + "empty and the rule checks the other two only. Transaction use: the type resides in an application namespace of some module root "
        + "(<module>.Application or below) or in an outgoing adapter namespace of some module root "
        + "(<module>.Adapter.Outgoing or below) - a domain, incoming-adapter or infrastructure namespace "
        + "is reported, the global one included. Wiring: additionally allowed in the global "
        + "infrastructure namespace (<Root>.Infrastructure, the composition root that declares the "
        + "manager) and in the shared kernel's infrastructure namespace (<Root>.SharedKernel.Infrastructure, "
        + "plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure "
        + "namespace is reported. One finding per type and transaction type, all collected into one "
        + "violation. The check is per type, not per method. Where manager and boundary dependencies "
        + "are allowed the rule cannot tell wiring from a call: a type in the global or shared-kernel "
        + "infrastructure namespace that obtains the manager and begins a transaction itself passes. "
        + "Which transaction a boundary opens is not checked.")
```

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/layered/dca-lay-004/overview.md)
- [`CollectedViolations.check`](/evidence/rule/layered/dca-lay-004/collectedviolations-check.md)
- [`CollectedViolations.add`](/evidence/rule/layered/dca-lay-004/collectedviolations-add.md)
- [`CollectedViolations.withoutHeader`](/evidence/rule/layered/dca-lay-004/collectedviolations-withoutheader.md)
- [`CollectedViolations.addAll`](/evidence/rule/layered/dca-lay-004/collectedviolations-addall.md)
- [`AnnotationRoles.annotatedWithAny`](/evidence/rule/layered/dca-lay-004/annotationroles-annotatedwithany.md)
- [`CollectedViolations.throwIfAny`](/evidence/rule/layered/dca-lay-004/collectedviolations-throwifany.md)
- [`CollectedViolations.isEmpty`](/evidence/rule/layered/dca-lay-004/collectedviolations-isempty.md)
- [C# expression](/evidence/rule/layered/dca-lay-004/c-expression.md)
