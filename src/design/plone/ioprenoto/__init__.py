# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from redturtle.prenotazioni import config

_ = MessageFactory("design.plone.ioprenoto")


# Non permettiamo ai redattori di scegliere se mostrare o meno il campo note,
# ma lo mettiamo di default nello schema
config.REQUIRABLE_AND_VISIBLE_FIELDS = [
    x for x in config.REQUIRABLE_AND_VISIBLE_FIELDS if x != "description"
]
config.DEFAULT_VISIBLE_BOOKING_FIELDS = [
    x for x in config.DEFAULT_VISIBLE_BOOKING_FIELDS if x != "description"
]
config.STATIC_REQUIRED_FIELDS = [x for x in config.STATIC_REQUIRED_FIELDS] + [
    "description"
]
