---
type: Rule
title: Value Objects must be records or immutable classes with attribute equality
rule: Value Objects must be records or immutable classes with attribute equality.
constraint: Value Objects must be records or immutable classes with attribute equality.
enforced_by: "DddTacticalPatternsArchUnitTest#Value Objects must be records or immutable classes with attribute equality"
status: enforced
test_class: DddTacticalPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddTacticalPatternsArchUnitTest.groovy
tags: [tactical, archunit]
---

```groovy
when:
// Records are the preferred implementation: the compiler grants final fields,
// no setters and attribute-based equality. A hand-written class is a permitted
// alternative — the immutability rules above (final class, final fields, no setters)
// apply to it unchanged. What they cannot check is the one thing a record gives for
// free: a Value Object compares by its attributes, so a non-record class must override
// equals and hashCode itself.
def valueObjectClasses = allClasses.stream()
  .filter { it.isAssignableTo(VALUE_MARKER) }
  .filter { !it.isInterface() && !it.isRecord() && !it.isEnum() }
  .collect()

def violations = []
valueObjectClasses.each { voClass ->
  def overridesOwn = { String name, int paramCount ->
    voClass.getAllMethods().any {
      it.getName() == name &&
        it.getRawParameterTypes().size() == paramCount &&
        it.getOwner().getName() != "java.lang.Object"
    }
  }
  if (!overridesOwn("equals", 1) || !overridesOwn("hashCode", 0)) {
    violations.add("${voClass.getName()} is a non-record Value Object without its own equals/hashCode")
  }
}

then:
if (!violations.isEmpty()) {
  throw new AssertionError(
  "Value Objects are records by preference; an immutable class is allowed, "
  + "but it must implement attribute equality itself.\n"
  + "Violations found:\n" + violations.join("\n"))
}
true
```
