---
type: Reference
title: Outgoing adapters must not call state-changing methods of aggregate roots — Overview
tags: [reference]
evidence_for: /rule/hexagonal/dca-hex-021.md
---

[Full node and context](/rule/hexagonal/dca-hex-021.md). This is an evidence excerpt; retain the parent selection and caveats.

# Outgoing adapters must not call state-changing methods of aggregate roots

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every class in <module>.adapter.outgoing.. of every module root, with the classes nested in it, and the method calls they make on a type carrying the aggregate-root role. A project without a type carrying the aggregate-root role selects nothing.

## Check

No code unit calls a method of a type carrying the aggregate-root role that changes its state - a non-static method that returns void, or one that sets a field of its own class; the called method is read where it is declared, methods inherited from the root's superclasses included. Static methods - factories, reconstitution - and methods that return a value without setting a field are queries and pass. A method declared by a type in the package of the aggregate-root role's own marker - the vocabulary's base, such as its domain-event bookkeeping that a publisher clears after publishing - is not the aggregate's behaviour and passes. A change made by writing to storage directly, past the aggregate, is not a call and is not seen. An empty selection passes.

## .NET reading

**Selection.** Every non-nested type in the outgoing adapter layer of every module root - by default <Module>.Adapter.Outgoing - with its runtime type in the loaded assemblies, together with its nested, async state-machine and closure types, and the calls their IL makes. Nothing is selected when no type carries the aggregate-root role.

**Check.** No code unit calls a method of a type carrying the aggregate-root role that changes its state - a non-static method that returns void, Task or ValueTask without a result, a property setter, or one that sets a field of its own class; the called method is read where it is declared, methods inherited from the root's base classes included. An init accessor runs only while the object is built and passes. Static methods - factories, reconstitution - and methods that return a value without setting a field are queries and pass. A method declared by a type in the namespace of the aggregate-root role's own marker - the vocabulary's base, such as its domain-event bookkeeping that a publisher clears after publishing - is not the aggregate's behaviour and passes. A change made by writing to storage directly, past the aggregate, is not a call and is not seen. An empty selection passes.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** Function bodies in the outgoing module of every adapters crate. Nothing is selected when no type implements AggregateRoot.

**Check.** No body calls, on a parameter, a local binding or a field of self whose type implements AggregateRoot, a method that takes &mut self - in Rust the receiver says which methods change the aggregate. A method of a building-block trait (clearing the recorded events after publishing) passes. A change written to storage directly, past the aggregate, is not seen. Planned: the suite does not implement it yet.

## Implementation

```java
DcaRule.check(
        "DCA-HEX-021",
        "Outgoing adapters must not call state-changing methods of aggregate roots",
        "An aggregate's state changes through its own methods, each with its guard and its"
            + " event, and the application decides when one runs. An outgoing adapter that"
            + " calls one changes the aggregate on a path no use case owns, outside the"
            + " transaction the use case draws and without the events it publishes. The"
            + " adapter stores and loads what the aggregate holds",
        arch -> {
          DescribedPredicate<JavaClass> aggregateRoot =
              arch.layout().markers().is("aggregateRoot");
          if (arch.classes().stream().noneMatch(aggregateRoot)) {
            return;
          }
          String marker = arch.layout().markers().aggregateRoot();
          String vocabulary =
              marker.contains(".") ? marker.substring(0, marker.lastIndexOf('.')) : "";
          DescribedPredicate<JavaClass> outgoing = arch.inOutgoingAdapter();
          java.util.Set<String> violations = new java.util.TreeSet<>();
          for (JavaClass adapter : arch.classes()) {
            if (!outgoing.test(adapter)) {
              continue;
            }
            for (JavaMethodCall call : adapter.getMethodCallsFromSelf()) {
              if (call.getOrigin().getName().equals("$deserializeLambda$")
                  || !aggregateRoot.test(call.getTargetOwner())) {
                continue;
              }
              String change = stateChangeOf(call, vocabulary);
              if (change != null) {
                violations.add(
                    call.getOrigin().getFullName()
                        + " calls "
                        + call.getTargetOwner().getSimpleName()
                        + "."
                        + call.getName()
                        + "(), which "
                        + change);
              }
            }
          }
          if (!violations.isEmpty()) {
            throw new DcaRuleViolation(
                "Outgoing adapters must not call state-changing methods of aggregate roots."
                    + " Fix: let a use case load the aggregate, call the method and save it;"
                    + " the adapter only stores what the aggregate holds.",
                new ArrayList<>(violations));
          }
        })
    .experimental()
    .selecting(
        "Every class in <module>.adapter.outgoing.. of every module root, with the classes"
            + " nested in it, and the method calls they make on a type carrying the"
            + " aggregate-root role. A project without a type carrying the aggregate-root role"
            + " selects nothing.")
    .checking(
        "No code unit calls a method of a type carrying the aggregate-root role that changes"
            + " its state - a non-static method that returns void, or one that sets a field of"
            + " its own class; the called method is read where it is declared, methods"
            + " inherited from the root's superclasses included. Static methods - factories,"
            + " reconstitution - and methods that return a value without setting a field are"
            + " queries and pass. A method declared by a type in the package of the"
            + " aggregate-root role's own marker - the vocabulary's base, such as its"
            + " domain-event bookkeeping that a publisher clears after publishing - is not the"
            + " aggregate's behaviour and passes. A change made by writing to storage directly, past the"
            + " aggregate, is not a call and is not seen. An empty selection passes.",
        "let a use case load the aggregate, call the method and save it; the adapter only"
            + " stores what the aggregate holds")
```

## Helpers
