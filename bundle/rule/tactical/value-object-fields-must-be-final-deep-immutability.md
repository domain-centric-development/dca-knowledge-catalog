---
type: Rule
title: "Value Object fields must be final (deep immutability)"
rule: "Value Object fields must be final (deep immutability)."
constraint: "Value Object fields must be final (deep immutability)."
enforced_by: "DddTacticalPatternsArchUnitTest#Value Object fields must be final (deep immutability)"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// All fields in value objects must be final to ensure deep immutability
// Records automatically have final fields, but regular classes need this check
// Enums are already immutable by design, so we exclude them too

def valueObjectClasses = allClasses.stream()
  .filter { it.isAssignableTo(Value.class) }
  .filter { !it.isInterface() }
  .filter { !it.isRecord() }  // Records have implicitly final fields
  .filter { !it.isEnum() }    // Enums are immutable by design
  .collect()

def violations = []
valueObjectClasses.each { voClass ->
  voClass.getAllFields().each { field ->
    if (!field.getModifiers().contains(JavaModifier.FINAL) &&
      !field.getModifiers().contains(JavaModifier.STATIC)) {
      // Static fields can be non-final
      violations.add("${voClass.getName()} has non-final field '${field.getName()}'")
    }
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Value Object fields must be final for deep immutability (Vernon's DDD).\n" +
  "Violations found:\n" + violations.join("\n"))
}
true
```

## Applies to markers

- [Value](/marker/tactical/value.md)
