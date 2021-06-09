from ui.locators.base_locators import *


class RegPageLocators(BasePageLocators):
    USERNAME = (By.ID, 'username')
    EMAIL = (By.ID, 'email')
    PASSWORD = (By.ID, 'password')
    PASSWORD_CONFIRM = (By.ID, 'confirm')
    ACCEPT = (By.ID, 'term')
    RETURN_LOGIN = (By.XPATH, '//a[@href="/login"]')
