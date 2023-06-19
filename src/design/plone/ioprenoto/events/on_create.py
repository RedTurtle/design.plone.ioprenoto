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

    portal_state = api.content.get_view(
        name="plone_portal_state",
        context=api.portal.get(),
        request=getRequest(),
    )
    booking_date = str(obj.booking_date and obj.booking_date.date() or "")
    booking_time = str(obj.booking_date and obj.booking_date.time() or "")
    booking_print_url = (
        "{root}/prenotazione-appuntamenti-uffici?booking_id={uid}".format(
            root=portal_state.navigation_root_url(), uid=obj.UID()
        )
    )

    message_store = getMultiAdapter(
        (api.portal.get(), getRequest()), IMessageContentStore
    )

    message_text = f"""La prenotazione per il {booking_date} alle {booking_time} è stata creata.\
        Riceverete una mail di conferma quando la prenotazione verrà confermata definitivamente.\
        Se non hai salvato o stampato il promemoria, puoi visualizzarlo a questo link: <a href={booking_print_url}>questo link</a>"""

    # message add here
    message_store.add(
        {
            "object_uid": obj.UID(),
            "title": "Prenotazione appuntamento: " + obj.booking_type,
            "message": message_text,
            "state": "sent",
            "notify_on_email": False,
        }
    )
