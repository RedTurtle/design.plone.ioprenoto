# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.restapi.testing import RelativeSession
from transaction import commit

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
        self.api_session.auth = (TEST_USER_NAME, TEST_USER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.prenotazioni_folder = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni folder",
        )

        api.content.transition(self.prenotazioni_folder, transition="publish")

        setRoles(self.portal, TEST_USER_ID, [])

        commit()

    def tearDown(self):
        self.api_session.close()

    def test_content_redirect_if_have_not_permission(self):
        """The serializer must redirect if have no
        redturtle.prenotazioni.ManagePrenotazioni permission
        """

        self.assertIn(
            "prenotazione-appuntamento",
            self.api_session.get(self.prenotazioni_folder.absolute_url()).url,
        )

    def test_access_content_if_have_permission(self):
        """Test access content only if have permission
        redturtle.prenotazioni.ManagePrenotazioni
        """
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.assertEquals(
            self.api_session.get(self.prenotazioni_folder.absolute_url()).json()["@id"],
            self.prenotazioni_folder.absolute_url(),
        )
