---
type: Reference
title: DOMAIN LAYER RULES — Value Object Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#value-object-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#value-object-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Value Object Rules
- Value Objects are immutable
- Value Objects have no identity
- Value Objects compared by all attributes
- Replace entire Value Object instead of modifying
- Value Objects can be shared freely
- Value Objects validate themselves; state the numeric range and rounding of every monetary value object. Reconstitution, deserialisation and default struct construction must not bypass invalid-state checks.
- **A rule is checked once — in the value object.** A value object built from input refuses everything its rule
  refuses, null included, with the rule's named failure. The incoming adapter hands it the raw value and does not
  check the rule again: no annotation that repeats it, no default that turns an absent value into an empty one.
  A second copy at the edge drifts from the first, and when the rule changes — null becomes valid, the limit grows —
  two places change instead of one. Bean Validation or DataAnnotations belong only where no value object carries the
  rule
- Side-effect-free methods only
- A value from a fixed set — a role, a status, a kind — is a type whose instances are the set. An enum when the
  members are names and nothing more; a value object with one instance per member as soon as a member carries data
  of its own — a code, a label, a rule — so the type reads the same in every language. A string compared against a
  literal in several places is a typo the compiler cannot see, and a class of string constants still lets every
  other string through
- A value object's operations take and return its own kind: a quantity is reduced by a quantity, an amount added
  to an amount. A bare number crossing the method leaves the check of its unit to every caller
- One factory per origin. A value built from input and a value rebuilt from storage are two origins with
  different checks — validated and derived on the way in, taken as given on the way back — and each has its own
  named factory (`fromInput(...)`, `fromStored(...)`). A neutral `of(...)` beside them leaves the caller to guess
  which checks run. A value with one origin keeps its one factory
- **A string, a number or a moment that means something is a value object.** A postal code, a quantity, an
  opening date each carry rules of their own — a format, a range, a meaning — and held as a bare `String`, `int` or
  `Instant` those rules are repeated at every use, or missing. A value of several components holds values too: an
  address holds a `Street`, a `PostalCode` and a `City`, not three strings. Only a wrapper — a value of exactly one
  component — holds the primitive it wraps. An identifier is a typed id, never a bare `UUID`: the type says whose it
  is. What a building block prescribes keeps its type: a domain event's `occurredOn()` and `eventId()` describe the
  event, not the domain, and carry no rules of their own — a business moment such as an opening date or a date of
  birth does, and is a value (`DCA-TAC-025`, experimental)
- **A single yes/no fact is a `boolean` field; a `boolean` parameter is a flag argument.** The aggregate keeps the
  fact to itself, is told to change it and answers when asked:

  ```java
  private boolean completed;

  public void complete() { this.completed = true; }

  public boolean isCompleted() { return completed; }
  ```

  `setCompleted(true)` would let the caller set the state instead of triggering the behaviour, so no domain method
  takes a `boolean`, and nothing outside sets the field. The one exception is the factory that rebuilds a stored
  aggregate — `reconstitute(...)`, or `restore(...)`: it hands the stored fact back to the type that holds it and
  triggers nothing, so it takes the `boolean` as it was stored. The rule recognises that factory by its name; a
  project that names it otherwise configures its own. A `boolean` returned is a question to the object and fine,
  though an aggregate is told what to do rather than asked and then decided about from outside. Three or more
  states, or transitions with rules of their own, are an enum or a value. Facts that hold independently — completed,
  archived, deleted — are separate fields, never one status. A project's glossary may decide otherwise; then the
  glossary applies (`DCA-TAC-025`)
