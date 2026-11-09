---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — Overview"
tags: [reference]
evidence_for: /rule/tactical/dca-tac-025.md
---

[Full node and context](/rule/tactical/dca-tac-025.md). This is an evidence excerpt; retain the parent selection and caveats.

# Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes, records, enums and interfaces in <module>.domain.. of every module root, the shared kernel's domain included - their instance fields and their methods, private ones included; constructors are not selected, the fields they fill are. Not selected: a wrapper value - a type assignable to the value or the id role with exactly one instance field - with everything it declares; a type declared inside a value or an id, such as the value's own error shapes, which carry the input it refused; a failure - a type of the domain-exception or use-case-exception role; synthetic and bridge members; equals, hashCode, toString and compareTo; the values() and valueOf(String) the language declares on an enum; a method that implements a method of a building block, such as a domain event's occurredOn() or a specification's isSatisfiedBy, and the field of the same name behind it. A field whose type is boolean or Boolean - a single yes/no fact - and a boolean return - a question to the object, a predicate - pass; a boolean parameter and a public non-final boolean field, flag arguments, do not. A boolean parameter of the factory that rebuilds a stored object - a static method returning its own type and named as configured, reconstitute or restore by default, case ignored - passes.

## Check

No selected field, return type or parameter type involves String, a primitive or its box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime, OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an identifier says whose it is through a typed id - generic type arguments included, so List<String> counts. BigDecimal, BigInteger, Duration and the project's own types pass. A field typed boolean or Boolean and a method returning one pass; a boolean among the parameters is a flag argument and counts - except in the reconstituting factory, whose other parameters are checked like any other - and so do a public non-final boolean field, which anyone may set, and a List<Boolean> field. A value object with several components is checked like any other type: each component is a value object itself. A record's accessor is not reported again beside its field. A reported type with exactly one instance field that is no value or id is told to carry the value or id role to count as a wrapper. A domain enum with exactly two constants that name one fact and its negation is a boolean in disguise and is reported where it is declared: the pairs YES/NO, TRUE/FALSE, ON/OFF, PRESENT/ABSENT, ENABLED/DISABLED, and any X with NOT_X, NO_X, NON_X or UN_X / UNX (compared case-insensitively, underscores ignored). A two-constant enum whose constants have names of their own (for example OPEN/CLOSED) passes. An empty selection passes.

## .NET reading

**Selection.** Classes, records, structs, enums and interfaces in <Module>.Domain of every module root, the shared kernel's domain included, with their runtime type in the loaded assemblies - their declared instance fields and properties and their declared methods, private ones included; constructors are not selected, the members they fill are. Not selected: a wrapper value - a type assignable to IValue or IId with exactly one instance field - with everything it declares; a type declared inside a value or an id, such as the value's own error shapes, which carry the input it refused; a failure - a type of the domain-exception or use-case-exception role; compiler- generated members (a property's backing field, a record's EqualityContract, Deconstruct, PrintMembers); property accessors and operators; Equals, GetHashCode, ToString and CompareTo; an enum's members; a member that implements a building block's, such as a domain event's OccurredOn and EventId. A field typed bool or bool? - a single yes/no fact - and a bool return - a question to the object, a predicate - pass, and so does a bool property without a public setter (get-only, a private or init setter); a bool parameter, a bool property with a public setter and a public non-readonly bool field are flag arguments and do not. A bool parameter of the factory that rebuilds a stored object - a static method returning its own type and named as configured, Reconstitute or Restore by default, case ignored - passes.

