---
type: Pitfall
title: "Chatty outgoing port: the adapter pays for every small question"
tags: [pitfall, hexagonal, port-out, adapter, performance]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/outputport.md, /marker/tactical/value.md, /guide/dependency-structure/the-composition-root.md]
---

**When it applies:** an outgoing adapter reaches something expensive (a process it starts, a remote service, a file it
reads, a database round trip) to answer a question whose answer stays the same while one use case or one run lasts.
The pitfall does not apply where the answer can change between two questions, or where a question costs nothing.

An output port asks small questions: where the data folder is, which tenant this is, which region is configured, which
schema version the store holds. Each method is clean on its own, and each adapter answers the obvious way: it asks the
outside again. One use case asks the same thing ten times from ten places, and every answer is the same. No single
call is wrong, so no review finds the problem, and a fast machine hides the cost. On a slower platform, over a remote
link or on a busy disk, the same code runs several times slower. The time is spread over a hundred calls of a few
milliseconds each, and no profile shows them as one hot spot.

## Why it happens

- **The port is cut by question, not by use.** Each caller needs one fact, so each fact gets a method, and the adapter
  reaches the outside once per method. The questions belong together because they describe one thing, but the port
  hands them out one at a time.
- **The cost is invisible where the code is written.** On the developer's machine a process start, a local socket or
  a cached file read takes about a millisecond. Where starting a process is expensive or the service is remote, the
  same call takes ten or thirty.
- **The callers do not know about each other.** Each caller asks once and looks cheap. Only the total over a use case
  or a run shows how often the same question was asked.

## The wrong cure: a cache without a lifetime

The obvious fix is to remember the answer in a dictionary at module level, a static field or a singleton. That removes
the calls, but the cache keeps answers after they stop being true. The process outlives the thing the answer described:
a folder becomes a repository of its own, a tenant is reconfigured, or a test fixture replaces the previous one in the
same process. The cache still answers for the old one. The failure appears far from the cache: two independent units
of work suddenly share a lock, or a record lands in the wrong place. It shows only on the platform or in the order
where the stale answer is reached. Keying the cache by a path or a name does not help, because the key stays the same
while the thing it names changes.

## How it shows up

- The same call to the outside appears many times in one trace, with the same arguments and the same answer.
- A suite or a batch run is several times slower on one platform than on another, and no single call is slow.
- After a cache is added to fix the slowness, tests fail only in a certain order, or only on a platform where the
  temporary folder lies inside something the cache remembered.

## Do instead

- **Build one value per use case or run.** Gather the facts the questions describe into one value object. Whoever
  starts the use case or the run builds it once, with one call to the outside, and hands it to the adapters that need
  it. The composition root of that entry point builds it, and the adapters take it instead of asking.
- **Give it the lifetime of the work, never of the process.** The value lives as long as the use case, request or run
  that built it, and is dropped with it. The next run builds its own and sees the world as it is at that time. When a
  run moves to another place, such as another tenant or another working copy, it builds the value for that place there.
- **Leave out what changes.** A fact that changes during the work (the latest version, a counter, the current head of
  a log) does not belong in the value. Read it when it is needed: from something cheap where the value says where to
  look, otherwise from the outside.
- **Treat "not there" as an answer.** Where the place does not exist yet, the value is absent, and the adapters treat
  it as absent. Never fill it with the answer for something around it.
- **Count before and after.** The evidence is the number of calls to the outside per use case or run, counted per
  caller. The time on one machine is not evidence.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [Value](/marker/tactical/value.md)
- Guide: [The composition root](/guide/dependency-structure/the-composition-root.md), where the value for one entry
  point is built and handed on
