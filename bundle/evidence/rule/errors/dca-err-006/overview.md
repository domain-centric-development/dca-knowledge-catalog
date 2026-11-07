---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — Overview"
tags: [reference]
evidence_for: /rule/errors/dca-err-006.md
---

[Full node and context](/rule/errors/dca-err-006.md). This is an evidence excerpt; retain the parent selection and caveats.

# Diagnostic: incoming adapter packages that drive a use case without translating its failures

## Selection

Incoming adapter packages of every module root (<module>.adapter.incoming..) that hold at least one non-interface class depending on a class assignable to InputPort - the packages that drive the application.

## Check

Informational diagnostic only: when no class of the scan is assignable to DomainException or UseCaseException, it lists no package and says once that it cannot see the failures; otherwise it lists a package when no class in it - a central exception handler beside the adapters included - depends on a class assignable to DomainException or UseCaseException, nor refers to a case of a closed result, and never fails. A closed result is a sealed type that a method of an input port returns or that an input port's use-case interface binds as a type argument; its cases are its permitted subclasses, recursively. A reference to a case is read from the class file's constant pool as well as from the import model, so a pattern-matching switch whose arms never touch the bound case is seen. This is an approximation of an exhaustive switch: one reference to one case counts, whether it is a switch arm, a type test, a cast or a construction, and whether the switch covers every case is left to the compiler. A handler in a different package of the same module is not seen, and a caught type is not visible to the import model, so this does not establish that a package translates nothing. Beside the packages it lists every incoming-adapter class that refers - through the import model or its class file's constant pool, where a catch clause's type is recorded - to the abstract bases PortException, InputPortException or OutputPortException themselves: it catches or tests the port failures generically.

## .NET reading

**Selection.** Incoming adapter namespaces of every module root (<Module>.Adapter.Incoming) that hold at least one non-interface type depending on a type assignable to IInputPort - the namespaces that drive the application.

**Check.** Informational diagnostic only: when no type of the scan is assignable to DomainException or UseCaseException, it lists no namespace and says once that it cannot see the failures; otherwise it lists a namespace when no type in it - a central exception handler beside the adapters included - depends on a type assignable to DomainException or UseCaseException, nor on a case of a closed result, and never fails. A closed result is a type an input port answers with - a type argument of its use-case interface or the return type of one of its methods, a task unwrapped - that derives from one of the configured closed-result base types (FrameworkTypes.ClosedResultBaseTypes, matched by name; every preset names the generic base of a discriminated-union library, for example OneOf.OneOfBase); its cases are the generic arguments of that base. A type test, a cast, a case type in a function's or an action's signature (one handler per case) and a member call on the union base that names its cases all count, so this approximates an exhaustive switch: one reference to one case counts, and whether every case is handled is left to the compiler. A handler in a different namespace of the same module is not seen, and a caught type is not visible to the type model, so this does not establish that a namespace translates nothing. Beside the namespaces it lists every incoming-adapter type that catches - read from the exception-handling clauses of its methods' bodies, compiler-generated nested types such as async state machines included - or refers to the abstract bases PortException, InputPortException or OutputPortException themselves: it handles the port failures generically.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Modules in the incoming part of every adapters crate that name an input port.

**Check.** Informational - lists a module when no item in it names a DomainFailure or UseCaseFailure type nor a variant of a closed result, and never fails. A closed result is an enum an input-port trait answers with - named in an associated-type binding of its bounds (Output = ...) or in a method's return type, through any wrapper such as Result. A variant counts when a path names it through its enum or through a use of it, so a match over the variants is seen; whether the match is exhaustive is left to the compiler. When the workspace has neither a failure type nor a closed result, nothing is listed. It also lists a module that names one of the classification traits PortFailure, InputPortFailure or OutputPortFailure itself - a bound or a trait object over the base is the generic handler that answers every outcome the same way.

## Implementation

