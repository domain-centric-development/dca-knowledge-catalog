---
type: Reference
title: ERROR HANDLING RULES — The adapter answers
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#the-adapter-answers"
---

[Full node and context](/guide/rules/error-handling-rules.md#the-adapter-answers). This is an evidence excerpt; retain the parent selection and caveats.

### The adapter answers

No base type and no case knows a status code, a header or a message shape. The incoming adapter maps the
outcome to the protocol's answer and writes the words itself — from the failure's values, never from an exception's
message. **The answer to each case is written once per context**: the switches at the call sites name the case,
and a class of the adapter writes the answer they all return (`OrderProblems` above). What is still thrown goes to
**one exception handler per context**:

```java
@RestControllerAdvice(basePackages = "com.company.project.order.adapter.incoming.api")
public class OrderApiExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail handleMalformedCall(final IllegalArgumentException exception) {
        return problem(HttpStatus.BAD_REQUEST, "Request not understood", null);
    }

    @ExceptionHandler(UseCaseException.class)
    public ProblemDetail handleUseCaseFailure(final UseCaseException exception) {
        return problem(HttpStatus.SERVICE_UNAVAILABLE, "Request cannot be served now", null);
    }

    private static ProblemDetail problem(final HttpStatus status, final String title, final String detail) {
        final ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setTitle(title);
        return problem;
    }
}
```

A context that throws its refusals maps them here too, one `@ExceptionHandler` per type, with the words and the
status a switch arm would have written:

```java
    @ExceptionHandler(OrderNotFoundException.class)
    public ProblemDetail handleOrderNotFound(final OrderNotFoundException exception) {
        return problem(HttpStatus.NOT_FOUND, "Order not found",
                "There is no order " + exception.orderId().value() + ".");
    }

    @ExceptionHandler(OrderAlreadyShippedException.class)
    public ProblemDetail handleAlreadyShipped(final OrderAlreadyShippedException exception) {
        return problem(HttpStatus.CONFLICT, "Order already shipped",
                "Order " + exception.orderId().value() + " left the warehouse on " + exception.shippedAt() + ".");
    }
```

Either way, the answer to each refusal is written once per context: in the handler where the context throws, in
the class the switches call where it returns.

The answer is an RFC 9457 problem document — `ProblemDetail` in Spring, `ProblemDetails` in ASP.NET Core.
No project needs an error DTO of its own.

**The status follows the failure, not the base type.** A position missing from a cart is a rule of the model
and still answers `404`, because what the caller has to do about it is ask for something that exists. As a
starting point: `404` for something that is not there, `409` for a conflict with existing state, `422` for a
rule that refused an understood request, `400` for a value the model does not accept at all, `503` for a foreign
system that did not answer.

**`404` belongs to the addressed resource.** It answers a path that names nothing. A reference in the request
body that parses but names nothing — an id posted to a resource that exists — answers `422`: the request was
understood, and what it refers to does not exist. A `404` there would claim something false about the resource
the path addresses, and the caller would look for the error in the wrong place. A reference that does not parse
at all is a malformed call and answers `400`, before any use case runs.

Page controllers of the same context switch over the same results — or, where the context throws, catch the same
types — and render the page's own words into the form it came from: a text the page keeps per refusal, or a message
key its translations resolve, filled with the refusal's values. One use case, several protocols, one answer per case on each, and every sentence in the language of the
surface that shows it.

Two things the adapter must not do: expose a stack trace or an internal detail to the outside, and catch
`Exception` or `RuntimeException` around a use case call. A blanket catch answers a defect of this
application the same way as a refusal the customer caused.
