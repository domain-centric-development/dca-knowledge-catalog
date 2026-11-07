---
type: Reference
title: "ERROR HANDLING RULES — Own infrastructure, a foreign system"
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#own-infrastructure-a-foreign-system"
---

[Full node and context](/guide/rules/error-handling-rules.md#own-infrastructure-a-foreign-system). This is an evidence excerpt; retain the parent selection and caveats.

### Own infrastructure, a foreign system

**Own infrastructure throws; a foreign system's expected failure is a refusal.** The system's own infrastructure —
its database, its broker — has to be there. When it fails, nothing in the request is wrong and no caller can answer
it: the failure stays the platform's exception, the transaction rolls back, and the delivery machinery or the
operator takes over. A foreign system behind an output port — a payment provider, a mail provider — is different.
That it refuses, times out or cannot be reached is expected behaviour of the integration, and the caller has an
answer for it: choose another provider, try again later, carry on without the mail.

- The output port declares that failure in its contract, as an `OutputPortException` subtype named in the port's
  language (`PaymentGatewayUnavailableException`).
- The adapter catches the client's own failure — the timeout, the refused connection, the error status — and throws
  the declared one. It decides nothing else.
- The use case catches the declared failure and turns it into its own refusal: a case of its result, marked
  `Refusal` (`PaymentProviderUnavailable`), where the context returns; its own use-case exception
  (`PaymentProviderUnavailableException`) where the context throws. Either way the transaction rolls back.

**Which systems are foreign is read from the context map, not decided per failure.** A system the context declares
as an external system it talks to (`@ExternalUpstream`) is foreign; every other piece of infrastructure is the
system's own. A failure of a foreign system that the port does not declare stays unexpected — the declaration is the
list of what the caller is meant to answer.

A caller with nobody to answer — an event consumer — throws the case back as an exception, so the delivery is
retried later; see [What a result does not do for you](#what-a-result-does-not-do-for-you).
