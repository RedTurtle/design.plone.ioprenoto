# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield.relation import RelationValue
from zope.component import queryUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class SummarySerializerTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.unita_organizzativa = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
        )
        self.prenotazioni_folder = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni Folder",
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

        api.content.transition(self.prenotazioni_folder, transition="publish")

        setRoles(self.portal, TEST_USER_ID, [])

        commit()

    def tearDown(self):
        self.api_session.close()

    def test_servizio_not_referenced_by_prenotazioni_folder_field(self):
        self.assertFalse(
            self.api_session.get(self.servizio.absolute_url()).json()[
                "referenced_by_prenotazioni_folder"
            ]
        )

    def test_servizio_referenced_by_prenotazioni_folder_field(self):
        self.prenotazioni_folder.uffici_correlati = [
            RelationValue(to_id=queryUtility(IIntIds).getId(self.unita_organizzativa))
        ]

        notify(ObjectModifiedEvent(self.prenotazioni_folder, ""))

        commit()

        self.assertTrue(
            self.api_session.get(self.servizio.absolute_url()).json()[
                "referenced_by_prenotazioni_folder"
            ]
        )
