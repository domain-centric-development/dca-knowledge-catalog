---
type: Rule
id: DCA-ERR-004
title: Domain and use-case exceptions must not carry prohibited framework metadata
rule: "An exception of an inner layer that carries container, persistence or protocol metadata has decided how the outside answers it, which is the incoming adapter's decision and only its."
constraint: Domain and use-case exceptions must not carry prohibited framework metadata.
selects: "Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, the building-blocks package excluded."
checks: "The type carries none of the configured injectable, persistence-entity, transactional, web-controller, REST-controller or event-listener annotations, directly or as a meta-annotation. Fields and methods are not inspected, and an annotation the layout classifies into no role is allowed. With those roles empty the rule selects no metadata and passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-004"
status: enforced
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Domain and use-case exceptions must not carry prohibited framework metadata

## Selection

Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, the building-blocks package excluded.

## Check

The type carries none of the configured injectable, persistence-entity, transactional, web-controller, REST-controller or event-listener annotations, directly or as a meta-annotation. Fields and methods are not inspected, and an annotation the layout classifies into no role is allowed. With those roles empty the rule selects no metadata and passes.

## .NET reading

**Selection.** Types anywhere under the root namespace that are assignable to DomainException or to UseCaseException, the building-blocks namespace excluded.

**Check.** The type carries no attribute the layout classifies into the container, persistence or transaction role, neither directly nor through a base attribute type. Fields, properties and methods are not inspected, and an attribute the layout classifies into no role is allowed. A type whose runtime reflection is unavailable is skipped. With those roles empty the rule selects no metadata and passes.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-004",
        "Domain and use-case exceptions must not carry prohibited framework metadata",
        "An exception of an inner layer that carries container, persistence or protocol"
            + " metadata has decided how the outside answers it, which is the incoming"
            + " adapter's decision and only its",
        arch -> {
          FrameworkAnnotations roles = layout.frameworkAnnotations();
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "DCA-ERR-004: prohibited metadata on an inner-layer exception");
          for (JavaClass type : arch.classes()) {
            if (!isProjectException(type)) {
              continue;
            }
            for (List<String> role :
                List.of(
                    roles.injectable(),
                    roles.persistenceEntity(),
                    roles.transactional(),
                    roles.webController(),
                    roles.restController(),
                    roles.eventListener())) {
              for (String annotation : role) {
                collected.require(
                    !type.isAnnotatedWith(annotation) && !type.isMetaAnnotatedWith(annotation),
                    type.getName() + " carries prohibited metadata " + annotation);
              }
            }
          }
          collected.throwIfAny();
        })
    .selecting(
        "Classes anywhere on the classpath under scan that are assignable to DomainException or"
            + " to UseCaseException, the building-blocks package excluded.")
    .checking(
        "The type carries none of the configured injectable, persistence-entity, transactional,"
            + " web-controller, REST-controller or event-listener annotations, directly or as a"
            + " meta-annotation. Fields and methods are not inspected, and an annotation the"
            + " layout classifies into no role is allowed. With those roles empty the rule"
            + " selects no metadata and passes.")
```

## Helpers

### `isProjectException`

```java
/** A project's own exception type: assignable to a base type, outside the building blocks. */
  private static boolean isProjectException(JavaClass type) {
    return (type.isAssignableTo(DomainException.class)
            || type.isAssignableTo(UseCaseException.class))
        && !type.getPackageName().startsWith(BUILDING_BLOCKS_PREFIX);
  }
```

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```

### `CollectedViolations.withHeader`

```java
/** A collector whose report starts with the given statement of what the rule demands. */
  static CollectedViolations withHeader(String header) {
    return new CollectedViolations(header);
  }
```

### `CollectedViolations.require`

```java
/** Records the violation unless the condition holds. */
  void require(boolean condition, String violation) {
    if (!condition) {
      add(violation);
    }
  }
```

### `CollectedViolations.throwIfAny`

```java
/**
   * Throws the collected violations as one {@link DcaRuleViolation}; nothing when there are none.
   */
  void throwIfAny() {
    if (!violations.isEmpty()) {
      throw new DcaRuleViolation(header, violations);
    }
  }
```

### `CollectedViolations.withoutHeader`

```java
/** A collector whose report is the bare list of violations. */
  static CollectedViolations withoutHeader() {
    return new CollectedViolations("");
  }
```

### `CollectedViolations.addAll`

```java
/**
   * Evaluates one ArchUnit rule and records each of its violation details, suffixed with the
   * explanation of what the rule was checking — the detail alone ({@code Class A depends on B})
   * does not say why that dependency is wrong.
   */
  void addAll(ArchRule rule, JavaClasses classes, String explanation) {
    for (String detail : rule.evaluate(classes).getFailureReport().getDetails()) {
      add(explanation.isEmpty() ? detail : detail + " - " + explanation);
    }
  }

/** Evaluates one ArchUnit rule and records its violation details as they are. */
  void addAll(ArchRule rule, JavaClasses classes) {
    addAll(rule, classes, "");
  }
```

### `CollectedViolations.add`

```java
/** Records one violation. */
  void add(String violation) {
    violations.add(Objects.requireNonNull(violation, "violation"));
  }
```

### `CollectedViolations.isEmpty`

```java
boolean isEmpty() {
  return violations.isEmpty();
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-004",
    "Domain and use-case exceptions must not carry prohibited framework metadata",
    "An exception of an inner layer that carries container, persistence or protocol metadata has"
        + " decided how the outside answers it, which is the incoming adapter's decision and only"
        + " its",
    arch =>
    {
        var roles = arch.Layout.FrameworkTypes;
        var violations = new List<string>();
        foreach (var type in ExceptionsOfEitherLayer(arch))
        {
            var runtime = arch.RuntimeType(type);
            if (runtime is null)
            {
                continue;
            }

            foreach (var attribute in runtime.GetCustomAttributesData())
            {
                for (var attributeType = attribute.AttributeType; attributeType is not null; attributeType = attributeType.BaseType)
                {
                    var classified = roles.PersistenceAttributeTypes.Contains(attributeType.FullName ?? "")
                        || roles.ContainerAttributeNamespaces
                            .Concat(roles.PersistenceAttributeNamespaces)
                            .Concat(roles.TransactionAttributeNamespaces)
                            .Any(prefix => DcaLayout.IsBelow(attributeType.Namespace ?? "", prefix));
                    if (!classified)
                    {
                        continue;
                    }

                    violations.Add($"{type.FullName} carries prohibited metadata {attribute.AttributeType.FullName}");
                    break;
                }
            }
        }

        DcaRule.Fail("DCA-ERR-004: prohibited metadata on an inner-layer exception", violations);
    })
    .Selecting(
        "Types anywhere under the root namespace that are assignable to DomainException or to "
        + "UseCaseException, the building-blocks namespace excluded.")
    .Checking(
        "The type carries no attribute the layout classifies into the container, persistence or "
        + "transaction role, neither directly nor through a base attribute type. Fields, properties "
        + "and methods are not inspected, and an attribute the layout classifies into no role is "
        + "allowed. A type whose runtime reflection is unavailable is skipped. With those roles "
        + "empty the rule selects no metadata and passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
