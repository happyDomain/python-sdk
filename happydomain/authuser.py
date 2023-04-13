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

    def ResetPassword(self, *args, **kwargs):
        self._session.authuser_reset_password(self.Id, *args, **kwargs)

    def Update(self):
        self._session.authuser_update(self.Id, self)
