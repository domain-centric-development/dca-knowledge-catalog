---
type: Rule
title: The Domain Model should be framework independent and should not use 3rd party libraries when possible
rule: "Domain should be framework-independent (Dependency Inversion Principle)."
constraint: The Domain Model should be framework independent and should not use 3rd party libraries when possible.
enforced_by: "OnionArchitectureArchUnitTest#The Domain Model should be framework independent and should not use 3rd party libraries when possible"
status: enforced
test_class: OnionArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/OnionArchitectureArchUnitTest.groovy
tags: [onion, archunit]
---

```groovy
expect:
final JavaClasses importedClasses = new ClassFileImporter()
.withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
.importPackages(BASE_PACKAGE)

final String[] domainPackagePatterns = [
  "${BASE_PACKAGE}.product.domain..",
  "${BASE_PACKAGE}.cart.domain..",
  "${BASE_PACKAGE}.checkout.domain..",
  "${BASE_PACKAGE}.account.domain..",
  "${BASE_PACKAGE}.inventory.domain..",
  "${BASE_PACKAGE}.pricing.domain..",
  "${BASE_PACKAGE}.sharedkernel.domain..",
  "${BASE_PACKAGE}.sharedkernel.marker.tactical..",   // Allow DDD marker interfaces
  "${BASE_PACKAGE}.sharedkernel.marker.port.out.."    // Allow output port interfaces (e.g., Repository)
] as String[]

final ArchRule domainClassesMustNotDependOnAnyFrameworkOr3rdParty =
classes()
.that().resideInAnyPackage(domainPackagePatterns)
.should().onlyDependOnClassesThat().resideInAnyPackage(Stream.concat(
THIRD_PARTY_PACKAGES_ALLOWED_IN_DOMAIN.stream(),
Arrays.stream(domainPackagePatterns)).toArray(String[]::new))
.because("Domain should be framework-independent (Dependency Inversion Principle)")

domainClassesMustNotDependOnAnyFrameworkOr3rdParty.check(importedClasses)
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
