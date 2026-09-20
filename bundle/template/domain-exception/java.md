---
type: Template
title: "Domain exception skeleton — Java"
parent: /template/domain-exception.md
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-005.md, /rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/rules.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Domain exception skeleton](/template/domain-exception.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Rule}Violated.java` — an invariant would break

```java
package {basePackage}.{context}.domain.{name};

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
// inside the use case — the lookup came back empty
{Name} {name} = {name}s.findById({name}Id).orElseThrow(() -> new {Name}NotFound({name}Id));
```

## Where each layer stands

- **Domain** raises `DomainException` subtypes and nothing else of its own. The exception is part of the model: named after the rule that was broken, typed fields for the facts it compared. No framework annotation, no transport concern. An argument guard keeps the platform's argument exception — it states a caller contract, not a rule of the model.
- **Application** raises `UseCaseException` subtypes: not found, not owned by this caller, a precondition on a second aggregate. It lets a domain exception propagate; it catches one only when it needs to *change behaviour* — try an alternative, compensate — never to translate it.
- **Adapter** catches — all of it. `@ExceptionHandler` in a page controller renders the 404 view; a `@RestControllerAdvice` maps each type to a `ProblemDetail` with a status (`404` for not found, `422` for a violated rule); an event consumer rejects or parks the message. The transport decision lives here and nowhere further in. The [page controller](/template/page-controller.md) and [REST resource](/template/rest-resource.md) templates show the handlers.

## Naming

The name comes from the ubiquitous language: what is missing or which rule was broken, in past or noun form (`{Name}NotFound`, `{Rule}Violated`, `{Name}AlreadyClosed`). An `Exception` suffix is fine — `{Name}NotFoundException` names a fact, not a technical role. What the rules reject is a name that decides the answer instead of stating the failure: `Error`, `Fault` and `Failure` as a suffix, and `Http`, `Status` or `Response` anywhere in the name. One type per outcome is what lets an adapter answer each of them differently; a single exception reused across a context puts that decision back into a string.
