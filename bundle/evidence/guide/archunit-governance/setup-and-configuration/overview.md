---
type: Reference
title: Setup and Configuration — Overview
tags: [reference]
evidence_for: /guide/archunit-governance/setup-and-configuration.md
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md). This is an evidence excerpt; retain the parent selection and caveats.

The DCA rules ship as a library — `dev.domaincentric:dca-archunit` — pinned to the building blocks
your code implements (`dev.domaincentric:dca-building-blocks`). A project adds one dependency and one
test class; the rule categories below explain what that class checks and serve as templates for the
project-specific rules you add next to it.
