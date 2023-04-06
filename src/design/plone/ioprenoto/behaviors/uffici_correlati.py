from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from plone.supermodel import model
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

from design.plone.ioprenoto import _


@provider(IFormFieldProvider)
class IUfficiCorrelati(model.Schema):
    """Add tags to content"""

    uffici_correlati = RelationList(
        title=_("Uffici corellati"),
        value_type=RelationChoice(
            title=_("Ufficio"),
            source=CatalogSource(portal_type="UnitaOrganizzativa"),
        ),
    )
    directives.widget(
        "uffici_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 100,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )


class UfficiCorrelati(object):
    def __init__(self, context):
        self.context = context
