# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from zope.component import getMultiAdapter


class BookableUOList(Service):
    def reply(self):
        """
        Return all UO with at least one back-refence from PrenotazioniFolder
        """

        response = {
            "@id": f"{self.context.absolute_url()}/@bookable-uo-list",
            "items": [],
        }
        uo_list = api.content.find(
            portal_type="UnitaOrganizzativa", sort_on="sortable_title"
        )
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        for brain in uo_list:
            uo = brain.getObject()
            folders = []
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(uo),
                    from_attribute="uffici_correlati",
                )
            )
            for rel in relations:
                prenotazioni_folder = rel.from_object
                if prenotazioni_folder:
                    folders.append(
                        {
                            "@id": prenotazioni_folder.absolute_url(),
                            "title": prenotazioni_folder.Title(),
                            "address": self.get_address(item=prenotazioni_folder),
                            "description": prenotazioni_folder.description,
                        }
                    )
            if folders:
                data = getMultiAdapter((uo, self.request), ISerializeToJsonSummary)()
                data["prenotazioni_folders"] = folders
                response["items"].append(data)
        return response

    def get_address(self, item):
        ref = getattr(item, "punto_di_contatto", None)
        if not ref:
            return None
        punto_di_contatto = ref[0].to_object
        if not punto_di_contatto:
            return None
        return getMultiAdapter(
            (punto_di_contatto, self.request), ISerializeToJsonSummary
        )()
