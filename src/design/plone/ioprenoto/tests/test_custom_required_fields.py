# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING


class CustomRequiredFieldsTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_does_not_return_description(self):
        factory = getUtility(
            IVocabularyFactory, "redturtle.prenotazioni.requirable_booking_fields"
        )
        vocabulary = factory(self.portal)

        self.assertNotIn("description", vocabulary.by_token)
