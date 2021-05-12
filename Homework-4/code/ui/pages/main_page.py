from ui.pages.base_page import BasePage
from ui.locators.locators_main import MainPageLocators
from ui.pages.settings_page import SettingsPage


class MainPage(BasePage):
    locators = MainPageLocators()

    def search_text(self, text, result):
        self.searchText(text)
        info = self.find(self.locators.FACT_CARD_CONTEXT).text
        assert result in info

    def search_additional_info(self, text, auxiliary, result):
        elem = (self.locators.TEXT[0],
                self.locators.TEXT[1].format(auxiliary))
        self.swipe_element_lo_left(elem)
        elem = (self.locators.TEXT[0],
                self.locators.TEXT[1].format(text))
        self.swipe_element_lo_left(elem)
        self.click(elem)
        count = (self.locators.TEXT[0],
                 self.locators.TEXT[1].format(result))
        assert self.find(count)

    def edit_source(self, name_source):
        self.click(self.locators.SETTINGS)
        SettingsPage(self.driver).edit_source_news(name_source)
        self.back(2)

    def calculation(self, expression, res):
        self.searchText(expression)
        result = (self.locators.TEXT[0],
                  self.locators.TEXT[1].format(res))
        return self.find(result).text

    def check_info(self, version):
        self.click(self.locators.SETTINGS)
        SettingsPage(self.driver).check_info(version)
