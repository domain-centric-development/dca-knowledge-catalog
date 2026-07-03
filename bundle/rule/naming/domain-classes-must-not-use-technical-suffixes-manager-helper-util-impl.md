---
type: Rule
title: "Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)"
rule: "Domain names come from the ubiquitous language - name services by their specialty, not by technical role."
constraint: "Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)."
enforced_by: "NamingConventionsArchUnitTest#Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)"
status: enforced
test_class: NamingConventionsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/NamingConventionsArchUnitTest.groovy
tags: [naming, archunit]
---

```groovy
expect:
// Domain concepts carry ubiquitous-language names. 'Manager'/'Helper'/'Util' signal
// a missing domain concept; 'Impl' signals naming by pattern instead of by specialty.
noClasses()
  .that().resideInAnyPackage(allDomainPatternsWithSharedKernel())
  .should().haveSimpleNameEndingWith("Manager")
  .orShould().haveSimpleNameEndingWith("Helper")
  .orShould().haveSimpleNameEndingWith("Util")
  .orShould().haveSimpleNameEndingWith("Utils")
  .orShould().haveSimpleNameEndingWith("Impl")
  .because("Domain names come from the ubiquitous language - name services by their specialty, not by technical role")
  .allowEmptyShould(true)
  .check(allClasses)
```
