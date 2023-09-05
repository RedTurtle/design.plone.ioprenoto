from design.plone.ioprenoto.interfaces import IDesignPloneIoprenotoLayer
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from redturtle.prenotazioni.content.prenotazioni_folder import IPrenotazioniFolder
from zope.component import adapter
from zope.interface import implementer


PRENOTAZIONI_MANAGE_PERMISSION = "redturtle.prenotazioni: Manage Prenotazioni"
# TODO: move to registry
PRENOTAZIONE_APPUNTAMENTO_ADDRESS = "prenotazione-appuntamenti-uffici"


@implementer(ISerializeToJsonSummary)
@adapter(IPrenotazioniFolder, IDesignPloneIoprenotoLayer)
class SerializePrenotazioniFolderToJsonSummary(DefaultJSONSummarySerializer):
    def __call__(self, *args, **kwargs):
        resp = super().__call__(*args, **kwargs)
        if not api.user.has_permission(
            PRENOTAZIONI_MANAGE_PERMISSION,
            obj=self.context,
        ):
            # XXX: this is a workaround to avoid the Unauthorized exception
            return {
                "@components": resp["@components"],
                "@id": resp["@id"],
                "@type": resp["@type"],
                "layout": resp["layout"],
                "title": resp["title"],
                "error": "Unauthorized",
                "anonymous": api.user.is_anonymous(),
            }
        return resp


@implementer(ISerializeToJson)
@adapter(IPrenotazioniFolder, IDesignPloneIoprenotoLayer)
class SerializePrenotazioniFolderToJson(SerializeFolderToJson):
    def __call__(self, *args, **kwargs):
        resp = super().__call__(*args, **kwargs)
        if not api.user.has_permission(
            PRENOTAZIONI_MANAGE_PERMISSION,
            obj=self.context,
        ):
            # XXX: this is a workaround to avoid the Unauthorized exception
            return {
                "@components": resp["@components"],
                "@id": resp["@id"],
                "@type": resp["@type"],
                "layout": resp["layout"],
                "title": resp["title"],
                "error": "Unauthorized",
                "anonymous": api.user.is_anonymous(),
            }
        return resp
