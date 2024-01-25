# -*- coding: utf-8 -*-
from design.plone.ioprenoto.utilities import get_uo_from_service
from plone import api
from redturtle.prenotazioni.vocabularies.tipologies import (
    PrenotazioneTypesVocabulary as Base,
)
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PrenotazioneTypesVocabulary(Base):
    def __call__(self, context):
        """
        Return all the tipologies defined in the PrenotazioniFolder related to a Service
        """
        terms = []
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        for uo in get_uo_from_service(context) or []:
            relations = catalog.findRelations(
                {
                    "to_id": intids.getId(uo),
                    "from_attribute": "uffici_correlati",
                }
            )
            for rel in relations:
                prenotazioni_folder = rel.from_object
                if prenotazioni_folder and api.user.has_permission(
                    "View", obj=prenotazioni_folder
                ):
                    for booking_type in prenotazioni_folder.get_booking_types():
                        term = self.booking_type2term(booking_type)
                        if term.value not in [t.value for t in terms]:
                            terms.append(term)
        terms.sort(key=lambda x: x.title)
        return SimpleVocabulary(terms)


PrenotazioneTypesVocabularyFactory = PrenotazioneTypesVocabulary()
