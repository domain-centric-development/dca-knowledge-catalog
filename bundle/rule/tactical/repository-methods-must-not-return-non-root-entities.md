---
type: Rule
id: DCA-TAC-017
title: Repository methods must not return non-root Entities
rule: "A caller receiving an Entity that is not an Aggregate Root could mutate part of an aggregate without passing its root, so the root's invariants would never run."
constraint: Repository methods must not return non-root Entities.
selects: "Interfaces anywhere under scan assignable to Repository, the marker Repository itself excluded."
checks: "No return type of a method declared on the interface itself - walked through raw type, array component, generic type arguments and wildcard bounds, so Optional<T>, List<T> and Map<K,V> are seen through - involves a class assignable to Entity that is not also assignable to AggregateRoot. Inherited methods and parameter types are not inspected."
enforced_by: "TacticalPatternRules#DCA-TAC-017"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan assignable to Repository, the marker Repository itself excluded.

## Check

No return type of a method declared on the interface itself - walked through raw type, array component, generic type arguments and wildcard bounds, so Optional<T>, List<T> and Map<K,V> are seen through - involves a class assignable to Entity that is not also assignable to AggregateRoot. Inherited methods and parameter types are not inspected.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository; an interface named exactly Repository excluded.

**Check.** No return type of a method declared on the interface itself - walked through generic type arguments, so Task<T?>, IReadOnlyList<T> and IAsyncEnumerable<T> are seen through - involves a type assignable to IEntity that is not also assignable to IAggregateRoot. Inherited methods, property accessors and parameter types are not inspected.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-017",
        "Repository methods must not return non-root Entities",
        "A caller receiving an Entity that is not an Aggregate Root could mutate part of an"
            + " aggregate without passing its root, so the root's invariants would never run",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass repository : repositoryInterfaces(arch)) {
            for (JavaMethod method : repository.getMethods()) {
              for (JavaClass type : TypeInspection.involvedTypes(method.getReturnType())) {
                if (type.isAssignableTo(Entity.class)
                    && !type.isAssignableTo(AggregateRoot.class)) {
                  violations.add(
                      repository.getName()
                          + "."
                          + method.getName()
                          + " exposes "
                          + type.getName()
                          + ", an Entity that is not an Aggregate Root");
                }
              }
            }
          }
          fail(
              "Repository methods must not expose an Entity that is not an Aggregate Root: a caller"
                  + " could mutate part of an aggregate without passing its root (DDD pattern).",
              violations);
        })
    .selecting(
        "Interfaces anywhere under scan assignable to Repository, the marker Repository "
            + "itself excluded.")
    .checking(
        "No return type of a method declared on the interface itself - walked through "
            + "raw type, array component, generic type arguments and wildcard bounds, so "
            + "Optional<T>, List<T> and Map<K,V> are seen through - involves a class "
            + "assignable to Entity that is not also assignable to AggregateRoot. Inherited "
            + "methods and parameter types are not inspected.")
```

## Helpers

### `repositoryInterfaces`

```java
private static List<JavaClass> repositoryInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(Repository.class)
              && c.isInterface()
              && !c.getSimpleName().equals(REPOSITORY_SUFFIX));
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

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
