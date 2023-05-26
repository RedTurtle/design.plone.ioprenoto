# -*- coding: utf-8 -*-
from plone import api
from redturtle.prenotazioni.adapters.stringinterp import (
    BookingPrintUrlWithDeleteTokenSubstitution as BaseUrlSubstitution,
    BookingPrintUrlWithDeleteTokenSubstitution as BaseUrlDeleteSubstitution,
)
from redturtle.prenotazioni.config import DELETE_TOKEN_KEY
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface)
class BookingUrlSubstitution(BaseUrlSubstitution):
    """
    Always return delete token (it is needed in frontend)
    """

    def safe_call(self):
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=self.context.REQUEST,
        )
        annotations = IAnnotations(self.context)
        token = annotations.get(DELETE_TOKEN_KEY, None)
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=self.context.REQUEST,
        )
        if not token:
            return "{url}/prenotazione-appuntamenti-uffici?booking_id={uid}".format(
                url=portal_state.navigation_root_url(),
                uid=self.context.UID(),
            )
        return "{url}/prenotazione-appuntamenti-uffici?booking_id={uid}&{token_key}={token}".format(
            url=portal_state.navigation_root_url(),
            uid=self.context.UID(),
            token_key=DELETE_TOKEN_KEY,
            token=token,
        )


@adapter(Interface)
class BookingPrintUrlWithDeleteTokenSubstitution(BaseUrlDeleteSubstitution):
    def safe_call(self):
        annotations = IAnnotations(self.context)
        token = annotations.get(DELETE_TOKEN_KEY, None)
        if not token:
            return ""
        portal_state = api.content.get_view(
            name="plone_portal_state",
            context=api.portal.get(),
            request=self.context.REQUEST,
        )
        return "{url}/prenotazione-appuntamenti-uffici?booking_id={uid}&{token_key}={token}".format(
            url=portal_state.navigation_root_url(),
            uid=self.context.UID(),
            token_key=DELETE_TOKEN_KEY,
            token=token,
        )
