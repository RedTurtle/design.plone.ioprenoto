# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from zc.relation.interfaces import ICatalog
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


class BookableUOList(Service):
    def reply(self):
        """
        Return all UO with at least one back-refence from PrenotazioniFolder
        """

        response = {
            "@id": f"{self.context.absolute_url()}/@bookable-uo-list",
            "items": [],
        }
        query = dict(portal_type="UnitaOrganizzativa", sort_on="sortable_title")
        uid = self.request.form.get("uid", "")
        if uid:
            query["UID"] = self.get_uo_from_service_uid(uid=uid)

        uo_list = api.content.find(**query)
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        for brain in uo_list:
            folders = []
            uo = brain.getObject()
            sede = self.get_sede(uo=uo)
            relations = catalog.findRelations(
                {
                    "to_id": intids.getId(uo),
                    "from_attribute": "uffici_correlati",
                }
            )
            for rel in relations:
                prenotazioni_folder = rel.from_object
                if prenotazioni_folder and api.user.has_permission(
                    "View", obj=prenotazioni_folder
                ):
                    folders.append(
                        {
                            "@id": prenotazioni_folder.absolute_url(),
                            "uid": prenotazioni_folder.UID(),
                            "title": prenotazioni_folder.Title(),
                            "orario_di_apertura": prenotazioni_folder.orario_di_apertura,
                            "address": sede,
                        }
                    )
            if folders:
                response["items"].append(
                    {
                        "@id": uo.absolute_url(),
                        "title": uo.Title(),
                        "id": uo.getId(),
                        "uid": uo.UID(),
                        "prenotazioni_folder": folders,
                    }
                )
        return response

    def get_sede(self, uo):
        ref = getattr(uo, "sede", [])
        if not ref:
            return {}
        venue = ref[0].to_object
        if not venue:
            return {}
        return getMultiAdapter((venue, self.request), ISerializeToJsonSummary)()

    def get_uo_from_service_uid(self, uid):
        """Dato lo UID di un servizio, restituisce lo UID dell'UO a cui è collegato
        come canale fisico o unità organizzativa responsabile"""
        service = api.content.get(UID=uid)
        if not service:
            return []
        if service.portal_type != "Servizio":
            return []
        canale_fisico = getattr(service, "canale_fisico", [])
        if canale_fisico:
            return [x.to_object.UID() for x in canale_fisico if x.to_object]
        ufficio_responsabile = getattr(service, "ufficio_responsabile", [])
        return [x.to_object.UID() for x in ufficio_responsabile if x.to_object]
