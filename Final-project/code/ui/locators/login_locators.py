from ui.locators.base_locators import *


class LoginPageLocators(BasePageLocators):
    USERNAME = (By.ID, 'username')
    PASSWORD = (By.ID, 'password')
    CREATE = (By.XPATH, '//a[@href="/reg"]')
