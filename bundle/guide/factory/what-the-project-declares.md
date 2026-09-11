---
type: Section
title: What the project declares
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Nothing above knows how your project builds. That knowledge lives in one file the project owns —
build and test commands, one entry per test source set, the architecture suite, the formatter — plus
the backlog, the glossary and the context map it keeps anyway. A stage asks the project; it never
assumes a build tool, a test framework or a directory layout.

Two consequences. Adding a capability (a formatter, a second test source set, another review
perspective) is a line in that file, not an edit to a stage. And a stage that would break in a
project without your domain in it is wrong: the process is general, the project's knowledge is the
project's.
