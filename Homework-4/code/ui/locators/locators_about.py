from selenium.webdriver.common.by import By
from ui.locators.locators_base import BasePageLocators


class AboutPageLocators(BasePageLocators):
    VERSION = (By.ID, 'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT = (By.ID, 'ru.mail.search.electroscope:id/about_copyright')
