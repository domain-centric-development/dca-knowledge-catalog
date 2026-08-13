---
type: Rule
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - even when the action raised no event."
constraint: Use cases that save an aggregate must publish its domain events.
enforced_by: "UseCasePatternsArchUnitTest#Use cases that save an aggregate must publish its domain events"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
given:
ArchCondition<JavaClass> publishAfterSaving =
  new ArchCondition<JavaClass>("publish the aggregate's domain events after saving it") {
    @Override
    void check(JavaClass item, ConditionEvents events) {
      boolean savesAnAggregate = item.methodCallsFromSelf.any {
        it.target.name == "save" && it.targetOwner.isAssignableTo(Repository)
      }
      if (!savesAnAggregate) {
        return
      }
      boolean publishes = item.methodCallsFromSelf.any {
        it.target.name == "publishAndClearEvents" && it.targetOwner.isAssignableTo(DomainEventPublisher)
      }
      events.add(publishes
        ? SimpleConditionEvent.satisfied(item, "${item.simpleName} publishes after saving")
        : SimpleConditionEvent.violated(item, "${item.simpleName} saves an aggregate without publishing its domain events"))
    }
  }

expect:
classes()
  .that().resideInAPackage(APPLICATION_PACKAGE)
  .and().haveSimpleNameEndingWith("UseCase")
  .and().areNotInterfaces()
  .should(publishAfterSaving)
  .because("A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - even when the action raised no event")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
