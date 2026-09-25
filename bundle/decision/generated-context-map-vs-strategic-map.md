---
type: Decision
title: Generated context map or strategic context map
tags: [decision, context-map, governance]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/contextmap/dca-map-001.md, /rule/contextmap/dca-map-004.md, /rule/contextmap/dca-map-012.md]
---

A project that declares its relationships in code has two context maps, not one, and they answer different
questions. Keep them in two files with two owners; one file that tries to be both drifts, because a generator
overwrites whatever a human wrote into it.

The **generated map** answers *which contexts exist and which dependencies they declare*. It is rendered from
the declarations on the context roots, it belongs beside the other derived architecture documents, and the test
that renders it compares the result with the committed file and fails when it was stale. Nobody edits it; the
fix for a difference is always to commit the regenerated file.

The **strategic map** answers *what kind of relationship this is and why*. Relationship pattern names, the
subdomain type of each context, and the reason a dependency has the shape it has are judgements, not facts a
declaration carries — no attribute or annotation states that a supplier relationship is Customer/Supplier
rather than Conformist, or that a context serves a supporting subdomain. It is written by hand, it is allowed
to be less complete than the generated map, and it names the generated map as authoritative wherever the two
disagree about a dependency's existence.

Two consequences worth stating, because both have been got wrong:

- A test that only writes the generated file, without comparing it to what was committed, is not a check. It
  repairs the document silently, and the drift it was installed against reaches the next reader unnoticed. The
  same holds when the test skips its comparison because it could not locate the target — that path must fail,
  not pass.
- The two files must not swap places between implementations of the same system. A reader who learns the
  layout from one code base and finds the opposite meaning under the same file name in the other has been
  taught a convention that does not hold.

A project without the declarations has only the strategic map, maintained by hand from the code; adding the
declarations later adds the generated map beside it and takes the dependency listing out of the hand-written
one.

- [Declared relationships must match real dependencies](/rule/contextmap/dca-map-001.md)
- [Upstream declarations reference an existing context](/rule/contextmap/dca-map-004.md)
- [Partnership declarations are symmetric](/rule/contextmap/dca-map-012.md)
- [New context or extend an existing one](/decision/new-context-vs-extend-existing.md)
- [Cross-context communication](/decision/cross-context-communication.md)
- [Designed context map reconciled to the code](/pitfall/designed-map-reconciled-to-the-code.md)
