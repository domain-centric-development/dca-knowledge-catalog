---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — Overview"
tags: [reference]
evidence_for: /rule/tactical/dca-tac-025.md
---

[Full node and context](/rule/tactical/dca-tac-025.md). This is an evidence excerpt; retain the parent selection and caveats.

# Domain types must not hold bare primitives, strings or time types

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes, records, enums and interfaces in <module>.domain.. of every module root, the shared kernel's domain included - their instance fields and their methods, private ones included; constructors are not selected, the fields they fill are. Not selected: a wrapper value - a type assignable to the value or the id role with exactly one instance field - with everything it declares; synthetic and bridge members; equals, hashCode, toString and compareTo; the values() and valueOf(String) the language declares on an enum; a method that implements a method of a building block, such as a domain event's occurredOn() or a specification's isSatisfiedBy, and the field of the same name behind it. A boolean return is a question to the object - a predicate - and passes; a boolean field or parameter does not.

## Check

No selected field, return type or parameter type involves String, a primitive or its box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime, OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an identifier says whose it is through a typed id - generic type arguments included, so List<String> counts. BigDecimal, BigInteger, Duration and the project's own types pass. A value object with several components is checked like any other type: each component is a value object itself. A record's accessor is not reported again beside its field. An empty selection passes.

## .NET reading

**Selection.** Classes, records, structs, enums and interfaces in <Module>.Domain of every module root, the shared kernel's domain included, with their runtime type in the loaded assemblies - their declared instance fields and properties and their declared methods, private ones included; constructors are not selected, the members they fill are. Not selected: a wrapper value - a type assignable to IValue or IId with exactly one instance field - with everything it declares; compiler- generated members (a property's backing field, a record's EqualityContract, Deconstruct, PrintMembers); property accessors and operators; Equals, GetHashCode, ToString and CompareTo; an enum's members; a member that implements a building block's, such as a domain event's OccurredOn and EventId. A bool return is a question to the object - a predicate - and passes; a bool field, property or parameter does not.

**Check.** No selected field, property, return type or parameter type involves string, bool, a numeric primitive or char, a point in time (DateTime, DateTimeOffset, DateOnly, TimeOnly), or a bare Guid - an identifier says whose it is through a typed id - nullable and generic arguments and arrays included, so IReadOnlyList<string> counts. decimal, TimeSpan and the project's own types pass. A value object with several components is checked like any other type: each component is a value object itself. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-025",
        "Domain types must not hold bare primitives, strings or time types",
        "A value with rules of its own - a postal code, a quantity, a status, a moment, an"
            + " identifier - is a value object; held as a bare String, int, boolean, Instant or UUID its"
            + " validation is"
            + " repeated at every use or missing. A value object with several components holds"
            + " value objects too; only a wrapper - a value of exactly one component - holds the"
            + " primitive it wraps",
        arch -> {
          DcaMarkers markers = arch.layout().markers();
          Set<String> buildingBlocks = buildingBlockTypes(markers);
          List<String> violations = new ArrayList<>();
          for (JavaClass type :
              classesMatching(
                  arch,
                  c ->
                      JavaClass.Predicates.resideInAnyPackage(arch.allDomainPatterns()).test(c)
                          && !c.getModifiers().contains(JavaModifier.SYNTHETIC))) {
            if (isWrapperValue(type, markers)) {
              continue;
            }
            List<String> bare = new ArrayList<>();
            Set<String> exemptAccessors = new java.util.HashSet<>();
            for (JavaMethod method : type.getMethods()) {
              if (implementsBuildingBlock(type, method, buildingBlocks)) {
                exemptAccessors.add(method.getName());
              }
            }
            Set<String> reportedFields = new java.util.HashSet<>();
            for (JavaField field : type.getFields()) {
              if (field.getModifiers().contains(JavaModifier.STATIC)
                  || field.getModifiers().contains(JavaModifier.SYNTHETIC)
                  || exemptAccessors.contains(field.getName())) {
                continue;
              }
              String found = bareTypesIn(field.getType());
              if (!found.isEmpty()) {
                bare.add("field " + field.getName() + " is " + found);
                reportedFields.add(field.getName());
              }
            }
            for (JavaMethod method : type.getMethods()) {
              Set<JavaModifier> modifiers = method.getModifiers();
              if (modifiers.contains(JavaModifier.SYNTHETIC)
                  || modifiers.contains(JavaModifier.BRIDGE)
                  || PLATFORM_METHODS.contains(method.getName())
                  || isEnumImplicit(type, method)
                  || exemptAccessors.contains(method.getName())) {
                continue;
              }
              boolean accessorOfReportedField =
                  method.getRawParameterTypes().isEmpty()
                      && reportedFields.contains(method.getName());
              String returnType = method.getRawReturnType().getName();
              boolean predicate =
                  returnType.equals("boolean") || returnType.equals("java.lang.Boolean");
              String returned = bareTypesIn(method.getReturnType());
              if (!returned.isEmpty() && !accessorOfReportedField && !predicate) {
                bare.add(method.getName() + "() returns " + returned);
              }
              List<JavaType> parameters = method.getParameterTypes();
              for (int i = 0; i < parameters.size(); i++) {
                String taken = bareTypesIn(parameters.get(i));
                if (!taken.isEmpty()) {
                  bare.add(
                      method.getName() + "(...) takes " + taken + " as parameter " + (i + 1));
                }
              }
            }
            if (!bare.isEmpty()) {
              violations.add(
                  type.getName() + ": " + String.join("; ", bare.stream().sorted().toList()));
            }
          }
          fail(
              "Domain types must not hold bare primitives, strings or time types. Fix: wrap each"
                  + " in a value object that carries its rules - a value of one component"
                  + " may hold the primitive it wraps.",
              violations);
        })
    .experimental()
    .selecting(
        "Classes, records, enums and interfaces in <module>.domain.. of every module root, the"
            + " shared kernel's domain included - their instance fields and their methods,"
            + " private ones included; constructors are not selected, the fields they fill are."
            + " Not selected: a wrapper value - a type assignable to the value or the id role"
            + " with exactly one instance field - with everything it declares; synthetic and"
            + " bridge members; equals, hashCode, toString and compareTo; the values() and"
            + " valueOf(String) the language declares on an enum; a method that implements a"
            + " method of a building block, such as a domain event's occurredOn() or a"
            + " specification's isSatisfiedBy, and the field of the same name behind it. A boolean"
            + " return is a question to the object - a predicate - and passes; a boolean field or"
            + " parameter does not.")
    .checking(
        "No selected field, return type or parameter type involves String, a primitive or its"
            + " box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime,"
            + " OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an"
            + " identifier says whose it is through a typed id - generic type arguments"
            + " included, so List<String> counts. BigDecimal, BigInteger, Duration and the"
            + " project's own types pass. A value object with several components is checked"
            + " like any other type: each component is a value object itself. A record's"
            + " accessor is not reported again beside its field. An empty selection passes.",
        "wrap the primitive in a value object that carries its rules; a value of one"
            + " component may hold it")
```

## Helpers
