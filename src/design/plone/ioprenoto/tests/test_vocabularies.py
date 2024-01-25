# -*- coding: utf-8 -*-
from datetime import date
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.venue = api.content.create(
            container=self.portal,
            title="Example venue",
            type="Venue",
            city="Ferrara",
            country="380",
            street="Foo Street 22",
        )
        self.unita_organizzativa = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
            sede=[RelationValue(to_id=queryUtility(IIntIds).getId(self.venue))],
        )
        self.servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            ufficio_responsabile=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
        )
        self.folder_prenotazioni = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Folder",
            description="",
            daData=date.today(),
            gates=["Gate A", "Gate B"],
            same_day_booking_disallowed="no",
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
        )
        api.content.create(
            type="PrenotazioneType",
            title="Type A",
            duration=30,
            container=self.folder_prenotazioni,
            gates=["all"],
        )
        api.content.create(
            type="PrenotazioneType",
            title="Type B è'&&==",
            duration=10,
            container=self.folder_prenotazioni,
            gates=["all"],
        )

        self.folder_prenotazioni_2 = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Folder 2",
            description="",
            daData=date.today(),
            gates=["Gate c", "Gate D"],
            same_day_booking_disallowed="no",
        )
        api.content.create(
            type="PrenotazioneType",
            title="Type C",
            duration=30,
            container=self.folder_prenotazioni_2,
            gates=["all"],
        )

    def tearDown(self):
        pass

    def test_booking_types(self):
        factory = getUtility(
            IVocabularyFactory, name="design.plone.ioprenoto.booking_types"
        )
        self.assertEqual(
            set(factory(self.servizio).by_token.keys()),
            {"Type%20A", "Type%20B%20%C3%A8%27%26%26%3D%3D"},
        )
