---
type: Section
title: Page Object Pattern
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### Why Page Objects?

Page Objects encapsulate page-specific selectors and interactions, providing:

- **Single point of change** - Selectors defined once per page
- **Readable tests** - Tests read like business workflows
- **Type-safe navigation** - Compiler catches invalid transitions
- **Reusability** - Page objects shared across test classes

### Design Rules

1. **One page object per page/view** - Each distinct page gets its own class
2. **Fluent API** - Navigation methods return the target page object
3. **URL validation** - Constructors validate expected URL pattern (fail-fast)
4. **Centralized selectors** - All `data-test` values are private constants
5. **No assertions in page objects** - Page objects return data; tests assert

### Structure

```
src/test-e2e/java/de/sample/aiarchitecture/e2e/pages/
├── BasePage.java              # Common methods for all pages
├── ProductCatalogPage.java    # Product listing interactions
├── ProductDetailPage.java     # Product detail and add to cart
├── CartPage.java              # Shopping cart operations
├── BuyerInfoPage.java         # Checkout: buyer information
├── DeliveryPage.java          # Checkout: delivery address
├── PaymentPage.java           # Checkout: payment selection
├── ReviewPage.java            # Checkout: order review
└── ConfirmationPage.java      # Order confirmation
```

### BasePage Implementation

```java
public abstract class BasePage {
    protected static final String BASE_URL = System.getProperty("e2e.baseUrl", "http://localhost:8080");
    protected final Page page;

    protected BasePage(Page page, String expectedUrlPattern) {
        this.page = page;
        page.waitForURL(BASE_URL + expectedUrlPattern);
    }

    protected BasePage(Page page) {
        this.page = page;
    }

    protected void click(String dataTest) {
        page.locator("[data-test='" + dataTest + "']").click();
    }

    protected void clickFirst(String dataTest) {
        page.locator("[data-test='" + dataTest + "']").first().click();
    }

    protected void fill(String name, String value) {
        page.locator("input[name='" + name + "']").fill(value);
    }

    protected void waitFor(String dataTest) {
        page.locator("[data-test='" + dataTest + "']").first().waitFor();
    }

    protected boolean exists(String dataTest) {
        return page.locator("[data-test='" + dataTest + "']").count() > 0;
    }

    protected boolean pageContains(String text) {
        return page.locator("body").textContent().contains(text);
    }
}
```

### Example Page Object

```java
public class BuyerInfoPage extends BasePage {
    private static final String URL_PATTERN = "/checkout/buyer";
    private static final String CONTINUE_BUTTON = "buyer-continue-button";
    private static final String LOGIN_LINK = "buyer-login-link";

    public BuyerInfoPage(Page page) {
        super(page, URL_PATTERN);
    }

    public BuyerInfoPage fillBuyerInfo(String email, String firstName,
                                        String lastName, String phone) {
        fill("email", email);
        fill("firstName", firstName);
        fill("lastName", lastName);
        fill("phone", phone);
        return this;
    }

    public DeliveryPage continueToDelivery() {
        click(CONTINUE_BUTTON);
        return new DeliveryPage(page);
    }

    public LoginPage goToLogin() {
        click(LOGIN_LINK);
        return new LoginPage(page);
    }

    public boolean hasValidationErrors() {
        return pageContains("valid email") || pageContains("error");
    }
}
```

### Example: ProductCatalogPage

```java
public class ProductCatalogPage extends BasePage {
    private static final String URL_PATTERN = "/products";
    private static final String PRODUCT_CARD = "product-card";
    private static final String VIEW_DETAILS_LINK = "product-view-details-link";

    public ProductCatalogPage(Page page) {
        super(page, URL_PATTERN);
        waitFor(PRODUCT_CARD);
    }

    public static ProductCatalogPage navigateTo(Page page) {
        page.navigate(BASE_URL + URL_PATTERN);
        return new ProductCatalogPage(page);
    }

    public ProductDetailPage viewFirstProduct() {
        clickFirst(VIEW_DETAILS_LINK);
        return new ProductDetailPage(page);
    }

    public boolean hasProducts() {
        return exists(PRODUCT_CARD);
    }
}
```

---
