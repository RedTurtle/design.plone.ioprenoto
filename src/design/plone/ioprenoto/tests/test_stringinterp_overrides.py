# -*- coding: utf-8 -*-
from datetime import date
from plone import api
from plone.app.testing import (
    TEST_USER_ID,
    setRoles,
)
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING
from datetime import datetime
from redturtle.prenotazioni.adapters.booker import IBooker
from zope.component import getAdapter
from plone.stringinterp.interfaces import IStringSubstitution

import unittest
import transaction


class TestStringinterpOverrides(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.folder_prenotazioni = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenota foo",
            description="",
            daData=date.today(),
            week_table=[
                {
                    "day": "Lunedì",
                    "morning_start": "0700",
                    "morning_end": "1000",
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Martedì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Mercoledì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Giovedì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Venerdì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Sabato",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Domenica",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
            ],
            booking_types=[
                {"name": "Type A", "duration": "30"},
            ],
            gates=["Gate A"],
        )

        year = api.content.create(
            container=self.folder_prenotazioni, type="PrenotazioniYear", title="Year"
        )
        week = api.content.create(container=year, type="PrenotazioniWeek", title="Week")
        self.day_folder = api.content.create(
            container=week, type="PrenotazioniDay", title="Day"
        )

        booker = IBooker(self.folder_prenotazioni)
        self.prenotazione = booker.create(
            {
                "booking_date": datetime.now(),
                "booking_type": "Type A",
                "title": "foo",
            }
        )

        transaction.commit()

    def test_booking_print_url_override(
        self,
    ):
        self.assertIn(
            "prenotazione-appuntamenti-uffici",
            getAdapter(self.prenotazione, IStringSubstitution, "booking_print_url")(),
        )

    def test_booking_print_url_with_delete_token_override(
        self,
    ):
        self.assertIn(
            "prenotazione-appuntamenti-uffici",
            getAdapter(
                self.prenotazione,
                IStringSubstitution,
                "booking_print_url_with_delete_token",
            )(),
        )
