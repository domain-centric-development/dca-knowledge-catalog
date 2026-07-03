---
type: ADR
title: "ADR-001: Separate REST API and Web MVC Controllers into Different Packages"
adr: 1
status: accepted
pattern: "We will separate REST API controllers and Web MVC controllers into distinct packages within each bounded context:."
resource: ai-architecture-sample/docs/architecture/adr/adr-001-api-web-package-separation.md
tags: [adr, package-structure]
---

We will separate REST API controllers and Web MVC controllers into distinct packages within each bounded context:.

**Consequences:** Clearer Architecture · Better Separation · Easier Security · Independent Versioning · Team Ownership · Discoverability · Testing · Documentation

## Enforced by

- [Controller classes must end with 'Controller'](/rule/naming/controller-classes-must-end-with-controller.md)
- [REST Controllers must end with 'Resource' (REST best practice)](/rule/naming/rest-controllers-must-end-with-resource-rest-best-practice.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
