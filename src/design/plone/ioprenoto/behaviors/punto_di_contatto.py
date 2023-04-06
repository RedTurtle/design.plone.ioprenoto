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
class IPuntoDiContatto(model.Schema):
    """Add tags to content"""

    punto_di_contatto = RelationList(
        title=_("Punto di contatto"),
        value_type=RelationChoice(
            title=_("Punto di contatto"),
            source=CatalogSource(portal_type="PuntoDiContatto"),
        ),
    )
    directives.widget(
        "punto_di_contatto",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["PuntoDiContatto"],
        },
    )


class PuntoDiContatto(object):
    def __init__(self, context):
        self.context = context
