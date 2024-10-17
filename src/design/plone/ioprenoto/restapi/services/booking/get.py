# TODO: il codice qui è temporaneo, va spostato in redturtle.prenotazioni

from AccessControl import Unauthorized
from plone import api
from redturtle.prenotazioni.interfaces import ISerializeToPrenotazioneSearchableItem
from redturtle.prenotazioni.restapi.services.booking.get import BookingInfo as Base
from zope.component import getMultiAdapter


class BookingInfo(Base):
    def reply(self):
        if not self.booking_uid:
            return self.reply_no_content(status=404)
        catalog = api.portal.get_tool("portal_catalog")
        query = {"portal_type": "Prenotazione", "UID": self.booking_uid}
        booking = catalog.unrestrictedSearchResults(query)

        if not booking:
            return self.reply_no_content(status=404)

        booking = booking[0]._unrestrictedGetObject()
        if not booking.canAccessBooking():
            raise Unauthorized

        # (Pdb) pp getMultiAdapter((booking, self.request), ISerializeToPrenotazioneSearchableItem)(fullobjects=True).keys()
        # dict_keys(['@id', 'title', 'description', 'booking_id', 'booking_code', 'booking_url', 'booking_date',
        # 'booking_expiration_date', 'booking_type', 'booking_gate', 'booking_status', 'booking_status_label',
        # 'booking_status_date', 'booking_status_notes', 'email', 'fiscalcode',
        # 'phone', 'staff_notes', 'company', 'vacation', 'modification_date', 'creation_date', 'booking_folder', 'booking_address',
        # 'booking_office', 'requirements', 'cosa_serve'])

        # (Pdb) pp getMultiAdapter((booking, self.request), ISerializeToJson)().keys()
        # dict_keys(['@id', 'UID', '@type', 'title', 'description', 'gate', 'id', 'phone', 'email', 'fiscalcode', 'company',
        # 'staff_notes', 'booking_date', 'booking_expiration_date', 'booking_status', 'booking_status_label',
        # 'booking_type', 'booking_folder_uid', 'vacation', 'booking_code', 'notify_on_confirm', 'cosa_serve', 'requirements',
        # 'modification_date', 'creation_date'])

        # nel cambio si perdono gli attributi:
        # UID (diventa booking_id),
        # @type (sempre 'Prenotazione'),
        # gate (diventa booking_gate),
        # id (ultimo pezzo dell'URL),
        # staff_notes (usato?)
        # booking_folder_uid (['booking_folder']['uid'])
        # notify_on_confirm (usato?)

        # response = getMultiAdapter((booking, self.request), ISerializeToJson)()
        response = getMultiAdapter(
            (booking, self.request), ISerializeToPrenotazioneSearchableItem
        )(fullobjects=True)

        # BBB:
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
