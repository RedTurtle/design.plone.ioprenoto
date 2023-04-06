from design.plone.ioprenoto import _
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


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
