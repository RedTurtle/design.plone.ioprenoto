# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import (
    DesignPloneContenttypesRestApiLayer,
)
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class DesignPloneIoprenotoLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.contentrules.mailfromfield
        import collective.taxonomy
        import collective.venue
        import collective.z3cform.datagridfield
        import design.plone.contenttypes

        # required to install redturtle.prenotazioni and design.plone.ioprenoto in test
        import design.plone.policy
        import eea.api.taxonomy
        import plone.app.caching
        import plone.app.dexterity
        import redturtle.bandi
        import redturtle.prenotazioni
        import redturtle.volto

        super().setUpZope(app, configurationContext)

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=design.plone.contenttypes)
        self.loadZCML(package=collective.contentrules.mailfromfield)
        self.loadZCML(package=redturtle.bandi)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=redturtle.volto)
        self.loadZCML(package=eea.api.taxonomy)
        self.loadZCML(package=collective.z3cform.datagridfield)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=redturtle.prenotazioni)

        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=design.plone.ioprenoto)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)

        applyProfile(portal, "plone.app.caching:default")

        # required by design.plone.contenttypes profile
        applyProfile(portal, "redturtle.bandi:default")
        applyProfile(portal, "collective.venue:default")
        applyProfile(portal, "redturtle.volto:default")
        applyProfile(portal, "collective.taxonomy:default")
        applyProfile(portal, "eea.api.taxonomy:default")
        applyProfile(portal, "collective.z3cform.datagridfield:default")

        # used by the current product
        applyProfile(portal, "design.plone.contenttypes:default")

        # required by design.plone.ioprenoto
        applyProfile(portal, "redturtle.prenotazioni:default")

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


class DesignPloneContenttypesRestApiLayer(
    DesignPloneIoprenotoLayer, DesignPloneContenttypesRestApiLayer
):
    pass


DESIGN_PLONE_IOPRENOTO_API_FIXTURE = DesignPloneContenttypesRestApiLayer()
DESIGN_PLONE_IOPRENOTO_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_API_FIXTURE,),
    name="DesignPloneIoprenotoRestApiLayer:Integration",
)

DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneIoprenotoRestApiLayer:Functional",
)
