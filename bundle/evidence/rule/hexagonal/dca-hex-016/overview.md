---
type: Reference
title: "Diagnostic: adapters that publish an enum by its member name — Overview"
tags: [reference]
evidence_for: /rule/hexagonal/dca-hex-016.md
---

[Full node and context](/rule/hexagonal/dca-hex-016.md). This is an evidence excerpt; retain the parent selection and caveats.

# Diagnostic: adapters that publish an enum by its member name

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.adapter.. of every module root, incoming and outgoing, and their method calls whose target is an enum declared in <module>.domain.. or <module>.application..

## Check

Informational diagnostic only: lists every call of name() or toString() on such an enum - inside a string concatenation as well - and never fails. The enum value itself concatenated ("text" + value) or passed to a formatting or string-building call reaches the platform as an Object - the compiler erases its type from the call - so it is not visible and is not listed, nor is a serializer that writes the name on its own; whether the value leaves the process is not established either.

## .NET reading

**Selection.** Non-nested types in <module>.Adapter of every module root, incoming and outgoing, with their runtime type in the loaded assemblies, together with their nested, async state-machine and closure types; enums declared in a domain or application namespace of any module root.

**Check.** Informational diagnostic only: lists a method that turns such an enum into its member name as the IL shows it - ToString in any overload, called through a constrained call or on the boxed value; the boxed value passed straight into a string-building call (concatenation, formatting, joining, appending); an interpolation hole of the enum type; Enum.GetName or Enum.GetNames over it - and never fails. Compiler-generated methods, such as a record's generated PrintMembers and ToString, are not read. A boxed value stored first and formatted later, a serializer that writes names, and a name read through a generic helper are not seen; whether the text reaches a client stays with review.

## Implementation

```java
DcaRule.informational(
        "DCA-HEX-016",
        "Diagnostic: adapters that publish an enum by its member name",
        "A value an adapter publishes from an enum is spelled explicitly - a code per value on"
            + " the enum or a mapping in the adapter - never derived from the member's name."
            + " Renaming a member is a refactoring inside the code and must not change what a"
            + " client reads",
        arch -> {
          var inner = arch.inDomain().or(arch.inApplication());
          java.util.Set<String> observed = new java.util.TreeSet<>();
          for (JavaClass adapter : arch.classes()) {
            if (!arch.inAdapter().test(adapter)) {
              continue;
            }
            for (JavaMethodCall call : adapter.getMethodCallsFromSelf()) {
              JavaClass owner = call.getTargetOwner();
              // the compiler's lambda deserialisation repeats the calls of a lambda's body
              if (call.getOrigin().getName().equals("$deserializeLambda$")) {
                continue;
              }
              if ((call.getName().equals("name") || call.getName().equals("toString"))
                  && call.getTarget().getRawParameterTypes().isEmpty()
                  && owner.isEnum()
                  && inner.test(owner)) {
                observed.add(
                    call.getOrigin().getFullName()
                        + " spells "
                        + owner.getSimpleName()
                        + " by its member name ("
                        + call.getName()
                        + "()) - give the enum a code per value, or map it in the adapter");
              }
            }
          }
          return new ArrayList<>(observed);
        })
    .experimental()
    .selecting(
        "Classes in <module>.adapter.. of every module root, incoming and outgoing, and their"
            + " method calls whose target is an enum declared in <module>.domain.. or"
            + " <module>.application..")
    .checking(
        "Informational diagnostic only: lists every call of name() or toString() on such an"
            + " enum - inside a string concatenation as well - and never fails. The enum value"
            + " itself concatenated (\"text\" + value) or passed to a formatting or"
            + " string-building call reaches the platform as an Object - the compiler erases"
            + " its type from the call - so it is not visible and is not listed, nor is a"
            + " serializer that writes the name on its own; whether the value leaves the"
            + " process is not established either.")
```

## Helpers
