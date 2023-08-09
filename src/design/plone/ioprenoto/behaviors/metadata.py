# -*- coding: utf-8 -*-
from plone.app.dexterity import _
from plone.app.dexterity.behaviors.metadata import IBasic as IBasicBase
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IBasic(IBasicBase):
    # default fieldset
    description = schema.Text(
        title=_("label_description", default="Summary"),
        description=_(
            "help_description", default="Used in item listings and search results."
        ),
        required=True,
        missing_value="",
    )
