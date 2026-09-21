---
type: Rule
id: DCA-TAC-003
title: Aggregate Roots must not have fields with other Aggregate Root types
rule: "Vernon's Aggregate Design Rule #3: reference other Aggregates by identity to keep aggregate boundaries and transactional consistency intact."
constraint: Aggregate Roots must not have fields with other Aggregate Root types.
selects: "Non-interface classes anywhere under scan assignable to AggregateRoot, abstract ones included."
checks: "No instance field - inherited ones included, static ones excluded - involves AggregateRoot through its type, arrays or nested generic arguments. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid."
enforced_by: "TacticalPatternRules#DCA-TAC-003"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Aggregate Roots must not have fields with other Aggregate Root types

## Selection

Non-interface classes anywhere under scan assignable to AggregateRoot, abstract ones included.

## Check

No instance field - inherited ones included, static ones excluded - involves AggregateRoot through its type, arrays or nested generic arguments. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IAggregateRoot, abstract ones included.

**Check.** No instance field or property - inherited ones included, static ones excluded - involves IAggregateRoot through its type, arrays or nested generic arguments. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-003",
        "Aggregate Roots must not have fields with other Aggregate Root types",
        "Vernon's Aggregate Design Rule #3: reference other Aggregates by identity to keep"
            + " aggregate boundaries and transactional consistency intact",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass aggregate :
              concreteClassesAssignableTo(arch, arch.layout().markers().aggregateRoot())) {
            for (JavaField field : TypeInspection.instanceFields(aggregate)) {
              for (JavaClass involved : TypeInspection.involvedTypes(field, aggregate)) {
                if (isConcreteAggregateRoot(involved, arch.layout().markers())) {
                  violations.add(
                      fieldDescription(aggregate, field, involved)
                          + " which is another aggregate root");
                }
              }
            }
          }
          fail(
              "Aggregates must reference other aggregates by ID only (Vernon's Rule #3).",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to AggregateRoot, "
            + "abstract ones included.")
    .checking(
        "No instance field - inherited ones included, static ones excluded - involves AggregateRoot through its type, arrays or nested generic arguments. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(DcaArchitecture arch, String marker) {
  return classesMatching(arch, c -> c.isAssignableTo(marker) && !c.isInterface());
}
```

### `isConcreteAggregateRoot`

```java
private static boolean isConcreteAggregateRoot(JavaClass type, DcaMarkers markers) {
  return type.isAssignableTo(markers.aggregateRoot());
}
```

### `fieldDescription`

```java
/**
   * {@code Owner has field 'f' of type X} when the field's own type is the offender, {@code Owner
   * has field 'f' containing X} when it is hidden in a container or type argument.
   */
  private static String fieldDescription(JavaClass owner, JavaField field, JavaClass involved) {
    String relation = involved.equals(field.getRawType()) ? "' of type " : "' containing ";
    return owner.getName() + " has field '" + field.getName() + relation + involved.getName();
  }
```

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```

### `TypeInspection.instanceFields`

```java
/**
   * The instance fields of a class, inherited ones included, sorted by name so that reports are
   * stable across runs. Static fields — constants, counters — are not part of an object's state.
   */
  static List<JavaField> instanceFields(JavaClass type) {
    return type.getAllFields().stream()
        .filter(field -> !field.getModifiers().contains(JavaModifier.STATIC))
        .sorted(Comparator.comparing(JavaField::getName))
        .toList();
  }
```

### `TypeInspection.involvedTypes`

```java
/**
   * Every raw class a type involves: the erasure, array component types and, recursively, all
   * generic type arguments and wildcard bounds. Type variables contribute their bounds. In
   * encounter order, without duplicates.
   */
  static List<JavaClass> involvedTypes(JavaType type) {
    Set<JavaClass> involved = new LinkedHashSet<>();
    collect(type, Map.of(), involved, new HashSet<>());
    return new ArrayList<>(involved);
  }

/**
   * Every raw class a field involves as seen from {@code viewedFrom}, which declares or inherits
   * the field: a type variable of the field's owner is replaced by the type argument the subclass
   * chain binds it to, through any number of levels and inside containers. An unbound variable
   * contributes its bounds.
   */
  static List<JavaClass> involvedTypes(JavaField field, JavaClass viewedFrom) {
    Set<JavaClass> involved = new LinkedHashSet<>();
    collect(field.getType(), typeArgumentBindings(viewedFrom), involved, new HashSet<>());
    return new ArrayList<>(involved);
  }
```

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

