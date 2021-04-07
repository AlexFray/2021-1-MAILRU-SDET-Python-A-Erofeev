from selenium.webdriver.common.by import By
from ui.locators.base_locators import BasePageLocators


class DashboardPageLocators(BasePageLocators):
    CREATE = (By.XPATH, "//*[text() = 'Создать кампанию']")
    CREATE_NEW = (By.XPATH, "//a[@href='/campaign/new']")
    NAME_CAMPAIGN = (By.XPATH, '//a[@title="{}"]')
    CAMPAIGN_CHECKBOX = (By.XPATH, '//div[./a[@title="{}"]]//input')
    ACTION_CAMPAIGN_MENU = (By.CSS_SELECTOR, '[class*="tableControls-module-selectItem"]')
    ACTION_CAMPAIGN_DELETE = (By.XPATH, "//li[@title='Удалить']")
