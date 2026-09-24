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

The same file says whether the project drives a browser: `browser: playwright` when its end-user command
runs a browser suite, `none` when it deliberately has none. A criterion only a browser can observe then
gets a browser test; with `none` the plan takes the next lower level and says what that cannot show.
Unset, such a criterion stops the plan once for the stack decision rather than degrading every story.

The same file may name the model each tool runs a stage on, as a key bound to the tool
(`model.<tool>.<stage>`). It is bound to the tool because a model's name means nothing to another
tool: an unbound key in a shared profile breaks a colleague's run with a different tool at the first
stage it names. The process itself names no model; which stages can run on a cheaper one without
the review finding more is the project's to measure. A stage run in its own process sees only the
project — its skills, its settings, the craft the profile names — and not the plugins or servers of
whoever starts it, so two people get the same pipeline.

Two consequences. Adding a capability (a formatter, a second test source set, another review
perspective) is a line in that file, not an edit to a stage. And a stage that would break in a
project without your domain in it is wrong: the process is general, the project's knowledge is the
project's.