```java
DcaRule.informational(
        "DCA-ERR-006",
        "Diagnostic: incoming adapter packages that drive a use case without translating its"
            + " failures",
        "A package that drives the application and knows neither failure type nor a case of"
            + " a closed result either lets everything escape to a generic handler or catches a"
            + " generic type and answers every outcome the same way; whether it does is not"
            + " visible in the import model. A use case may return its expected refusals as"
            + " cases of a closed result instead of throwing them; a switch over those cases is"
            + " the translation then. An adapter that names the abstract base of the port"
            + " failures catches them generically and answers every outcome the same way",
        arch -> {
          String domainException = arch.layout().markers().domainException();
          String useCaseException = arch.layout().markers().useCaseException();
          boolean anyFailureType =
              arch.classes().stream()
                  .anyMatch(
                      type ->
                          !type.getName().equals(domainException)
                              && !type.getName().equals(useCaseException)
                              && (arch.layout().markers().is("domainException").test(type)
                                  || arch.layout()
                                      .markers()
                                      .is("useCaseException")
                                      .test(type)));
          if (!anyFailureType) {
            return List.of(
                "no class of the scan is assignable to "
                    + domainException
                    + " or "
                    + useCaseException
                    + ", so no package can be seen to name a failure - nothing is listed."
                    + " Where the project has failure types of its own, point the"
                    + " domainException and useCaseException roles at their base types"
                    + " (DcaMarkers.withDomainException / withUseCaseException).");
          }
          List<String> observed = new ArrayList<>();
          DcaMarkers markers = arch.layout().markers();
          Set<String> genericBases =
              Set.of(
                  markers.portException(),
                  markers.inputPortException(),
                  markers.outputPortException());
          for (JavaClass type : arch.classes()) {
            if (!arch.inIncomingAdapter().test(type)) {
              continue;
            }
            for (String base : genericBases.stream().sorted().toList()) {
              if (namesAnyOf(type, Set.of(base))) {
                observed.add(
                    type.getName()
                        + ": names the abstract base "
                        + base.substring(base.lastIndexOf('.') + 1)
                        + " - catch the named failures, each with its own answer");
              }
            }
          }
          Set<String> resultCases = casesOfClosedResults(arch);
          Map<String, List<JavaClass>> drivingByPackage = new TreeMap<>();
          Set<String> packagesThatName = new HashSet<>();
          for (JavaClass type : arch.classes()) {
            if (!arch.inIncomingAdapter().test(type)) {
              continue;
            }
            if (dependsOnAssignableTo(type, arch.layout().markers().is("domainException"))
                || dependsOnAssignableTo(type, arch.layout().markers().is("useCaseException"))
                || namesAnyOf(type, resultCases)) {
              packagesThatName.add(type.getPackageName());
            }
            if (!type.isInterface()
                && dependsOnAssignableTo(type, arch.layout().markers().is("inputPort"))) {
              drivingByPackage
                  .computeIfAbsent(type.getPackageName(), pkg -> new ArrayList<>())
                  .add(type);
            }
          }
          drivingByPackage.forEach(
              (pkg, driving) -> {
                if (packagesThatName.contains(pkg)) {
                  return;
                }
                observed.add(
                    pkg
                        + ": drives an input port and names neither a failure type of the inner"
                        + " layers nor a case of a closed result ("
                        + driving.stream().map(JavaClass::getSimpleName).sorted().toList()
                        + ")");
              });
          return observed;
        })
    .selecting(
        "Incoming adapter packages of every module root (<module>.adapter.incoming..) that hold"
            + " at least one non-interface class depending on a class assignable to InputPort -"
            + " the packages that drive the application.")
    .checking(
        "Informational diagnostic only: when no class of the scan is assignable to"
            + " DomainException or UseCaseException, it lists no package and says once that it"
            + " cannot see the failures; otherwise it lists a package when no class in it - a"
            + " central exception handler beside the adapters included - depends on a class"
            + " assignable to DomainException or UseCaseException, nor refers to a case of a"
            + " closed result, and never fails. A closed result is a sealed type that a method"
            + " of an input port returns or that an input port's use-case interface binds as a"
            + " type argument; its cases are its permitted subclasses, recursively. A reference"
            + " to a case is read from the class file's constant pool as well as from the"
            + " import model, so a pattern-matching switch whose arms never touch the bound"
            + " case is seen. This is an approximation of an exhaustive switch: one reference"
            + " to one case counts, whether it is a switch arm, a type test, a cast or a"
            + " construction, and whether the switch covers every case is left to the compiler."
            + " A handler in a different package of the same module is not seen, and a caught"
            + " type is not visible to the import model, so this does not establish that a"
            + " package translates nothing. Beside the packages it lists every incoming-adapter"
            + " class that refers - through the import model or its class file's constant pool,"
            + " where a catch clause's type is recorded - to the abstract bases PortException,"
            + " InputPortException or OutputPortException themselves: it catches or tests the"
            + " port failures generically.")
```

## Helpers
