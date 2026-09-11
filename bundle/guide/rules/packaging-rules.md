---
type: Section
title: PACKAGING RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

- Package by bounded context, then by layer; inside the application layer by use case — optionally grouped into
  features (see [Grouping use cases into features](/guide/package-structure/grouping-use-cases-into-features.md))
- Layer separation enforced by module structure
- Domain module has zero external dependencies
- Application module depends only on domain
- Adapter modules depend on application
- Infrastructure module depends on adapters
- Modules can be independently deployed

> **Note:** For Spring Modulith module organization, see [Spring Modulith Implementation](/guide/spring-modulith.md)


Entity constructors may be public. Construction belongs to the entity itself or
to an aggregate, entity or cooperating factory in the same context's domain layer.
Adapters reconstitute through the aggregate's or factory's reconstitution method,
without raising a creation event. The architecture check cannot identify ownership
inside a context: another aggregate in that same context passes, so review must
verify the actual invariant boundary.
