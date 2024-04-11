# -*- coding: utf-8 -*-
from design.plone.ioprenoto.vocabularies.tipologies import IPrenotazioneTypesVocabulary
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.vocabularies import SerializeVocabularyToJson as Base
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IPrenotazioneTypesVocabulary, Interface)
class SerializeVocabularyToJson(Base):
    def __call__(self, vocabulary_id):
        b_size = self.request.form.get("b_size", "")
        if not b_size:
            self.request.form["b_size"] = "200"
        return super().__call__(vocabulary_id)
