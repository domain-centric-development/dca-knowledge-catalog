---
type: Rule
id: DCA-ERR-004
title: Domain and use-case exceptions must not carry prohibited framework metadata
rule: "An exception of an inner layer that carries container, persistence or protocol metadata has decided how the outside answers it, which is the incoming adapter's decision and only its; an annotation that fixes the answer's status decides it for every protocol at once, including the ones the exception knows nothing about."
constraint: Domain and use-case exceptions must not carry prohibited framework metadata.
selects: "Classes anywhere on the classpath under scan that are assignable to DomainException or to UseCaseException, the building-blocks package excluded."
checks: "The type carries none of the configured injectable, persistence-entity, transactional, web-controller, REST-controller, event-listener or transport-status annotations, directly or as a meta-annotation. The transport-status role is the one that fixes the protocol answer on the exception itself; where the framework answers through a mapper class instead of an annotation the role is empty and nothing is selected for it. Fields and methods are not inspected, and an annotation the layout classifies into no role is allowed. With those roles empty the rule selects no metadata and passes."
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

The type carries none of the configured injectable, persistence-entity, transactional, web-controller, REST-controller, event-listener or transport-status annotations, directly or as a meta-annotation. The transport-status role is the one that fixes the protocol answer on the exception itself; where the framework answers through a mapper class instead of an annotation the role is empty and nothing is selected for it. Fields and methods are not inspected, and an annotation the layout classifies into no role is allowed. With those roles empty the rule selects no metadata and passes.

## .NET reading

**Selection.** Types anywhere under the root namespace that are assignable to the domain-exception or the use-case-exception role, the vocabulary's own code excluded: the namespaces the configured role types live in are not selected, so a project's own base type is not reported as residing outside a layer it never claimed.

**Check.** The type carries no attribute the layout classifies into the container, persistence, transaction, transport-status, web-controller, REST-controller or event-listener role, neither directly nor through a base attribute type - the same seven roles the Java twin forbids. Four of them are empty in every preset: the platform has no container stereotype, no controller attribute a failure could carry and no event-listener attribute, and it answers a failure through a mapper type rather than through an attribute on it. They exist so the id has one contract in both languages and a project whose framework does have such an attribute names it. Fields, properties and methods are not inspected, and an attribute the layout classifies into no role is allowed. A type whose runtime reflection is unavailable is not inspected; it is counted and named on standard output rather than passing silently. With the roles empty the rule selects no metadata and passes.

## Implementation

```java
DcaRule.check(
        "DCA-ERR-004",
        "Domain and use-case exceptions must not carry prohibited framework metadata",
        "An exception of an inner layer that carries container, persistence or protocol"
            + " metadata has decided how the outside answers it, which is the incoming"
            + " adapter's decision and only its; an annotation that fixes the answer's status"
            + " decides it for every protocol at once, including the ones the exception knows"
            + " nothing about",
        arch -> {
          FrameworkAnnotations roles = layout.frameworkAnnotations();
          CollectedViolations collected =
              CollectedViolations.withHeader("Prohibited metadata on an inner-layer exception");
          for (JavaClass type : arch.classes()) {
            if (!isProjectException(type, arch.layout().markers())) {
              continue;
            }
            for (List<String> role :
                List.of(
                    roles.injectable(),
                    roles.persistenceEntity(),
                    roles.transactional(),
                    roles.webController(),
                    roles.restController(),
                    roles.eventListener(),
                    roles.transportStatus())) {
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
            + " web-controller, REST-controller, event-listener or transport-status"
            + " annotations, directly or as a meta-annotation. The transport-status role is the"
            + " one that fixes the protocol answer on the exception itself; where the framework"
            + " answers through a mapper class instead of an annotation the role is empty and"
            + " nothing is selected for it. Fields and methods are not inspected, and an"
            + " annotation the layout classifies into no role is allowed. With those roles"
            + " empty the rule selects no metadata and passes.")
```

## Helpers

### `isProjectException`

```java
/** A project's own exception type: assignable to a base type, outside the building blocks. */
  private static boolean isProjectException(JavaClass type, DcaMarkers markers) {
    return (type.isAssignableTo(markers.domainException())
            || type.isAssignableTo(markers.useCaseException()))
        && !markers.declaresTypesIn(type.getPackageName());
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ERR-004",
    "Domain and use-case exceptions must not carry prohibited framework metadata",
    "An exception of an inner layer that carries container, persistence or protocol metadata has"
        + " decided how the outside answers it, which is the incoming adapter's decision and only"
        + " its; an attribute that fixes the answer's status decides it for every protocol at once,"
        + " including the ones the exception knows nothing about",
    arch =>
    {
        var roles = arch.Layout.FrameworkTypes;
        var violations = new List<string>();
        var unreadable = new List<string>();
        foreach (var type in ExceptionsOfEitherLayer(arch))
        {
            var runtime = arch.RuntimeType(type);
            if (runtime is null)
            {
                // Not a violation, but not a clean pass either: say so rather than skip silently.
                unreadable.Add(type.FullName);
                continue;
            }

            foreach (var attribute in runtime.GetCustomAttributesData())
            {
                for (var attributeType = attribute.AttributeType; attributeType is not null; attributeType = attributeType.BaseType)
                {
                    var classified = roles.PersistenceAttributeTypes.Contains(attributeType.FullName ?? "")
                        || roles.TransportStatusAttributeTypes.Contains(attributeType.FullName ?? "")
                        || roles.ContainerAttributeNamespaces
                            .Concat(roles.PersistenceAttributeNamespaces)
                            .Concat(roles.TransactionAttributeNamespaces)
                            .Concat(roles.WebControllerAttributeNamespaces)
                            .Concat(roles.RestControllerAttributeNamespaces)
                            .Concat(roles.EventListenerAttributeNamespaces)
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

        if (unreadable.Count > 0)
        {
            Console.Out.WriteLine(
                $"[DCA-ERR-004] {unreadable.Count} exception type(s) not inspected, runtime type unavailable: "
                + string.Join(", ", unreadable));
        }

        DcaRule.Fail("Prohibited metadata on an inner-layer exception", violations);
    })
    .Selecting(
        "Types anywhere under the root namespace that are assignable to the domain-exception or the "
        + "use-case-exception role, the vocabulary's own code excluded: the namespaces the configured "
        + "role types live in are not selected, so a project's own base type is not reported as "
        + "residing outside a layer it never claimed.")
    .Checking(
        "The type carries no attribute the layout classifies into the container, persistence, "
        + "transaction, transport-status, web-controller, REST-controller or event-listener role, "
        + "neither directly nor through a base attribute type - the same seven roles the Java twin "
        + "forbids. Four of them are empty in every preset: the platform has no container "
        + "stereotype, no controller attribute a failure could carry and no event-listener "
        + "attribute, and it answers a failure through a mapper type rather than through an "
        + "attribute on it. They exist so the id has one contract in both languages and a project "
        + "whose framework does have such an attribute names it. Fields, properties and methods "
        + "are not inspected, and an attribute the layout classifies into no role is allowed. A "
        + "type whose runtime reflection is unavailable is not inspected; it is counted and named "
        + "on standard output rather than passing silently. With the roles empty the rule selects "
        + "no metadata and passes.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