**Check.** No selected field, property, return type or parameter type involves string, bool, a numeric primitive or char, a point in time (DateTime, DateTimeOffset, DateOnly, TimeOnly), or a bare Guid - an identifier says whose it is through a typed id - nullable and generic arguments and arrays included, so IReadOnlyList<string> counts. decimal, TimeSpan and the project's own types pass. A field or a property typed bool or bool? and a method returning one pass, unless anyone may set it - a public setter, a public non-readonly field; a bool among the parameters is a flag argument and counts - except in the reconstituting factory, whose other parameters are checked like any other - and so does an IReadOnlyList<bool>. A value object with several components is checked like any other type: each component is a value object itself. A reported type with exactly one instance field that is no value or id is told to carry the value or id role to count as a wrapper. A domain enum with exactly two members that name one fact and its negation is a boolean in disguise and is reported where it is declared: the pairs Yes/No, True/False, On/Off, Present/Absent, Enabled/Disabled, and any X with NotX, NoX, NonX or UnX (compared case-insensitively, underscores ignored). A two-member enum whose members have names of their own (for example Open/Closed) passes. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Types, fields and pub signatures in every domain crate, the shared kernel's included. Not selected: a single-field newtype that implements Value or Id, failures, and trait methods of a building block.

**Check.** No field, parameter or return type, through generic arguments, is String, &str, a primitive, a time type (std::time::SystemTime, chrono, time) or a bare Uuid. A private field of type bool - a single yes/no fact - and a bool return - a predicate - pass; a bool parameter and a pub bool struct field, flag arguments, do not. A bool parameter of the factory that rebuilds a stored value - an associated function without a receiver that returns Self or the type, named as [workspace.metadata.dca] reconstituting-factories lists, reconstitute and restore by default, case ignored - passes; its other parameters are checked. The two-variant enum that names one fact and its negation, which the other languages report as a boolean in disguise, is not checked by the Rust suite yet.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-025",
        "Domain types must not hold bare primitives, strings or time types; a boolean only as a"
            + " field or a predicate",
        "A value with rules of its own - a postal code, a quantity, a moment, an identifier -"
            + " is a value object; held as a bare String, int, Instant or UUID its validation is"
            + " repeated at every use or missing. A value object with several components holds"
            + " value objects too; only a wrapper - a value of exactly one component - holds the"
            + " primitive it wraps. A single yes/no fact may stay a boolean field: the type is"
            + " told (complete()) and answers (isCompleted()). A boolean parameter is a flag"
            + " argument - setCompleted(true) lets the caller set the state instead of"
            + " triggering the behaviour - except in the factory that rebuilds a stored object,"
            + " which hands the stored fact back to the type that holds it. Three or more"
            + " states, or transitions with rules, are an enum or a value",
        arch -> {
          DcaMarkers markers = arch.layout().markers();
          Set<String> reconstituting =
              arch.layout().reconstitutingFactories().stream()
                  .map(name -> name.toLowerCase(java.util.Locale.ROOT))
                  .collect(java.util.stream.Collectors.toSet());
          Set<String> buildingBlocks = buildingBlockTypes(markers);
          List<String> violations = new ArrayList<>();
          for (JavaClass type :
              classesMatching(
                  arch,
                  c ->
                      arch.inDomain().test(c)
                          && !c.getModifiers().contains(JavaModifier.SYNTHETIC))) {
            if (isWrapperValue(type, markers)
                || isFailure(type, markers)
                || nestedInWrapperOrValue(type, markers)) {
              continue;
            }
            List<String> bare = new ArrayList<>();
            String negation = booleanInDisguise(type);
            if (negation != null) {
              bare.add(negation);
            }
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
              if (isBoolean(field.getRawType())) {
                if (field.getModifiers().contains(JavaModifier.PUBLIC)
                    && !field.getModifiers().contains(JavaModifier.FINAL)) {
                  bare.add(
                      "field "
                          + field.getName()
                          + " is a public boolean anyone may set - a flag argument");
                }
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
              boolean predicate = isBoolean(method.getRawReturnType());
              String returned = bareTypesIn(method.getReturnType());
              if (!returned.isEmpty() && !accessorOfReportedField && !predicate) {
                bare.add(method.getName() + "() returns " + returned);
              }
              boolean rebuilds = isReconstitutingFactory(type, method, reconstituting);
              List<JavaType> parameters = method.getParameterTypes();
              for (int i = 0; i < parameters.size(); i++) {
                if (rebuilds && isBoolean(method.getRawParameterTypes().get(i))) {
                  continue;
                }
                String taken = bareTypesIn(parameters.get(i));
                if (!taken.isEmpty()) {
                  bare.add(
                      method.getName() + "(...) takes " + taken + " as parameter " + (i + 1));
                }
              }
            }
            if (!bare.isEmpty()) {
              violations.add(
                  type.getName()
                      + ": "
                      + String.join("; ", bare.stream().sorted().toList())
                      + (instanceFieldCount(type) == 1 && !reportedFields.isEmpty()
                          ? " - it has one field: mark it as a value or an id ("
                              + markers.marker("value")
                              + ") to count as a wrapper"
                          : ""));
            }
          }
          fail(
              "Domain types must not hold bare primitives, strings or time types; a boolean only"
                  + " as a field or a predicate. Fix: wrap each in a value object that carries its"
                  + " rules - a value of one component may hold the primitive it wraps; replace a"
                  + " boolean parameter by a method that names the behaviour.",
              violations);
        })
    .experimental()
    .selecting(
        "Classes, records, enums and interfaces in <module>.domain.. of every module root, the"
            + " shared kernel's domain included - their instance fields and their methods,"
            + " private ones included; constructors are not selected, the fields they fill are."
            + " Not selected: a wrapper value - a type assignable to the value or the id role"
            + " with exactly one instance field - with everything it declares; a type declared"
            + " inside a value or an id, such as the value's own error shapes, which carry the"
            + " input it refused; a failure - a type of the domain-exception or use-case-exception"
            + " role; synthetic and"
            + " bridge members; equals, hashCode, toString and compareTo; the values() and"
            + " valueOf(String) the language declares on an enum; a method that implements a"
            + " method of a building block, such as a domain event's occurredOn() or a"
            + " specification's isSatisfiedBy, and the field of the same name behind it. A field"
            + " whose type is boolean or Boolean - a single yes/no fact - and a boolean return -"
            + " a question to the object, a predicate - pass; a boolean parameter and a public"
            + " non-final boolean field, flag arguments, do not. A boolean parameter of the"
            + " factory that rebuilds a stored object - a static method returning its own"
            + " type and named as configured, reconstitute or restore by default, case"
            + " ignored - passes.")
    .checking(
        "No selected field, return type or parameter type involves String, a primitive or its"
            + " box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime,"
            + " OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an"
            + " identifier says whose it is through a typed id - generic type arguments"
            + " included, so List<String> counts. BigDecimal, BigInteger, Duration and the"
            + " project's own types pass. A field typed boolean or Boolean and a method"
            + " returning one pass; a boolean among the parameters is a flag argument and"
            + " counts - except in the reconstituting factory, whose other parameters are"
            + " checked like any other - and so do a public non-final boolean field, which anyone may set, and"
            + " a List<Boolean> field. A value object with several components is checked"
            + " like any other type: each component is a value object itself. A record's"
            + " accessor is not reported again beside its field. A reported type with exactly one"
            + " instance field that is no value or id is told to carry the value or id role to"
            + " count as a wrapper. A domain enum with exactly two constants that name one fact"
            + " and its negation is a boolean in disguise and is reported where it is declared:"
            + " the pairs YES/NO, TRUE/FALSE, ON/OFF, PRESENT/ABSENT, ENABLED/DISABLED, and any"
            + " X with NOT_X, NO_X, NON_X or UN_X / UNX (compared case-insensitively, underscores"
            + " ignored). A two-constant enum whose constants have names of their own (for"
            + " example OPEN/CLOSED) passes. An empty selection passes.",
        "wrap the primitive in a value object that carries its rules; a value of one"
            + " component may hold it; a boolean parameter becomes a method that names the"
            + " behaviour - complete() instead of setCompleted(true)")
```

## Helpers
