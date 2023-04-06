from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model

from zope.schema import Text

from design.plone.ioprenoto import _


@provider(IFormFieldProvider)
class IOrarioDiApertura(model.Schema):
    """Add tags to content"""

    orario_di_apertura = Text(title=_("Orario di apertura"), required=False)


class OrarioDiApertura(object):
    def __init__(self, context):
        self.context = context
