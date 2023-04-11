# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import (
    DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING,
)
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone import api

import unittest


class TestPrenotazioniFolder(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.prenotazioni_folder = api.content.create(
            type="PrenotazioniFolder",
            title="Prenotazioni Folder",
            container=self.portal,
        )

    def test_exclude_from_nav(self):
        self.assertTrue(self.prenotazioni_folder.exclude_from_nav)
