---
type: Rule
id: DCA-USE-015
title: Use Case Result Models must not expose aggregate roots or entities
rule: "A result is the use case's answer, not a handle on the model: identity and behaviour stay behind the port; values, enriched models and read models may cross. Checked transitively through nested records, part records anywhere in the application layer (application.shared included), generic type arguments (List<T>, Optional<T>, Map<K,V>) and inherited fields, a generic base class's type parameters resolved as the result binds them."
constraint: Use Case Result Models must not expose aggregate roots or entities.
selects: "Non-interface, non-nested classes in <module>.application.. whose simple name ends with Result, types assignable to the value role excluded - a domain value object named *Result crosses the port as a value, as DCA-USE-006 already allows."
checks: "No instance field - inherited ones included, walked through raw type and generic type arguments, and transitively into every record that lives in an application package - involves a type assignable to AggregateRoot or Entity. Records outside the application layer (domain value objects, read models) are not walked. Every offending path is reported."
enforced_by: "UseCaseRules#DCA-USE-015"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use Case Result Models must not expose aggregate roots or entities

## Selection

Non-interface, non-nested classes in <module>.application.. whose simple name ends with Result, types assignable to the value role excluded - a domain value object named *Result crosses the port as a value, as DCA-USE-006 already allows.

## Check

No instance field - inherited ones included, walked through raw type and generic type arguments, and transitively into every record that lives in an application package - involves a type assignable to AggregateRoot or Entity. Records outside the application layer (domain value objects, read models) are not walked. Every offending path is reported.

## .NET reading

**Selection.** Top-level classes and structs in each module application namespace ending in Result, excluding IValue types.

**Check.** No instance result member of any visibility - the walk binds public and non-public members - transitively through application part records and generic wrappers exposes IAggregateRoot or IEntity; classes and structs are checked. Domain values and read models are not traversed. A type the loader cannot resolve is not walked.

## Implementation

```java
DcaRule.check(
        "DCA-USE-015",
        "Use Case Result Models must not expose aggregate roots or entities",
        "A result is the use case's answer, not a handle on the model: identity and behaviour stay"
            + " behind the port; values, enriched models and read models may cross. Checked"
            + " transitively through nested records, part records anywhere in the application layer"
            + " (application.shared included), generic type arguments (List<T>, Optional<T>,"
            + " Map<K,V>) and inherited fields, a generic base class's type parameters resolved as"
            + " the result binds them",
        arch -> checkResultsCarryNoIdentities(arch))
    .selecting(
        "Non-interface, non-nested classes in <module>.application.. whose simple name ends"
            + " with Result, types assignable to the value role excluded - a domain value"
            + " object named *Result crosses the port as a value, as DCA-USE-006 already"
            + " allows.")
    .checking(
        "No instance field - inherited ones included, walked through raw type and generic type arguments, and transitively into every record that lives in an application package - involves a type assignable to AggregateRoot or Entity. Records outside the application layer (domain value objects, read models) are not walked. Every offending path is reported.",
        "carry ids and primitives in a result, never an aggregate, an entity or a domain object")
```

## Helpers

### `checkResultsCarryNoIdentities`

```java
private static void checkResultsCarryNoIdentities(DcaArchitecture arch) {
  List<String> violations = new ArrayList<>();
  for (JavaClass result : arch.classes()) {
    if (result.isInterface()
        || result.isNestedClass()
        || !result.getSimpleName().endsWith("Result")
        || result.isAssignableTo(arch.layout().markers().value())
        || !residesInAny(result, arch.allApplicationPatterns())) {
      continue;
    }
    walkResult(
        arch.allApplicationPatterns(),
        result,
        result.getSimpleName(),
        new ArrayDeque<>(),
        violations,
        arch.layout().markers());
  }
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(
        "Use Case Result Models must not expose aggregate roots or entities", violations);
  }
}
```

### `residesInAny`

```java
private static boolean residesInAny(JavaClass javaClass, String[] packagePatterns) {
  for (String pattern : packagePatterns) {
    if (JavaClass.Predicates.resideInAPackage(pattern).test(javaClass)) {
      return true;
    }
  }
  return false;
}
```

### `walkResult`

```java
/**
   * Walks the instance fields of a result or part record — inherited ones included, a base class
   * need not carry the suffix, and a generic base's type parameters are read as the result binds
   * them — and every type each field involves. The path of records currently being walked guards
   * against a self-referencing part record; it is not a global visited set, so the same part record
   * reached through two fields is reported on both paths.
   */
  private static void walkResult(
      String[] applicationPatterns,
      JavaClass current,
      String path,
      Deque<String> recordsOnPath,
      List<String> violations,
      DcaMarkers markers) {
    if (recordsOnPath.contains(current.getName())) {
      return;
    }
    recordsOnPath.push(current.getName());
    for (JavaField field : TypeInspection.instanceFields(current)) {
      String fieldPath = path + "." + field.getName();
      for (JavaClass involved : TypeInspection.involvedTypes(field, current)) {
        String identity = identityKind(involved, markers);
        if (identity != null) {
          violations.add(fieldPath + " : " + involved.getSimpleName() + " (" + identity + ")");
        } else if (isPartRecord(involved, applicationPatterns)) {
          walkResult(
              applicationPatterns,
              involved,
              fieldPath + " -> " + involved.getSimpleName(),
              recordsOnPath,
              violations,
              markers);
        }
      }
    }
    recordsOnPath.pop();
  }
```

### `identityKind`

```java
/** The marker a class carries into the result, or null when it is a value or plain type. */
  private static String identityKind(JavaClass javaClass, DcaMarkers markers) {
    if (javaClass.isAssignableTo(markers.aggregateRoot())) {
      return simpleName(markers.aggregateRoot());
    }
    if (javaClass.isAssignableTo(markers.entity())) {
      return simpleName(markers.entity());
    }
    return null;
  }
```

### `isPartRecord`

```java
/**
   * A part record: a record that lives in an application package - nested in the result, declared
   * next to it, or shared in {@code application.shared}. Records from other layers (value objects,
   * read models) are values by contract and are not walked.
   */
  private static boolean isPartRecord(JavaClass candidate, String[] applicationPatterns) {
    return candidate.isRecord() && residesInAny(candidate, applicationPatterns);
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

### `simpleName`

```java
/** The simple name of a configured marker, for a message a reader has to recognise. */
  private static String simpleName(String fqn) {
    return fqn.substring(fqn.lastIndexOf('.') + 1);
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-015",
        "Use Case Result Models must not expose aggregate roots or entities",
        "A result is the use case's answer, not a handle on the model: identity and behaviour stay behind"
            + " the port; values, enriched models and read models may cross. Checked transitively through"
            + " nested records, part records anywhere in the application layer (Application.Shared included),"
            + " arrays and generic type arguments (IReadOnlyList<T>, T?, IReadOnlyDictionary<K,V>)",
        CheckResultsCarryNoIdentities)
    .Selecting("Top-level classes and structs in each module application namespace ending in Result, excluding IValue types.")
    .Checking(
        "No instance result member of any visibility - the walk binds public and non-public members - "
        + "transitively through application part records and generic wrappers exposes IAggregateRoot or "
        + "IEntity; classes and structs are checked. Domain values and read models are not traversed. A "
        + "type the loader cannot resolve is not walked.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
