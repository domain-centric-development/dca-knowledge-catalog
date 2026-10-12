---
type: Section
title: "Tasks: what keeps behaviour"
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Not every change is behaviour. Dead code, a method a port inherits and nobody calls, a placeholder file, copied test
helpers, a dependency to raise, a build to configure — no actor would notice any of them, so none has a criterion, and
a story would have to invent one to get past its red test. Such a change is a backlog item of its own
(`kind: task`): no criterion, a sentence of what changes in the code, and — where it settles a judge's finding — the
finding rows it closes. It runs plan, build, tidy, judge and document; there is no test stage, because there is
nothing new to prove. Its evidence is everything proven before: the build and tidy gates run the whole suite, and a
test that existed before the task may not change. The judge asks the one question that tells the kinds apart —
would an actor notice? — and a yes makes it a story.

The question also places what looks like a task and is not. A bug is a story: something an actor sees is wrong, and a
test shows it red. Taking a feature away is a story too: the absence is its criterion, and the scenarios that held
leave the spec with it. A task is only as safe as the suite under it — a framework upgrade that changes a default no
test covers passes as a task and changes behaviour all the same.
