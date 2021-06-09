import pytest

from api.client import ErrorRequest
from base import ApiBase


class TestsMock(ApiBase):
    def test_post_user(self):
        name = "Vasya"
        response = self.client.post_user(name)
        assert name in response['name']

    def test_get_user(self, create_user):
        response = self.client.get_user(create_user['id'])
        assert response['name'] == create_user['name']

    def test_put_user(self, create_user):
        name = 'Petya'
        response = self.client.put_user(create_user['id'], name)
        assert name in response['name']

    def test_delete(self, create_user):
        with pytest.raises(ErrorRequest):
            response = self.client.delete_user(create_user['id'])
            assert response['id'] == create_user['id']
            self.client.get_user(response['id'])
