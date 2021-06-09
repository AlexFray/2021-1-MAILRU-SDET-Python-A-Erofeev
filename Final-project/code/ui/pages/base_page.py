import allure
import logging
from selenium.common import exceptions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ui.locators.base_locators import BasePageLocators
from utils.decorators import wait

logger = logging.getLogger('test')
CLICK_RETRY = 3
TIME_WAIT = 10


class PageNotLoadedException(Exception):
    pass


class TextNotFound(Exception):
    pass


class BasePage:
    url = 'http://testapp:8080'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'Страница по ссылке {self.__class__.__name__} открыта...')
        assert self.is_opened()

    def is_opened(self):
        def _check_url():
            current: str = self.driver.current_url
            if self.url not in current:
                raise PageNotLoadedException(
                    f'{self.url} did not opened in {TIME_WAIT} for {self.__class__.__name__}.\n'
                    f'Current url: {self.driver.current_url}.')
            return True

        return wait(_check_url, error=PageNotLoadedException, check=True, timeout=TIME_WAIT, interval=0.3)

    def find(self, locator, timeout=TIME_WAIT):
        try:
            def _find():
                return self.driver.find_element(*locator)

            return wait(_find, error=exceptions.NoSuchElementException, check=True, timeout=timeout, interval=0.2)
        except TimeoutError:
            return None

    def finds(self, locator):
        return self.driver.find_elements(*locator)

    def wait_text(self, text, locator, timeout=2):
        try:
            def _wait_text():
                txt: str = self.find(locator).text
                if txt != text:
                    raise TextNotFound(f'Текст: "{text}" не найден. Текущий текст: {txt}.')
                return txt

            return wait(_wait_text, error=TextNotFound, check=True, timeout=timeout, interval=0.2)
        except TimeoutError:
            return None

    @allure.step('Ввод текста "{text} в поле с локатором {locator}."')
    def inputText(self, text, locator):
        input = self.find(locator)
        input.clear()
        input.send_keys(text)

    def wait(self, timeout: int = TIME_WAIT):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @allure.step('Клик по элементу с локатором {locator}.')
    def click(self, locator, timeout=TIME_WAIT):
        for i in range(CLICK_RETRY):
            logger.info(f'Клик по элементу {locator}. Попытка {i + 1} из {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(ec.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
