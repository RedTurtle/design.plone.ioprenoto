# -*- coding: utf-8 -*-
from plone import api

import logging

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.ioprenoto:default"


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def update_catalog(context):
    update_profile(context, "catalog")


def to_1001(context):
    """ """
    # Fix behaviors
    fti = api.portal.get_tool(name="portal_types")["Prenotazione"]
    behaviors = fti.behaviors
    to_remove = [
        "plone.app.dexterity.behaviors.metadata.IBasic",
    ]
    new_behaviors = [x for x in behaviors if x not in to_remove]
    new_behaviors.append("ioprenoto.basic")
    fti.behaviors = tuple(new_behaviors)

    for brain in api.content.find(portal_type="PrenotazioniFolder"):
        folder = brain.getObject()
        if folder.visible_booking_fields:
            folder.visible_booking_fields = [
                x for x in folder.visible_booking_fields if x != "description"
            ]
        if folder.required_booking_fields:
            folder.required_booking_fields = [
                x for x in folder.required_booking_fields if x != "description"
            ]
