# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from redturtle.prenotazioni.interfaces import IRedturtlePrenotazioniLayer


class IDesignPloneIoprenotoLayer(IRedturtlePrenotazioniLayer):
    """Marker interface that defines a browser layer."""
