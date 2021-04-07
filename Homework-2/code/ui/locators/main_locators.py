from selenium.webdriver.common.by import By


class MainPageLocators:
    SIGN_IN = (By.CSS_SELECTOR, '[class*="responseHead-module-button"]')
    LOGIN = (By.CSS_SELECTOR, '[placeholder="Email или номер телефона"]')
    PASSWORD = (By.CSS_SELECTOR, '[placeholder="Пароль"]')
    ENTER = (By.CSS_SELECTOR, '[class*="authForm-module-button"]')