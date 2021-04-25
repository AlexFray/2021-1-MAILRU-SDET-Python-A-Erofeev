import allure
import logging

from ui.locators.segment_locators import SegmentPageLocators
from ui.pages.segment_new_page import SegmentNewPage
from ui.pages.base_page import BasePage

logger = logging.getLogger('test')


class SegmentPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentPageLocators()

    @allure.step('Создание сегмента.')
    def create_segment(self, name):
        create = self.find(self.locators.CREATE_NEW)
        if create is None or not create.is_displayed():
            create = self.find(self.locators.SAVE_SEGMENT)
        create.click()
        segmentNew = SegmentNewPage(self.driver)
        segmentNew.create_segment(name)
        assert self.is_opened()

    @allure.step('Удаление сегмента.')
    def delete_segment(self, name):
        logger.info(f'Поиск сегмента с названием {name} и его выделение в таблице.')
        checkbox = (self.locators.CHECKBOX_SEGMENT[0], self.locators.CHECKBOX_SEGMENT[1].format(name))
        self.click(checkbox)
        logger.info(f'Открытие меню действий с сегментами.')
        self.click(self.locators.ACTION_FOR_SEGMENT)
        logger.info(f'Удаление сегмента.')
        self.click(self.locators.DELETE_SEGMENT)
