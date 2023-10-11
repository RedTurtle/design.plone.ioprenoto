# -*- coding: utf-8 -*-
import collective.contentrules.mailfromfield
import redturtle.prenotazioni
from design.plone.policy.testing import (
    DesignPlonePolicyLayer,
    DesignPlonePolicyRestApiLayer,
)
from plone.app.testing import FunctionalTesting, IntegrationTesting, applyProfile
from plone.testing import z2

import design.plone.ioprenoto

try:
    import design.plone.iocittadino

    iocittadino_installed = True
except ImportError:
    iocittadino_installed = False


class DesignPloneIoprenotoLayer(DesignPlonePolicyLayer):
    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)

        self.loadZCML(package=design.plone.policy)
        self.loadZCML(package=redturtle.prenotazioni)
        self.loadZCML(package=collective.contentrules.mailfromfield)
        self.loadZCML(package=design.plone.ioprenoto)

        if iocittadino_installed:
            self.loadZCML(package=design.plone.iocittadino)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)

        applyProfile(portal, "design.plone.ioprenoto:default")


# if iocittadino_installed:
#     applyProfile(portal, "design.plone.iocittadino:default")


DESIGN_PLONE_IOPRENOTO_FIXTURE = DesignPloneIoprenotoLayer()


DESIGN_PLONE_IOPRENOTO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_FIXTURE,),
    name="DesignPloneIoprenotoLayer:IntegrationTesting",
)


DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_FIXTURE,),
    name="DesignPloneIoprenotoLayer:FunctionalTesting",
)


class DesignPloneIoprenotoRestApiLayer(
    DesignPloneIoprenotoLayer, DesignPlonePolicyRestApiLayer
):
    pass


DESIGN_PLONE_IOPRENOTO_API_FIXTURE = DesignPloneIoprenotoRestApiLayer()
DESIGN_PLONE_IOPRENOTO_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_API_FIXTURE,),
    name="DesignPloneIoprenotoRestApiLayer:Integration",
)

DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_IOPRENOTO_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneIoprenotoRestApiLayer:Functional",
)
