from ui.locators.base_locators import *


class MainPageLocators(BasePageLocators):
    LOGOUT = (By.XPATH, '//a[@href="/logout"]')
    VK_ID = (By.XPATH, '//*[text()="VK ID: {}"]')
    USER_ID = (By.XPATH, '//*[text()="Logged as {}"]')
    QUOTE = (By.XPATH, '//footer/div/p')
