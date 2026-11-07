---
type: Marker
title: "Owned<OWNER>"
category: tactical
kind: interface
signature: "public interface Owned<OWNER extends Id>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
generics: OWNER extends Id
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Owned.java
tags: [tactical, marker]
---

Marker interface for an Aggregate Root that belongs to someone.

An owned aggregate is reachable only through its owner. Its Repository therefore declares a
lookup that takes the aggregate's id *and* the owner's id, and a use case acting for a
caller loads it through that lookup — never by id alone. An object loaded by its id alone is
reachable by anyone who knows or guesses the id: the insecure direct object reference of broken
access control (OWASP Top 10, A01).

The type argument names the owner's id type: `MedicalRecord implements Owned`, `Workspace implements Owned`. The marker carries no method;
the owner is a field of the aggregate like any other, and the owner id type is what the
Repository's scoped lookup takes.

**What it says, and what not:**

- "Has an owner", not "always the same owner". The owner may change, but only through an
explicit operation of the aggregate — a draft a visitor started as a guest, taken over by
the account they sign into — called after the use case proved the caller's right to the
change. That proof is logic of the use case, which no marker can verify; its tests prove
it.
- An owner need not be an account. A guest given a pseudonymous identity on the first request
is an owner: the aggregate belongs to that identity, provided it comes from a signed token
and is not guessable, never from a value the client names.
- Where no identity exists and the aggregate's id itself is the secret — a long random id in
a link, "whoever holds it may" — there is no owner to scope a lookup by, and the aggregate
is not `Owned`. Its safety is the id's unguessability.

**Example:**

```java
public final class MedicalRecord extends BaseAggregateRoot<MedicalRecord, MedicalRecordId>
    implements Owned<PatientId> {
  private PatientId patient;
  ...
}

public interface MedicalRecordRepository extends Repository<MedicalRecord, MedicalRecordId> {
  Optional<MedicalRecord> findByIdForPatient(MedicalRecordId id, PatientId patient);
}
```

Forgetting `implements Owned` silences every rule that selects on it; marking the
aggregates that belong to someone is part of modelling them.

## Related mentions in guides (heuristic)

- [APPLICATION LAYER RULES](/guide/rules/application-layer-rules.md)
