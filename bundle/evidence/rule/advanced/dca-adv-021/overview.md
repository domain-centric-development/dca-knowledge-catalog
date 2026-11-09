---
type: Reference
title: Domain services are used only by the application and by other domain services — Overview
tags: [reference]
evidence_for: /rule/advanced/dca-adv-021.md
---

[Full node and context](/rule/advanced/dca-adv-021.md). This is an evidence excerpt; retain the parent selection and caveats.

# Domain services are used only by the application and by other domain services

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every class under scan outside the application layer that does not carry the domain-service role, with the classes nested in it - the domain model, the adapters of both directions, the composition root (the infrastructure layer) and classes outside every layer. A class nested in an application class or in a domain service counts as its outer class and is not selected.

## Check

None of them calls a method of, reads a field of, references a method of or instantiates a type carrying the domain-service role. A class in the infrastructure layer - the composition root - may construct one (a constructor call or a constructor reference) to hand it to a use case; a call there is reported. Naming the type as a parameter, a field or a return type is not an access and is not reported. An empty selection passes.

## .NET reading

**Selection.** Every type under scan, with its runtime type in the loaded assemblies, outside the application layer that does not carry the domain-service role - the domain model, the adapters of both directions, the composition root (the infrastructure layer) and types outside every layer - with the types nested in it, compiler-generated state machines and closures included. A type nested in an application type or in a domain service counts as its outer type and is not selected.

**Check.** No method body calls a method or property of, constructs, or makes a delegate of a method of a type carrying the domain-service role. A type in the infrastructure layer - the composition root - may construct one to hand it to a use case; a call there is reported. Naming the type as a parameter, a field or a return type is not a use and is not reported; a public field of a service read directly is not seen. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Every function body - free functions and the methods of impl blocks - in every crate except the application crates, the impls of a type that implements DomainService excluded. A domain service is a type that implements DomainService, as DCA-ADV-010 selects it: Rust marks no module, so a module of free functions is no domain service by this rule.

**Check.** No body names a type that implements DomainService as an expression (a struct literal, a unit value, an associated function), nor calls a method on a parameter, a local binding or a field of self whose type implements it, nor on one built in place. In an infrastructure or bootstrap crate - the composition root - a construction (a struct literal, a unit value, an associated function without a receiver that returns Self) passes; a call there is reported. A parameter or a field of that type alone is not reported; a call through a generic bound or a trait object is not seen.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-021",
        "Domain services are used only by the application and by other domain services",
        "A domain service holds logic that spans aggregates, and the use case decides when it"
            + " runs and puts its outcome into the result. A model type, a read model, an"
            + " adapter or the composition root that calls one takes that decision outside the"
            + " application - the incoming adapter and the model type are each held by a"
            + " narrower rule too (DCA-HEX-012, DCA-ADV-019)",
        arch -> {
          var domainService = arch.layout().markers().is("domainService");
          var inApplication = arch.inApplication();
          var inInfrastructure = arch.inInfrastructure();
          List<String> violations = new ArrayList<>();
          for (JavaClass caller : arch.classes()) {
            JavaClass outermost = outermost(caller);
            if (inApplication.test(outermost) || domainService.test(outermost)) {
              continue;
            }
            boolean compositionRoot = inInfrastructure.test(outermost);
            for (JavaAccess<?> access : caller.getAccessesFromSelf()) {
              JavaClass target = access.getTargetOwner();
              if (!domainService.test(target)) {
                continue;
              }
              boolean construction =
                  access instanceof JavaConstructorCall
                      || access instanceof JavaConstructorReference;
              if (compositionRoot && construction) {
                continue;
              }
              violations.add(access.getDescription());
            }
          }
          failIfAny(
              violations.stream().distinct().sorted().toList(),
              "Domain services are used only by the application and by other domain services."
                  + " Fix: let the use case call the domain service and carry its outcome in the"
                  + " result; the composition root constructs the service and hands it to the"
                  + " use case.");
        })
    .experimental()
    .selecting(
        "Every class under scan outside the application layer that does not carry the"
            + " domain-service role, with the classes nested in it - the domain model, the"
            + " adapters of both directions, the composition root (the infrastructure layer)"
            + " and classes outside every layer. A class nested in an application class or in"
            + " a domain service counts as its outer class and is not selected.")
    .checking(
        "None of them calls a method of, reads a field of, references a method of or"
            + " instantiates a type carrying the domain-service role. A class in the"
            + " infrastructure layer - the composition root - may construct one (a constructor"
            + " call or a constructor reference) to hand it to a use case; a call there is"
            + " reported. Naming the type as a parameter, a field or a return type is not an"
            + " access and is not reported. An empty selection passes.",
        "let the use case call the domain service and carry its outcome in the result; the"
            + " composition root only constructs it")
```

## Helpers
