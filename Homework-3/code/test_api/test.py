import pytest

from api.client import Client
from test_api.base import ApiBase


class TestApi(ApiBase):
    @pytest.mark.API
    def test_create_campaign(self, create_campaign):
        response = self.api_client.post_campaign_banner(name=create_campaign['name'], url_id=create_campaign['id_url'],
                                                        image_id=create_campaign['id_image'])
        campaigns = self.api_client.get_campaign()
        campaign = [camp for camp in campaigns['items'] if camp['name'] in create_campaign['name']]
        assert len(campaign) == 1
        assert campaign[0]['id'] == response['id']

    @pytest.mark.API
    def test_create_segment(self, name_segment):
        response = self.api_client.post_segment(name_segment)
        segments = self.api_client.get_segments()
        segment = [segm for segm in segments['items'] if segm['name'] in name_segment]
        assert len(segment) == 1
        assert segment[0]['id'] == response['id']

    @pytest.mark.API
    def test_delete_segment(self, create_segment_id):
        response = self.api_client.delete_segment(create_segment_id)
        assert response['successes'][0].get('source_id') == create_segment_id
        segments = self.api_client.get_segments()
        id_segment = [segm['id'] for segm in segments['items'] if segm['id'] == create_segment_id]
        assert len(id_segment) == 0
