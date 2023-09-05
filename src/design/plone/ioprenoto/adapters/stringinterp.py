# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from plone.volto.interfaces import IVoltoSettings
from redturtle.prenotazioni.adapters import stringinterp as base
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface


@adapter(Interface)
class BookingUrlSubstitution(base.BookingUrlSubstitution):
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
class BookingOperatorUrlSubstitution(base.BookingOperatorUrlSubstitution):
    def safe_call(self):
        portal = api.portal.get()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings_frontend_domain = getattr(settings, "frontend_domain", None)
        if (
            settings_frontend_domain
            and settings_frontend_domain != "http://localhost:3000"
        ):
            portal_url = settings_frontend_domain
        else:
            portal_url = api.portal.get_navigation_root(self.context).absolute_url()
        if portal_url.endswith("/"):
            portal_url = portal_url[:-1]
        booking_folder = self.context
        for ctx in self.context.aq_chain:
            if ctx.portal_type == "PrenotazioniFolder":
                booking_folder = ctx
                break
        # XXX: questo non va bene in ogni caso perchè considera le url fatte con il path,
        #      e non con il virtual host, ma nel caso di volto al momento le due cose sono
        #      coincidenti
        booking_folder_path = "/".join(
            booking_folder.getPhysicalPath()[len(portal.getPhysicalPath()) :]  # noqa
        )
        return f"{portal_url}/{booking_folder_path}?tab=search&SearchableText={self.context.getBookingCode()}&login=1"
