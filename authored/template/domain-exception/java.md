---
type: Template
title: "Domain exception skeleton — Java"
parent: /template/domain-exception.md
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainexception.md, /marker/application/portexception.md, /marker/application/inputportexception.md, /marker/application/usecaseexception.md, /marker/application/outputportexception.md, /marker/application/refusal.md, /rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-008.md, /rule/errors/dca-err-005.md, /rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/rules.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Domain exception skeleton](/template/domain-exception.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Rule}Violated.java` — an invariant would break

```java
package {basePackage}.{context}.domain.model;

import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainException;

/** Raised by the aggregate when a behaviour method would violate the {Rule} rule. */
public class {Rule}Violated extends DomainException {

    private final {Name}Id {name}Id;
    private final int requested;
    private final int available;

    public {Rule}Violated(final {Name}Id {name}Id, final int requested, final int available) {
        super("{Rule} violated for " + {name}Id.value()
                + ": requested " + requested + ", available " + available);
        this.{name}Id = {name}Id;
        this.requested = requested;
        this.available = available;
    }

    public {Name}Id {name}Id() { return {name}Id; }
    public int requested() { return requested; }
    public int available() { return available; }
}
```

```java
// inside the aggregate — the invariant is checked before state changes
public void take(final int quantity) {
    if (quantity < 1) throw new IllegalArgumentException("quantity must be positive"); // argument guard
    if (quantity > available) throw new {Rule}Violated(id, quantity, available);        // business rule
    available -= quantity;
    registerEvent({Name}Taken.of(id, quantity));
}
```

## `{Name}NotFound.java` — the request addressed something that is not there

```java
package {basePackage}.{context}.application.{operation};

import dev.domaincentric.dca.buildingblocks.application.UseCaseException;

/** Raised when a {Name} is addressed by an id that does not exist. Carries the id, not a message. */
public class {Name}NotFound extends UseCaseException {

    private final {Name}Id {name}Id;

    public {Name}NotFound(final {Name}Id {name}Id) {
        super("{Name} not found: " + {name}Id.value());
        this.{name}Id = {name}Id;
    }

    public {Name}Id {name}Id() {
        return {name}Id;
    }
}
```

```java
// inside the use case — the lookup came back empty, before anything is written
{Name} {name} = {name}s.findById({name}Id).orElseThrow(() -> new {Name}NotFound({name}Id));
```

## `Duplicate{Name}.java` — a conflict an output port declares

```java
package {basePackage}.{context}.application.shared;

import dev.domaincentric.dca.buildingblocks.application.OutputPortException;

/** Declared by {Name}Repository: another {Name} already carries that {key}. Thrown by every adapter of the port. */
public class Duplicate{Name} extends OutputPortException {

    private final {Name}Id {name}Id;

    public Duplicate{Name}(final {Name}Id {name}Id) {
        super("{Name} already exists: " + {name}Id.value());
        this.{name}Id = {name}Id;
    }

    public {Name}Id {name}Id() {
        return {name}Id;
    }
}
```

```java
// the port declares it — part of the contract every adapter keeps
public interface {Name}Repository extends Repository<{Name}, {Name}Id> {
    /** @throws Duplicate{Name} if another {name} already carries that {key} */
    @Override
    {Name} save({Name} {name});
}

// inside the use case — caught by its concrete type, inside the transaction too
try {
    {name}s.save({name});
} catch (Duplicate{Name} duplicate) {
    throw new {Name}AlreadyRegistered(duplicate.{name}Id());   // a context that throws: its own use-case exception
}
```

## In a context that returns its refusals

`{Rule}Violated` and `Duplicate{Name}` stay exceptions — the model and the adapter throw them. `{Name}NotFound` has no file of its own; it is a case of the use case's result, and the use case turns the two exceptions into cases:

```java
public sealed interface {Operation}Result
        permits {Operation}Result.{Done}, {Operation}Result.{Name}NotFound,
                {Operation}Result.{Rule}Violated, {Operation}Result.{Name}AlreadyRegistered {

    record {Done}({Name}Id {name}Id) implements {Operation}Result {}
    record {Name}NotFound({Name}Id {name}Id) implements {Operation}Result, Refusal {}
    record {Rule}Violated({Name}Id {name}Id, int requested, int available) implements {Operation}Result, Refusal {}
    record {Name}AlreadyRegistered({Name}Id {name}Id) implements {Operation}Result, Refusal {}
}
```

```java
// inside the use case — decide, then write; only the save's own conflict can come from the write itself
Optional<{Name}> found = {name}s.findById({name}Id);
if (found.isEmpty()) {
    return new {Name}NotFound({name}Id);
}
try {
    found.get().take(command.quantity());
} catch ({Rule}Violated violated) {
    return new {Operation}Result.{Rule}Violated(violated.{name}Id(), violated.requested(), violated.available());
}
try {
    {name}s.save(found.get());
} catch (Duplicate{Name} duplicate) {
    return new {Name}AlreadyRegistered(duplicate.{name}Id());   // the boundary rolls back on the returned Refusal
}
return new {Done}({name}Id);
```

## Where each layer stands

- **Domain** raises `DomainException` subtypes and nothing else of its own. The exception is part of the model: named after the rule that was broken, typed fields for the facts it compared. No framework annotation, no transport concern. An argument guard keeps the platform's argument exception — it states a caller contract on a value only code passes, not a rule of the model. A value object built from input refuses null with its rule's named failure.
- **Application** declares two kinds. A use case throws `UseCaseException` subtypes — never `InputPortException` directly: not found, not owned by this caller, a precondition on a second aggregate. An output port declares `OutputPortException` subtypes its adapters throw, and the use case catches each by its concrete type. In a context that throws, the use case lets a domain exception propagate and catches one only when it needs to *change behaviour* — try an alternative, compensate. In a context that returns, it catches the concrete domain and output-port exceptions it can raise and returns their cases.
- **Adapter** answers — all of it, once per context. In a context that throws, `@ExceptionHandler` in a page controller renders the 404 view, a `@RestControllerAdvice` maps each type to a `ProblemDetail` with a status (`404` for not found, `422` for a violated rule), an event consumer rejects or parks the message. In a context that returns, a switch over the result names every case and the handler keeps the rest. Never a handler for `PortException` or `InputPortException`. The transport decision lives here and nowhere further in. The [page controller](/template/page-controller.md) and [REST resource](/template/rest-resource.md) templates show both forms.

## Naming

The name comes from the ubiquitous language: what is missing or which rule was broken, in past or noun form (`{Name}NotFound`, `{Rule}Violated`, `{Name}AlreadyClosed`). An `Exception` suffix is fine — `{Name}NotFoundException` names a fact, not a technical role. What the rules reject is a name that decides the answer instead of stating the failure: `Error`, `Fault` and `Failure` as a suffix, and `Http`, `Status` or `Response` anywhere in the name. One type per outcome is what lets an adapter answer each of them differently; a single exception reused across a context puts that decision back into a string.
