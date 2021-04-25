from selenium.webdriver.common.by import By
from ui.locators.base_locators import BasePageLocators


class SegmentPageLocators(BasePageLocators):
    CREATE_NEW = (By.XPATH, "//a[@href='/segments/segments_list/new/']")
    ADD_SEGMENT = (By.XPATH, "//button[./div[text()='Добавить сегмент']]")
    SAVE_SEGMENT = (By.XPATH, "//button[./div[text()='Создать сегмент']]")
    CHECKBOX_SEGMENT = (By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid__innerScrollContainer') and .//a[text()='{}']]//div//div//input")
    ACTION_FOR_SEGMENT = (By.CSS_SELECTOR, '[class*="segmentsTable-module-selectItem"]')
    DELETE_SEGMENT = (By.XPATH, "//li[@title='Удалить']")
    NEW_SEGMENT = (By.XPATH, "//a[text() = '{}']")

