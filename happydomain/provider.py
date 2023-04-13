import json

from .error import HappyError
from .domain import Domain

class Provider:

    def __init__(self, _session, _srctype, _id, _ownerid, _comment, **kwargs):
        self._session = _session

        self._srctype = _srctype
        self._id = _id
        self._ownerid = _ownerid
        self._comment = _comment
        self.args = kwargs

    def _dumps(self):
        d = {
            "_srctype": self._srctype,
            "_id": self._id,
            "_ownerid": self._ownerid,
            "_comment": self._comment,
        }
        d.update(self.kwargs)
        return json.dumps(d)

    def domain_add(self, dn):
        r = self._session.session.post(
            self._session.baseurl + "/api/domains",
            data=json.dumps({
                "domain": dn,
                "id_provider": self._id,
            })
        )

        if r.status_code != 200:
            raise HappyError(r.status_code, **r.json())

        return Domain(self, **r.json())

    def delete(self):
        r = self._session.session.delete(
            self.baseurl + "/api/providers/" + quote(self._id),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()

    def update(self):
        r = self._session.session.put(
            self.baseurl + "/api/providers/" + quote(self._id),
            date=self._dumps(),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()
