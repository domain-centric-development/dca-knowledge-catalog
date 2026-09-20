---
type: Pitfall
title: "A committed default that only a comment forbids"
tags: [pitfall, security, infrastructure, bootstrap]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/jwt-implementation-guide/7b-a-committed-default-must-not-start-a-real-deployment.md]
---

A value checked into the repository so the application starts without configuration — a signing secret, an
administrative account, a cookie policy that omits `Secure` because the developer's URL is `http` — marked dev-only
by a comment, a property name or a paragraph in the README, and by nothing the runtime can act on.

## Why it is wrong

- A committed secret is a published secret. Whoever can read the repository can mint a token the deployment
  accepts, as any user and with any role. The same is true of an administrative password, and of a session cookie
  that travels over plain HTTP where it is readable in transit.
- Nothing announces the mistake. The application starts, the pages render, the suites pass, and the behaviour is
  identical to a development run. The only thing that changed is who else can read the traffic.
- The comment is read by the person who already knows. The deployment is done by someone who does not, often
  through an image that carries no configuration of its own and therefore keeps every default in it.
- The default of the runtime's own switch usually points the wrong way for this purpose: an application that is
  not told what it is either defaults to production and keeps the development values, or defaults to development
  and excuses them. Neither default refuses them.

## Do instead

Name each shipped value as a constant, and refuse it at startup unless the runtime says this is a development run.
The input is the platform's own switch — an active profile, a hosting environment — never a hostname, a port or a
guess, and an application that is not told what it is treats itself as real.

Fail while the deployment is being watched, not on first use: a configuration refused at startup is a rollback,
the same refusal on a user's first request is an incident. Put the check where the options are bound, one per
group of settings, so a context owns the rule about its own configuration instead of one class knowing everybody's
secrets — and make sure the components agree on what a development run is, because two answers means one of them
accepts a shipped value where the other refuses it.

Say in the failure message which variable supplies a proper value. A fail-fast the operator cannot act on is only
an outage.

Two traps sit inside the fix itself:

- **The guard compares against a value nobody uses.** The constant and the fallback in the configuration file are
  two copies of one string, and they drift: then the guard refuses a value that never appears and passes the one
  that does. Pin them to each other with a test that reads the configuration file.
- **The validator is written but never registered.** A guard nobody wires refuses nothing, and the class reads
  exactly the same either way. The test that proves the rule must start the real application, not construct the
  validator.

Declare the development run everywhere a developer starts the application — the build's run task, the test tasks,
the compose file, the IDE run configuration — and nowhere else. The deployable artifact carries no such
declaration, so running it unconfigured is a refusal with a message rather than a silent weakness.

- Related pitfalls: [Authenticated is not authorized: a filter that enriches every request](/pitfall/authenticated-is-not-authorized.md)

## Anchors

- Guide: [A committed default must not start a real deployment](/guide/jwt-implementation-guide/7b-a-committed-default-must-not-start-a-real-deployment.md) · [Cookie requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md)
