import pytest
from tests.base import BaseCase


class TestAndroid(BaseCase):
    @pytest.mark.AndroidUI
    def test_search_text(self):
        self.main_page.search_text('Russia', 'население страны составляет 146')
        self.main_page.search_additional_info('население россии', 'сша', '146 млн.')

    @pytest.mark.AndroidUI
    def test_change_source_news(self, source_name='Вести FM'):
        self.main_page.edit_source(source_name)
        self.main_page.searchText('News')
        assert self.main_page.find(self.main_page.locators.TRACK_NAME).text == 'Вести ФМ'

    @pytest.mark.AndroidUI
    def test_calculation(self, expression='5*5', res='25'):
        assert self.main_page.calculation(expression, res) == res

    @pytest.mark.AndroidUI
    def test_info_app(self, version):
        self.main_page.check_info(version)
