---
type: Reference
title: Transaction boundaries belong to the application layer — Overview
tags: [reference]
evidence_for: /rule/layered/dca-lay-004.md
---

[Full node and context](/rule/layered/dca-lay-004.md). This is an evidence excerpt; retain the parent selection and caveats.

# Transaction boundaries belong to the application layer

## Selection

Two mechanisms. Declarative: methods and classes under scan that carry one of the configured transactional annotations directly (meta-annotations do not count). Programmatic: classes under scan that depend on one of the configured transaction-API types (role transactionApi - a transaction template, manager or user transaction) or on TransactionBoundary, at any depth of the dependency (field, parameter, call); implementations of TransactionBoundary itself and classes in the global infrastructure package (<base>.infrastructure.., the composition root that wires the transaction manager) or in the shared kernel's infrastructure package (<base>.sharedkernel.infrastructure.., its plumbing) are not selected. With both roles empty only TransactionBoundary dependencies are selected.

## Check

Each annotated method is declared in, and each annotated class and each dependent class resides in, an application package of some module root (<module>.application..) or an outgoing adapter package (..adapter.outgoing..) anywhere. An annotation in a domain, incoming-adapter or infrastructure package is reported; a transaction-API or TransactionBoundary dependency in a domain, incoming-adapter or module-infrastructure package is reported; all findings are collected into one violation. Which transaction a boundary opens is not checked.

## .NET reading

**Selection.** Types under scan that have any dependency on a configured transaction type - TransactionScope (by default System.Transactions.TransactionScope) or one of the TransactionApiTypes (by default CommittableTransaction, IDbTransaction, DbTransaction and the persistence library's IDbContextTransaction) - or on ITransactionBoundary; a field, a local, a method call or a using block all count. Implementations of ITransactionBoundary itself and types in the global infrastructure namespace (<Root>.Infrastructure, the composition root that wires the transaction handle) or in the shared kernel's infrastructure namespace (<Root>.SharedKernel.Infrastructure, its plumbing) are not selected. With no transaction type configured only ITransactionBoundary dependencies are selected.

**Check.** Each resides in an application namespace of some module root (<module>.Application or below) or in an outgoing adapter namespace of some module root (<module>.Adapter.Outgoing or below). A use in a domain, incoming-adapter or module-infrastructure namespace is reported, one finding per type and transaction type; all findings are collected into one violation. The check is per type, not per method; which transaction a boundary opens is not checked.

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
          // site that depends on both, wherever they live; the composition root (the global
          // infrastructure package) and the shared kernel's infrastructure wire the transaction
          // manager and its plumbing and draw no boundary.
          List<String> wiringAllowed = new ArrayList<>(allowedPatterns);
          wiringAllowed.add(layout.infrastructurePattern());
          wiringAllowed.add(
              layout.sharedKernelPackage() + "." + layout.infrastructureSubpackage() + "..");
          DescribedPredicate<JavaClass> programmaticBoundary =
              DescribedPredicate.describe(
                  "a configured transaction API or TransactionBoundary",
                  c ->
                      transactionApi.contains(c.getName())
                          || c.isAssignableTo(TransactionBoundary.class));
          violations.addAll(
              noClasses()
                  .that()
                  .resideOutsideOfPackages(wiringAllowed.toArray(String[]::new))
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
            + " (field, parameter, call); implementations of TransactionBoundary itself and"
            + " classes in the global infrastructure package (<base>.infrastructure.., the"
            + " composition root that wires the transaction manager) or in the shared kernel's"
            + " infrastructure package (<base>.sharedkernel.infrastructure.., its plumbing) are"
            + " not selected. With both roles empty only TransactionBoundary dependencies are"
            + " selected.")
    .checking(
        "Each annotated method is declared in, and each annotated class and each dependent"
            + " class resides in, an application package of some module root"
            + " (<module>.application..) or an outgoing adapter package (..adapter.outgoing..)"
            + " anywhere. An annotation in a domain, incoming-adapter or infrastructure package"
            + " is reported; a transaction-API or TransactionBoundary dependency in a domain,"
            + " incoming-adapter or module-infrastructure package is reported; all findings are"
            + " collected into one violation. Which transaction a boundary opens is not"
            + " checked.")
```

## Helpers
