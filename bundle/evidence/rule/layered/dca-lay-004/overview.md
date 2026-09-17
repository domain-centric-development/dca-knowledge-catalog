---
type: Reference
title: Transaction boundaries belong to the application layer — Overview
tags: [reference]
evidence_for: /rule/layered/dca-lay-004.md
---

[Full node and context](/rule/layered/dca-lay-004.md). This is an evidence excerpt; retain the parent selection and caveats.

# Transaction boundaries belong to the application layer

## Selection

Three selections. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Transaction use: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template or user transaction, the types code runs a transaction with). Wiring: classes under scan that depend on one of the configured transaction-manager types (role transactionManager) or on TransactionBoundary. A dependency counts at any depth (field, parameter, call); implementations of TransactionBoundary itself are never selected. With the roles empty only TransactionBoundary dependencies are selected.

## Check

Annotations and transaction use: the method is declared in, or the class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere - a domain, incoming-adapter or infrastructure package is reported, the global infrastructure package included. Wiring: additionally allowed in the global infrastructure package (<base>.infrastructure.., the composition root that declares the manager) and in the shared kernel's infrastructure package (<base>.sharedkernel.infrastructure.., plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure package is reported. All findings are collected into one violation. Where manager and boundary dependencies are allowed the rule cannot tell wiring from a call: a class in the global or shared-kernel infrastructure package that obtains the manager and begins a transaction itself passes. Which transaction a boundary opens is not checked.

## .NET reading

**Selection.** Two selections. Transaction use: types under scan that depend on a configured transaction-API type - TransactionScope (by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's IDbContextTransaction), the types code runs a transaction with. Wiring: types under scan that depend on one of the TransactionManagerTypes (empty by default) or on ITransactionBoundary. A field, a local, a method call or a using block all count; implementations of ITransactionBoundary itself are never selected. With no transaction type configured only ITransactionBoundary dependencies are selected.

**Check.** Transaction use: the type resides in an application namespace of some module root (<module>.Application or below) or in an outgoing adapter namespace of some module root (<module>.Adapter.Outgoing or below) - a domain, incoming-adapter or infrastructure namespace is reported, the global one included. Wiring: additionally allowed in the global infrastructure namespace (<Root>.Infrastructure, the composition root that declares the manager) and in the shared kernel's infrastructure namespace (<Root>.SharedKernel.Infrastructure, plumbing that hooks into the boundary); a domain, incoming-adapter or module-infrastructure namespace is reported. One finding per type and transaction type, all collected into one violation. The check is per type, not per method. Where manager and boundary dependencies are allowed the rule cannot tell wiring from a call: a type in the global or shared-kernel infrastructure namespace that obtains the manager and begins a transaction itself passes. Which transaction a boundary opens is not checked.

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
                  .areNotAssignableTo(TransactionBoundary.class)
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
                          || c.isAssignableTo(TransactionBoundary.class));
          violations.addAll(
              noClasses()
                  .that()
                  .resideOutsideOfPackages(wiringAllowed.toArray(String[]::new))
                  .and()
                  .areNotAssignableTo(TransactionBoundary.class)
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
