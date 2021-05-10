from selenium.webdriver.common.by import By
from ui.locators.locators_base import BasePageLocators


class MainPageLocators(BasePageLocators):
    FACT_CARD_CONTEXT = (By.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_content_text')
    TEXT = (By.XPATH, "//android.widget.TextView[@text = '{}']")
    SETTINGS = (By.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    TRACK_NAME = (By.ID, 'ru.mail.search.electroscope:id/player_track_name')
