from design.plone.ioprenoto.interfaces import IDesignPloneIoprenotoLayer
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from redturtle.prenotazioni.content.prenotazioni_folder import IPrenotazioniFolder
from zope.component import adapter
from zope.interface import implementer


PRENOTAZIONI_MANAGE_PERMISSION = "redturtle.prenotazioni.ManagePrenotazioni"
PRENOTAZIONE_APPUNTAMENTO_ADDRESS = "prenotazione-appuntamento"


@implementer(ISerializeToJsonSummary)
@adapter(IPrenotazioniFolder, IDesignPloneIoprenotoLayer)
class SerializePrenotazioniFolderToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self, *args, **kwargs):
        if not api.user.has_permission(
            PRENOTAZIONI_MANAGE_PERMISSION, user=api.user.get_current()
        ):
            self.request.response.redirect(
                self.context.portal_url() + "/" + PRENOTAZIONE_APPUNTAMENTO_ADDRESS
            )

            return

        return super().__call__(*args, **kwargs)


@implementer(ISerializeToJson)
@adapter(IPrenotazioniFolder, IDesignPloneIoprenotoLayer)
class SerializePrenotazioniFolderToJson(SerializeFolderToJson):
    def __call__(self, *args, **kwargs):
        if not api.user.has_permission(PRENOTAZIONI_MANAGE_PERMISSION):
            self.request.response.redirect(
                self.context.portal_url() + "/" + PRENOTAZIONE_APPUNTAMENTO_ADDRESS
            )

            return

        return super().__call__(*args, **kwargs)
