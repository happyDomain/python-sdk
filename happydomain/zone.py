import json
from urllib.parse import quote

from .error import HappyError
from .service import HService

class ZoneMeta:

    def __init__(self, _session, **kwargs):
        self._session = _session
        self._load(**kwargs)

    def _load(self, id, id_author, default_ttl, last_modified="", commit_message=None, commit_date=None, published=None):
        self.id = id
        self.id_author = id_author
        self.default_ttl = default_ttl
        self.last_modified = last_modified
        self.commit_message = commit_message
        self.commit_date = commit_date
        self.published = published

    def _dumps(self):
        return json.dumps({
            "id": self.id,
            "id_author": self.id_author,
            "default_ttl": self.default_ttl,
            "last_modified": self.last_modified,
            "commit_message": self.commit_message,
            "commit_date": self.commit_date,
            "published": self.published,
        })


class Zone(ZoneMeta):

    def __init__(self, _session, _domainid, services, **kwargs):
        super(Zone, self).__init__(_session, **kwargs)

        self._domainid = _domainid
        self._load(services)


    def _load(self, services, **kwargs):
        if "id" in kwargs:
            super(Zone, self).__init__(**kwargs)

        self.services = {}
        if services is not None:
            for k in services:
                self.services[k] = []
                for s in services[k]:
                    self.services[k].append(HService(_session, self._domainid, self.id, **s))

    def _svc_dumps(self):
        services = {}

        for k in self.services:
            services[k] = []
            for s in self.services[k]:
                services[k].append(s._flat())

        return services

    def _dumps(self):
        return json.dumps({
            "id": self.id,
            "id_author": self.id_author,
            "default_ttl": self.default_ttl,
            "last_modified": self.last_modified,
            "commit_message": self.commit_message,
            "commit_date": self.commit_date,
            "published": self.published,
            "services": self._svc_dumps(),
        })

    def add_zone_service(self, subdomain, svctype, svc):
        r = self._session.session.post(
            self._session.baseurl + "/api/domains/" + quote(self._domainid) + "/zone/" + quote(self.id) + "/" + quote(subdomain) + "/services",
            data=HService(self._session, self._domainid, self.id, Service=svc, _svctype=svctype, _domain=subdomain, _ttl=self.default_ttl)._dumps(),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        self._load(**r.json())

        return self

    def view_dump(self):
        r = self._session.session.post(
            self._session.baseurl + "/api/domains/" + quote(self._domainid) + "/zone/" + quote(self.id) + "/view",
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()

    def apply_changes(self):
        r = self._session.session.post(
            self._session.baseurl + "/api/domains/" + quote(self._domainid) + "/zone/" + quote(self.id) + "/apply_changes",
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()
