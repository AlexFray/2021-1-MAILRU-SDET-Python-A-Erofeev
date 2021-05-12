from selenium.webdriver.common.by import By

from ui.locators.locators_base import BasePageLocators


class SourceNewsLocators(BasePageLocators):
    SOURCE = (By.XPATH, "//*[@text='{}']")
    SELECTED_SOURCE = (By.XPATH, "//android.widget.FrameLayout[.//*[@text='{}']]//android.widget.ImageView")  # Вести FM