### `TypeInspection.collect`

```java
private static void collect(
    JavaType type,
    Map<String, JavaType> bindings,
    Set<JavaClass> involved,
    Set<String> resolving) {
  if (type instanceof JavaTypeVariable<?> variable) {
    String key = variableKey(variable);
    JavaType bound = bindings.get(key);
    if (bound != null && resolving.add(key)) {
      collect(bound, bindings, involved, resolving);
      resolving.remove(key);
    } else {
      involved.addAll(type.getAllInvolvedRawTypes());
    }
  } else if (type instanceof JavaParameterizedType parameterized) {
    involved.add(parameterized.toErasure());
    for (JavaType argument : parameterized.getActualTypeArguments()) {
      collect(argument, bindings, involved, resolving);
    }
  } else if (type instanceof JavaWildcardType wildcard) {
    for (JavaType bound : wildcard.getUpperBounds()) {
      collect(bound, bindings, involved, resolving);
    }
    for (JavaType bound : wildcard.getLowerBounds()) {
      collect(bound, bindings, involved, resolving);
    }
  } else if (type instanceof JavaGenericArrayType array) {
    collect(array.getComponentType(), bindings, involved, resolving);
  } else {
    involved.addAll(type.getAllInvolvedRawTypes());
  }
}
```

### `TypeInspection.typeArgumentBindings`

```java
/**
   * What each superclass's type variables are bound to, walking up from {@code type}: for {@code
   * OrderResult extends Intermediate<Order>} and {@code Intermediate<U> extends Base<List<U>>} the
   * map holds {@code Intermediate.U -> Order} and {@code Base.T -> List<U>}; {@link #collect}
   * resolves the chain when it meets {@code U} inside {@code List<U>}.
   */
  private static Map<String, JavaType> typeArgumentBindings(JavaClass type) {
    Map<String, JavaType> bindings = new HashMap<>();
    Optional<JavaType> superclass = type.getSuperclass();
    while (superclass.isPresent()) {
      JavaType current = superclass.get();
      JavaClass erasure = current.toErasure();
      if (current instanceof JavaParameterizedType parameterized) {
        List<JavaTypeVariable<JavaClass>> parameters = erasure.getTypeParameters();
        List<JavaType> arguments = parameterized.getActualTypeArguments();
        for (int i = 0; i < Math.min(parameters.size(), arguments.size()); i++) {
          bindings.put(variableKey(parameters.get(i)), arguments.get(i));
        }
      }
      superclass = erasure.getSuperclass();
    }
    return bindings;
  }
```

### `TypeInspection.variableKey`

```java
/** A type variable is identified by its owner and name; {@code T} of two classes differ. */
  private static String variableKey(JavaTypeVariable<?> variable) {
    Object owner = variable.getOwner();
    String ownerName =
        owner instanceof JavaClass javaClass
            ? javaClass.getName()
            : owner instanceof JavaMethod method ? method.getFullName() : String.valueOf(owner);
    return ownerName + "#" + variable.getName();
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-003",
    "Aggregate Roots must not have fields with other Aggregate Root types",
    "Vernon's Aggregate Design Rule #3: reference other Aggregates by identity to keep"
    + " aggregate boundaries and transactional consistency intact",
    arch =>
    {
        var violations = new List<string>();
        foreach (var aggregate in ConcreteTypesAssignableTo(arch, arch.Layout.Markers.AggregateRoot))
        {
            foreach (var member in InstanceDataMembers(arch, aggregate))
            {
                if (IsConcreteAggregateRoot(arch, member.Type))
                {
                    violations.Add($"{FieldDescription(aggregate, member)} which is another aggregate root");
                }

                foreach (var element in member.ElementTypes)
                {
                    if (IsConcreteAggregateRoot(arch, element))
                    {
                        violations.Add($"{ContainsDescription(aggregate, member, element)} which is an aggregate root");
                    }
                }
            }
        }

        DcaRule.Fail("Aggregates must reference other aggregates by ID only (Vernon's Rule #3).", violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IAggregateRoot, "
        + "abstract ones included.")
    .Checking(
    "No instance field or property - inherited ones included, static ones excluded - involves IAggregateRoot through its type, arrays or nested generic arguments. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.")
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
