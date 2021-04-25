from urllib.parse import urljoin

import requests


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.session = requests.Session()
        self.csrf = None
        self.ssdc = None
        self.mrcu = None
        self.mc = None
        self.sdcs = None
        self.get_cookie()
        print(self.session.cookies)

    @property
    def target_page_headers(self):
        return {'Referer': 'https://target.my.com/'}

    @property
    def dashboard_page_headers(self):
        return {'Referer': 'https://target.my.com/dashboard',
                'X-CSRFToken': self.csrf}

    @property
    def campaign_page_headers(self):
        return {'Referer': 'https://target.my.com/campaign/new',
                'X-CSRFToken': self.csrf}

    @property
    def segment_page_headers(self):
        return {'Referer': 'https://target.my.com/segments/segments_list',
                'X-CSRFToken': self.csrf}

    def get_cookie(self, login='ero-feev7@yandex.ru', password='CPaf9Cm9P484BPB'):
        location = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'
        data = {
            'email': login,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        response = self._requests('POST', location, data=data, header=self.target_page_headers, full_url=True)
        assert response.status_code == 302
        self.ssdc = response.cookies.get('ssdc')
        self.mrcu = response.cookies.get('mrcu')
        assert response.cookies.get('ssdc') is not None
        assert response.cookies.get('mrcu') is not None
        response = self._requests('GET', response.headers.get('Location'), header=self.target_page_headers,
                                  full_url=True)
        assert response.status_code == 302
        response = self._requests('GET', response.headers.get('Location'), header=self.target_page_headers,
                                  full_url=True)
        assert response.status_code == 302
        self.mc = response.cookies.get('mc')
        assert response.cookies.get('ssdc')
        assert response.cookies.get('mc')
        response = self._requests('GET', response.headers.get('Location'), header=self.target_page_headers,
                                  full_url=True)
        assert response.status_code == 302
        self.sdcs = response.cookies.get('sdcs')
        assert response.cookies.get('sdcs')
        response = self._requests('GET', '/csrf/', header=self.target_page_headers)
        assert response.status_code == 200
        self.csrf = response.cookies.get('csrftoken')
        assert response.cookies.get('csrftoken')

    def _requests(self, method, path, data=None, params=None, json=None, file=None, header=None,
                  full_url=False):
        kwargs = {
            'allow_redirects': False
        }
        if params:
            kwargs['params'] = params
        if json:
            kwargs['json'] = json
        if file:
            kwargs['files'] = file
        if data:
            kwargs['data'] = data
        if full_url:
            url = path
        else:
            url = urljoin(self.addr, path)
        kwargs['headers'] = header
        return self.session.request(method, url, **kwargs)

    def upload_image(self, image=None):
        id_image = self.post_image(image=image)
        self.post_description_image(id_image)
        return id_image

    def post_image(self, expected_status=200, image=None):
        r = self._requests('POST', '/api/v2/content/static.json', file={'file': open(image, 'rb')},
                           header=self.campaign_page_headers)
        assert r.status_code == expected_status
        id_image = r.json().get('id')
        assert id_image is not None
        return id_image

    def post_description_image(self, id_image, expected_status=201):
        r = self._requests('POST', '/api/v2/mediateka.json',
                           json={"description": "Test.jpg", "content": {"id": id_image}},
                           header=self.campaign_page_headers)
        assert r.status_code == expected_status

    def get_campaign(self, expected_status=200, fields='id,name', sorting='-id', limit=10, offset=0,
                     status_in='active', user_id=10910718):
        r = self._requests(method='GET', path='api/v2/campaigns.json', header=self.target_page_headers,
                           params=[('fields', fields), ('sorting', sorting), ('limit', limit), ('offset', offset),
                                   ('_status__in', status_in), ('_user_id__in', user_id), ('_', '1618324905434')])
        assert r.status_code == expected_status
        return r.json()

    def get_url_id(self, expected_status=200, url=None):
        r = self._requests('GET', '/api/v1/urls/', params=[('url', url)])
        assert r.status_code == expected_status
        return r.json()

    def post_campaign_banner(self, name, url_id, image_id, objective='traffic', expected_status=200):
        headers = self.campaign_page_headers
        headers.update({'X-Campaign-Create-Action': 'new'})
        json_ = {
            "name": name,
            "conversion_funnel_id": None,
            "objective": objective,
            "enable_offline_goals": False,
            "targetings": {
                "split_audience": [1],
                "sex": ["male", "female"],
                "age":
                    {
                        "age_list": [21, 22, 23],
                        "expand": True
                    },
                "geo":
                    {
                        "regions": [188]
                    },
                "interests_soc_dem": [],
                "segments": [],
                "interests": [],
                "fulltime": {
                    "flags": ["use_holidays_moving", "cross_timezone"],
                    "mon": list(range(10)),
                    "tue": list(range(10)),
                    "wed": list(range(10)),
                    "thu": list(range(10)),
                    "fri": list(range(10)),
                    "sat": list(range(10)),
                    "sun": list(range(10))
                },
                "pads": [102643],
                "mobile_types": ["tablets", "smartphones"],
                "mobile_vendors": [],
                "mobile_operators": []
            },
            "age_restrictions": None,
            "date_start": None,
            "date_end": None,
            "autobidding_mode": "second_price_mean",
            "budget_limit_day": None,
            "budget_limit": None,
            "mixing": "fastest",
            "utm": None,
            "enable_utm": True,
            "price": "9.68",
            "max_price": "0",
            "package_id": 961,
            "banners": [
                {
                    "urls": {
                        "primary":
                            {
                                "id": url_id
                            }
                    },
                    "textblocks": {},
                    "content": {
                        "image_240x400":
                            {
                                "id": image_id
                            }
                    },
                    "name": ""
                }
            ]
        }
        r = self._requests('POST', '/api/v2/campaigns.json', json=json_, header=headers)
        assert r.status_code == expected_status
        return r.json()

    def delete_campaign(self, id_campaign, expected_status=204):
        r = self._requests('POST', '/api/v2/campaigns/mass_action.json',
                           json=[{"id": id_campaign, "status": "deleted"}], header=self.dashboard_page_headers)
        assert expected_status == r.status_code

    def post_segment(self, name, object_type='remarketing_player', expected_status=200):
        json_ = {
            "name": name,
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": object_type,
                    "params":
                        {
                            "type": "positive",
                            "left": 365,
                            "right": 0
                        }
                }
            ],
            "logicType": "or"
        }
        r = self._requests('POST', '/api/v2/remarketing/segments.json', json=json_, header=self.segment_page_headers)
        assert r.status_code == expected_status
        return r.json()

    def get_segments(self, fields='id,name', expected_status=200):
        r = self._requests('GET', '/api/v2/remarketing/segments.json',
                           params=[('fields', fields), ('_', '1618671455958')],
                           header=self.segment_page_headers)
        assert r.status_code == expected_status
        return r.json()

    def delete_segment(self, id_segment, expected_status=200):
        r = self._requests('POST', '/api/v1/remarketing/mass_action/delete.json',
                           json=[{"source_id": id_segment, "source_type": "segment"}],
                           header=self.segment_page_headers)
        assert r.status_code == expected_status
        return r.json()
