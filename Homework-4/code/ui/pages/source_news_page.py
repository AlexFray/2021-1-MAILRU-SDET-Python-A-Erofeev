from ui.locators.locators_sourse_news import SourceNewsLocators
from ui.pages.base_page import BasePage


class SourceNewsPage(BasePage):
    locators = SourceNewsLocators()

    def change_source(self, name_source):
        button = (self.locators.SOURCE[0], self.locators.SOURCE[1].format(name_source))
        self.click(button)
        selected = (self.locators.SELECTED_SOURCE[0], self.locators.SELECTED_SOURCE[1].format(name_source))
        assert self.find(selected)
        self.driver.back()
