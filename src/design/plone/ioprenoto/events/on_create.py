# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from plone import api


def exclude_from_nav(obj, event):
    """
    Exclude from navigation
    """
    obj.exclude_from_nav = True


def create_message(obj, *args, **kwargs):
    """
    Create message on prenotazione creation
    """
    from design.plone.iocittadino.interfaces.store import (
        IMessageContentStore,
    )

    booking_date = str(obj.booking_date and obj.booking_date.date() or "")
    booking_time = str(obj.booking_date and obj.booking_date.time() or "")
    booking_print_url = "{folder}/@@prenotazione_print?uid={uid}".format(
        folder=obj.getPrenotazioniFolder().absolute_url(), uid=obj.UID()
    )

    message_store = getMultiAdapter(
        (api.portal.get(), getRequest()), IMessageContentStore
    )

    message_text = f"""La prenotazione per il {booking_date} alle {booking_time} è stata creata.
                      Riceverete una mail di conferma quando la prenotazione verrà confermata definitivamente.
                      Se non hai salvato o stampato il promemoria, puoi visualizzarlo a questo link: {booking_print_url}
                    """

    # message add here
    message_store.add(
        {
            "object_uid": obj.UID(),
            "message": message_text,
            "state": "sent",
            "notify_on_email": False,
        }
    )
