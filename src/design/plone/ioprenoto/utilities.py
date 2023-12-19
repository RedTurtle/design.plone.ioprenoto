# -*- coding: utf-8 -*-


def get_uo_from_service(service):
    """Dato lo UID di un servizio, restituisce le UO a cui è collegato
    come canale fisico o unità organizzativa responsabile"""
    canale_fisico = getattr(service, "canale_fisico", [])
    if canale_fisico:
        return [x.to_object for x in canale_fisico if x.to_object]
    ufficio_responsabile = getattr(service, "ufficio_responsabile", [])
    return [x.to_object for x in ufficio_responsabile if x.to_object]
