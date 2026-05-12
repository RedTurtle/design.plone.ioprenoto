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


def has_backreferences(service):
    """Returns true if service has backreferences to PrenotazioniFolder
    throught correlated UO"""
    for ref_ou in get_referenced_relations_from_obj(service):
        if ref_ou.to_object and ref_ou.to_object.portal_type == "UnitaOrganizzativa":
            for ref_pf in get_referenced_relations_to_obj(ref_ou.to_object):
                if (
                    ref_pf.from_object
                    and ref_pf.from_object.portal_type == "PrenotazioniFolder"
                ):
                    return True
    return False


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
            result["referenced_by_prenotazioni_folder"] = has_backreferences(
                self.context
            )
        return result


@implementer(ISerializeToJson)
@adapter(IServizio, IDesignPloneIoprenotoLayer)
class SerializeServizioToJson(SerializeFolderToJson):
    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)
        if result:
            result["referenced_by_prenotazioni_folder"] = has_backreferences(
                self.context
            )
        return result
