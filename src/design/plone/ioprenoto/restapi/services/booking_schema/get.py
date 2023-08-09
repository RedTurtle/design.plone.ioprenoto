# -*- coding: utf-8 -*-
from redturtle.prenotazioni.restapi.services.booking_schema.get import (
    BookingSchema as BaseService,
)


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
