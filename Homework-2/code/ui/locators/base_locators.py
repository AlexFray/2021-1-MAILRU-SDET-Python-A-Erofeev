from selenium.webdriver.common.by import By


class BasePageLocators:
    SEGMENTS = (By.XPATH, '//li//a[@href="/segments"]')
    STATISTICS = (By.XPATH, '//li//a[@href="/statistics"]')
    USER_ACCOUNT = (By.CSS_SELECTOR, '[class*="right-module-rightButton"]')
    MENU_ACCOUNT = (By.CSS_SELECTOR, '[class*="rightMenu-module-visibleRightMenu"]')
