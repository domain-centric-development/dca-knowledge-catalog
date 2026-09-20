---
type: Section
title: 7b. A Committed Default Must Not Start a Real Deployment
chapter: JWT Implementation Guide
source: guide
resource: dca-guide/topics/jwt-implementation-guide.md
tags: [guide, section]
---

Everything above is configuration, and configuration ships with a value that makes the application
start on a laptop: a signing secret in the repository, an operator account with a password anyone
can read, cookies without `Secure` because the developer's URL is `http`. Each is deliberate and
each is fine — until the same values start somewhere else, which they do silently. Nothing fails, no
log line says anything, and the application behaves exactly as it does in development. A committed
secret is a published secret: whoever can read the repository can mint a token the deployment
accepts.

Documenting them as dev-only does not hold. A comment is read by the person who already knows;
the deployment is done by someone who does not.

> **Rule:** name the development values as constants, and refuse them at startup unless the runtime
> says it is a development run. The runtime's own switch is the input — an active profile, a
> hosting environment — never a hostname or a guess, and the default of that switch is *not*
> development: an application that is not told what it is treats itself as real. The failure message
> names the variable that supplies a proper value, because a fail-fast an operator cannot act on is
> only an outage.

Fail at startup rather than on first use. A configuration refused while the deployment is watched is
a rollback; the same refusal on a visitor's first request is an incident.

The check belongs where the options are bound, one per group of settings, so a context owns the
rule about its own configuration rather than a central class knowing everybody's secrets. What must
not differ is the answer to "is this a development run" — two components disagreeing on that is one
of them accepting a shipped value where the other refuses it.

---
