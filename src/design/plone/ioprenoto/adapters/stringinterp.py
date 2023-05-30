# -*- coding: utf-8 -*-
from plone import api
from redturtle.prenotazioni.adapters.stringinterp import (
    BookingPrintUrlWithDeleteTokenSubstitution as BaseUrlSubstitution,
)
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface)
class BookingUrlSubstitution(BaseUrlSubstitution):
    """ """

    def safe_call(self):
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=self.context.REQUEST,
        )
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=self.context.REQUEST,
        )
        return "{url}/prenotazione-appuntamenti-uffici?booking_id={uid}".format(
            url=portal_state.navigation_root_url(),
            uid=self.context.UID(),
        )


@adapter(Interface)
class BookingPrintUrlWithDeleteTokenSubstitution(BookingUrlSubstitution):
    """
    deprecated
    """
