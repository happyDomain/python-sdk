import json
from urllib.parse import quote

from .error import HappyError
from .zone import ZoneMeta, Zone

class Domain:

    def __init__(self, _session, id, id_owner, id_provider, domain, zone_history, group=""):
        self._session = _session

        self.id = id
        self.id_owner = id_owner
        self.id_provider = id_provider
        self.domain = domain
        self.group = group
        self.zone_history = zone_history if zone_history is not None else []

    def _dumps(self):
        return json.dumps({
            "id": self.id,
            "id_owner": self.id_owner,
            "id_provider": self.id_provider,
            "domain": self.domain,
            "group": self.group,
            "zone_history": self.zone_history,
        })

    @property
    def current_zone(self):
        if len(self.zone_history) == 0:
            self.import_zone()

        return self.zone_history[0]

    def delete(self):
        r = self._session.session.delete(
            self.baseurl + "/api/domains/" + quote(self.id),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()

    def update(self):
        r = self._session.session.put(
            self._session.baseurl + "/api/domains/" + quote(self.id),
            date=self._dumps(),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return r.json()

    def import_zone(self):
        r = self._session.session.post(
            self._session.baseurl + "/api/domains/" + quote(self.id) + "/import_zone",
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        zm = ZoneMeta(self._session, **r.json())
        self.zone_history.append(zm)
        return zm

    def get_zone(self, zid):
        r = self._session.session.get(
            self._session.baseurl + "/api/domains/" + quote(self.id) + "/zone/" + quote(zid),
        )

        if r.status_code > 300:
            raise HappyError(r.status_code, **r.json())

        return Zone(self._session, self.id, **r.json())

    def get_current_zone(self):
        return self.get_zone(self.current_zone)
