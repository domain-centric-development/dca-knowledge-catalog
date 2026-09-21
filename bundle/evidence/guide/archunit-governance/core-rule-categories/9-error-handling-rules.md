---
type: Reference
title: Core Rule Categories — 9. Error Handling Rules
tags: [reference]
evidence_for: "/guide/archunit-governance/core-rule-categories.md#9-error-handling-rules"
---

[Full node and context](/guide/archunit-governance/core-rule-categories.md#9-error-handling-rules). This is an evidence excerpt; retain the parent selection and caveats.

### 9. Error Handling Rules

A failure of an inner layer has its own type, and the type says which layer owns the failure: a broken rule of
the model extends `DomainException`, a request the application cannot serve extends `UseCaseException`. Both
base types come from the building blocks, so a rule can select on them.

```java
// Every exception the domain layer declares extends the model's base type. Catalog: DCA-ERR-001.
@ArchTest
static final ArchRule domain_exceptions_extend_the_domain_base_type =
    classes().that().resideInAPackage("..domain..")
        .and().areAssignableTo(Throwable.class)
        .and().areNotAssignableFrom(DomainException.class)
        .should().beAssignableTo(DomainException.class)
        .because("A failure the model raises is a broken business rule and says so through its type");

// A subtype lives in the layer whose failure it names. Catalog: DCA-ERR-002.
@ArchTest
static final ArchRule domain_exceptions_reside_in_the_domain_layer =
    classes().that().areAssignableTo(DomainException.class)
        .and().resideOutsideOfPackage("dev.domaincentric.dca.buildingblocks..")
        .should().resideInAPackage("..domain..")
        .because("The base type states which layer owns the failure");

// No container, persistence or protocol metadata on an inner-layer failure. Catalog: DCA-ERR-004.
@ArchTest
static final ArchRule failures_carry_no_framework_metadata =
    noClasses().that().areAssignableTo(DomainException.class)
        .or().areAssignableTo(UseCaseException.class)
        .should().beAnnotatedWith(ResponseStatus.class)
        .because("@ResponseStatus on a domain exception is the adapter's decision taken in the domain layer");

// The name says what went wrong, not what the caller should be told. Catalog: DCA-ERR-005.
@ArchTest
static final ArchRule failure_names_stay_in_the_language_of_their_layer =
    noClasses().that().areAssignableTo(DomainException.class)
        .or().areAssignableTo(UseCaseException.class)
        .should().haveSimpleNameEndingWith("Error")
        .orShould().haveSimpleNameContaining("Http")
        .because("A failure named after a transport concept decides the answer in a layer that does not know "
            + "the protocol");
```

The catalog states these as `DCA-ERR-001` … `DCA-ERR-005`, plus `DCA-ERR-003` for the application layer's own
base type: an exception declared in an application package extends `UseCaseException`, and a `DomainException`
subtype declared there is reported too, because a failure of the model belongs to the model.

`DCA-ERR-006` is the one diagnostic in the set. It lists incoming adapter packages that drive an input port and
name neither base type, and it never fails the build. That is as far as static analysis reaches: **a `throw` and
a `catch` are not part of the import model.** Whether a specific refusal should have been a domain exception,
and whether an adapter catches `Exception` around a use-case call, no rule can decide. A package on the
diagnostic's list is not a finding by itself — an event consumer whose failed reaction belongs to the delivery
machinery's retry is a good answer — but each entry should have one.

---
