import pytest
from api.client import Client


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request):
        self.api_client: Client = request.getfixturevalue('api_client')
