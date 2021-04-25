from selenium.webdriver.common.by import By
from ui.locators.locators_base import BasePageLocators


class SettingsPageLocators(BasePageLocators):
    SOURCE_NEWS = (By.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT = (By.ID, 'ru.mail.search.electroscope:id/user_settings_about')
