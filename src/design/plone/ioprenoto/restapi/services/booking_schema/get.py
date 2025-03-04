# -*- coding: utf-8 -*-
from plone import api
from redturtle.prenotazioni.restapi.services.booking_schema.get import (
    BookingSchema as BaseService,
)
from zope.component import queryMultiAdapter


try:
    from design.plone.iocittadino.interfaces import IDesignPloneIocittadinoLayer
    from design.plone.iocittadino.interfaces import IUserStore

    WITH_IOCITTADINO = True
except ImportError:
    WITH_IOCITTADINO = False


class BookingSchema(BaseService):
    labels_mapping = {
        "email": {
            "label": "Email",
            "description": "Inserisci l'email",
        },
        "fiscalcode": {
            "label": "Codice Fiscale",
            "description": "Inserisci il codice fiscale",
        },
        "phone": {
            "label": "Numero di telefono",
            "description": "Inserisci il numero di telefono",
        },
        "description": {
            "label": "Dettagli",
            "description": "Aggiungi ulteriori dettagli",
        },
        "company": {
            "label": "Azienda",
            "description": "Inserisci il nome dell'azienda",
        },
        "title": {
            "label": "Nome completo",
            "description": "Inserire il nome completo",
        },
    }

    def reply(self):
        data = super().reply()
        if WITH_IOCITTADINO and IDesignPloneIocittadinoLayer.providedBy(self.request):
            # se è configurato iocittadino fare onceonly con i dati di iocittadino
            if not api.user.is_anonymous():
                user = api.user.get_current()
                userstore = queryMultiAdapter(
                    (self.context, user, self.request), IUserStore
                )
                defaults = userstore.get()
                for field in data["fields"]:
                    if field["name"] in userstore.user_properties:
                        if defaults.get(field["name"]):
                            field["value"] = defaults[field["name"]]
                        field["readonly"] = (
                            field["name"] in userstore.strict_user_properties
                        )
        return data
