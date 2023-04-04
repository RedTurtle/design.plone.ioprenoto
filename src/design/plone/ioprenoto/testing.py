# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import design.plone.ioprenoto


class DesignPloneIoprenotoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=design.plone.ioprenoto)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "design.plone.ioprenoto:default")


DESIGN_PLONE_IOPRENOTO_FIXTURE = DesignPloneIoprenotoLayer()


DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_FIXTURE,),
    name="DesignPloneIoprenotoLayer:IntegrationTesting",
)


DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_FIXTURE,),
    name="DesignPloneIoprenotoLayer:FunctionalTesting",
)


DESIGN_PLONE_IOPRENOTO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DESIGN_PLONE_IOPRENOTO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="DesignPloneIoprenotoLayer:AcceptanceTesting",
)
