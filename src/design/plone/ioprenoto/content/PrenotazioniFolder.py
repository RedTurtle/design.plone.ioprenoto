from redturtle.prenotazioni.content.prenotazioni_folder import (
    PrenotazioniFolder as PrenotazioniFolder_original,
)


class PrenotazioniFolder(PrenotazioniFolder_original):
    @property
    def exclude_from_nav(self):
        return True
