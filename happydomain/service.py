import json
from urllib.parse import quote

from .error import HappyError

class ServiceMeta:

    def __init__(self, _session, _svctype, _domain, _ttl, _id=None, _ownerid=None, _comment="", _mycomment="", _aliases=[], _tmp_hint_nb=0):
        self._session = _session

        self._svctype = _svctype
        self._domain = _domain
        self._ttl = _ttl
        self._id = _id
        self._ownerid = _ownerid
        self._comment = _comment
        self._mycomment = _mycomment
        self._aliases = _aliases
        self._tmp_hint_nb = _tmp_hint_nb

    def _dumps(self):
        return json.dumps({
            "_svctype": self._svctype,
            "_domain": self._domain,
            "_ttl": self._ttl,
            "_id": self._id,
            "_ownerid": self._ownerid,
            "_comment": self._comment,
            "_mycomment": self._mycomment,
            "_aliases": self._aliases,
            "_tmp_hint_nb": self._tmp_hint_nb,
        })


class HService(ServiceMeta):

    def __init__(self, _session, _domainid, _zoneid, Service, **kwargs):
        super(HService, self).__init__(_session, **kwargs)
        self._domainid = _domainid
        self._zoneid = _zoneid
        self.service = Service

    def _dumps(self):
        return json.dumps(self._flat())

    def _flat(self):
        d = {
            "_svctype": self._svctype,
            "_domain": self._domain,
            "_ttl": self._ttl,
            "_comment": self._comment,
            "_mycomment": self._mycomment,
            "_aliases": self._aliases,
            "_tmp_hint_nb": self._tmp_hint_nb,
            "Service": self.service,
        }
        if self._id is not None:
            d["_id"] = self._id
        if self._ownerid is not None:
            d["_ownerid"] = self._ownerid
        return d

    def delete(self):
        r = self._session.session.delete(
            self._session.baseurl + "/api/domains/" + quote(self._domainid) + "/zone/" + quote(self._zoneid) + "/" + quote(self._domain) + "/services/" + quote(self._id),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()
