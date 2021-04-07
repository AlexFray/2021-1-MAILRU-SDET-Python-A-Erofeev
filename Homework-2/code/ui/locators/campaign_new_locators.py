from selenium.webdriver.common.by import By
from ui.locators.base_locators import BasePageLocators


class CampaignPageLocators(BasePageLocators):
    TRAFFIC = (By.XPATH, "//*[text() = 'Трафик']")
    LINK = (By.CSS_SELECTOR, '[placeholder="Введите ссылку"]')
    BANNER = (By.XPATH, "//*[text() = 'Баннер']")
    LINK_FOR_BANNER = (By.CSS_SELECTOR, '[placeholder="Введите адрес ссылки"]')
    NAME = (By.XPATH, '//div[@class="input input_campaign-name input_with-close"]//div//input')
    UPLOAD_FILE = (By.XPATH, "//input[@data-test='image_240x400']")
    SAVE_IMAGE = (By.CSS_SELECTOR, '[class="image-cropper__save js-save"]')
    CREATE_CAMPAIGN = (By.XPATH, "//div[@class='button__text' and text() = 'Создать кампанию']")
