# TODO: il codice qui è temporaneo, va spostato in redturtle.prenotazioni
#       di conseguenza l'implementazione si semplifica

from plone import api
from redturtle.prenotazioni.interfaces import ISerializeToPrenotazioneSearchableItem
from redturtle.prenotazioni.restapi.services.booking.add import (
    AddBooking as BaseAddBooking,
)
from zope.component import getMultiAdapter


class AddBooking(BaseAddBooking):
    def reply(self):
        result = super().reply()
        catalog = api.portal.get_tool("portal_catalog")
        uid = result["UID"]
        booking = catalog.unrestrictedSearchResults(UID=uid)[0]._unrestrictedGetObject()

        response = getMultiAdapter(
            (booking, self.request), ISerializeToPrenotazioneSearchableItem
        )(fullobjects=True)

        # BBB:
        response["@type"] = booking.portal_type
        response["id"] = booking.getId()  # response["@id"].split("/")[-1]
        response["UID"] = response["booking_id"]
        response["gate"] = response["booking_gate"]
        response["booking_folder_uid"] = (
            response["booking_folder"]["uid"] if "booking_folder" in response else None
        )
        if "notify_on_confirm" not in response:
            prenotazioni_folder = booking.getPrenotazioniFolder()
            response["notify_on_confirm"] = prenotazioni_folder.notify_on_confirm
        return response
