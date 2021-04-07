import allure
import logging

from ui.locators.segment_new_locators import SegmentNewPageLocators
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class SegmentNewPage(BasePage):
    url = 'https://target.my.com/segments/segments_list/new'
    locators = SegmentNewPageLocators

    @allure.step('Заполнение данных сегмента и сохранение.')
    def create_segment(self, name):
        logger.info('Выбор сегмента.')
        self.click(self.locators.PLAY_AND_PAY_CHECKBOX)
        logger.info('Добавление сегмента.')
        self.click(self.locators.ADD_SEGMENT)
        logger.info('Ввод названия сегмента.')
        self.inputText(name, self.locators.NAME_SEGMENT)
        logger.info('Сохранение сегмента.')
        self.click(self.locators.SAVE_SEGMENT)
