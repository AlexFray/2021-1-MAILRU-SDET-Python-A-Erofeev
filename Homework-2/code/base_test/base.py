import allure
import pytest
from _pytest.fixtures import FixtureRequest
from mimesis import Text
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.segment_page import SegmentPage
TIME_WAIT = 10


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.MainPage: MainPage = request.getfixturevalue('main_page')

    @pytest.fixture()
    def dashboard(self):
        self.MainPage.authorization('ero-feev7@yandex.ru', 'CPaf9Cm9P484BPB')
        return DashboardPage(self.driver)

    @pytest.fixture()
    @allure.title('Генерация названия кампании и удаление после выполнения теста.')
    def name_campaign(self, dashboard):
        name = Text().word()
        yield dashboard, name
        dashboard.delete_campaign(name)

    @pytest.fixture()
    @allure.title('Переход на страницу "Аудитории"')
    def segment(self, dashboard):
        self.driver.get('https://target.my.com/segments/segments_list')
        return SegmentPage(self.driver)

    @pytest.fixture()
    @allure.title('Генерация сегмента для удаления.')
    def segment_for_delete(self, segment):
        name = Text().word()
        segment.create_segment(name)
        yield segment, name

    @pytest.fixture()
    @allure.title('Генерация названия сегмента и удаление.')
    def segment_for_create(self, segment):
        name = Text().word()
        yield segment, name
        segment.delete_segment(name)