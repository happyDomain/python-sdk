"""Handle administration tasks through happyDomain's admin API"""

from datetime import datetime
import json
import os
from urllib.parse import quote_plus

import requests

from .error import HappyError
from .domain import Domain
from .provider import Provider

COOKIE_NAME = "happydomain_session"

class HappyDomain:

    def __init__(self, scheme="http", host="127.0.0.1", port=8081, baseurl="", token=None):
        self.session = requests.Session()
        self.baseurl = scheme + "://" + host + ":" + str(port) + baseurl
        self.token = token

    def login(self, username, password):
        r = self.session.post(
            self.baseurl + "/api/auth",
            data=json.dumps({
                "email": username,
                "password": password,
            })
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **json.loads(r.text))

        self.token = r.cookies[COOKIE_NAME]

        return json.loads(r.text)

    # Domains

    def domain_list(self):
        r = self.session.get(
            self.baseurl + "/api/domains",
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **json.loads(r.text))

        ret = []
        val = json.loads(r.text)

        if val is not None:
            for au in val:
                ret.append(Domain(self, zone_history_are_ids=True, **au))

        return ret

    # Providers

    def provider_list(self):
        r = self.session.get(
            self.baseurl + "/api/providers",
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **json.loads(r.text))

        ret = []
        val = json.loads(r.text)

        if val is not None:
            for au in val:
                ret.append(Provider(self, **au))

        return ret

    def provider_get(self, id):
        r = self.session.get(
            self.baseurl + "/api/providers/" + quote_plus(id),
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        return Provider(self, **r.json())

    def provider_add(self, type, name, data):
        r = self.session.post(
            self.baseurl + "/api/providers",
            data=json.dumps({
                "Provider": data,
                "_comment": name,
                "_srctype": type,
            })
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **json.loads(r.text))

        return Provider(self, **json.loads(r.text))
