---
type: Template
title: "Domain exception skeleton — Java"
parent: /template/domain-exception.md
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/rules.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Domain exception skeleton](/template/domain-exception.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}NotFound.java` — a lookup came back empty

```java
package {basePackage}.{context}.domain.{name};

/** Raised when a {Name} is addressed by an id that does not exist. Carries the id, not a message. */
public class {Name}NotFound extends RuntimeException {

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

## `{Rule}Violated.java` — an invariant would break

```java
package {basePackage}.{context}.domain.{name};

/** Raised by the aggregate when a behaviour method would violate the {Rule} rule. */
public class {Rule}Violated extends RuntimeException {

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
    if (quantity > available) throw new {Rule}Violated(id, quantity, available);
    available -= quantity;
    registerEvent({Name}Taken.of(id, quantity));
}
```

## Where each layer stands

- **Domain** throws. The exception is part of the model: named after the rule or the missing thing, typed fields for the facts, an unchecked base (`RuntimeException` or one abstract domain base per context). No framework type, no transport concern.
- **Application** lets it propagate, or throws `{Name}NotFound` itself when `repository.findById(...)` is empty. A use case catches a domain exception only when it needs to *change behaviour* — try an alternative, compensate — never to translate it.
- **Adapter** catches — all of it. `@ExceptionHandler` in a page controller renders the 404 view; a `@RestControllerAdvice` maps to `ProblemDetail` with a status (`404` for not-found, `422` for a violated rule); an event consumer rejects or parks the message. The transport decision lives here and nowhere further in. The [page controller](/template/page-controller.md) and [REST resource](/template/rest-resource.md) templates show the handlers.

## Naming

The name comes from the ubiquitous language: what is missing or which rule was broken, in past or noun form (`{Name}NotFound`, `{Rule}Violated`, `{Name}AlreadyClosed`). An `Exception` suffix is acceptable — `{Name}NotFoundException` names a fact, not a technical role — and the naming rule that forbids `Manager`, `Helper`, `Util`, `Impl` on domain classes does not object to it. What it does object to is a technical name over a domain fact: `{Name}Error`, `DomainException` reused everywhere, `ValidationHelper`. A dedicated marker interface and rule set for exceptions may come later; the template needs neither — a plain `RuntimeException` subclass in the domain package is complete.
