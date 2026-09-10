# onion

- [Domain must not access Application Services (Onion Architecture - Domain is innermost layer)](dca-oni-001.md) — Domain is the innermost layer in onion architecture and should not depend on application services.
- [The Domain Model should be framework independent and should not use 3rd party libraries when possible](dca-oni-002.md) — Domain should be framework-independent (Dependency Inversion Principle).
- [Domain models must not carry prohibited framework metadata](dca-oni-003.md) — Domain objects carry no metadata for container management, persistence or transaction coordination.
