---
type: Rule
id: DCA-TAC-007
title: Entities must not have fields with Aggregate Root types
rule: "An entity inside an aggregate references other aggregates by identity only, otherwise the aggregate boundary leaks."
constraint: Entities must not have fields with Aggregate Root types.
selects: Non-interface classes anywhere under scan assignable to Entity but not to AggregateRoot; records and abstract classes included.
checks: "No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid."
enforced_by: "TacticalPatternRules#DCA-TAC-007"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Entities must not have fields with Aggregate Root types

## Selection

Non-interface classes anywhere under scan assignable to Entity but not to AggregateRoot; records and abstract classes included.

## Check

No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IEntity but not to IAggregateRoot; records, structs and abstract classes included.

**Check.** No instance state, including inherited state, arrays and nested generic arguments, involves IAggregateRoot. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-007",
        "Entities must not have fields with Aggregate Root types",
        "An entity inside an aggregate references other aggregates by identity only, otherwise the"
            + " aggregate boundary leaks",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass entity : nonRootEntities(arch)) {
            for (JavaField field : TypeInspection.instanceFields(entity)) {
              for (JavaClass involved : TypeInspection.involvedTypes(field, entity)) {
                if (isConcreteAggregateRoot(involved, arch.layout().markers())) {
                  violations.add(
                      fieldDescription(entity, field, involved)
                          + " which is an aggregate root");
                }
              }
            }
          }
          fail(
              "Entities must not contain references to aggregate roots (reference by ID only).",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to Entity but not to "
            + "AggregateRoot; records and abstract classes included.")
    .checking(
        "No instance state, including inherited state, arrays and nested generic arguments, involves AggregateRoot. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid.")
```

## Helpers

### `nonRootEntities`

```java
private static List<JavaClass> nonRootEntities(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(arch.layout().markers().entity())
              && !c.isAssignableTo(arch.layout().markers().aggregateRoot())
              && !c.isInterface());
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
    "DCA-TAC-007",
    "Entities must not have fields with Aggregate Root types",
    "An entity inside an aggregate references other aggregates by identity only, otherwise the aggregate boundary leaks",
    arch =>
    {
        var violations = new List<string>();
        foreach (var entity in NonRootEntities(arch))
        {
            foreach (var member in InstanceDataMembers(arch, entity))
            {
                if (IsConcreteAggregateRoot(arch, member.Type))
                {
                    violations.Add($"{FieldDescription(entity, member)} which is an aggregate root");
                }

                foreach (var element in member.ElementTypes)
                {
                    if (IsConcreteAggregateRoot(arch, element))
                    {
                        violations.Add($"{ContainsDescription(entity, member, element)} which is an aggregate root");
                    }
                }
            }
        }

        DcaRule.Fail("Entities must not contain references to aggregate roots (reference by ID only).", violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IEntity but not "
        + "to IAggregateRoot; records, structs and abstract classes included.")
    .Checking(
    "No instance state, including inherited state, arrays and nested generic arguments, involves IAggregateRoot. Same-type references and interfaces extending the marker are included. Interfaces that do not extend the marker are invisible; references by id are valid." )
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
