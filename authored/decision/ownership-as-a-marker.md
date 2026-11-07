---
type: Decision
title: Ownership as a marker — an aggregate that belongs to someone, and where the marker stops
tags: [decision, tactical, aggregate, repository, security, application]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/application-layer-rules.md, /marker/tactical/owned.md, /marker/port-out/repository.md, /rule/tactical/dca-tac-026.md, /pitfall/resource-id-without-an-owner.md, /decision/where-authorization-and-validation-live.md]
---

Some aggregates belong to someone — a patient's record, a tenant's workspace, a visitor's draft — and some belong to nobody: a catalogue entry, a price list, a stock level. An aggregate that belongs to someone must never be reachable by its id alone: whoever knows or guesses the id would get it. That is the insecure direct object reference of broken access control, OWASP Top 10 **A01**. A review perspective and a pitfall can name the defect; they do not stop it from coming back in the next use case. A marker on the aggregate makes the distinction visible to a rule.

## The discriminator

1. **Does the aggregate belong to an identity the system knows — an account, a tenant, a pseudonymous guest?** Mark it `Owned<OwnerId>` (`IOwned<TOwnerId>` in C#, `impl Owned { type OwnerId = … }` in Rust). Its repository declares a lookup by the aggregate's id *and* the owner's id, and every use case acting for a caller loads it through that lookup.
2. **Does it belong to nobody?** Leave it unmarked. A rule that demanded a scoped lookup from every repository would demand one from the catalogue too — wrong, which is why the rule selects on the marker and not on every aggregate.
3. **Is there no identity at all, and is the id itself the secret?** Leave it unmarked as well — see the alternative below.

## Options

### Mark the aggregate `Owned` (do this where an owner exists)

```java
public final class MedicalRecord extends BaseAggregateRoot<MedicalRecord, MedicalRecordId>
    implements Owned<PatientId> { … }

public interface MedicalRecordRepository extends Repository<MedicalRecord, MedicalRecordId> {
    Optional<MedicalRecord> findByIdForPatient(MedicalRecordId id, PatientId patient);
}
```

`DCA-TAC-026` (experimental) then holds the repository to the scoped lookup: a method taking the aggregate's id type and the owner's id type, returning the aggregate. "Not there" and "not yours" become one answer, which is what the caller should be told.

### Leave ownership to review and the pitfall

Cheaper to start with, and it does not hold: the defect a review found once appears again in the next aggregate that belongs to someone, written by someone who did not read the review.

### The id as the secret (the deliberate alternative to `Owned`)

A system without any identity for its visitors — "whoever holds the link may" — keeps a long random id in a cookie or a link. There is no owner to scope a lookup by; the safety is the id's unguessability. Such an aggregate is not `Owned`, and that is a choice, not an omission: say so where the aggregate is defined, so nobody mistakes it for a forgotten marker.

## What the marker says, and what it does not

- **"Has an owner", not "always the same owner".** The owner may change — a visitor's draft taken over by the account they sign into — but only through an explicit operation of the aggregate (`takeOverBy(account)`), called after the use case proved the caller's right to the change. Before and after it, both aggregates are found through their owner; the rule holds through the whole flow.
- **The guard of a change of owner is not the marker's.** Whether the caller may take over what they name — for example, that the guest identity carried in the signed token is the draft's owner, and a request naming another guest is refused before anything is read — is use-case logic no marker can verify. Its tests prove it. Do not read `DCA-TAC-026` as covering it.
- **A guest is an owner.** A visitor given a pseudonymous identity on the first request owns what they create, and the scoped lookup works the same for them. Registering keeps the identity, so nothing moves. The identity is safe when it comes from a signed token and is not guessable — never from a value the client names.
- **A forgotten marker silences the rule.** An aggregate that belongs to someone but carries no `Owned` is not selected, and the suite reports nothing. Marking it is part of modelling it, like naming its invariants.
- **The rule checks the repository, not the call.** Whether a use case calls the scoped lookup or the unscoped `findById` is a review question. A path that holds no owner to name — a migration, a scheduled clean-up over all aggregates — may use `findById` and says why. An event that asks for an effect on somebody's aggregate usually carries whose it is; then the consumer's use case loads through the owner too.

## Consequences

- Repositories of owned aggregates carry two lookups: the scoped one for every caller, `findById` for the paths without an owner.
- The ownership check is the data-dependent half of authorization ("is this yours?"); it lives in the use case, where the stored aggregate is. The claims-only half ("is this caller staff?") may sit on the route — see [Where authorization and validation live](/decision/where-authorization-and-validation-live.md).

## Anchors

- Guide: [Application layer rules](/guide/rules/application-layer-rules.md) — *Owned aggregates*, under the repository rules
- Marker: [Owned&lt;OWNER&gt;](/marker/tactical/owned.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Rule: [The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id](/rule/tactical/dca-tac-026.md)
- Pitfall: [Resource id without an owner](/pitfall/resource-id-without-an-owner.md)
- Related decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
