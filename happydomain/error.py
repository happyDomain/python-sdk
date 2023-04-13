class HappyError(BaseException):

    def __init__(self, status_code, errmsg, href=""):
        self.errmsg = errmsg
        self.status_code = status_code

    def __str__(self):
        return str(self.status_code) + ": " + self.errmsg
