# -*- coding: utf-8 -*-
from redturtle.prenotazioni.restapi.services.bookings.search import (
    BookingsSearch as BookingsSearchBase,
)  # noqa: E501
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone import api


@implementer(IPublishTraverse)
class BookingsSearch(BookingsSearchBase):
    def reply(self):
        response = super(BookingsSearch, self).reply()
        base_url = f"{api.portal.get().absolute_url()}/prenotazione-appuntamenti-uffici"
        for item in response.get("items") or []:
            item["url"] = f"{base_url}?booking_id={item['booking_id']}"
        return response
