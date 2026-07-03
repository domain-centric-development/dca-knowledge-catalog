---
type: Rule
title: Domain model classes must not have public setter methods
rule: Domain model classes must not have public setter methods.
constraint: Domain model classes must not have public setter methods.
enforced_by: "DddTacticalPatternsArchUnitTest#Domain model classes must not have public setter methods"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Behavior-rich domain models change state through intention-revealing methods
// (e.g. activate(), changePrice()) - never through public setters.
// Mirrors the Value Object setter rule, extended to Entities and Aggregate Roots.

def domainClasses = allClasses.stream()
  .filter { it.isAssignableTo(Entity.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []
domainClasses.each { domainClass ->
  domainClass.getMethods().each { method ->
    if (method.getName().startsWith("set") &&
      method.getName().length() > 3 &&
      Character.isUpperCase(method.getName().charAt(3)) &&
      method.getRawParameterTypes().size() == 1 &&
      method.getRawReturnType().getName() == "void" &&
      method.getModifiers().contains(JavaModifier.PUBLIC)) {
      violations.add("${domainClass.getName()} has public setter '${method.getName()}'")
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Domain model classes must not expose public setters - use intention-revealing methods from the ubiquitous language.\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Entity<T, ID>](/marker/tactical/entity.md)
