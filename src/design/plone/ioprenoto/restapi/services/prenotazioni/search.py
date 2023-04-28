# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import getMultiAdapter


class PrenotazioniSearch(Service):
    """
    Preonotazioni search view
    """

    def reply(self):
        start_date = self.request.get("start_date", None)
        end_date = self.request.get("end_date", None)

        query = {
            "portal_type": "Prenotazione",
            "fiscalcode": self.request.get("fiscalcode", None),
            "Date": {
                "query": [DateTime(i) for i in [start_date, end_date] if i],
                "range": f"{start_date and 'min' or ''}{start_date and end_date and ':' or ''}{end_date and 'max' or ''}",
            },
        }

        results = getMultiAdapter(
            (api.portal.get_tool("portal_catalog")(**query), self.request),
            ISerializeToJson,
        )(fullobjects=self.request.form.get("fullobjects"))

        return results
