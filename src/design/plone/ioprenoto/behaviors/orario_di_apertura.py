from design.plone.ioprenoto import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider
from zope.schema import Text


@provider(IFormFieldProvider)
class IOrarioDiApertura(model.Schema):
    """Add tags to content"""

    orario_di_apertura = Text(title=_("Orario di apertura"), required=False)


class OrarioDiApertura(object):
    def __init__(self, context):
        self.context = context
