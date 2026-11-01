---
type: Pitfall
title: An event without a type of its own
tags: [pitfall, domain, domain-event, events, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainevent.md, /rule/advanced/dca-adv-001.md, /rule/advanced/dca-adv-008.md, /guide/elements.md]
---

An aggregate's events written as the cases of one type, each case with its fields inline:

```java
public sealed interface TaskEvent extends DomainEvent {
    // every case is only a name and a set of fields inside the one type
    enum Kind { CREATED, COMPLETED }
    Kind kind();
    Map<String, Object> data();
}
```

In a language whose enums carry data the same shape is one enum with a variant per event and the fields
in the variant. It is short, and the aggregate gets one event type to collect. But no single event can be
named: there is no type `TaskCompleted`.

## Why it is wrong

- A consumer that reacts to one event cannot ask for that event. It takes the whole set and picks the case
  out, and the compiler no longer tells it which fields it gets.
- The rules on an event read a type: immutable shape (`DCA-ADV-001`), a timestamp field (`DCA-ADV-008`), no
  schema version in the payload. A case without a type is checked as part of the set or not at all.
- A story or a metric names the event (`TaskCompleted`). The code then holds no declaration of that name to
  find, test or document.
- The same event becomes a record in one language and a case in another, so two implementations of the
  same story drift apart.

## Do instead

Every event is a type of its own that implements `DomainEvent`. The aggregate's set of events is a closed
type over those types, never a place for fields:

```java
public sealed interface TaskEvent extends DomainEvent permits TaskCreated, TaskCompleted {}
public record TaskCompleted(UUID eventId, TaskId task, Instant occurredOn) implements TaskEvent {}
```

```csharp
public abstract record TaskEvent : IDomainEvent;
public sealed record TaskCompleted(Guid EventId, TaskId Task, DateTimeOffset OccurredOn) : TaskEvent;
```

In a language with data-carrying enums, the enum has one variant per event, and each variant carries
exactly that event's type (`TaskEvent::Completed(TaskCompleted)`).

## Anchors

- Markers: [DomainEvent](/marker/tactical/domainevent.md)
- Rules: [Domain Events must implement DomainEvent and have immutable shape](/rule/advanced/dca-adv-001.md) · [Domain Events must have a timestamp field](/rule/advanced/dca-adv-008.md)
- Guide: [Elements](/guide/elements.md)
