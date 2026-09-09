---
type: Reference
title: RULES — ERROR HANDLING RULES
tags: [reference]
evidence_for: "/guide/readme/rules.md#error-handling-rules"
---

[Full node and context](/guide/readme/rules.md#error-handling-rules). This is an evidence excerpt; retain the parent selection and caveats.

### ERROR HANDLING RULES

#### Exception Layer Placement
- **Domain Exceptions** - Business rule violations (e.g., `InsufficientStockException`, `InvalidOrderStateException`)
- **Application Exceptions** - Use case failures (e.g., `OrderNotFoundException`, `CustomerNotActiveException`)
- **Adapter Exceptions** - Translated to appropriate responses (HTTP status codes, error DTOs)

#### Exception Flow Pattern
```
Domain Exception (invariant violation)
    ↓ propagates to
Application Layer (can catch, wrap, or let propagate)
    ↓ propagates to
Adapter Layer (translates to external format)
    ↓ returns
HTTP 400/404/422 + Error DTO
```

#### Error Handling Best Practices
- Domain exceptions should be **domain language** (not technical)
- Use cases catch domain exceptions only when they need to **transform behavior**
- Adapters (controllers) handle **all exceptions** and convert to external format
- Never expose stack traces or internal details to external consumers
- Use **exception mappers** or `@ExceptionHandler` in adapters for consistent responses

#### Example - Exception Handling Across Layers
```java
// Domain exception (business rule violation)
public class InsufficientStockException extends RuntimeException {
    private final ProductId productId;
    private final int requested;
    private final int available;
    // Constructor with domain details
}

// Application exception (use case failure)
public class ProductNotFoundException extends RuntimeException {
    private final ProductId productId;
    public ProductNotFoundException(ProductId productId) {
        super("Product not found: " + productId.value());
        this.productId = productId;
    }
}

// Adapter - Exception handler (translates to HTTP response)
@RestControllerAdvice
public class OrderExceptionHandler {
    @ExceptionHandler(ProductNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handle(ProductNotFoundException ex) {
        return new ErrorResponse("PRODUCT_NOT_FOUND", ex.getMessage());
    }

    @ExceptionHandler(InsufficientStockException.class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    public ErrorResponse handle(InsufficientStockException ex) {
        return new ErrorResponse("INSUFFICIENT_STOCK", "Not enough stock available");
    }
}
```
