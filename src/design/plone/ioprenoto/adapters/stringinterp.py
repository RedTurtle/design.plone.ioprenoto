# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from plone.volto.interfaces import IVoltoSettings
from redturtle.prenotazioni.adapters.stringinterp import (
    BookingPrintUrlWithDeleteTokenSubstitution as BaseUrlSubstitution,
)
from zope.component import adapter
from zope.component import getUtility
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
        portal_url = portal_state.navigation_root_url()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings_frontend_domain = getattr(settings, "frontend_domain", None)
        if (
            settings_frontend_domain
            and settings_frontend_domain != "http://localhost:3000"
        ):
            portal_url = settings_frontend_domain
        if portal_url.endswith("/"):
            portal_url = portal_url[:-1]
        return "{url}/prenotazione-appuntamenti-uffici?booking_id={uid}".format(
            url=portal_url,
            uid=self.context.UID(),
        )


@adapter(Interface)
class BookingPrintUrlWithDeleteTokenSubstitution(BookingUrlSubstitution):
    """
    deprecated
    """
