import json
from urllib.parse import quote

class AuthUser:

    def __init__(self, _session, Id, Email, EmailVerification, Password, CreatedAt, LastLoggedIn, AllowCommercials):
        self._session = _session

        self.Id = Id
        self.Email = Email
        self.EmailVerification = EmailVerification
        self.Password = Password
        self.CreatedAt = CreatedAt
        self.LastLoggedIn = LastLoggedIn
        self.AllowCommercials = AllowCommercials

    def Delete(self):
        self._session.authuser_delete(self.Id)

    def ResetPassword(self, NewPassword):
        r = self._session.session.post(
            "http+unix://" + self._session.socket_path + "/api/auth/" + quote(self.Id) + "/reset_password",
            data=json.dumps({
                "password": NewPassword,
            })
        )

        if r.status_code != 200 and r.status_code != 406:
            raise HappyError(r.status_code, **r.json())

        return r.status_code == 200

    def Update(self):
        self._session.authuser_update(self.Id, self)
