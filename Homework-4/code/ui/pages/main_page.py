from ui.pages.base_page import BasePage
from ui.locators.locators_main import MainPageLocators
from ui.pages.settings_page import SettingsPage


class MainPage(BasePage):
    locators = MainPageLocators()

    def search_text(self, text, cart_info, additional_info, result):
        self.click(self.locators.KEYBOARD)
        self.inputText(text, self.locators.SEARCH_INPUT)
        self.click(self.locators.INPUT_ACTION)
        self.driver.hide_keyboard()
        info = self.find(self.locators.FACT_CARD_CONTEXT).text
        assert cart_info in info
        count = (self.locators.TEXT[0],
                 self.locators.TEXT[1].format(additional_info))
        self.click(count)
        count = (self.locators.TEXT[0],
                 self.locators.TEXT[1].format(result))
        assert self.find(count)

    def edit_source(self, name_source):
        self.click(self.locators.SETTINGS)
        SettingsPage(self.driver).edit_source_news(name_source)
        self.click(self.locators.KEYBOARD)
        self.inputText('News', self.locators.SEARCH_INPUT)
        self.click(self.locators.INPUT_ACTION)
        self.driver.hide_keyboard()
        return self.find(self.locators.TRACK_NAME).text

    def calculation(self, expression, res):
        self.click(self.locators.KEYBOARD)
        self.inputText(expression, self.locators.SEARCH_INPUT)
        self.click(self.locators.INPUT_ACTION)
        self.driver.hide_keyboard()
        result = (self.locators.TEXT[0],
                  self.locators.TEXT[1].format(res))
        return self.find(result).text

    def check_info(self, version):
        self.click(self.locators.SETTINGS)
        SettingsPage(self.driver).check_info(version)
