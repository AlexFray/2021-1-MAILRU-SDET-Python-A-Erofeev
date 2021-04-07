from selenium.webdriver.common.by import By
from ui.locators.segment_locators import SegmentPageLocators


class SegmentNewPageLocators(SegmentPageLocators):
    NAME_SEGMENT = (By.XPATH, "//div[@class='input input_create-segment-form']//div/input")
    PLAY_AND_PAY_CHECKBOX = (By.CSS_SELECTOR, '[class*="adding-segments-source__checkbox js-main-source-checkbox"]')
