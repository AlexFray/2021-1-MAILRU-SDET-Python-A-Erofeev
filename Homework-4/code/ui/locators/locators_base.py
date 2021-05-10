from selenium.webdriver.common.by import By


class BasePageLocators:
    KEYBOARD = (By.ID, 'ru.mail.search.electroscope:id/keyboard')
    SEARCH_INPUT = (By.ID, 'ru.mail.search.electroscope:id/input_text')
    INPUT_ACTION = (By.ID, 'ru.mail.search.electroscope:id/text_input_action')
