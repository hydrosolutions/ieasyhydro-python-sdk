
import os
from functools import partial
from urllib.parse import urljoin

import requests


class IEasyHydroSDKBase:

    def __init__(
            self,
            host=None,
            username=None,
            password=None,
            organization_id=None,
    ):
        self.host = host or os.environ.get('IEASYHYDRO_HOST', 'https://api.ieasyhydro.org')
        self.username = username or os.environ.get('IEASYHYDRO_USERNAME')
        self.password = password or os.environ.get('IEASYHYDRO_PASSWORD')
        self.organization_id = organization_id or os.environ.get('ORGANIZATION_ID')
        self.bearer_token = None

        for name, env_name in (
                ('host', 'IEASYHYDRO_HOST'),
                ('username', 'IEASYHYDRO_USERNAME'),
                ('password', 'IEASYHYDRO_PASSWORD'),
        ):
            if getattr(self, name) is None:
                raise ValueError(
                    f'The {name} is not set. Either provide "{name}" parameter in class '
                    f'initialization or set the "{env_name}" environment variable.')

    def _login(self):
        print("sending login request")
        response = requests.post(
            url=urljoin(self.host, 'access_tokens'),
            json={'usernameOrEmail': self.username, 'password': self.password}
        )
        print("login response", response.json())

        if response.status_code == 201:
            token = response.json()['resources'][0]['tokenString']
            self.bearer_token = token

        elif response.status_code == 400 and response.json()['errorCode'] == "11001":
            raise ValueError('Configured username and password are not valid.')

    def _call_api(
            self,
            method,
            relative_url,
            headers=None,
            json_body=None,
            params=None,
            paginated_endpoint=True,
            offset=0,
            page_size=100,
    ):
        if not self.bearer_token:
            self._login()

        if relative_url is None:
            raise ValueError('No path provided or the provided path is None')

        headers = headers or {}
        headers.update({'Authorization': f'Bearer {self.bearer_token}'})

        params = params or {}
        if paginated_endpoint:
            params.update({
                'offset': offset,
                'page_size': page_size,
            })

        if self.organization_id:
            headers.update({'organization': str(self.organization_id)})
        response = requests.request(
            method=method,
            url=urljoin(self.host, relative_url),
            headers=headers,
            json=json_body,
            params=params,
        )

        if not paginated_endpoint:
            return response

        response_json = response.json()

        offset = response_json['offset']
        count = response_json['count']
        resources = response_json['resources']

        response.has_next_page = count > (offset + len(resources))
        response.has_prev_page = offset > 0
        next_page_fn = partial(
            self._call_api,
            method=method,
            relative_url=relative_url,
            headers=headers,
            json_body=json_body,
            params=params,
            page_size=page_size,
            offset=offset + page_size,
        )

        prev_page_fn = partial(
            self._call_api,
            method=method,
            relative_url=relative_url,
            headers=headers,
            json_body=json_body,
            params=params,
            page_size=page_size,
            offset=offset + page_size,
        )
        response.next_page = next_page_fn
        response.prev_page = prev_page_fn
        return response

    @staticmethod
    def _get_all_pages(response, resources_key='resources'):
        data = response.json()[resources_key]
        while response.has_next_page:
            response = response.next_page()
            data += response.json()[resources_key]

        return data


class IEasyHydroHFSDKBase(IEasyHydroSDKBase):
    def __init__(self, host=None, username=None, password=None, organization_id=None):
        self.host = host or os.environ.get('IEASYHYDROHF_HOST', 'https://hf.ieasyhydro.org/api/v1/')
        self.username = username or os.environ.get('IEASYHYDROHF_USERNAME')
        self.password = password or os.environ.get('IEASYHYDROHF_PASSWORD')
        self.organization_id = organization_id or os.environ.get('ORGANIZATION_ID')
        self.organization_uuid = None
        self.bearer_token = None

        for name, env_name in (
                ('host', 'IEASYHYDROHF_HOST'),
                ('username', 'IEASYHYDROHF_USERNAME'),
                ('password', 'IEASYHYDROHF_PASSWORD'),
        ):
            if getattr(self, name) is None:
                raise ValueError(
                    f'The {name} is not set. Either provide "{name}" parameter in class '
                    f'initialization or set the "{env_name}" environment variable.')

        self._login()

    def _login(self):
        response = requests.post(
            url=urljoin(self.host, 'auth/token-obtain'),
            json={'username': self.username, 'password': self.password}
        )
        if response.status_code == 200:
            response_json = response.json()
            self.bearer_token = response_json["access"]
            self.organization_uuid = response_json["user"]["organization"]["uuid"]
        else:
            raise ValueError('Configured username and password are not valid.')
