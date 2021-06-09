from selenium.webdriver.common.by import By


class BasePageLocators:
    SUBMIT = (By.ID, 'submit')
    ERROR = (By.ID, 'flash')
