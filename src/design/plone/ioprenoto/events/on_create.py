# -*- coding: utf-8 -*-

try:
    from design.plone.iocittadino.interfaces.store import (
        IPraticaContentStore,
        IMessageContentStore,
    )
    iocittadino_installed = True
except ImportError as e:
    iocittadino_installed = False


def exclude_from_nav(obj, event):
    """
    Exclude from navigation
    """
    obj.exclude_from_nav = True

def create_message(obj, event):
    """
        Create message on prenotazione creation
    """
    import pdb;pdb.set_trace()
    message_store = queryMultiAdapter((self.portal, getRequest()), IMessageContentStore)
    message_text = f"""La prenotazione per il {booking_date} alle {booking_time} è stata creata.
                      Riceverete una mail di conferma quando la prenotazione verrà confermata definitivamente.
                      Se non hai salvato o stampato il promemoria, puoi visualizzarlo a questo link: {booking_print_url}
                """
    