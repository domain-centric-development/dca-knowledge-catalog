---
type: Section
title: Test Organization
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### Directory Structure

```
src/test-e2e/java/de/sample/aiarchitecture/e2e/
├── BaseE2ETest.java           # Common test setup
├── CheckoutGuestE2ETest.java  # Guest checkout flow tests
├── CheckoutLoginE2ETest.java  # Authenticated checkout tests
└── pages/                     # Page objects
    ├── BasePage.java
    ├── ProductCatalogPage.java
    └── ...
```

### BaseE2ETest Setup

```java
public abstract class BaseE2ETest {
    protected static final String BASE_URL = System.getProperty("e2e.baseUrl", "http://localhost:8080");
    protected static final boolean HEADLESS = Boolean.parseBoolean(System.getProperty("e2e.headless", "true"));

    protected static Playwright playwright;
    protected static Browser browser;
    protected BrowserContext context;
    protected Page page;

    @BeforeAll
    static void launchBrowser() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new BrowserType.LaunchOptions().setHeadless(HEADLESS)
        );
    }

    @AfterAll
    static void closeBrowser() {
        if (browser != null) browser.close();
        if (playwright != null) playwright.close();
    }

    @BeforeEach
    void createContextAndPage() {
        context = browser.newContext();
        page = context.newPage();
    }

    @AfterEach
    void closeContext() {
        if (context != null) context.close();
    }

    protected void navigateTo(String path) {
        page.navigate(BASE_URL + path);
    }

    protected void waitForUrl(String urlPattern) {
        page.waitForURL(BASE_URL + urlPattern);
    }

    protected String getCurrentPath() {
        return page.url().replace(BASE_URL, "");
    }
}
```

---
