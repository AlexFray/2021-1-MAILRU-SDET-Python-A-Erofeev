from ui.locators.authorization_location import AuthorizationPageLocation
from ui.pages.base_page import BasePage


class AuthorizationPage(BasePage):
    url = 'https://account.my.com/login/'
    locators = AuthorizationPageLocation()
