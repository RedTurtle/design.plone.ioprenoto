# -*- coding: utf-8 -*-
from plone import api
from redturtle.prenotazioni.restapi.services.bookings.search import (
    BookingsSearch as BookingsSearchBase,
    BookingsSearchFolder as BookingsSearchFolderBase,
)  # noqa: E501
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


# TODO: in alternativa si poteva sovrascrivere il serializer
@implementer(IPublishTraverse)
class BookingsSearch(BookingsSearchBase):
    def reply(self):
        response = super().reply()
        base_url = api.portal.get_registry_record(
            name="volto.frontend_domain", default=""
        )
        base_url = f"{base_url}/prenotazione-appuntamenti-uffici"
        for item in response.get("items") or []:
            item["booking_url"] = f"{base_url}?booking_id={item['booking_id']}"
        return response


# TODO: in alternativa si poteva sovrascrivere il serializer
@implementer(IPublishTraverse)
class BookingsSearchFolder(BookingsSearchFolderBase):
    def reply(self):
        response = super().reply()
        base_url = api.portal.get_registry_record(
            name="volto.frontend_domain", default=""
        )
        base_url = f"{base_url}/prenotazione-appuntamenti-uffici"
        for item in response.get("items") or []:
            item["booking_url"] = f"{base_url}?booking_id={item['booking_id']}"
        return response
