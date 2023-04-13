"""Handle administration tasks through happyDomain's admin API"""

from datetime import datetime, timezone
import json
import os
from urllib.parse import quote_plus

import requests
import requests_unixsocket

from .api import HappyError

class Admin:

    def __init__(self, socket="./happydomain.sock"):
        self.session = requests_unixsocket.Session()
        self.socket_path = quote_plus(os.path.abspath(socket))

    def authuser_create(self, email, password, allowcommercials=False, email_verified=False):
        email_verification = None
        if email_verified:
            now = datetime.now()
            now = now.replace(microsecond=0, tzinfo=timezone.utc)
            email_verification = now.isoformat()

        r = self.session.post(
            "http+unix://" + self.socket_path + "/api/auth",
            data=json.dumps({
                "email": email,
                "EmailVerification": email_verification,
                "AllowCommercials": allowcommercials,
            }),
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        from .authuser import AuthUser
        u = AuthUser(self, **r.json())

        u.Password = u.ResetPassword(password)
        return u

    def authuser_delete(self, Id):
        r = self.session.delete("http+unix://" + self.socket_path + "/api/auth/" + quote_plus(Id))

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        return r.json()

    def authuser_list(self):
        r = self.session.get("http+unix://" + self.socket_path + "/api/auth")

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        ret = []
        val = r.json()

        if val is not None:
            from .authuser import AuthUser
            for au in val:
                ret.append(AuthUser(self, **au))

        return ret

    def authuser_update(self, Id, au):
        r = self.session.put(
            "http+unix://" + self.socket_path + "/api/auth/" + quote_plus(Id),
            data=json.dumps({
                "Id": au.Id,
                "Email": au.Email,
                "EmailVerification": au.EmailVerification,
                "Password": au.Password,
                "CreatedAt": au.CreatedAt,
                "LastLoggedIn": au.LastLoggedIn,
                "AllowCommercials": au.AllowCommercials,
            })
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        from .authuser import AuthUser
        return AuthUser(self, **r.json())
