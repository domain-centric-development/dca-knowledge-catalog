---
type: Rule
title: "Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)"
rule: "Outgoing adapters in '<context>' must not access domain layer of '<context>' - use api/ or events/ packages instead."
constraint: "Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)."
enforced_by: "DddStrategicPatternsArchUnitTest#Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)"
status: enforced
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
given:
Map<String, BoundedContext> boundedContexts = discoverBoundedContextPackages()
List<String> contextPackages = boundedContexts.keySet().toList()

expect:
// For each bounded context's outgoing adapters, verify they only access
// @OpenHostService annotated classes (or Shared Kernel) from other contexts
// Exception: Documented ACL patterns in ALLOWED_ADAPTER_CROSS_CONTEXT_ACCESS
contextPackages.each { sourceContext ->
  String sourceName = boundedContexts[sourceContext].name()
  String sourceContextShort = extractContextName(sourceContext)

  // Get allowed ACL targets for this source
  List<String> allowedAclTargets = ALLOWED_ADAPTER_CROSS_CONTEXT_ACCESS.getOrDefault(sourceContextShort, [])

  // Get all other contexts, excluding allowed ACL targets
  List<String> otherContexts = contextPackages.findAll { targetContext ->
    if (targetContext == sourceContext) return false
    String targetContextShort = extractContextName(targetContext)
    return !allowedAclTargets.contains(targetContextShort)
  }

  if (!otherContexts.isEmpty()) {
    // For each other context (not in ACL exceptions), outgoing adapters should only access
    // api/ packages (Open Host Services) or events/ packages (Integration Events)
    otherContexts.each { targetContext ->
      String targetName = boundedContexts[targetContext].name()

      // Forbid access to domain layers of other contexts
      noClasses()
        .that().resideInAPackage("${sourceContext}.adapter.outgoing..")
        .should().accessClassesThat()
          .resideInAPackage("${targetContext}.domain..")
        .allowEmptyShould(true)
        .because("Outgoing adapters in '${sourceName}' must not access domain layer of '${targetName}' - use api/ or events/ packages instead")
        .check(allClasses)

      // Forbid access to application layers of other contexts
      noClasses()
        .that().resideInAPackage("${sourceContext}.adapter.outgoing..")
        .should().accessClassesThat()
          .resideInAPackage("${targetContext}.application..")
        .allowEmptyShould(true)
        .because("Outgoing adapters in '${sourceName}' must not access application layer of '${targetName}' - use api/ or events/ packages instead")
        .check(allClasses)
    }
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)
