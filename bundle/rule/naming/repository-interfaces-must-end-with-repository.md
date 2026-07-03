---
type: Rule
title: Repository Interfaces must end with 'Repository'
rule: "Repository interfaces should follow consistent naming conventions (DDD pattern)."
constraint: Repository Interfaces must end with 'Repository'.
enforced_by: "NamingConventionsArchUnitTest#Repository Interfaces must end with 'Repository'"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
classes()
  .that().resideInAPackage(APPLICATION_PACKAGE)  // Repositories are now in application.shared
  .and().areInterfaces()
  .and().haveSimpleNameContaining("Repository")
  .and().doNotHaveSimpleName("Repository")  // Exclude the base Repository interface
  .should().haveSimpleNameEndingWith("Repository")
  .because("Repository interfaces should follow consistent naming conventions (DDD pattern)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
