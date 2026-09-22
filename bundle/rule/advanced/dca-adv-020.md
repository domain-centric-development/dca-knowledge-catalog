---
type: Rule
id: DCA-ADV-020
title: Domain service operations take an aggregate or an entity
rule: A domain service works on the model itself; an operation that only takes extracted values moves the decision out of the domain and into its caller.
constraint: Domain service operations take an aggregate or an entity.
selects: "Public methods declared on non-interface classes carrying the domain-service role, except the methods every object has (equals, hashCode, toString) and compiler generated ones."
checks: "At least one parameter of the method carries the aggregate-root or the entity role. Value objects and foreign facts may be passed alongside but do not satisfy the check on their own: a calculation that needs no aggregate is behaviour of the value object or the aggregate, not a domain service. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-020"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain service operations take an aggregate or an entity

## Selection

Public methods declared on non-interface classes carrying the domain-service role, except the methods every object has (equals, hashCode, toString) and compiler generated ones.

## Check

At least one parameter of the method carries the aggregate-root or the entity role. Value objects and foreign facts may be passed alongside but do not satisfy the check on their own: a calculation that needs no aggregate is behaviour of the value object or the aggregate, not a domain service. An empty selection passes.

## .NET reading

**Selection.** Public methods declared on non-interface types carrying the domain-service role, except the methods every object has (Equals, GetHashCode, ToString) and compiler generated ones.

**Check.** At least one parameter of the method carries the aggregate-root or the entity role. Value objects and foreign facts may be passed alongside but do not satisfy the check on their own: a calculation that needs no aggregate is behaviour of the value object or the aggregate, not a domain service. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-020",
        "Domain service operations take an aggregate or an entity",
        "A domain service works on the model itself; an operation that only takes extracted"
            + " values moves the decision out of the domain and into its caller",
        arch -> {
          CollectedViolations collected =
              CollectedViolations.withHeader(
                  "A domain service operation takes at least one aggregate or entity");
          String aggregateRoot = arch.layout().markers().aggregateRoot();
          String entity = arch.layout().markers().entity();
          for (JavaClass type :
              arch.classes()
                  .that(
                      DescribedPredicate.describe(
                          "domain services",
                          candidate ->
                              candidate.isAssignableTo(arch.layout().markers().domainService())
                                  && !candidate.isInterface()))) {
            for (JavaMethod method : type.getMethods()) {
              if (!method.getModifiers().contains(JavaModifier.PUBLIC)
                  || method.getModifiers().contains(JavaModifier.SYNTHETIC)
                  || method.getModifiers().contains(JavaModifier.BRIDGE)
                  || OBJECT_METHODS.contains(method.getName())) {
                continue;
              }
              boolean takesModelObject =
                  method.getRawParameterTypes().stream()
                      .anyMatch(
                          parameter ->
                              parameter.isAssignableTo(aggregateRoot)
                                  || parameter.isAssignableTo(entity));
              collected.require(
                  takesModelObject,
                  type.getName()
                      + "."
                      + method.getName()
                      + " takes no aggregate and no entity");
            }
          }
          collected.throwIfAny();
        })
    .selecting(
        "Public methods declared on non-interface classes carrying the domain-service role,"
            + " except the methods every object has (equals, hashCode, toString) and compiler"
            + " generated ones.")
    .checking(
        "At least one parameter of the method carries the aggregate-root or the entity role."
            + " Value objects and foreign facts may be passed alongside but do not satisfy the"
            + " check on their own: a calculation that needs no aggregate is behaviour of the"
            + " value object or the aggregate, not a domain service. An empty selection passes.",
        "pass the aggregate itself, or move the operation onto the value object it computes on")
```

## Helpers

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
    "DCA-ADV-020",
    "Domain service operations take an aggregate or an entity",
    "A domain service works on the model itself; an operation that only takes extracted values "
        + "moves the decision out of the domain and into its caller",
    arch =>
    {
        var violations = new List<string>();
        foreach (var service in arch.Types.Where(t =>
            t is not Interface && t.IsAssignableTo(arch.Layout.Markers.DomainService)))
        {
            foreach (var method in service.GetMethodMembers()
                .Where(m => m.MethodForm == MethodForm.Normal && m.Visibility == Visibility.Public))
            {
                if (ObjectMethods.Contains(SimpleName(method)))
                {
                    continue;
                }

                var takesModelObject = method.Parameters.Any(parameter =>
                    parameter.IsAssignableTo(arch.Layout.Markers.AggregateRoot)
                    || parameter.IsAssignableTo(arch.Layout.Markers.Entity));
                if (!takesModelObject)
                {
                    violations.Add($"{service.FullName}.{SimpleName(method)} takes no aggregate and no entity");
                }
            }
        }

        DcaRule.Fail("A domain service operation takes at least one aggregate or entity", violations,
            "pass the aggregate itself, or move the operation onto the value object it computes on");
    })
    .Selecting(
        "Public methods declared on non-interface types carrying the domain-service role, except the "
        + "methods every object has (Equals, GetHashCode, ToString) and compiler generated ones.")
    .Checking(
        "At least one parameter of the method carries the aggregate-root or the entity role. Value "
        + "objects and foreign facts may be passed alongside but do not satisfy the check on their "
        + "own: a calculation that needs no aggregate is behaviour of the value object or the "
        + "aggregate, not a domain service. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
