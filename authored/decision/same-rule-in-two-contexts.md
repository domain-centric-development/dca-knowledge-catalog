---
type: Decision
title: The same rule in two contexts — share the code or share the contract
tags: [decision, bounded-context, shared-kernel, domain]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/sharedkernel.md, /rule/strategic/dca-str-003.md, /decision/cross-context-communication.md]
---

Two contexts check something that looks like the same thing, and the duplicated code is uncomfortable. Before
moving it into a shared kernel, look at what is actually the same — usually it is the *form*, not the rule.

**Read the two versions side by side and separate three layers.** The arithmetic — summing amounts, comparing
quantities — is not domain knowledge; it belongs to the value objects both contexts already share, and it is
not duplication worth a decision. The *shape* — iterate the items, collect the findings, answer with a result
— repeats, and repeats cheaply. The *rule* is where they differ, and the difference is usually consequence,
not condition: one context reports what it found so a person can react, the other refuses to proceed. Both
may check availability; only one turns a changed price into a refusal.

**Prefer duplication over a shared kernel here.** A shared kernel is the most expensive relationship on the
context map: every change has to be agreed between both sides, and the rules that look alike today are the
ones that drift tomorrow, because each context acquires its own obligations. Sharing the code freezes them
together at exactly the moment they start to differ. Duplication across a context boundary is not the
duplication that DRY warns about — the two copies answer to different owners.

**Do not let the downstream ask the upstream to decide.** Moving the check into the other context because it
already has one puts a decision in the hands of a context that does not carry its consequence. Whoever is
committed by the outcome owns the rule.

**Share the contract instead of the code.** Write the overlap down where both sides can be held to it: a
scenario with data that every implementation must satisfy, and beside it the scenario that only one of them
must satisfy. The agreement then lives in a form that survives both implementations, the divergence becomes a
statement rather than a suspicion, and neither context depends on the other to keep it.

**When it really is one rule with one owner,** the answer is not a shared kernel either: it is one context
publishing it, and the other consuming the answer through its published interface — a dependency with a
direction, which a shared kernel does not have.

- [Shared kernel](/marker/strategic/sharedkernel.md)
- [Modules must not access each other in the application layer](/rule/strategic/dca-str-003.md)
- [Cross-context communication](/decision/cross-context-communication.md)
- [New context or extend an existing one](/decision/new-context-vs-extend-existing.md)
