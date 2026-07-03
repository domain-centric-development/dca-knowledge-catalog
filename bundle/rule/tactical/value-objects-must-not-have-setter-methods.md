---
type: Rule
title: Value Objects must not have setter methods
rule: Value Objects must not have setter methods.
constraint: Value Objects must not have setter methods.
enforced_by: "DddTacticalPatternsArchUnitTest#Value Objects must not have setter methods"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Value Objects are immutable, so they should not have setter methods
// Records don't have setters, but regular classes need this check

def valueObjectClasses = allClasses.stream()
  .filter { it.isAssignableTo(Value.class) }
  .filter { !it.isInterface() }
  .collect()

def violations = []
valueObjectClasses.each { voClass ->
  voClass.getAllMethods().each { method ->
    if (method.getName().startsWith("set") &&
      method.getName().length() > 3 &&
      Character.isUpperCase(method.getName().charAt(3)) &&
      method.getRawParameterTypes().size() == 1 &&
      method.getRawReturnType().getName() == "void") {
      violations.add("${voClass.getName()} has setter method '${method.getName()}'")
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Value Objects must be immutable and should not have setter methods.\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Value](/marker/tactical/value.md)
