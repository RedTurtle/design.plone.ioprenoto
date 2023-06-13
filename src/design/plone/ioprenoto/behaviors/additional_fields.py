from design.plone.ioprenoto import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.supermodel import model
from plone.autoform import directives
from zope.interface import provider
from zope.schema import Text
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


@provider(IFormFieldProvider)
class IAdditionalFields(model.Schema):
    """Add fields to content"""

    orario_di_apertura = Text(
        title=_("Orario di apertura"),
        description=_("Orario di apertura della stanza prenotazioni"),
        required=False,
    )
    uffici_correlati = RelationList(
        title=_("Uffici correlati"),
        description=_("Uffici correlati al contesto corrente"),
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


class AdditionalFields(object):
    def __init__(self, context):
        self.context = context
