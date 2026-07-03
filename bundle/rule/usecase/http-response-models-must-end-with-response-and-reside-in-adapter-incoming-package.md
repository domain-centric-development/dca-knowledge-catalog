---
type: Rule
title: HTTP Response Models must end with 'Response' and reside in adapter incoming package
rule: "HTTP response models should be in adapter incoming layer (ADR-020: Adapter layer uses *Response)."
constraint: HTTP Response Models must end with 'Response' and reside in adapter incoming package.
enforced_by: "UseCasePatternsArchUnitTest#HTTP Response Models must end with 'Response' and reside in adapter incoming package"
status: enforced
test_class: UseCasePatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/UseCasePatternsArchUnitTest.groovy
tags: [usecase, archunit]
---

```groovy
expect:
// Use allIncomingAdapterPatterns() — covers all bounded contexts via @BoundedContext
// discovery PLUS the @SharedKernel-annotated module's adapter, where cross-cutting
// Response classes (ErrorResponse, base Response, SimpleResponse) typically live.
// Hardcoded context lists are fragile — they break the moment a new context is added.
classes()
  .that().haveSimpleNameEndingWith("Response")
  .and().resideInAnyPackage(BASE_PACKAGE + "..")
  .should().resideInAnyPackage(allIncomingAdapterPatterns())
  .because("HTTP response models should be in adapter incoming layer (ADR-020: Adapter layer uses *Response)")
  .allowEmptyShould(true)
  .check(allClasses)
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
