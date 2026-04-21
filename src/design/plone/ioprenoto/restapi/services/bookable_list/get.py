# -*- coding: utf-8 -*-
from logging import getLogger
from plone import api
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from urllib.parse import unquote
from urllib.parse import urlencode
from zope.component import getMultiAdapter

import re

logger = getLogger(__name__)


class BookableList(Service):
    def reply(self):
        """
        Return all UO with at least one back-refence from PrenotazioniFolder
        """
        response = {
            "@id": f"{self.context.absolute_url()}/@bookable-list",
            "items": [],
        }
        portal_url = api.portal.get().absolute_url()
        query = {"portal_type": "Servizio", "sort_on": "sortable_title"}
        for brain_service in api.content.find(**query):
            # XXX: get_uo_from_service_uid ha l'object, ma anzichè usarlo, si tira fuori lo UID
            #      e poi si cerca quell'UID nel catalog. Sicuarmente questo aiuta a escludere
            #      oggetti privati, ma sembra un passaggio inutilmente complicato (?)
            for brain_uo in api.content.find(
                UID=self.get_uo_from_service_uid(uid=brain_service.UID)
            ):
                uo = brain_uo.getObject()
                sede = self.get_sede(uo=uo)
                relations = api.relation.get(target=uo, relationship="uffici_correlati")
                for rel in relations:
                    prenotazioni_folder = rel.from_object
                    if not prenotazioni_folder:
                        continue
                    for booking_type in (
                        getattr(prenotazioni_folder, "booking_types", []) or []
                    ):
                        query = urlencode(
                            {
                                # "uid": prenotazioni_folder.UID(),
                                "uid": brain_service.UID,
                                "booking_type": booking_type["name"],
                            }
                        )
                        response["items"].append(
                            {
                                "url": f"{portal_url}/prenotazione-appuntamenti-uffici?{query}",  # noqa: E501
                                "booking_type": booking_type["name"],
                                "booking_duration": booking_type.get("duration"),
                                "service_title": brain_service.Title,
                                "booking_opening_hours": prenotazioni_folder.orario_di_apertura,  # noqa: E501
                                "address": sede,
                                "uo_title": brain_uo.Title,
                                "description_agenda": json_compatible(
                                    prenotazioni_folder.descriptionAgenda,
                                    prenotazioni_folder,
                                ),  # noqa: E501
                            }
                        )
        return response

    def get_sede(self, uo):
        ref = getattr(uo, "sede", [])
        if not ref:
            return {}
        venue = ref[0].to_object
        if venue and api.user.has_permission("View", obj=venue):
            return getMultiAdapter((venue, self.request), ISerializeToJsonSummary)()
        else:
            return {}

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


class BookableUOList(BookableList):

    UO_CONTENT_TYPE = "UnitaOrganizzativa"
    FOLDER_CONTENT_TYPE = "PrenotazioniFolder"

    def booking_type_check(self, prenotazioni_folder, booking_type):
        if not booking_type:
            return True
        tocheck = [booking_type, unquote(booking_type)]
        # XXX: per qualche problema di doppio encoding arrivano dal frontend delle
        #      stringhe con caratteri in hex, questo codice serve a gestire quelle
        #      casistiche. Una volta fissato sul frontend può essere tolto.
        try:
            tocheck.append(
                re.sub(
                    r"\\x([0-9a-fA-F]{2})",
                    lambda x: bytes.fromhex(x.group(1)).decode("unicode-escape"),
                    booking_type,
                )
            )
        except Exception:
            logger.exception("Error in booking_type_check %s", booking_type)
        booking_types = [
            b_type["name"]
            for b_type in getattr(prenotazioni_folder, "booking_types", [])
        ]
        return bool(set(tocheck).intersection(booking_types))

    def reply(self):
        """
        Return all UO_CONTENT_TYPE with at least one back-refence from a FOLDER_CONTENT_TYPE
        """
        response = {
            "@id": f"{self.context.absolute_url()}/@bookable-uo-list",
            "items": [],
        }
        query = dict(portal_type=self.UO_CONTENT_TYPE, sort_on="sortable_title")
        uid = self.request.form.get("uid", "")
        booking_type = self.request.form.get("booking_type", "")
        if uid:
            query["UID"] = self.get_uo_from_service_uid(uid=uid)

        uo_list = api.content.find(**query)
        for brain in uo_list:
            folders = []
            uo = brain.getObject()
            sede = self.get_sede(uo=uo)  # la prima delle possibili N sedi
            relations = api.relation.get(target=uo, relationship="uffici_correlati")
            for rel in relations:
                folder = rel.from_object
                if not folder or not folder.portal_type == self.FOLDER_CONTENT_TYPE:
                    continue
                if not self.booking_type_check(folder, booking_type):
                    continue
                folders.append(
                    {
                        "@id": folder.absolute_url(),
                        "uid": folder.UID(),
                        "title": folder.Title(),
                        "orario_di_apertura": folder.orario_di_apertura,
                        "address": sede,
                        "description_agenda": json_compatible(
                            folder.descriptionAgenda,
                            folder,
                        ),
                    }
                )
            if len(folders) == 0:
                continue
            response["items"].append(
                {
                    "@id": uo.absolute_url(),
                    "title": uo.Title(),
                    "id": uo.getId(),
                    "uid": uo.UID(),
                    "contact_info": self.get_uo_contact_info(uo),
                    "prenotazioni_folder": sorted(folders, key=lambda x: x["title"]),
                }
            )
        return response

    def get_uo_contact_info(self, uo):
        result = []

        for contact in getattr(uo, "contact_info", None) or []:
            if contact.isBroken():
                logger.warning(
                    "Broken relation found in <{UID}>.contact_info".format(UID=uo.UID())
                )
                continue

            result.append(
                getMultiAdapter(
                    (contact.to_object, self.request), ISerializeToJsonSummary
                )()
            )

        return result
