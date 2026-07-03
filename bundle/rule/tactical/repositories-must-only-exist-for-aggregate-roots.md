---
type: Rule
title: Repositories must only exist for Aggregate Roots
rule: Repositories must only exist for Aggregate Roots.
constraint: Repositories must only exist for Aggregate Roots.
enforced_by: "DddTacticalPatternsArchUnitTest#Repositories must only exist for Aggregate Roots"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
def repositoryInterfaces = allClasses.stream()
  .filter { it.isAssignableTo(Repository.class) }
  .filter { it.isInterface() }
  .filter { !it.getSimpleName().equals("Repository") }
  .collect()

def violations = []
repositoryInterfaces.each { repoInterface ->
  def repoName = repoInterface.getSimpleName()
  if (repoName.endsWith("Repository")) {
    def domainObjectName = repoName.substring(0, repoName.length() - "Repository".length())

    def domainClass = allClasses.stream()
      .filter { it.getSimpleName().equals(domainObjectName) }
      .findFirst()
      .orElse(null)

    if (domainClass != null) {
      boolean isAggregateRoot = domainClass.isAssignableTo(AggregateRoot.class)

      if (!isAggregateRoot) {
        violations.add("${repoInterface.getName()} exists for ${domainClass.getName()} which does not implement AggregateRoot")
      }
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Repositories should only exist for Aggregate Roots, not for Entities (DDD pattern).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
