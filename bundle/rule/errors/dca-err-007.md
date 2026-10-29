---
type: Rule
id: DCA-ERR-007
title: "Diagnostic: failures that carry display data or objects instead of ids and figures"
rule: "A failure carries ids and figures, never what a page shows. Its fields are the typed identities and the values the rule compared; a name or a description of the thing an id refers to is resolved by the translation site through the queries it already has. A failure that carries the name decides for every surface what it shows, and one that carries an aggregate or an entity hands the model out through the error path."
constraint: "Diagnostic: failures that carry display data or objects instead of ids and figures."
selects: "Concrete project classes assignable to DomainException or UseCaseException - the building blocks' own types excluded - and their instance fields, inherited ones declared in project classes included."
checks: "Informational diagnostic only: lists every field that involves - through its raw type or a type argument - a plain string, an aggregate or entity, or any other type that is neither assignable to the id or value role, nor a number, a primitive, an enum or a date and time type of the platform, and never fails. Container types such as lists are looked through. The message the base type carries is not a field of the project's failure and is not listed. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code."
enforced_by: "ErrorHandlingRules#DCA-ERR-007"
status: informational
maturity: experimental
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Diagnostic: failures that carry display data or objects instead of ids and figures

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Concrete project classes assignable to DomainException or UseCaseException - the building blocks' own types excluded - and their instance fields, inherited ones declared in project classes included.

## Check

Informational diagnostic only: lists every field that involves - through its raw type or a type argument - a plain string, an aggregate or entity, or any other type that is neither assignable to the id or value role, nor a number, a primitive, an enum or a date and time type of the platform, and never fails. Container types such as lists are looked through. The message the base type carries is not a field of the project's failure and is not listed. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code.

## .NET reading

**Selection.** The project's own types below DomainException or UseCaseException, with their runtime type in the loaded assemblies, and the instance fields they and their project base types declare - the backing fields of auto-properties included.

**Check.** Informational diagnostic only: lists a field whose type is a plain string, or is assignable to IAggregateRoot or IEntity - directly, as an array element or as a generic type argument - and never fails. Ids, values, numbers and every other type pass. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code.

## Implementation

```java
DcaRule.informational(
        "DCA-ERR-007",
        "Diagnostic: failures that carry display data or objects instead of ids and figures",
        "A failure carries ids and figures, never what a page shows. Its fields are the typed"
            + " identities and the values the rule compared; a name or a description of the"
            + " thing an id refers to is resolved by the translation site through the queries"
            + " it already has. A failure that carries the name decides for every surface what"
            + " it shows, and one that carries an aggregate or an entity hands the model out"
            + " through the error path",
        arch -> {
          List<String> observed = new ArrayList<>();
          DcaMarkers markers = arch.layout().markers();
          for (JavaClass failure : arch.classes()) {
            if (failure.isInterface() || !isProjectException(failure, markers)) {
              continue;
            }
            for (JavaField field : TypeInspection.instanceFields(failure)) {
              JavaClass owner = field.getOwner();
              if (field.getModifiers().contains(JavaModifier.SYNTHETIC)
                  || owner.getPackageName().startsWith("java.")
                  || markers.declaresTypesIn(owner.getPackageName())) {
                continue;
              }
              for (JavaClass involved : TypeInspection.involvedTypes(field, failure)) {
                String finding = fieldFinding(involved, arch);
                if (finding != null) {
                  observed.add(
                      failure.getName()
                          + "."
                          + field.getName()
                          + " is "
                          + finding
                          + " ("
                          + involved.getSimpleName()
                          + ") - carry the id or the figure the rule compared");
                }
              }
            }
          }
          return observed;
        })
    .experimental()
    .selecting(
        "Concrete project classes assignable to DomainException or UseCaseException - the"
            + " building blocks' own types excluded - and their instance fields, inherited"
            + " ones declared in project classes included.")
    .checking(
        "Informational diagnostic only: lists every field that involves - through its raw type"
            + " or a type argument - a plain string, an aggregate or entity, or any other type"
            + " that is neither assignable to the id or value role, nor a number, a primitive,"
            + " an enum or a date and time type of the platform, and never fails. Container"
            + " types such as lists are looked through. The message the base type carries is"
            + " not a field of the project's failure and is not listed. A string that holds a"
            + " code rather than display text is listed as well: the type does not tell the"
            + " two apart, and the remedy is a typed value for the code.")
```

## Helpers

### `isProjectException`

```java
/** A project's own exception type: assignable to a base type, outside the building blocks. */
  private static boolean isProjectException(JavaClass type, DcaMarkers markers) {
    return (markers.is("domainException").test(type) || markers.is("useCaseException").test(type))
        && !markers.declaresTypesIn(type.getPackageName());
  }
```

### `fieldFinding`

```java
/** What is wrong with a type a failure's field involves, or {@code null} when it is fine. */
  private static String fieldFinding(JavaClass type, DcaArchitecture arch) {
    DcaMarkers markers = arch.layout().markers();
    String name = type.getName();
    if (markers.is("aggregateRoot").test(type) || markers.is("entity").test(type)) {
      return "an aggregate or entity";
    }
    if (type.isAssignableTo(CharSequence.class)) {
      return "a plain string";
    }
    if (type.isPrimitive()
        || type.isEnum()
        || type.isAssignableTo(Number.class)
        || markers.is("id").test(type)
        || markers.is("value").test(type)
        || name.equals("java.lang.Boolean")
        || name.equals("java.lang.Character")
        || type.getPackageName().equals("java.time")
        || arch.layout().timestampTypes().contains(name)
        || type.getPackageName().equals("java.util")
        || name.equals("java.lang.Object")) {
      return null;
    }
    return "neither an id, a value nor a number";
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
DcaRule.Informational(
    "DCA-ERR-007",
    "Diagnostic: failures that carry display data or objects instead of ids and figures",
    "A failure carries ids and figures, never what a page shows: its fields are the typed identities"
        + " and the values the rule compared. A name or a description of the thing the id refers to is"
        + " resolved by the translation site, through the queries it already has; a failure that"
        + " carries it decides for every surface what it shows, and one that carries the aggregate"
        + " hands its state to every caller",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var observed = new List<string>();
        foreach (var exception in ExceptionsOfEitherLayer(arch).OrderBy(t => t.FullName, StringComparer.Ordinal))
        {
            var runtime = arch.RuntimeType(exception);
            for (var type = runtime; type is not null && !DcaMarkers.IsRole(type, markers.DomainException)
                && !DcaMarkers.IsRole(type, markers.UseCaseException) && type != typeof(Exception); type = type.BaseType)
            {
                foreach (var field in type.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.DeclaredOnly))
                {
                    var finding = FieldFinding(field.FieldType, markers);
                    if (finding is not null)
                    {
                        observed.Add($"{exception.FullName} holds {FieldName(field)} as {finding} - carry the id or the value the rule compared");
                    }
                }
            }
        }

        return observed.Distinct().ToList();
    })
    .Experimental()
    .Selecting(
        "The project's own types below DomainException or UseCaseException, with their runtime type in"
        + " the loaded assemblies, and the instance fields they and their project base types declare -"
        + " the backing fields of auto-properties included.")
    .Checking(
        "Informational diagnostic only: lists a field whose type is a plain string, or is assignable to"
        + " IAggregateRoot or IEntity - directly, as an array element or as a generic type argument -"
        + " and never fails. Ids, values, numbers and every other type pass. A string that holds a code"
        + " rather than display text is listed as well: the type does not tell the two apart, and the"
        + " remedy is a typed value for the code.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
