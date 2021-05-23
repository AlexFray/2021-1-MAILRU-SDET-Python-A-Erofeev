from appium.webdriver.common.touch_action import TouchAction
from selenium.common import exceptions
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators.locators_base import BasePageLocators
from utils.decorators import wait
from selenium.webdriver.support import expected_conditions as EC

CLICK_RETRY = 3
TIME_WAIT = 10


class ItemNotFound(Exception):
    pass


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout: int = TIME_WAIT):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=TIME_WAIT):
        try:
            def _find():
                return self.driver.find_element(*locator)

            return wait(_find, error=exceptions.NoSuchElementException, check=True, timeout=timeout, interval=0.2)
        except TimeoutError:
            return None

    def click(self, locator, timeout=TIME_WAIT):
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator, timeout=timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def inputText(self, text, locator):
        input = self.find(locator)
        input.clear()
        input.send_keys(text)

    def searchText(self, text):
        self.click(self.locators.KEYBOARD)
        self.inputText(text, self.locators.SEARCH_INPUT)
        self.click(self.locators.INPUT_ACTION)
        self.driver.hide_keyboard()

    def swipe_up(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, немного ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element(self, locator, max_swipes):
        """
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать вверх
        """
        already_swiped = 0
        while self.find(locator) is None:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def swipe_element_lo_left(self, locator):
        """
        :param locator: локатор, который мы ищем
        1. Находим наш элемент на экране
        2. Получаем его координаты (начала, конца по ширине и высоте)
        3. Находим центр элемента (по высоте)
        4. Делаем свайп влево, двигая центр элемента за его правую часть в левую сторону.
        """
        web_element = self.find(locator)
        if web_element is not None:
            left_x = web_element.location['x']
            right_x = left_x + web_element.rect['width']
            upper_y = web_element.location['y']
            lower_y = upper_y + web_element.rect['height']
            middle_y = (upper_y + lower_y) / 2
            action = TouchAction(self.driver)
            action. \
                press(x=right_x, y=middle_y). \
                wait(ms=300). \
                move_to(x=left_x, y=middle_y). \
                release(). \
                perform()
        else:
            raise ItemNotFound(f'Элемент не найден. Локатор: {locator}.')

    def back(self, count):
        for i in list(range(count)):
            self.driver.back()
