import os
import pytest
import faker

fake = faker.Faker()


@pytest.fixture(scope='function')
def file_path(repo_root):
    return os.path.join(repo_root, 'Resources', '240x400.jpg')


@pytest.fixture(scope='function')
def create_image(api_client, file_path):
    return api_client.post_image(image=file_path)


@pytest.fixture(scope='function')
def get_id_url(api_client):
    return api_client.get_url_id(url='http://mail.ru')['id']


@pytest.fixture()
def create_campaign(api_client, create_image, get_id_url):
    name = fake.lexify(text='??????????')
    yield {'name': name, 'id_image': create_image, 'id_url': get_id_url}
    campaigns = api_client.get_campaign()
    id_campaign = [camp['id'] for camp in campaigns['items'] if camp['name'] in name]
    api_client.delete_campaign(id_campaign[0])


@pytest.fixture()
def name_segment(api_client):
    name = fake.lexify(text='??????????')
    yield name
    segments = api_client.get_segments()
    id_segment = [segm['id'] for segm in segments['items'] if segm['name'] in name]
    api_client.delete_segment(id_segment[0])


@pytest.fixture()
def create_segment_id(api_client):
    name = fake.lexify(text='??????????')
    return api_client.post_segment(name)['id']
