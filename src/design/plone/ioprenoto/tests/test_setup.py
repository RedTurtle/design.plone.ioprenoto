# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.ioprenoto.testing import (  # noqa: E501
    DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that design.plone.ioprenoto is properly installed."""

    layer = DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if design.plone.ioprenoto is installed."""
        self.assertTrue(self.installer.is_product_installed("design.plone.ioprenoto"))

    def test_browserlayer(self):
        """Test that IDesignPloneIoprenotoLayer is registered."""
        from design.plone.ioprenoto.interfaces import IDesignPloneIoprenotoLayer
        from plone.browserlayer import utils

        self.assertIn(IDesignPloneIoprenotoLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("design.plone.ioprenoto")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if design.plone.ioprenoto is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("design.plone.ioprenoto"))

    def test_browserlayer_removed(self):
        """Test that IDesignPloneIoprenotoLayer is removed."""
        from design.plone.ioprenoto.interfaces import IDesignPloneIoprenotoLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDesignPloneIoprenotoLayer, utils.registered_layers())
