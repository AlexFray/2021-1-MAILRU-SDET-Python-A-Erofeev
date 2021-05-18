import pytest
from api.client import ClientSocket


class ApiBase:
    @pytest.fixture(scope='function')
    def client(self, setting_mock):
        return ClientSocket(setting_mock['HOST'], setting_mock['PORT'])

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client):
        self.client: ClientSocket = client