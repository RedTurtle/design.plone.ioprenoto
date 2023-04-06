# -*- coding: utf-8 -*-

from design.plone.ioprenoto.testing import (
    DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING,
)
from plone import api

import unittest


class TestPrenotazioniFolder(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_behaviors_enabled_for_persona(self):
        """Test that PrenotazioniFolder has all the behaviors
        assigned by this product
        """
        portal_types = api.portal.get_tool(name="portal_types")

        for behavior in (
            "design.plone.ioprenoto.behaviors.uffici_correlati",
            "design.plone.ioprenoto.behaviors.punto_di_contatto",
            "design.plone.ioprenoto.behaviors.orario_di_apertura",
        ):
            self.assertIn(behavior, portal_types["PrenotazioniFolder"].behaviors)
