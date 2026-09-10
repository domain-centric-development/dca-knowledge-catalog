---
type: Rule
id: DCA-TAC-008
title: Value Objects must not contain Aggregate Roots or Entities
rule: A Value Object is defined by its attributes; holding an object with identity would give it a lifecycle it must not have.
constraint: Value Objects must not contain Aggregate Roots or Entities.
selects: "Non-interface classes anywhere under scan assignable to Value - records, enums and hand-written classes alike."
checks: "No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot or Entity. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid."
enforced_by: "TacticalPatternRules#DCA-TAC-008"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Objects must not contain Aggregate Roots or Entities

## Selection

Non-interface classes anywhere under scan assignable to Value - records, enums and hand-written classes alike.

## Check

No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot or Entity. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IValue - records, structs, enums and hand-written classes alike.

**Check.** No instance state, including inherited state, arrays and nested generic arguments, involves IAggregateRoot or IEntity. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-008",
        "Value Objects must not contain Aggregate Roots or Entities",
        "A Value Object is defined by its attributes; holding an object with identity would give"
            + " it a lifecycle it must not have",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
            for (JavaField field : TypeInspection.instanceFields(valueObject)) {
              for (JavaClass involved : TypeInspection.involvedTypes(field, valueObject)) {
                if (isConcreteAggregateRoot(involved)) {
                  violations.add(
                      fieldDescription(valueObject, field, involved)
                          + " which is an aggregate root");
                }
                if (isConcreteNonRootEntity(involved)) {
                  violations.add(
                      fieldDescription(valueObject, field, involved) + " which is an entity");
                }
              }
            }
          }
          fail(
              "Value Objects must only contain other Value Objects or primitives (Vernon's DDD).",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to Value - records, enums "
            + "and hand-written classes alike.")
    .checking(
        "No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot or Entity. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(
    DcaArchitecture arch, Class<?> marker) {
  return classesMatching(arch, c -> c.isAssignableTo(marker) && !c.isInterface());
}
```

### `isConcreteAggregateRoot`

```java
private static boolean isConcreteAggregateRoot(JavaClass type) {
  return type.isAssignableTo(AggregateRoot.class);
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

### `isConcreteNonRootEntity`

```java
private static boolean isConcreteNonRootEntity(JavaClass type) {
  return type.isAssignableTo(Entity.class) && !type.isAssignableTo(AggregateRoot.class);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-008",
    "Value Objects must not contain Aggregate Roots or Entities",
    "A Value Object is defined by its attributes; holding an object with identity would give it a lifecycle it must not have",
    arch =>
    {
        var violations = new List<string>();
        foreach (var valueObject in ConcreteTypesAssignableTo(arch, typeof(IValue)))
        {
            foreach (var member in DataMembers(arch, valueObject))
            {
                if (IsConcreteAggregateRoot(arch, member.Type))
                {
                    violations.Add($"{FieldDescription(valueObject, member)} which is an aggregate root");
                }

                if (IsConcreteNonRootEntity(arch, member.Type))
                {
                    violations.Add($"{FieldDescription(valueObject, member)} which is an entity");
                }

                foreach (var element in member.ElementTypes)
                {
                    if (IsConcreteAggregateRoot(arch, element))
                    {
                        violations.Add($"{ContainsDescription(valueObject, member, element)} which is an aggregate root");
                    }

                    if (IsConcreteNonRootEntity(arch, element))
                    {
                        violations.Add($"{ContainsDescription(valueObject, member, element)} which is an entity");
                    }
                }
            }
        }

        DcaRule.Fail("Value Objects must only contain other Value Objects or primitives (Vernon's DDD).", violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IValue - records, "
        + "structs, enums and hand-written classes alike.")
    .Checking(
    "No instance state, including inherited state, arrays and nested generic arguments, involves IAggregateRoot or IEntity. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid." )
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)

## Applies to markers

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
