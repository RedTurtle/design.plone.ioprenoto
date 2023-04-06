from Acquisition import aq_inner
from design.plone.contenttypes.interfaces.servizio import IServizio
from design.plone.contenttypes.restapi.serializers.servizio import (
    SerializeServizioToJsonSummary as ServizioSummaryOriginal,
)
from design.plone.ioprenoto.interfaces import IDesignPloneIoprenotoLayer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.intid.interfaces import IntIdMissingError


class CartellaPrenotazioneBackreferences:
    @staticmethod
    def has_backreferences(service):
        """Returns backreferences to PrenotazioniFolder throught correlated UO"""

        referenced_uo = [
            i.to_object
            for i in (
                CartellaPrenotazioneBackreferences.get_referenced_relations_from_obj
            )(service)
            if i.to_object.portal_type == "UnitaOrganizzativa"
        ]
        pernotazioni_folder_refencing_uo = []

        for uo in referenced_uo:
            folders = [
                i
                for i in (
                    CartellaPrenotazioneBackreferences.get_referenced_relations_to_obj
                )(uo)
                if i.from_object.portal_type == "PrenotazioniFolder"
            ]

            if folders:
                pernotazioni_folder_refencing_uo += folders

        return bool(pernotazioni_folder_refencing_uo)

    @staticmethod
    def get_referenced_relations_from_obj(obj):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        try:
            relations = catalog.findRelations(
                dict(
                    from_id=intids.getId(aq_inner(obj)),
                )
            )
        except IntIdMissingError:
            return []

        return list(relations)

    @staticmethod
    def get_referenced_relations_to_obj(obj):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        try:
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(aq_inner(obj)),
                )
            )
        except IntIdMissingError:
            return []

        return list(relations)


@implementer(ISerializeToJsonSummary)
@adapter(IServizio, IDesignPloneIoprenotoLayer)
class SerializeServizioToJsonSummary(ServizioSummaryOriginal):
    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)

        if result:
            result[
                "referenced_by_prenotazioni_folder"
            ] = CartellaPrenotazioneBackreferences.has_backreferences(self.context)

        return result


@implementer(ISerializeToJson)
@adapter(IServizio, IDesignPloneIoprenotoLayer)
class SerializeServizioToJson(SerializeFolderToJson):
    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)

        if result:
            result[
                "referenced_by_prenotazioni_folder"
            ] = CartellaPrenotazioneBackreferences.has_backreferences(self.context)

        return result
