
from plone import api
from redturtle.prenotazioni.interfaces import ISerializeToPrenotazioneSearchableItem
from redturtle.prenotazioni.restapi.services.booking.add import (
    AddBooking as BaseAddBooking,
)
from zope.component import getMultiAdapter
try:
    from design.plone.iocittadino.interfaces import IDesignPloneIocittadinoLayer
    WITH_IOCITTADINO = True
except ImportError:
    WITH_IOCITTADINO = False


class AddBooking(BaseAddBooking):
    def reply(self):
        result = super().reply()

        # XXX: questa parte riguarda onceonly con design.plone.iocittadino, è la parte
        #      che rimane comunque qui
        if WITH_IOCITTADINO and IDesignPloneIocittadinoLayer.providedBy(self.request):
            # se è configurato iocittadino fare onceonly con i dati di iocittadino
            if not api.user.is_anonymous():
                user = api.user.get_current()
                userstore = queryMultiAdapter(
                    (self.context, user, self.request), IUserStore
                )
                import pdb; pdb.set_trace()
                userstore.set(data={"data": {}}, onceoonly_fields=["email", "phone"])

        # TODO: il codice qui è temporaneo, va spostato in redturtle.prenotazioni
        #       di conseguenza l'implementazione si semplifica
        catalog = api.portal.get_tool("portal_catalog")
        uid = result["UID"]
        booking = catalog.unrestrictedSearchResults(UID=uid)[0]._unrestrictedGetObject()

        response = getMultiAdapter(
            (booking, self.request), ISerializeToPrenotazioneSearchableItem
        )(fullobjects=True)

        # BBB: la response deve riportare tutte le info del CT prenotazione
        response["@type"] = booking.portal_type
        response["id"] = booking.getId()  # response["@id"].split("/")[-1]
        if "booking_id" in response:
            response["UID"] = response["booking_id"]
        if "booking_gate" in response:
            response["gate"] = response["booking_gate"]
        response["booking_folder_uid"] = (
            response["booking_folder"]["uid"] if "booking_folder" in response else None
        )
        if "notify_on_confirm" not in response:
            prenotazioni_folder = booking.getPrenotazioniFolder()
            response["notify_on_confirm"] = prenotazioni_folder.notify_on_confirm
        return response
